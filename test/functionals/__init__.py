#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Test harness
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.configuration import ConfigurationFactory
import configparser
from copy import deepcopy
from gnupg import GPG
import os
import shutil
import subprocess
import sys
import time
import unittest

class ModuleFunctionalTestCase(unittest.TestCase):
    """
    Base test case.

    Configure and launch the agent daemon for the purposes of a test suite to
    run, then tear it down once the suite has run.
    """

    # How many seconds the test harness should wait for the agent to initialise.
    agent_init_time = 1

    agent_proc = None

    agent_env  = {}
    client_env = {}

    # Both host and port must be strings
    agent_addr = ('localhost', '10101')

    # Result set from last client action; used by the agent functions.
    #
    # When an error occurs in the context of a test suite, we can output this to
    # give the developer a better idea of what was expected.
    last_result = ()

    gpg_params = {
        'key_type':     'RSA',
        'key_length':   1024,
        'name_real':    'HyperNova testing',
        'name_comment': 'HyperNova testing',
        'name_email':   'test@hn.org',
    }

    def __init__(self, tests=()):
        """
        Initialise the testing environment.
        """

        super().__init__(tests)

        self.agent_env = dict(deepcopy(os.environ).items())
        agent_env_overrides = {
            'CONFDIR': os.path.join(os.environ['HOME'], '._hypernova',
                                    'agent.ini'),
        }
        self.agent_env.update(agent_env_overrides)

        self.client_env = dict(deepcopy(os.environ).items())
        client_env_overrides = {
            'CONFDIR': os.path.join(os.environ['HOME'], '._hypernova')
        }
        self.client_env.update(client_env_overrides)

    def setUp(self):
        """
        Construct environment.

        Here, we adopt the configuration used by the production or development
        installation and make the necessary changes before writing it to a new
        file in the etc directory. When we're finished, we'll remove it in the
        tearDown() function.
        """

        if not os.path.exists(self.client_env['CONFDIR']):

            # Don't waste time and entropy on keys if we can't write configuration
            # files -- that's a very distressing experience.
            assert len(sys.argv) == 2

            # Prepare two GPG keypairs; one for the agent, one for the client
            agent_gpg_dir  = os.path.join(self.client_env['CONFDIR'], 'agent_gpg')
            agent_gpg      = GPG(gnupghome=agent_gpg_dir)
            agent_key      = agent_gpg.gen_key(agent_gpg.gen_key_input(**self.gpg_params))
            client_gpg_dir = os.path.join(self.client_env['CONFDIR'], 'client_gpg')
            client_gpg     = GPG(gnupghome=client_gpg_dir)
            client_key     = client_gpg.gen_key(client_gpg.gen_key_input(**self.gpg_params))

            # Export both public keys; import them into the opposing side
            agent_key_blob  = agent_gpg.export_keys(agent_key.fingerprint)
            client_gpg.import_keys(agent_key_blob)
            client_gpg.sign_key(agent_key.fingerprint)
            client_key_blob = client_gpg.export_keys(client_key.fingerprint)
            agent_gpg.import_keys(client_key_blob)
            agent_gpg.sign_key(client_key.fingerprint)

            # Configure the agent to run in a development-safe configuration.
            #
            # Here, we load the base configuration we ship with the application
            # as the default. All other configuration will be ignored for the
            # purposes of the test run, since this is outside of our scope.
            with open(self.agent_env['CONFDIR'], 'w') as f:
                l = os.path.join(self.client_env['CONFDIR'], 'agent_%s.log')
                agent_cfg = ConfigurationFactory.get('hypernova.agent',
                                                     root_dir=sys.argv[1])
                agent_cfg.set('server',  'address',     self.agent_addr[0])
                agent_cfg.set('server',  'port',        self.agent_addr[1])
                agent_cfg.set('server',  'daemon',      'false')
                agent_cfg.set('gpg',     'key_store',   agent_gpg_dir)
                agent_cfg.set('gpg',     'fingerprint', agent_key.fingerprint)
                agent_cfg.set('logging', 'main_log',    l %('main'))
                agent_cfg.set('logging', 'request_log', l %('request'))
                agent_cfg.set('logging', 'error_log',   l %('error'))
                agent_cfg.write(f)

            # The client has to use two different configuration files, both in
            # the same directory.
            client_cfg_dir = self.client_env['CONFDIR']

            # Configure the client to use its temporary key.
            #
            # To communicate with the agent (which will be running in a limited
            # testing mode), we'll need to reconfigure the client with a keypair
            # we've imported into the agent. This keystore manipulation has
            # already taken place, so we know the fingerprint of our new private
            # key.
            client_cfg_file = os.path.join(client_cfg_dir, 'client.ini')
            with open(client_cfg_file, 'w') as f:
                client_cfg      = configparser.SafeConfigParser()
                client_cfg.add_section('client')
                client_cfg.set('client', 'privkey', client_key.fingerprint)
                client_cfg.write(f)

            # Pair the client to the agent.
            #
            # We do this manually, since the importer requires that we write the
            # public key to a file before we import it. This would be a
            # pointless exercise and an unnecessary complication.
            client_srv_file = os.path.join(client_cfg_dir, 'servers.ini')
            with open(client_srv_file, 'w') as f:
                client_srv_cfg  = configparser.SafeConfigParser()
                client_srv_cfg.add_section('local')
                client_srv_cfg.set('local', 'addr', ':'.join(self.agent_addr))
                client_srv_cfg.set('local', 'pubkey', agent_key.fingerprint)
                client_srv_cfg.write(f)

        # TODO: instead of lazily and unreliably falling asleep on the job,
        #       we should probably use a regular expression to check the output.
        #       Time is of the essence, though!
        #       No, we'll use pexpect instead, since it's now shipped as a py3k
        #       dependency.
        agent_cmd = [
            'hn-agent',
            self.agent_env['CONFDIR']
        ]
        self.agent_proc = subprocess.Popen(agent_cmd, env=self.agent_env,
                                           stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
        time.sleep(self.agent_init_time)


    def tearDown(self):
        """
        Destruct environment.
        """

        self.agent_proc.kill()

    def spawnSubProcess(self, cmd, env):
        """
        Spawn a subprocess in the HyperNova environment.

        Handles all environment finickiness of launching a process with the
        correct environment variables. All paths are considered to be relative
        to the HyperNova BINDIR (they'll be prefixed with this).
        """

        if not os.path.isabs(cmd[0]):
            cmd[0] = os.path.join(self.agent_env['BINDIR'], cmd[0])

        return subprocess.Popen(cmd, env=self.agent_env)

    def clientAction(self, params):
        """
        Do something with the client.
        """

        cmd = ['hn-client']
        cmd.extend(params)

        proc = self.spawnSubProcess(cmd, self.client_env)
        proc.wait()

        return (proc.returncode, proc.stdout, proc.stderr)

    def doRequest(self, module, action, params={}):
        """
        hn-client subprocess spawn shortcut.

        Returns a tuple containing the exit status (return code), standard out
        and standard error output.
        """

        cmd = [
            'hn-client',
            'request',
            '--gpg-dir', os.path.join(self.client_env['CONFDIR'], 'client_gpg'),
            'local',
            module,
            action
        ]
        cmd.extend(params)

        proc = subprocess.Popen(cmd, env=self.client_env, stdin=subprocess.PIPE,
                                                          stdout=subprocess.PIPE,
                                                          stderr=subprocess.PIPE)
        proc.wait()

        self.last_result = (proc.returncode, str(proc.stdout.read(), 'UTF-8'),
                                             str(proc.stderr.read(), 'UTF-8'))
        return self.last_result

    def assertZeroLength(self, s):
        """
        Assert a string to contain no characters.
        """

        self.assertZero(len(s))

    def assertZero(self, n):
        """
        Assert a number to be zero.
        """

        self.assertEqual(n, 0)

    def assertNonZero(self, n):
        """
        Assert a number to be anything other than zero.
        """

        self.assertNotEqual(n, 0)

    def _executeTestPart(self, function, outcome, isTest=False):
        """
        Trap failures to display debugging aids.
        """

        super()._executeTestPart(function, outcome, isTest)

        if self.last_result and not outcome.success:
            last_result = (
                self.last_result[0],
                self.last_result[1],
                self.last_result[2],
            )

            # Prevent useless repetition
            self.last_result = ()

            msg = 'Exit status: %s\n\nOutput:\n%s\n\nErrors:\n%s'
            print(msg %last_result)
