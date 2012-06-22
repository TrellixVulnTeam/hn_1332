#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Templates, utility functions and class definitions to represent and generate
# nginx configuration files.
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig.httpserver import HttpServerConfigBase, \
                                                     VirtualHostBase
from hypernova.libraries.permissionelevation import elevate_cmd
from os.path import abspath, isfile, join
from subprocess import Popen

# Global blocks
templ_block_events   = """events {
    %s
}"""
templ_block_http     = """http {
    %s
}"""
templ_block_location = """location {
    %s
}"""
templ_block_server   = """server {
    %s
}"""
templ_block_types    = """types {
    %s
}"""

# Global directives
templ_directive_daemon           = "daemon %s;"
templ_directive_default_type     = "default_type %s;"
templ_directive_include          = "include %s;"
templ_directive_user             = {1: "user %s;", 2: "user %s %s;"}
templ_directive_worker_processes = "worker_processes %i;"

# events {  } directives
templ_directive_use                = "use %s;"
templ_directive_worker_connections = "worker_connections %i;"

# http { server {  } } directives
templ_directive_auto_index         = "autoindex %s;"
templ_directive_indexes           = "index %s;"
templ_directive_keepalive_timeout = "keepalive_timeout %s;"
templ_directive_listen            = "listen %s;"
templ_directive_document_root     = "root %s;"
templ_directive_sendfile          = "sendfile %s;"
templ_directive_server_names      = "server_name %s;"

def to_nginx_bool(self, bool_val):
    """
    Convert to nginx boolean.

    nginx uses on and off instead of true and false, so we account for that
    here by converting Python bool()s into nginx booleans.
    """

    if bool_val:
        return 'on'
    else:
        return 'off'

class AppConfig(HttpServerConfigBase):
    """
    nginx configurator.
    """

    def __init__(self, config_dir, dir_mapping=None):
        if not dir_mapping:
            dir_mapping = {}

        if 'virtualhosts' not in dir_mapping.keys():
            dir_mapping['virtualhosts'] = 'sites'

        self.config_dir = abspath(config_dir)
        self.vhost_dir  = join(self.config_dir, dir_mapping['virtualhosts'])

    def add_virtualhost(self, vhost):
        if self.has_virtualhost(vhost):
            raise VirtualHostCollisionError()

        self.commit_virtualhost(vhost)

    def commit_virtualhost(self, vhost):
        if not vhost.is_valid():
            raise InvalidVirtualHostError()

        with open(join(self.vhost_dir, vhost.server_names[0]), 'w') as f:
            f.write(str(vhost))

    def get_virtualhost(self):
        return VirtualHost()

    def has_virtualhost(self, vhost):
        return isfile(join(self.vhost_dir, vhost.server_names[0]))

    def reload_service(self):
        Popen(elevate_cmd(['service', 'nginx', 'reload']))


class VirtualHost(VirtualHostBase):
    """
    nginx virtualhost.
    """

    def fmt_directive_includes(self, includes):
        """
        Convert the dynamic languages dictionary into nginx configuration file
        includes.
        """

        opts = []

        for i in includes:
            opts.append(globals()['templ_directive_include'] %(i))

        return "\n    ".join(opts)

    def fmt_directive_indexes(self, indexes):
        """
        Format a list of index files for a configuration file.
        """

        return globals()['templ_directive_indexes'] %(' '.join(indexes))

    def fmt_directive_server_names(self, server_names):
        """
        Format a list of server names for a configuration file.
        """

        return globals()['templ_directive_server_names'] %(' '.join(server_names))

    def is_valid(self):
        # TODO: validation
        return True

    def __str__(self):
        templates  = globals()
        directives = ['auto_index', 'document_root', 'includes', 'indexes',
                      'listen', 'server_names']
        blocks     = ['location']
        chunks     = []

        # Format each individual directive.
        #
        # Attempt to find fmt_directive_*() methods to handle the translation of
        # special directives which cannot follow the conventional use of a
        # format string. Else, look for a global templ_directive_* variable to
        # use as a format string.
        #
        # TODO: add support for location blocks and fancier directives.
        for d in directives:
            value = getattr(self, d, None)

            if not value:
                continue

            try:
                chunk = getattr(self, 'fmt_directive_' + d)(value)
            except AttributeError:
                chunk = templates['templ_directive_' + d] %(value)
            chunks.append(chunk)

        return templates['templ_block_server'] %("\n    ".join(chunks))
