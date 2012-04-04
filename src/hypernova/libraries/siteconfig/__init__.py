#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Site configuration management package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from copy import deepcopy
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.permissionelevation import elevate_cmd
from os import unlink
from os.path import dirname, isdir, join, realpath
import pkgutil
from shutil import rmtree
import subprocess
import sys
import gzip
import tarfile
import tempfile
from urllib import request

class SiteConfigBase:
    """
    Base class for all configuration objects.
    """

    pass


class SiteProvisionerBase:
    """
    Base class for all provisioner objects.
    """

    module_name = ''

    # Base command to shell out with
    _base_cmd = [
        sys.executable,
        realpath(join(dirname(sys.argv[0]), 'provisioner.py')),
        'site',
    ]

    # The command we'll actually execute
    cmd = []

    # These files should be cleaned up post-provisioning
    temporary_files = []

    def __init__(self, **args):
        """
        Initialise the provisioner.
        """

        self.parameters = args
        self.config = ConfigurationFactory.get('hypernova')

    def download_url(self, url):
        """
        Download a URL to a local temporary file and return the file's path.
        """

        file = tempfile.mkstemp()[1]
        self.temporary_files.append(file)

        request.urlretrieve(url, file)

        return file

    def extract_gzipped_tarball(self, archive):
        """
        Unpack the specified archive to the specified target.
        """

        target = tempfile.mkdtemp()
        self.temporary_files.append(target)

        with tarfile.open(archive) as a:
            a.extractall(path=target)

        return target

    def do_provision(self, *args):
        """
        Called by the app provisioner to perform the provisioning operation.

        Note: you should NOT call this method from your own code. Doing so will
              lead to huge permission issues. Use provision() instead, which
              handles the initialisation of the provisioner utility.
        """

        try:
            self._provision()
        finally:
            # Clean up temporary files used during the installation
            for i in self.temporary_files:
                if isdir(i):
                    rmtree(i)
                else:
                    unlink(i)

    def provision(self):
        """
        Provision the service unit in a subprocess.

        Handle the initialisation of the provisioner utility and hand off the
        deployment of the unit to it. This is the method which should be called
        from agent modules, not do_provision().
        """

        self.cmd = deepcopy(self._base_cmd)

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

        # This will only be possible when in the context of the agent, so if we
        # fail, it's not an issue. This ought to be cleaned up.
        try:
            self.cmd.append(self.config['provisioner']['config_dir'])
        except KeyError:
            pass

        self.cmd.append(self.module_name)
        [self.cmd.append(o) for o in self.parameters.values()]

        self.proc = subprocess.Popen(elevate_cmd(self.cmd))

def get_provisioner(profile_name):
    """
    Attempt to get a site profile.
    """

    return getattr(globals()[profile_name], 'SiteProvisioner')

# Import submodules
#
# Since __all__ only contains imported submodules, we need to walk through the
# packages under this namespace and import them here in order to work with them
# later. This isn't pretty, but it works.
__all__ = []
for (loader, module_name, is_package) in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    module = loader.find_module(module_name).load_module(module_name)
    exec("%s = module" %(module_name))
