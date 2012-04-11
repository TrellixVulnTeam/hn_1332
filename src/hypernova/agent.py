#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent application package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from http.server import HTTPServer, BaseHTTPRequestHandler
from hypernova import GPG, modules
import json
import logging
import logging.handlers
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.proc import daemonise
import os
import socket
from socketserver import ThreadingMixIn
import sys

# Log types, used within hypernova.agent.AgentRequestHandler
LOG_MESSAGE = 1
LOG_ERROR   = 2

class Agent:
    """
    HyperNova agent.

    The agent class provides a long-running daemon process that behaves as an
    HTTP server. Once launched, it listens on the specified address and port
    combination for PGP-encrypted (and signed) connections, calling out to its
    modules to perform actions on the server and returning relevant data to the
    client.
    """

    _server = None

    _main_log           = None
    _main_log_formatter = None
    _main_log_handler   = None
    _req_main_log       = None
    _req_log_formatter  = None
    _req_log_handler    = None
    _err_log            = None
    _err_log_formatter  = None
    _err_log_handler    = None

    _config = None

    _gpg = None

    def __init__(self, config_root_dir):
        """
        Prepare the agent daemon.

        Initialise the internals of the daemon such that it can be executed as
        desired. The agent first opens its log files to ensure errors are duly
        noted before parsing all files in the specified directory.

        To launch the server, simple call the execute() method on the agent
        object.
        """

        # Initialise logging early
        #
        # This allows us to print messages to the screen when errors occur
        # without the developer having to be wary of whether the loggers have
        # been configured yet.
        self._init_logging()

        self._init_config(config_root_dir)

    def execute(self):
        """
        Execute the agent daemon.

        Enters into the main server loop after configuring the loggers to write
        their output to the logs specified in the configuration, instead of
        sys.STDOUT.
        """

        self._init_gpg()
        self._config_logging()

        if self._config.getboolean('server', 'daemon'):
            daemonise()

        self._init_modules()

        addr = (self._config['server']['address'],
                int(self._config['server']['port']))
        self._server = AgentServer(addr, AgentRequestHandler, self._gpg)
        self._main_log.info('entering server main loop')
        self._server.serve_forever()
        self._main_log.info('server exiting')

    def _init_config(self, config_root_dir):
        """
        Initialise configuration values.

        See __init__() for more information.
        """

        self._main_log.info('loading configuration from directory %s'
                            %(config_root_dir))
        self._config = ConfigurationFactory.get('hypernova',
                                                root_dir=config_root_dir,
                                                log=self._main_log)

        if not self._config:
            self._main_log.critical('loading configuration failed')
            sys.exit(78)

    def _init_gpg(self):
        """
        Initialise GPG encryption and signing mechanisms.

        See __init__() for more information.
        """

        self._gpg = GPG.get_gpg(gnupghome=self._config['gpg']['key_store'],
                                          instancename='hn-agent')
        gpg_secrets = self._gpg.list_keys(True)

        for key in gpg_secrets:
            if key['fingerprint'] == self._config['gpg']['fingerprint']:
                self._gpg._secret_key = key
                break

        if not hasattr(self._gpg, '_secret_key'):
            self._main_log.error('no GPG private key configured; aborting')
            sys.exit(78)

    def _init_logging(self):
        """
        Initialise logs.

        Ensure that logging output doesn't get lost; since log files aren't
        available until configuration has been loaded. This is necessary before
        configuration is loaded in case an error occurs during initialisation.

        See __init__() for more information.
        """

        self._main_log_formatter = logging.Formatter(
            fmt = '[%(asctime)s] [%(levelname)-1s] %(message)s',
            datefmt = '%d/%m/%Y %I:%M:%S')

        self._main_log = logging.getLogger('hn-main')
        self._main_log.setLevel(logging.DEBUG)

        self._req_log = logging.getLogger('hn-request')
        self._req_log.setLevel(logging.DEBUG)

        self._err_log = logging.getLogger('hn-error')
        self._err_log.setLevel(logging.DEBUG)

        self._main_log.info('initialised logging')

    def _config_logging(self):
        """
        Configure the logs with known paths.

        Allow the log objects to log to their respective files instead of
        STDOUT, since log paths are known after configuration has been loaded.
        """

        self._main_log.info('redirecting logging output to files')

        self._main_log_handler = logging.handlers.RotatingFileHandler(
            self._config['logging']['main_log'], mode='a')
        self._main_log_handler.setFormatter(self._main_log_formatter)
        self._main_log.addHandler(self._main_log_handler)

        self._req_log_handler = logging.handlers.RotatingFileHandler(
            self._config['logging']['request_log'], mode='a')
        self._req_log_handler.setFormatter(self._main_log_formatter)
        self._req_log.addHandler(self._req_log_handler)

        self._err_log_handler = logging.handlers.RotatingFileHandler(
            self._config['logging']['error_log'], mode='a')
        self._err_log_handler.setFormatter(self._main_log_formatter)
        self._err_log.addHandler(self._err_log_handler)

    def _init_modules(self):
        """
        Allow modules a chance to initialise (if necessary).

        Some modules may require specialised configuration in order to function.
        here, the agent passes the configuration it has loaded to the
        initialisation methods of each of the modules it has loaded. This
        facilitates loading custom configuration directly from the configuration
        files.
        """

        for module_name in modules.__all__:
            self._main_log.info('initialising module %s' %(module_name))
            module = getattr(modules, module_name)
            if not hasattr(module, '_agent_init'):
                self._main_log.warn('module %s had no initialiser (_agent_init)'
                                    %(module_name))
                continue

            module._agent_init(self._config)

