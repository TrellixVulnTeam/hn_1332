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
import gzip
from hypernova.libraries.appconfig import httpserver
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.permissionelevation import elevate_cmd
from hypernova.libraries.usermanagement import Group, User
from os import chown, unlink, walk
from os.path import dirname, isdir, join, realpath
import oursql
import pkgutil
from random import choice
from shutil import move, rmtree
import string
import subprocess
import sys
import tarfile
import tempfile
from urllib import request

class SiteConfigBase:
    """
    Base class for all configuration objects.
    """

    def __str__(self):
        """
        Return a string representation.

        Assemble a configuration file from the options defined within the
        object.
        """


class SiteProvisionerBase:
    """
    Base class for all provisioner objects.

    This class is comprised mostly of utility functions that provide a good
    starting point for deployment. In the long run, we probably want to move
    most of this code into more focused modules.
    """

    # Different associated resources
    #
    # We "serialise" these resources' properties to store them in the data store
    # database. This enables us to associate a site with all of its components
    # without shoehorning applications into a "one size fits all" pattern.
    resources = []

    # The name of the current module
    #
    # We use this string to seek related classes required in the provisioning
    # run.
    module_name = ''

    # Base command to shell out with
    _base_cmd = []

    # The command we'll actually execute
    cmd = []

    # These files should be cleaned up post-provisioning
    temporary_files = []

    def __init__(self, *args):
        """
        Initialise the provisioner.
        """

        self.parameters = args
        self.config = ConfigurationFactory.get('hypernova')

        # Try to be tolerant of calls outside of the agent where we don't have
        # access to our normal configuration
        try:
            self._base_cmd.append(self.config['provisioner']['binary'])
        except KeyError:
            self._base_cmd.append(join(dirname(sys.argv[0]), 'provisioner.py'))
        self._base_cmd.append('site')

        self.env = deepcopy(environ)
        try:
            self.env['CONFDIR'] = self.config['provisioner']['config_dir']
        except KeyError:
            pass

    def _init_http_server(self):
        """
        Get an HTTP server object.

        The resulting object will correspond with the provisioner configuration.
        I.e. if the server is an Apache HTTPd one, we'll return an Apache
        object, etc.

        TODO: properly take into account directory mapping for custom
              configurations (see httpserver.AppConfig.__init__()).
        """

        server_mod = getattr(httpserver, self.config['web']['server'])
        self.http_server = server_mod.AppConfig(self.config['web']['conf_dir'])

    def _random_string(self, length):
        """
        Generate a random alphabetical string.
        """

        result = ''

        for i in range(length):
            result += choice(string.ascii_letters)

        return result

    def create_mysql_database(self):
        """
        Create a database and associated credentials.

        TODO: keep a mapping of all of these.
        TODO: move this code into another library.
        """

        CREATE_USER = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s'"
        CREATE_DB   = "CREATE DATABASE `%s` CHARACTER SET '%s'"
        GRANT       = "GRANT ALL PRIVILEGES ON `%s`.* TO '%s'@'%s'"

        self.credentials = {
            'host':   self.config['mysql']['host'],
            'user':   self.config['mysql']['username'],
            'passwd': self.config['mysql']['password'],
        }
        db = oursql.connect(**self.credentials)

        user_and_db = self._random_string(int(self.config['mysql']['username_length']))
        password    = self._random_string(int(self.config['mysql']['password_length']))
        host        = self.config['mysql']['host']

        try:
            with db as cursor:
                cursor.execute(CREATE_USER %(user_and_db, host, password),
                               plain_query=True)
            with db as cursor:
                cursor.execute(CREATE_DB %(user_and_db, 'utf8'),
                               plain_query=True)
            with db as cursor:
                cursor.execute(GRANT %(user_and_db, user_and_db, host),
                               plain_query=True)
        finally:
            db.close()

        return {
            'host':     host,
            'username': user_and_db,
            'password': password,
            'db':       user_and_db,
        }

    def create_system_user(self):
        """
        Add a new system user.
        """

        user = User()
        user.account  = self._random_string(int(self.config['system']['account_length']))
        user.password = self._random_string(int(self.config['system']['password_length']))

        if self.config['core']['mode'] == 'production':
            user.create()
        elif self.config['core']['mode'] == 'development':
            user.repopulate(self.config['system']['development_user'])

        return user

    def get_web_group(self):
        """
        Get a web server's group.

        For careless applications who demand insane permissions.
        """

        return Group(self.config['web']['group'])

    def set_ownership(self, user, group, path, recursive=True):
        """
        Give ownership over the specified files to the specified user.

        Wrapper for os.chown() that provides recursive functionality.
        """

        if recursive:
            for root, dirs, files in walk(path):
                for f in dirs + files:
                    chown(join(root, f), user.uid, group.gid)
        else:
            chown(path, user.uid, group.gid)

    def add_vhost(self):
        """
        Get a new VirtualHost instance.

        Note that this method does not commit a virtualhost, but merely provides
        you with an object you may modify and later commit to disk with the
        create_vhost() method.
        """

        if not hasattr(self, 'http_server'):
            self._init_http_server()

        return self.http_server.get_virtualhost()

    def create_vhost(self, vhost):
        """
        Add a virtualhost to the system's web server.
        """

        self.http_server.commit_virtualhost(vhost)
        self.http_server.reload_service()

    def reload_web_server(self):
        """
        Reload the system's web server via its adapter.
        """

        if not hasattr(self, 'http_server'):
            self._init_http_server()

        self.http_server.reload_service()

    def download_url(self, url, suffix=''):
        """
        Download a URL to a local temporary file and return the file's path.
        """

        file = tempfile.mkstemp(suffix=suffix)[1]
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

    def move_tree(self, source, destination):
        """
        Move a tree of files to their destination.
        """

        return move(source, destination)

    def do_provision(self, *args):
        """
        Called by the app PROVISIONER to perform the provisioning operation.

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

        When called from within the agent, handles the initialisation of the
        provisioner utility and hand off the deployment of the unit to it. This
        is the method which should be called from AGENT modules, not
        do_provision().
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
        self.cmd.extend(self.parameters)

        self.proc = subprocess.Popen(elevate_cmd(self.cmd))


    """
    """



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
