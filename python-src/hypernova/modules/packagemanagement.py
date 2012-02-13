#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Package management module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.packagemanagement import get_package_manager
from hypernova.modules import AgentRequestHandlerBase

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_refresh(params):

        pm = get_package_manager()
        (success, needs_update) = pm.refresh()

        return AgentRequestHandler._format_response(
            {
                'needs_update': needs_update
            },
            success,
            int(success)
        )
