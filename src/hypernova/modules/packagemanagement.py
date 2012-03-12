#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Package management module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.packagemanagement import get_package_db, \
                                                  get_package_manager
from hypernova.modules import AgentRequestHandlerBase, ClientQueryInterfaceBase

class AgentRequestHandler(AgentRequestHandlerBase):

    def do_get_package_names(params):

        pdb = get_package_db()
        package_names = pdb.resolve(*params['packages'])

        return AgentRequestHandler._format_response(
            {
                'packages': package_names
            },
            True,
            1
        )

    def do_install(params):

        pm = get_package_manager()
        pdb = get_package_db()

        packages = pdb.resolve(*params['packages'])
        status = pm.install(packages)

        return AgentRequestHandler._format_response(
            None,
            True,
            1
        )

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

    def do_uninstall(params):

        pm = get_package_manager()
        pdb = get_package_db()

        packages = pdb.resolve(*params['packages'])
        status = pm.uninstall(packages)

        return AgentRequestHandler._format_response(
            None,
            True,
            1
        )

    def do_update(params):

        pm = get_package_manager()
        pm.refresh()

        if 'upgrade' in params and params['upgrade']:
            upgrade = True
        else:
            upgrade = False
        success = pm.update(upgrade)

        return AgentRequestHandler._format_response(
            '',
            success,
            int(success)
        )


class ClientQueryInterface(ClientQueryInterfaceBase):
    pass
