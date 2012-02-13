#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Package management API
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import platform
import subprocess
from hypernova.libraries.permissionelevation import elevate_cmd

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

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        status = proc.wait()

        if status not in expected_statuses:
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

    def update(self, *pkgs, upgrade=False):
        """
        Update packages.
        """

        pass

class PackageManagerError(Exception):
    pass
