#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Site deployment module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>

from hypernova.modules import AgentRequestHandlerBase, \
                              ClientRequestBuilderBase, \
                              ClientResponseFormatterBase

class AgentRequestHandler(AgentRequestHandlerBase):
    """
    Site deployment/management for the agent.
    """

    def do_deploy():
        """
        Deploy a site from a profile.
        """

class ClientRequestBuilder(ClientRequestBuilderBase):
    """
    Site deployment/management for the client request assembler.
    """

    def init_subparser(subparser, subparser_factory):
        sp = subparser_factory.add_parser('deploy')
        for a in ['profile']:
            sp.add_argument(a)

    def do_deploy():
        """
        Deploy a site from a profile.
        """

class ClientResponseFormatter(ClientResponseFormatterBase):
    """
    Site deployment/management for the client response formatter.
    """

    def do_deploy():
        """
        Deploy a site from a profile.
        """
