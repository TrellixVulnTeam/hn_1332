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
import json
import logging
import logging.handlers
import socket
import sys

if __name__ == '__main__':
    Agent().execute()

class Agent:

    addr = None
    port = None
    log  = None

    def __init__(self, addr='0.0.0.0', port=8080, log='/tmp/hn-main.log'):
        self.addr = addr
        self.port = port
        self.log  = log

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

    error_message_format_native = {
        'status': {
            'successful': False,
            'error_code': '%(code)d',
            'message': '%(message)s',
            'explanation': '%(explain)s'
        }
    }

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

            # Regardless of what happens here, we send a JSON response
            self.send_header('Content-Type', 'application/json');

            # Try to find the right module RequestHandler
            try:
                module_name = self.url.replace('/', '.')
                module = getattr(modules, module_name)
            except AttributeError:
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return

            method()
            self.wfile.flush()

        except socket.timeout as e:
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return

    def send_error(self, code, message=None):

        self.error_message_format = json.dumps(self.error_message_format_native)
        super().send_error(code, message)
