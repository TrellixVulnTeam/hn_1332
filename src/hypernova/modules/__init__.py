#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent application
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import pkgutil
import json

class AgentRequestHandlerBase:

    def _format_response(response={}, successful=True, error_code=0,
                         message='', explanation=''):

        return {
            'status': {
                'successful': successful,
                'error_code': int(error_code),
                'message': message,
                'explanation': explanation
            },
            'response': response,
        }




def serialise(native_response):
    """
    Serialise a request or response as JSON.
    """

    return json.dumps(native_response)


# Import submodules
#
# Since __all__ only contains imported submodules, we need to walk through the
# packages under this namespace and import them here in order to work with them
# later. This isn't pretty, but it works.
__all__ = []
for (loader, module_name, is_package) in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    module = loader.find_module(module_name).load_module(module_name)
    exec("%s = module" %(module_name))
