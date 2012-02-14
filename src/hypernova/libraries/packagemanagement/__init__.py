#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Package management API
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import json
import os
import platform
import subprocess
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.permissionelevation import elevate_cmd

def get_package_db(pdb_name=None):
    """
    Get the system's associated package DB.
    """

    prof_dir = ConfigurationFactory.get('hn-agent')['platforms']['profile_dir']
    pdb_fmt = os.path.join(prof_dir, '%s', 'packages.json')

    if not pdb_name:
        os_info = platform.dist()

        if os_info[0].lower() in ('centos', 'fedora'):
            pdb_name = 'rhel-6'

    return PackageDB(pdb_fmt %(pdb_name))

def get_package_manager(pm_info=None):
    """
    Get an instance of the system's package manager interface.
    """

    if not pm_info:
        os_info = platform.dist()

        if os_info[0].lower() in ('centos', 'fedora'):
            pm_info = ('rpm', 'yum')

    try:
        module = __import__('%s.%s' %(__name__, pm_info[1]),
                            fromlist=['PackageManager'])
        return module.PackageManager()
    except ImportError:
        return None

class PackageDB:
    """
    Package database.

    Provides a means of abstracting across package names on different Linux
    distributions.
    """

    _db = None

    def __init__(self, packagedb):
        """
        Prepare the package DB.
        """

        with open(packagedb, 'r') as f:
            self._db = json.load(f)

    def resolve(self, *pkgs):
        """
        Translate a set of package aliases into their platform-native
        equivalents.
        """

        resolved = {}

        for pkg in pkgs:
            resolved[pkg] = self._db[pkg]

        return resolved

class PackageManagerBase:
    """
    Package manager base class.
    """

    def __init__(self):

        """
        Initialise the package manager interface.
        """

        pass

    def exec_cmd(self, cmd, expected_statuses=[0], elevate=True):
        """
        Run a command via the package manager.
        """

        if elevate:
            cmd = elevate_cmd(cmd)

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        status = proc.wait()

        if status not in expected_statuses:
            print(str(proc.communicate()))
            raise PackageManagerError('Unexpected exit status %i' %(status))

        return status

    def install(self, *pkgs):
        """
        Install package(s).
        """

        pass

    def refresh(self):
        """
        Refresh the list of available packages.

        Accepts no parameters, and so cannot check whether or not certain
        packages are in need of updating. Returns a tuple:

            (successful, needs_updating)
        """

        pass

    def uninstall(self, *pkgs):
        """
        Uninstall package(s).
        """

        pass

    def update(self, upgrade=False, *pkgs):
        """
        Update packages.
        """

        pass

class PackageManagerError(Exception):
    pass
