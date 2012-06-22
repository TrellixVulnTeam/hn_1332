#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Database server configuration API interface
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#


class ServerBase:
    """
    Individual server representation.
    """

    host     = ""
    username = ""
    password = ""

    def __init__(self, host=None, username=None, password=None):
        """
        Instantiate a new Server object.
        """

    def add_user(self, user):
        """
        Add a User object.
        """

    def rm_user(self, user):
        """
        Remove a User object.
        """

    def add_database(self, database):
        """
        Add a Database object.
        """

    def rm_database(self, database):
        """
        Remove a Database object.
        """

    def grant(self, database, user, host, tables, privileges, limit_options=[]):
        """
        Grant a User specific privileges on a Database.
        """


class Database:
    """
    Database representation.
    """

    name          = ""
    character_set = ""

    def __init__(self, name=None, character_set=None):
        """
        Instantiate a new Database object.
        """

        self.name = name
        self.character_set = character_set


class User:
    """
    Individual user representation.
    """

    username = ""
    password = ""
    host     = ""

    def __init__(self, username=None, password=None, host=None):
        """
        Create a new user.
        """

        self.username = username
        self.password = password
        self.host     = host


def get_dbms(**kwargs):
    adapter = kwargs.pop('adapter')
    module_name = "hypernova.libraries.appconfig.dbserver.%s" %(adapter)

    module = __import__(module_name, fromlist=['Server'])
    Klass  = getattr(module, 'Server')

    return Klass(**kwargs)
