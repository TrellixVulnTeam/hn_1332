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
    """
    Agent request handler base class.

    Request handler classes operate within the HyperNova agent. They're called
    on by the agent to respond to certain types of incoming request, based on
    the name of the module and the function that was called.
    """

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


class ClientRequestBuilderBase:
    """
    Client query interface base class.

    Client query interface classes provide simple interfaces to request handler
    classes, enabling the command line client to expose the functionality within
    the request handler classes to human beings.
    """

    def _format_request(action, parameters={}):
        """
        """

        return {
            'action': '.'.join(action),
            'parameters': parameters,
        }

    def init_subparser(subparser, subparser_factory):
        """
        Initialise a subparser
        """

        return subparser


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
