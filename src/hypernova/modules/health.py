#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Node health module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.modules import AgentRequestHandlerBase
import subprocess

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_load_averages(params):

        try:
            with open('/proc/loadavg', 'r') as f:
                raw = f.read()
        except IOError as e:
            return AgentRequestHandler._format_response(False, 1)

        parts = raw.split(' ')

        return AgentRequestHandler._format_response(
            {
                '1m':  float(parts[0]),
                '5m':  float(parts[1]),
                '15m': float(parts[2])
            },
            True,
            200
        )
