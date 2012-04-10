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
import pkgutil
import sys

class HttpServerConfigBase(AppConfigBase):
    """
    Base representation of an HTTP server's configuration.

    Note: these classes are strictly one-way only -- no attempts are made to
          load existing configuration. Such attempts are unreliable and by no
          means suited to use in production environments.
    """

    def __init__(self, config_dir, dir_mapping=None):
        """
        Initialise an HTTP server configuration instance.

        The configuration directory is the root directory of the webserver's
        configuration, usually /etc/somewhere. The mapping parameters should be
        either None or a dictionary containing all or some of the following
        keys, as is necessary in the given environment:

          * virtualhosts - the directory to store virtual hosts in.

        The defaults for the given web server will be assumed if not present in
        the mapping dictionary.
        """

        pass

    def commit_virtualhost(self, vhost):
        """
        Commit a changed virtualhost.
        """

        pass

    def get_virtualhost(self):
        """
        Create a new virtualhost.
        """

        pass

    def has_virtualhost(self, vhost):
        """
        Does this server object have a vhost with that name?
        """

        pass


class VirtualHostBase(AppConfigBase):
    """
    Virtual host object.
    """

    # Listening socket
    #
    # [0] = network
    # [1] = port
    listen = []

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

    # External configuratrion file includes
    #
    # If unsupported by the web server itself, these should be handled at
    # write-time, as they're an essential part of configuration.
    #
    # Except in those servers which don't natively support an include
    # directive, these files are assumed to be relative to the server's
    # configuration root directory. You should consult the documentation for
    # specific modules if you suspect this path is wrong.
    includes = []

    # Location blocks
    #
    # The concept is based on that of nginx:
    #    http://wiki.nginx.org/HttpCoreModule#location
    locations = []

    def add_location(self):
        """
        Add a location block to the stack.
        """

        Klass = getattr(sys.modules[__name__], 'VirtualHost')
        location = self.locations.append(Klass())
        return location

    def is_valid(self):
        """
        Is the vhost semantically valid?

        This will always be a best guess attempt and will never be truly in line
        with the validations of the server, but should provide a good indication
        when dire things are afoot.
        """

        pass


class VirtualHostLocationBase(AppConfigBase):
    """
    Virtual host location object.
    """

    MODES = [
        'exact',
        'regex',
    ]

    # Location
    uri = ''

    # Match mode
    mode = ''


class InvalidVirtualHostError(Exception):
    """
    Thrown when a commit is attempted on an invalid virtual host.
    """

    pass

def get_server(server):
    """
    Get an HTTP server configuration instance.
    """

    return getattr(globals()[server], 'AppConfig')

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
