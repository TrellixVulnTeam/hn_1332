#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# MySQL application configuration management library tests.
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from unit import UnitTestCase

from hypernova.libraries.appconfig.dbserver import Database, User
from hypernova.libraries.appconfig.dbserver.mysql import Server
import oursql

class TestLibrariesAppconfigDbserverMysql(UnitTestCase):
    """
    Test methods provided by the MySQL application configuration management
    library.
    """

    credentials = {
        "host":     "127.0.0.1",
        "username": "hntestuser",
        "password": "apassword",
    }

    test_db   = "hntestdb"
    test_user = ("hntestusera", "apassword")

    def count_db(self):
        with self.get_db() as dbms:
            with dbms as cursor:
                cursor.execute("SELECT COUNT(`Db`) FROM `mysql`.`db` WHERE `Db` = ?",
                               (self.test_db,))
                return cursor.fetchone()[0]

    def create_db(self):
        with self.get_db() as dbms:
            with dbms as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS `%s`" %(self.test_db))

    def drop_db(self):
        with self.get_db() as dbms:
            with dbms as cursor:
                cursor.execute("DROP DATABASE IF EXISTS `%s`" %(self.test_db))

    def get_db(self):
        return oursql.connect(host=self.credentials["host"],
                              user=self.credentials["username"],
                              passwd=self.credentials["password"])

    def drop_user(self):
        with self.get_db() as dbms:
            with dbms as cursor:
                try:
                    cursor.execute("DROP USER '%s'@'localhost'" %(self.test_user[0]))
                except oursql.OperationalError:
                    pass

    def test_add_user(self):
        self.drop_user()

        server = Server(**self.credentials)
        user = User(username=self.test_user[0], password=self.test_user[1],
                    host="localhost")
        result = server.add_user(user)

        with self.get_db() as dbms:
            with dbms as cursor:
                cursor.execute("SELECT COUNT(`User`) FROM `mysql`.`user` WHERE `User` = ?",
                               (self.test_user[0],))
                self.assertEqual(1, cursor.fetchone()[0])

        self.drop_user()

    def test_add_database(self):
        self.drop_db()

        server = Server(**self.credentials)
        db = Database(name=self.test_db, character_set="utf8")
        server.add_database(db)

        self.assertEqual(1, self.count_db())

        self.drop_db()

    def test_rm_database(self):
        self.create_db()

        server = Server(**self.credentials)
        db = Database(self.test_db)
        server.rm_database(db)

        self.assertEqual(0, self.count_db())

    def test_rm_user(self):
        pass
