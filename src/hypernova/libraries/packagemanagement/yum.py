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
        cmd = [self.__yum_path, '--assumeyes', 'install']
        cmd.extend(*pkgs)

        status = super().exec_cmd(cmd, [0, 1])

        if status in (0, 1):
            status = True
        else:
            Status = False

        return status

    def refresh(self):
        status = super().exec_cmd([self.__yum_path, 'check-update'],
                                  expected_statuses=[0, 100])

        if status == 0:
            status = (True, False)
        elif status == 100:
            status = (True, True)

        return status

    def uninstall(self, *pkgs):
        cmd = [self.__yum_path, '--assumeyes', 'remove']
        cmd.extend(*pkgs)

        status = super().exec_cmd(cmd)

        if status == 0:
            status = True
        else:
            Status = False

    def update(self, upgrade=False, *pkgs):
        cmd = [self.__yum_path]

        if upgrade:
            cmd.append('upgrade')
        else:
            cmd.append('update')

        cmd.append('--assumeyes')

        if len(pkgs) > 0:
            cmd.extend(pkgs)

        status = super().exec_cmd(cmd, expected_statuses=[0])

        if status == 0:
            return True
        else:
            return False
