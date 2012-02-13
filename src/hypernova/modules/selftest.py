#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Self-test module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.modules import AgentRequestHandlerBase
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.environment import where_is
from hypernova.libraries.permissionelevation import elevate_cmd
import subprocess

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_elevation(params):

        cmd    = elevate_cmd([where_is('whoami')])
        target = ConfigurationFactory.get('hn-agent')['elevation']['target']

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
