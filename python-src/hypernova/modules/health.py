#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Node health module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.agent.modulebase import BaseRequestHandler
import subprocess

class AgentRequestHandler(BaseRequestHandler):

    def do_load_averages(params):

        try:
            with open('/proc/loadavgs', 'r') as f:
                raw = f.read()
        except IOError:
            return BaseRequestHandler._format_response(False, 0x00000001)

        parts = raw.split(' ')

        return BaseRequestHandler._format_response(
            {
                '1m':  float(parts[0]),
                '5m':  float(parts[1]),
                '15m': float(parts[2])
            },
            True,
            200
        )
