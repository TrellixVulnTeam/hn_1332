#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Service provisioning module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig import snmpd
from hypernova.modules import AgentRequestHandlerBase, \
                              ClientRequestBuilderBase, \
                              ClientResponseFormatterBase

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_install(params):

        config = snmpd.AppConfig()

        config.sys_contact  = params['system']['contact']
        config.sys_location = params['system']['location']

        config.load = params['load']

        config.rw_communities = params['communities']['rw']

        config.disks = params['disks']

        unit = snmpd.AppProvisioner(config)
        result = unit.provision()

        return AgentRequestHandler._format_response(
            {
                'configuration': str(config)
            },
            False,
            500
        )


class ClientRequestBuilder(ClientRequestBuilderBase):
    pass
