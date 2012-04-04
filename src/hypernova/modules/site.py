#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Site deployment module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>

from hypernova.libraries.siteconfig import get_provisioner
from hypernova.modules import AgentRequestHandlerBase, \
                              ClientRequestBuilderBase, \
                              ClientResponseFormatterBase

class AgentRequestHandler(AgentRequestHandlerBase):
    """
    Site deployment/management for the agent.
    """

    def do_deploy(params):
        """
        Deploy a site from a profile.
        """

        try:
            Provisioner = get_provisioner(params['profile'])
        except KeyError:
            result = {'error': 'NonexistentProfile'}
            successful = False

        site = Provisioner(domain=params['domain'])
        site.provision()

        result = {}
        successful = True

        return AgentRequestHandlerBase._format_response(
            result,
            successful=successful
        )

class ClientRequestBuilder(ClientRequestBuilderBase):
    """
    Site deployment/management for the client request assembler.
    """

    def init_subparser(subparser, subparser_factory):
        sp = subparser_factory.add_parser('deploy')
        for a in ['profile', 'domain']:
            sp.add_argument(a)

    def do_deploy(cli_args, client):
        """
        Deploy a site from a profile.
        """

        return ClientRequestBuilderBase._format_request(
            ['site', 'deploy'], {
                'profile': cli_args.profile,
                'domain':  cli_args.domain,
            }
        )

class ClientResponseFormatter(ClientResponseFormatterBase):
    """
    Site deployment/management for the client response formatter.
    """

    errors = {
        'NonexistentProfile': 'the specified profile does not exist or is not installed',
    }

    def do_deploy(cli_args, response):
        """
        Deploy a site from a profile.
        """

        result = "Failed: %s"

        if response['status']['successful']:
            result = str(response) #''
        else:
            result = result %(
                ClientResponseFormatter.errors[response['response']['error']])

        return result
