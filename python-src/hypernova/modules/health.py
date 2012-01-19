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

class AgentRequestHandler(BaseRequestHandler):
    def do_status():
        return BaseRequestHandler._format_response(True, 200)
