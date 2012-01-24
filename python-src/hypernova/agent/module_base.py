#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Base classes for modules
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import json

class BaseRequestHandler:

    def _format_response(response={}, successful=True, error_code=0,
                         message='', explanation=''):

        return {
            'status': {
                'successful': successful,
                'error_code': int(error_code),
                'message': message,
                'explanation': explanation
            },
            'response': response
        }

    def _serialise_response(native_response):

        return json.dumps(native_response)
