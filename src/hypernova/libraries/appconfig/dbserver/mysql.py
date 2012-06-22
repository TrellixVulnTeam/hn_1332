#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# MySQL database server management adapter
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig.dbserver import Database, User, ServerBase
import inspect
import oursql

class Server(ServerBase):

    DEFAULT_CHARACTER = 'utf8'

    CREATE_USER = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s'"
    DELETE_USER = "DROP USER '%s'@'%s'"

    CREATE_DATABASE = "CREATE DATABASE `%s` CHARACTER SET '%s'"
    DELETE_DATABASE = "DROP DATABASE `%s`"

    GRANT = "GRANT %s ON `%s`.%s TO '%s'@'%s'"

    PERMISSIONS = {
        'all':   'ALL',
        'alter': 'ALTER',
    }

    LIMIT_OPTIONS = {
        'grant': "GRANT OPTION",
    }

    __conn = None

    def __init__(self, host=None, username=None, password=None, port=3306):
        for attr in ('host', 'username', 'password', 'port'):
            setattr(self, attr, locals()[attr])

        credentials = {
            'host':   self.host,
            'user':   self.username,
            'passwd': self.password,
            'port':   self.port,
        }

        self.__conn = oursql.connect(**credentials)

    def add_user(self, user):
        with self.__conn as cursor:
            return cursor.execute(self.CREATE_USER %(user.username,
                                                     user.host,
                                                     user.password),
                                  plain_query=True)

    def rm_user(self, user):
        with self.__con as cursor:
            return cursor.execute(self.DELETE_USER %(user.username, user.host),
                                  plain_query=True)

    def add_database(self, database):
        character_set = 'utf8'
        if hasattr(database, 'character_set'):
            character_set = database.character_set

        with self.__conn as cursor:
            return cursor.execute(self.CREATE_DATABASE %(database.name,
                                                         character_set))

    def rm_database(self, database):
        with self.__conn as cursor:
            return cursor.execute(self.DELETE_DATABASE %(database.name))

    def grant(self, database, user, host, tables, privileges, limit_options=[]):

        if tables == '*':
            database_tables = '*'
        elif (isinstance(tables, list) and len(tables) > 1) \
                or not isinstance(tables, str):
            database_tables = '`' + '`, `'.join(tables) + '`'

        permissions = ''
        for p in privileges:
            permissions += (' ' + self.PERMISSIONS[p])

        permissions += ' WITH'
        for l in limit_options:
            if isinstance(l, list):
                permissions += ' %s %s' %l
            else:
                permissions += (' ' + l)

        with self.__conn as cursor:
            return cursor.execute(self.GRANT %(permissions,
                                               database.name, database_tables,
                                               user.username, host))

    def __del__(self):
        self.__conn.close()
