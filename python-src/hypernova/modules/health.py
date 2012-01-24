#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Node health module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.agent.module_base import BaseRequestHandler
from hypernova.client.module_base import BaseActionHandler
import subprocess

class AgentRequestHandler(BaseRequestHandler):

    def do_load_averages(params):

        raw = str(subprocess.check_output(['cat', '/proc/loadavg']), 'UTF-8')
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