class AgentServer(ThreadingMixIn, HTTPServer):
    """
    Agent multi-threaded HTTP server.

    The HyperNova agent executes each operation in its own thread to increase
    performance, scalability and stability. In doing so, the server is always
    free to open new connections with clients, since all requests are
    non-blocking.

    For details of the execution workflow used to serve each request, see the
    AgentRequestHandler class.
    """
    pass


class AgentRequestHandler(BaseHTTPRequestHandler):
    """
    Agent request handler.

    This class is instantiated once per request, and is active only during the
    lifetime of this request.
    """

    _log = None
    _err = None

    def __init__(self, request, client_address, server):
        """
        Initialise the request.

        Initialises the logger and GPG interface in preparation for handling the
        request. This enables us to write any debugging information to the log
        and retain key metadata to save resources with larger GPG keyrings.
        """

        # Overridden from BaseHTTPRequestHandler
        #
        # This override enables logging to our dedicated request log.

        self._log = logging.getLogger('hn-request')
        self._err = logging.getLogger('hn-error')

        self._gpg = GPG.get_gpg(instancename='hn-agent')

        super().__init__(request, client_address, server)

    def handle_one_request(self):
        """
        Serve a single request.
        """

        # Overridden from BaseHTTPRequestHandler
        #
        # By overriding the method, we're able to use custom HTTP methods in
        # module request handlers without defining the methods in this class.

        try:
            self.raw_requestline = self.rfile.readline(65537)

            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414, 'Request entity too large')
                return

            if not self.raw_requestline:
                self.close_connection = 1
                return

            if not self.parse_request():
                return

            # We will *always* return JSON from this point onward
            self.send_header('Content-Type', 'application/json');

            # Ensure the request has a body
            #
            # To ensure security, the action to perform is ascertained based
            # upon the action value in the JSON body of the request. If this is
            # not set, there's no point wasting CPU cycles trying to decrypt it.
            try:
                length = int(self.headers.get('Content-Length'))
                raw = self.rfile.read(length)
            except TypeError:
                self.log_error('Content-Length not set; assuming no parameters')
                self.send_error(400, 'No parameters')
                return

            # Verify signature trustworthiness and decrypt parameters
            #
            # The body of the request will be an ASCII-armored PGP message. In
            # order to read it we must do two things:
            #
            # * ensure that the content within the body was signed by a trusted
            #   keypair present in our keyring; and
            # * successfully decrypt the output using the server's private key.
            #
            # Only when both criteria are met can we be sure that the request
            # came from an authorised machine.
            self.clear = self._gpg.decrypt(raw)
            if str(self.clear) == '':
                self.log_error('decrypted request body empty; potential authentication failure')
                self.send_error(403, 'Access denied')
                return

            if not hasattr(self.clear, 'fingerprint'):
                self.log_error('data unsigned or signing key not in local key store')
                self.send_error(403, 'Access denied')
                return

            # Decode the parameters
            try:
                params = json.loads(str(self.clear))
            except ValueError:
                self.log_error('failed to interpret parameters as JSON')
                self.send_error(400, 'Invalid parameters')
                return

            # Establish the action to perform
            #
            # The action parameter in the request is passed in the form:
            #
            #     module.submodule.action
            #
            # Submodule support is not yet part of the agent, but is likely to
            # be incorporated very soon and will enable cleaner namespacing of
            # actions.
            try:
                (self.module_name, self.action) = params['action'].rsplit('.', 1)
            except ValueError:
                self.send_error(400, 'Action not namespaced')

            try:
                module = getattr(modules, self.module_name)
                handler = getattr(module, 'AgentRequestHandler')
            except (AttributeError, KeyError):
                self.send_error(501, 'Unsupported module')
                return

            try:
                method = getattr(handler, 'do_' + self.action.lower())
            except AttributeError:
                self.send_error(405, 'Unsupported method')
                return

            # Perform the action
            if 'parameters' not in params:
                params['parameters'] = {}

            self.send_response(200, 'OK')

            # Handle all exceptions
            #
            # http://wiki.python.org/moin/HandlingExceptions#line-26
            try:
                response = method(params['parameters'])
                self.send_preformatted_response(response)
            except:
                self.send_error(500, 'Module execution failure')
                return

        except socket.timeout as e:
            self.log_error('request timed out (%r)', e)
            self.close_connection = 1
            return

    def log_error(self, format, *args):
        """
        Write an error to the log.
        """

        # Overridden from BaseHTTPRequestHandler
        #
        # Implement logging to a different place, since the Python standard
        # library edition doesn't seem to support it.

        msg = format %(args)
        self._err.error("[%s:%d] %s" %(self.client_address[0],
                                       self.client_address[1], msg))

    def log_exception(self, exc):
        """
        Write an exception to the log.
        """

        self._err.exception("[%s:%d] exception:" %(self.client_address[0],
                                                   self.client_address[1]))

    def log_message(self, format, *args):
        """
        Write a message to the log.
        """

        # Overridden from BaseHTTPRequestHandler
        #
        # The override enables us to reformat the logs to preserve information
        # crucial to issue diagnosis and troubleshooting, like the details of
        # socket, which would otherwise be discarded.

        msg = format %(args)
        self._log.info("[%s:%d] %s" %(self.client_address[0],
                                      self.client_address[1], msg))

    def log_request(self, code):

        # Overridden from BaseHTTPRequestHandler.
        #
        # Don't display the HTTP request line in the log, since it's useless to
        # us. If possible, log the module and action, else log a warning.

        self.log_message("%s.%s - %i", self.module_name, self.action, code)

    def send_error(self, code, message=None, exception=None):

        # Overridden from BaseHTTPRequestHandler
        #
        # In order to ensure consistency and stability in client applications,
        # we must format the data we're sending to the client in JSON at all
        # times. By default, HTTP-style errors are returned by instances.

        try:
            shortmsg, longmsg = self.responses[code]
        except KeyError:
            shortmsg, longmsg = '', ''

        if message is None:
            message = shortmsg

        explain = longmsg

        if not exception:
            exception = sys.exc_info()

        self.log_error('returning %d: %s', code, message)
        self.log_exception(exception)

        self.send_response(code, message)
        self.send_header('Content-Type', self.error_content_type)
        self.send_header('Connection', 'close')
        self.end_headers()

        response = modules.AgentRequestHandlerBase._format_response({}, False, code, '')

        self.send_preformatted_response(response)

    def send_preformatted_response(self, response):
        """
        Encrypt, encode and send a pre-formatted response.
        """

        self.end_headers()
        response = modules.serialise(response)
        response = self._gpg.encrypt(response,
                                     self.clear.fingerprint,
                                     sign=self._gpg._secret_key['fingerprint'])
        self.wfile.write(bytes(str(response), 'UTF-8'))
        self.wfile.flush()

# Execute the agent application.
#
# If the module file was the entry point for execution, instantiate the agent
# class and execute it. This won't occur if the module was imported from
# elsewhere.
if __name__ == '__main__':
    try:
        Agent(sys.argv[1]).execute()
    except IndexError:
        print('%s <config dir>' %(sys.argv[0]),)
        sys.exit(78)
