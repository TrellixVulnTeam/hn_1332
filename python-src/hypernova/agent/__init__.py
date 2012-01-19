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
import json
import logging
import logging.handlers
import socket
import sys

class Agent:

    addr    = None
    port    = None
    log     = None
    timeout = None

    _log           = None
    _log_formatter = None
    _log_handler   = None
    _server        = None

    def __init__(self, addr='0.0.0.0', port=8080, log='/tmp/hn-main.log',
                 timeout=0.5):
        self.addr    = addr
        self.port    = port
        self.log     = log
        self.timeout = timeout

    def execute(self):
        self._init_logging()

        self._server = HTTPServer((self.addr, self.port), AgentRequestHandler)
        self._log.info('entering server main loop')
        self._server.serve_forever()
        self._log.info('server exiting')

    def _init_logging(self):
        self._log_formatter = logging.Formatter(
            fmt = '[%(asctime)s] [%(levelname)-1s] %(message)s',
            datefmt = '%d/%m/%Y %I:%M:%S'
        )

        self._log_handler = logging.handlers.RotatingFileHandler(
            self.log, mode = 'w')
        self._log_handler.setFormatter(self._log_formatter)

        self._log = logging.getLogger('hn-main')
        self._log.addHandler(self._log_handler)
        self._log.setLevel(logging.DEBUG)

        self._log.info('initialised logging')


class AgentRequestHandler(BaseHTTPRequestHandler):

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

            result = method(params)
            self.wfile.write(result)
            self.wfile.flush()

        except socket.timeout as e:
            self.log_error('Request timed out: %r', e)
            self.close_connection = 1
            return

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

        self.wfile.write(BaseRequestHandler._format_response({}, False, code, ''))
