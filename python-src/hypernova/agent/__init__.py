#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent application package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from http.server import HTTPServer, BaseHTTPRequestHandler
from hypernova import modules
from hypernova.agent.module_base import BaseRequestHandler
import gnupg
import json
import logging
import logging.handlers
import socket
from socketserver import ThreadingMixIn
import sys

class Agent:

    addr    = None
    port    = None
    timeout = None

    main_main_log = None
    req_main_log  = None
    log_level     = None

    name   = None
    domain = None

    gnupg_home        = None
    gnupg_fingerprint = None

    _server = None

    _main_main_log      = None
    _main_log_formatter = None
    _main_log_handler   = None
    _req_main_log       = None
    _req_log_formatter  = None
    _req_log_handler    = None

    _gpg = None

    def __init__(self, addr='0.0.0.0', port=8080, timeout=0.5,
                 main_log='/tmp/hn-main.log', req_log='/tmp/hn-request.log',
                 log_level='debug',
                 name='box', domain='example.net',
                 gnupg_home='/tmp/hn-gnupg', gnupg_fingerprint=''):

        self.addr = addr
        self.port = port
        self.timeout = timeout

        self.main_log = main_log
        self.req_log = req_log
        self.log_level = log_level.upper()

        self.name       = name
        self.domain     = domain
        self.full_name  = '%s.%s' %(name, domain)
        self.email_addr = '%s@%s' %(name, domain)

        self.gnupg_home        = gnupg_home
        self.gnupg_fingerprint = gnupg_fingerprint

    def execute(self):

        self._init_logging()
        self._init_gpg()

        self._server = AgentServer((self.addr, self.port),
            AgentRequestHandler, self._gpg)
        self._main_log.info('entering server main loop')
        self._server.serve_forever()
        self._main_log.info('server exiting')

    def get_gpg_credentials(self):

        return (self._gpg, self._gpg_)

    def _init_gpg(self):

        self._gpg = gnupg.GPG(gnupghome=self.gnupg_home)
        gpg_secrets = self._gpg.list_keys(True)

        for key in gpg_secrets:
            if key['fingerprint'] == self.gnupg_fingerprint:
                self._gpg_secret_key = key
                break

        if not hasattr(self, '_gpg_secret_key'):
            self._main_log.error('no GPG private key configured; aborting')
            sys.exit(78) # configuration issue (sysexits.h)

    def _init_logging(self):

        log_level = getattr(logging, self.log_level)

        self._main_log_formatter = logging.Formatter(
            fmt = '[%(asctime)s] [%(levelname)-1s] %(message)s',
            datefmt = '%d/%m/%Y %I:%M:%S')

        self._main_log = logging.getLogger('hn-main')
        self._main_log.setLevel(log_level)
        self._main_log_handler = logging.handlers.RotatingFileHandler(
            self.main_log, mode='a')
        self._main_log_handler.setFormatter(self._main_log_formatter)
        self._main_log.addHandler(self._main_log_handler)

        self._req_log = logging.getLogger('hn-request')
        self._req_log.setLevel(log_level)
        self._req_log_handler = logging.handlers.RotatingFileHandler(
            self.req_log, mode='a')
        self._req_log_handler.setFormatter(self._main_log_formatter)
        self._req_log.addHandler(self._req_log_handler)

        self._main_log.info('initialised logging')


class AgentServer(ThreadingMixIn, HTTPServer):
    pass


class AgentRequestHandler(BaseHTTPRequestHandler):

    _log = None

    def __init__(self, request, client_address, server):

        # Overridden from BaseHTTPRequestHandler
        #
        # This override enables logging to our dedicated request log.

        self._log = logging.getLogger('hn-request')

        super().__init__(request, client_address, server)

    def handle_one_request(self):

        # Overridden from BaseHTTPRequestHandler
        #
        # By overriding the method, we're able to use custom HTTP methods in
        # module request handlers without defining the methods in this class.

        try:
            self.raw_requestline = self.rfile.readline(65537)

            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return

            if not self.raw_requestline:
                self.close_connection = 1
                return

            if not self.parse_request():
                return

            self.send_header('Content-Type', 'application/json');

            module_name = self.path[1:].replace('/', '.')
            try:
                module = getattr(modules, module_name)
                handler = getattr(module, 'AgentRequestHandler')
            except AttributeError:
                self.send_error(501, 'Unsupported module')
                return

            try:
                method = getattr(handler, 'do_' + self.command.lower())
            except AttributeError:
                self.send_error(405, 'Unsupported method')
                return

            try:
                length = int(self.headers.get('Content-Length'))
                raw = self.rfile.read(length)

                try:
                    params = json.loads(str(raw))
                except ValueError:
                    self.log_error('Failed to interpret parameters as valid JSON!')
                    self.send_error(400, 'Invalid parameters')
                    return

            except TypeError:
                self.log_message('Content-Length not set; assuming no parameters')
                params = {}

            self.log_message('Executing action')
            result = method(params)

            self.log_message('Sending response')
            self.wfile.write(BaseRequestHandler._serialise_response(result))
            self.wfile.flush()
            self.send_response(result['status']['error_code'])

            self.log_message('Processing complete')

        except socket.timeout as e:
            self.log_error('Request timed out: %r', e)
            self.close_connection = 1
            return

    def log_message(self, format, *args):

        msg = format %args
        self._log.info('[%s:%d] %s'
            %(self.client_address[0], self.client_address[1], msg))

    def send_error(self, code, message=None):

        try:
            shortmsg, longmsg = self.responses[code]
        except KeyError:
            shortmsg, longmsg = '', ''

        if message is None:
            message = shortmsg

        explain = longmsg

        self.log_error("Returning %d: %s", code, message)

        self.send_response(code, message)
        self.send_header('Content-Type', self.error_content_type)
        self.send_header('Connection', 'close')
        self.end_headers()

        response = BaseRequestHandler._format_response({}, False, code, '')
        self.wfile.write(BaseRequestHandler._serialise_response(response))
