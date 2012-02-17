#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# nginx configurator
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig.httpserver import HttpServerConfigBase, \
                                                     VirtualHostBase

class HttpServerConfig(HttpServerConfigBase):
    """
    nginx configurator.
    """

    def get_virtualhost(self):
        return VirtualHost()

class VirtualHost(VirtualHostBase):
    """
    nginx virtualhost.
    """

    # Virtual host template
    __templ = """
server {
    listen %s:%s;
    server_name %s;

    root %s;

    index %s;
    auto_index %s;

    %s
}
"""

    def __str__(self):
        return self.__templ %(self.listen_socket[0],
                              self.listen_socket[1],
                              ' '.join(self.server_names),
                              self.document_root,
                              ' '.join(self.indexes),
                              self.__to_nginx_bool(self.auto_index),
                              self.__to_nginx_includes(self.dynamic_langs))

    def __to_nginx_bool(self, bool_val):
        """
        Convert to nginx boolean.

        nginx uses on and off instead of true and false, so we account for that
        here by converting Python bool()s into nginx booleans.
        """

        if bool_val:
            return 'on'
        else:
            return 'off'

    def __to_nginx_includes(self, dynamic_langs):
        """
        Convert the dynamic languages dictionary into nginx configuration file
        includes.
        """

        opts = []

        if not 'php' in dynamic_langs:
            dynamic_langs = False

        if dynamic_langs['php']:
            opts.append('   include enable_php;');

        return '\n'.join(opts)
