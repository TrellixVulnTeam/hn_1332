#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Node health module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.modules import AgentRequestHandlerBase, \
                              ClientRequestBuilderBase, \
                              ClientResponseFormatterBase
import os

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_load_averages(params):

        try:
            avgs = os.getloadavg()
        except OSError as e:
            return AgentRequestHandler._format_response(False, 1)

        return AgentRequestHandler._format_response(
            {
                '1m':  float(avgs[0]),
                '5m':  float(avgs[1]),
                '15m': float(avgs[2])
            },
            successful=True,
            error_code=0
        )


class ClientRequestBuilder(ClientRequestBuilderBase):

    def init_subparser(subparser, subparser_factory):
        subparser_factory.add_parser('load_averages')
        return subparser

    def do_load_averages(cli_args, client):
        return ClientRequestBuilderBase._format_request(
            ['health', 'load_averages']
        )


class ClientResponseFormatter(ClientResponseFormatterBase):

    def do_load_averages(cli_args, response):
        result = 'Load averages:'
        for pair in response['response'].items():
            result += "\n* %s: %s" %pair

        return result
