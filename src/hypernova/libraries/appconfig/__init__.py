#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Application configuration generation/parsing
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from copy import deepcopy
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.environment import service_ctl as env_service_ctl
from hypernova.libraries.packagemanagement import get_package_db, \
                                                  get_package_manager
from hypernova.libraries.permissionelevation import elevate_cmd
from os import environ, listdir, unlink
from os.path import dirname, join, realpath
import json
import subprocess
import sys

class AppConfigBase:
    """
    Base class for all configuration objects.
    """

    pass


class AppProvisionerBase:
    """
    Base class for all "initial" (i.e. run once) configuration objects.

    For information on the execution entry points for this class, please consult
    the hypernova.provisioner package documentation.
    """

    _module_name = None

    _base_cmd = [
        sys.executable,
        realpath(join(dirname(sys.argv[0]), 'provisioner.py')),
        'app',
    ]

    _packages = None

    proc = None

    def __init__(self, **args):
        """
        Initialise the provisioner.
        """

        self.parameters = args

        config = ConfigurationFactory.get('hypernova')

        # This will only be possible when in the context of the agent, so if we
        # fail, it's not an issue. This ought to be cleaned up.
        try:
            self._base_cmd.append(config['provisioner']['config_dir'])
        except KeyError:
            pass

    def install_packages(self):
        """
        Install system packages.
        """

        packages = get_package_db().resolve(*self._packages).values()

        get_package_manager().install(packages)

    def do_provision(self, *args):
        """
        Called by the app provisioner to perform the provisioning operation.

        Note: you should NOT call this method from your own code. Doing so will
              lead to huge permission issues. Use provision() instead, which
              handles the initialisation of the provisioner utility.
        """

        self._provision(*args)

    def provision(self):
        """
        Provision the service unit in a subprocess.

        Handle the initialisation of the provisioner utility and hand off the
        deployment of the unit to it. This is the method which should be called
        from agent modules, not do_provision().
        """

        # It's busy -- leave it well alone.
        #
        # Under normal circumstances it's impossible for this to happen, since
        # a call to wait() will block the thread. It may catch calls to other
        # threads, but we really need a true semaphore locking solution to
        # ensure robustness under load.
        try:
            if self.proc.poll() is None:
                raise ProvisioningError('attempted to provision whilst another '
                                        + 'operation was in progress')
        except AttributeError:
            pass

        # Copy value, don't get a reference.
        #
        # This isn't very "pythonic", but we need to ensure we don't taint the
        # base command just in case a developer reuses the provisioning class.
        cmd = deepcopy(self._base_cmd)

        cmd.append(self.module_name)
        cmd.extend(list(map(str, self.parameters)))

        self.proc = subprocess.Popen(elevate_cmd(cmd))

    def service_ctl(self, action):
        """
        Perform an action on the application's service.

        To use this method, you'll need to define __sys_service on your
        provisioning class. It's this name and the method parameter which is
        passed to HyperNova's underlying environment library.
        """

        env_service_ctl(self._sys_service, action, require_elevation=False)


class ProvisioningError:
    pass
