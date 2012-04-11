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

import grp
from hypernova.libraries.permissionelevation import elevate_cmd
import pwd

# Global system options
BASE_DIR = None
SKEL     = None

class Group:
    """
    Group structure and associated logic.
    """

    name   = None
    passwd = None
    gid    = None
    mem    = []

    def __init__(self, name_or_id=None):
        """
        Load group information.
        """

        if not name_or_id: # new instance?
            return

        if isinstance(name_or_id, str):
            info = grp.getgrnam(name_or_id)
        elif isinstance(name_or_id, int):
            info = grp.getgrgid(name_or_id)

        (self.name, self.passwd, self.gid, self.mem) = info


class User:
    """
    User structure and associated logic.

    Used to represent a single system user. Note that this class also provides a
    variety of associated logic capable of utilising the system's passwd tool to
    manipulate accounts.

    TODO: implement the remaining options from useradd.
    """

    CREATE_ACCT_CMD   = ['useradd']
    CREATE_ACCT_ARG   = ('%(account)s')
    CREATE_ACCT_KWARG = [
                            ('--base-dir', '%(base_dir)s'),
                            ('--comment', '%(comment)s'),
                            ('--home', '%(home)s'),
                            ('--expiredate', '%(expire_date)i'),
                            ('--inactive', '%(inactive)i'),
                            ('--gid', '%(gid)i'),
                            ('--groups', '%(groups)s'),
                            ('--skel', '%(skel_dir)s'),
                            ('--password', '%(password)s'),
                            ('--shell', '%(shell)s'),
                            ('--uid', '%(uid)i'),
                        ]

    account   = None
    passwd    = None
    uid       = None
    gid       = None
    gecos     = None
    directory = None
    shell     = None

    def __init__(self, name_or_id=None):
        """
        Load user information.
        """

        if name_or_id:
            self.repopulate(name_or_id)

    def repopulate(self, name_or_id):
        """
        Update all ofthe things.
        """

        if isinstance(name_or_id, str):
            info = pwd.getpwnam(name_or_id)
        elif isinstance(name_or_id, int):
            info = pwd.getpwuid(name_or_id)

        (self.account, self.passwd, self.uid, self.gid, self.gecos,
         self.directory, self.shell) = info

    def __run_cmd(self, cmd, kwarg, arg, elevate=True):
        """
        Shortcut for running commands.
        """

        for a, v in args.items():
            cmd.extend((a, v %params))
        cmd.extend(arg)

        if elevate:
            elevate_cmd(cmd)

        print(str(cmd))

        #return result

    def create(self):
        """
        Create a new system user.
        """

        kwarg    = {}
        defaults = globals()

        for p in ['base_dir', 'skel_dir']:
            kwarg[p] = defaults[p.upper()]

        for p in ['passwd', 'uid', 'gid', 'gecos', 'directory', 'shell']:
            kwarg[p] = getattr(self, p)

        arg = [self.CREATE_ACCT_ARG[0] %(getattr(self, 'account'))]

        self.__run_cmd(self.CREATE_ACCT_CMD, self.CREATE_ACCT_KWARGS,
                       arg, elevate=True)

        self.repopulate(self.account)

    def destroy(self):
        """
        Delete a matching system user.
        """


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

