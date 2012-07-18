#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# System user management (shadow passwords)
#
# NOTE: this module will crash under Windows, since the grp and pwd modules
#       aren't available for it.
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig.authserver import ServerBase, User
from hypernova.libraries.environment import where_is
from hypernova.libraries.permissionelevation import elevate_cmd
import pwd
import subprocess

# Global system options
BASE_DIR = None
SKEL_DIR = None

class Server(ServerBase):
    """
    Authentication server.

    TODO: account for varying Linux distributions and their user management
          quirks.
    """

    # Command formatting
    UTIL_ARGS = {
        "base_dir":  "--base-dir",
        "gecos":     "--comment",
        "directory": "--home",
        "gid":       "--gid",
        "skel_dir":  "--skel",
        "password":  "--password",
        "shell":     "--shell",
        "uid":       "--uid",
    }

    # Default values for CLI arguments
    UTIL_DEFAULTS = {
        "base_dir": BASE_DIR,
        "skel_dir": SKEL_DIR,
    }

    # Action -> utility mappings; their full path is identified at runtime using
    # where_is()
    ACTIONS = {
        "add":    "useradd",
        "rm":     "userdel",
        "update": "usermod",
    }

    # pwd -> User field mappings
    PWD_USER_MAPPING = {
        "pw_name":   "account",
        "pw_passwd": "password",
        "pw_uid":    "uid",
        "pw_gid":    "gid",
        "pw_gecos":  "comment",
        "pw_dir":    "directory",
        "pw_shell":  "shell",
    }

    def __run_cmd(self, action, user, arguments=[], elevate=True):
        """
        Shortcut for running commands.

        Accepts the following parameters:
          * action: determines the command line utility to execute.
          * user: the user to perform the operation upon.
        """

        cmd = []
        cmd.append(where_is(self.ACTIONS[action]))
        cmd += arguments
        cmd.append(user)

        if elevate:
            cmd = elevate_cmd(cmd)

        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        status = proc.wait()
        (stdout, stderr) = proc.communicate()

        return (status, stdout, stderr)

    def add_user(self, user):
        args = []
        for (param, shell_arg) in self.UTIL_ARGS.items():
            try:
                value = getattr(user, param)
                if value:
                    args += [shell_arg, value]
            except AttributeError:
                # This occurs when looking for skel_dir and base_dir overrides
                pass

        status = self.__run_cmd("add", user.account, args)

        if status[0] == 0:
            (user.password, user.uid, user.gid, user.gecos, user.directory,
             user.shell) = list(pwd.getpwnam(user.account))[1:]

        return status

    def get_user(self, account):
        pwd_info = pwd.getpwnam(account)
        user     = User()
        for (pwd_name, user_name) in self.PWD_USER_MAPPING.items():
            try:
                value = getattr(pwd_info, pwd_name, None)
                setattr(user, user_name, value)
            except KeyError:
                pass

    def rm_user(self, user):
        self.__run_cmd("rm", user.account)

    def update_user(self, user):
        return self.__run_cmd("update", user.account)
