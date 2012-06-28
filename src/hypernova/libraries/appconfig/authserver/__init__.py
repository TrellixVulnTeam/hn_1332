#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# System user management
#
# NOTE: this module will crash under Windows, since the grp and pwd modules
#       aren't available for it.
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

class ServerBase:
    """
    Authentication server.

    All authentication servers should extend this class, which outlines the
    basic API. Note that this API is _not_ a catch-all for all of the different
    properties available with different accounting systems; properties common to
    users on shadow passworded systems are _not_ akin to those on Kerberos, for
    instance. Be wary of this when interfacing with different authentication and
    authorisation solutions.
    """

    def add_user(self, user):
        """
        Add a new user to the system.
        """

        pass

    def get_user(self, account):
        """
        Get a user by its account name.
        """

        pass

    def rm_user(self, user):
        """
        Remove a user from the system.
        """

        pass

    def update_user(self, user):
        """
        Update a user on the system.
        """

        pass

    def add_group(self, user):
        """
        Add a new group to the system.
        """

        pass

    def get_group(self, group):
        """
        Get a group by its name.
        """

        pass

    def rm_group(self, group):
        """
        Remove a group from the system.
        """

        pass

    def update_group(self, group):
        """
        Update a group on the system.
        """

        pass


class User:
    """
    User structure.

    Used to represent a single system user. In conjuction with the Server class,
    this structure can be used to perform a variety of operations on a server's
    system user accounts.
    """

    account   = None
    passwd    = None
    uid       = None
    gid       = None
    gecos     = None
    directory = None
    shell     = None

    def __init__(self, account=None, password=None, uid=None, gid=None,
                 comment=None, directory=None, shell=None):
        """
        Create a new user.
        """

        self.account   = account
        self.password  = password
        self.uid       = uid
        self.gid       = gid
        self.comment   = comment
        self.directory = directory
        self.shell     = shell


class Group:
    def __init__(self):
        raise Exception("not yet implemented")


class NonexistentUserError(Exception):
    """
    Nonexistent user error.

    Thrown when an account operation is attempted on an account which does not
    exist.
    """

    pass


class UserCollisionError(Exception):
    """
    User collision error.

    Thrown when an attempt to create a user fails because a user with the same
    account name or uid already exists.
    """

    pass


def get_auth_server(adapter):
    """
    Seek and attempt to load a password management tool.
    """

    module_name = "hypernova.libraries.appconfig.authserver.%s" %(adapter)

    module = __import__(module_name, fromlist=["Server"])
    Klass  = getattr(module, "Server")

    return Klass(**kwargs)

