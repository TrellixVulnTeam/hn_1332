#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Self-test module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.modules import AgentRequestHandlerBase, \
                              ClientRequestBuilderBase, \
                              ClientResponseFormatterBase
from hypernova.libraries.appconfig.snmpd import AppConfig as SnmpdConfig
from hypernova.libraries.appconfig.httpserver.nginx import AppConfig
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.environment import where_is
from hypernova.libraries.permissionelevation import elevate_cmd
import subprocess

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_elevation(params):

        cmd    = elevate_cmd([where_is('whoami')])
        target = ConfigurationFactory.get('hypernova')['elevation']['target']

        try:
            elevated_user = str(subprocess.check_output(cmd), 'UTF-8').strip('\n')
        except subprocess.CalledProcessError:
            elevated_user = None

        if elevated_user == target:
            status = True
        else:
            status = False

        result = {
            "response": status,
            "successful": status,
        }
        return AgentRequestHandlerBase._format_response(**result)

    def do_httpserver_nginx_vhost(params):

        conf = AppConfig()
        vhost = conf.get_virtualhost()

        vhost.listen_socket = ['0.0.0.0', 80]
        vhost.server_names  = ['google.com']
        vhost.document_root = '/var/www/html'
        vhost.indexes       = ['index.php']
        vhost.auto_index    = True

        vhost.dynamic_langs['php'] = True

        vhost_repr = str(vhost)

        result = {
            "response": {
                "translated": vhost_repr
            },
            "successful": isinstance(vhost_repr, str)
        }
        return AgentRequestHandlerBase._format_response(**result)

    def do_snmpd_conf(params):

        conf = SnmpdConfig()
        conf.sys_contact = 'Joe Bloggs <joe@bloggs.host.name>'
        conf.sys_location = 'HyperNova Project <hypernova.org>'
        conf.rw_communities = [
            ['communityname', 'arbitrary.host.name']
        ]
        conf.load = (1.0, 0.9, 0.8)
        conf.disks = [
            ('/', 10)
        ]

        conf_repr = str(conf)

        result = {
            "response": {
                "translated": conf_repr
            },
            "successful": isinstance(conf_repr, str)
        }
        return AgentRequestHandlerBase._format_response(**result)

    def do_raise(params):

        raise Exception('testing exception handling')


class ClientRequestBuilder(ClientRequestBuilderBase):
    pass
