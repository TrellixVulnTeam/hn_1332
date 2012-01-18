#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent application
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import logging
import logging.handlers
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys

if __name__ == '__main__':
    Agent().execute()

class Agent:

    addr = None
    port = None
    log  = None

    def __init__(self, addr = '0.0.0.0', port = 8080, log = '/tmp/hn-main.log'):
        self.addr = addr
        self.port = port
        self.log  = log

    def execute(self):
        self._initLogging()

        self._server = HTTPServer((self.addr, self.port), AgentRequestHandler)
        self._log.info("entering server main loop")
        self._server.serve_forever()
        self._log.info("server exiting")


    def _initLogging(self):
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

    def do_HEAD(self):
        self.send_response(500)
        self.end_headers()

    def do_GET(self):
        self.send_response(500)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'<html><head><title>HyperNova</title></head><body><h1>HyperNova</h1><p>It\'s alive!</p></body></html>')
