#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Simple client library
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from http.client import HTTPConnection
from hypernova import GPG
import json
import os

class Client:

    host = None
    port = None

    connection = None

    M_GET  = 'GET'
    M_POST = 'POST'

    def __init__(self, host='127.0.0.1', port=8080):

        self.host = host
        self.port = port

        self._init_connection()
        self._init_gpg()

    def _init_connection(self):

        self._connection = HTTPConnection(self.host, self.port)

    def _init_gpg(self):

        self._gpg = GPG.get_gpg(gnupghome=os.path.join(os.getenv('HOME'),
                                                       '.gnupg'))

    def query(self, params, client_fp, server_fp):

        if not isinstance(params, str):
            params = json.dumps(params)

        params = self._gpg.encrypt(params, server_fp, sign=client_fp)
        encrypted_params = str(params)

        if not params:
            raise ValueError('Invalid passphrase, or the server\'s key has ' \
                             'not been signed')

        http_headers = {'Content-Length': len(encrypted_params)}
        self._connection.request(self.M_GET, '/', body=encrypted_params,
                                 headers=http_headers)

        response = self._connection.getresponse()
        response_data = str(response.read(), 'UTF-8')

        response_data = self._gpg.decrypt(response_data)
        if response_data.fingerprint != server_fp:
            raise ValueError('Response was not signed')

        self._connection.close()

        return json.loads(str(response_data))
