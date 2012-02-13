#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Yum package manager interface
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.packagemanagement import PackageManagerBase, \
                                                  PackageManagerError
from hypernova.libraries.environment import where_is
from hypernova.libraries.permissionelevation import elevate_cmd
import subprocess

class PackageManager(PackageManagerBase):
    """
    Yum package manager.
    """

    __path = None

    def __init__(self):
        self.__yum_path = where_is('yum')

    def install(self, *pkgs):
        pass

    def refresh(self):
        status = super().exec_cmd([self.__yum_path, 'check-update'],
                                  expected_statuses=[0, 100])

        if status == 0:
            status = (True, False)
        elif status == 100:
            status = (True, True)

        return status

    def uninstall(self, *pkgs):
        pass
