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

    def _format_response(response={}, successful=False, error_code=500,
                         message='', explanation=''):
        native = {
            'status': {
                'successful': successful,
                'error_code': error_code,
                'message': message,
                'explanation': explanation
            },
            'response': response
        }

        return bytes(json.dumps(native), 'UTF-8')
