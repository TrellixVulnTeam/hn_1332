#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Client application package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from http.client import HTTPConnection
from hypernova import GPG
import json
import os
import sys

class Client:

    addr = None
    port = None

    connection = None

    M_GET  = 'GET'
    M_POST = 'POST'

    def __init__(self, addr='127.0.0.1', port=8080):

        self.addr = addr
        self.port = port

        self._init_connection()
        self._init_gpg()

    def _init_connection(self):

        self._connection = HTTPConnection(self.addr, self.port)

    def _init_gpg(self):

        self._gpg = GPG.get_gpg(gnupghome=os.path.join(os.getenv('HOME'), '.gnupg'))

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
            print(server_fp, '  ', response_data.fingerprint)
            raise ValueError('Response was not signed')

        self._connection.close()

        return json.loads(str(response_data))


if __name__ == '__main__':
    try:
        print(json.dumps(Client().query(sys.argv[1], sys.argv[2], sys.argv[3]),
                         sort_keys=True, indent=4))
    except IndexError:
        print('%s <message> <client f/p> <server f/p>' %(sys.argv[0]))
        sys.exit(75)
