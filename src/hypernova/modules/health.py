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
import subprocess

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
            True,
            200
        )


class ClientRequestBuilder(ClientRequestBuilderBase):
    pass


class ClientResponseFormatter(ClientResponseFormatterBase):
    pass
