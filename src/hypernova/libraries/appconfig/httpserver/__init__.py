#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# HTTP server configurator base
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig import AppConfigBase

class HttpServerConfigBase(AppConfigBase):

    def get_virtualhost(self):
        pass

class VirtualHostBase(AppConfigBase):
    """
    Virtual host object.
    """

    # Listening socket
    #
    # [0] = network
    # [1] = port
    listen_socket = []

    # Server names
    #
    # [0]  = Apache ServerName
    # [1:] = Apache ServerAlias
    server_names  = []

    # Document root
    document_root = ''

    # Index order
    indexes = []

    # Automatically index directory contents?
    auto_index = False

    # Dynamic languages
    #
    # ['php'] = True|False
    dynamic_langs = {}

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

