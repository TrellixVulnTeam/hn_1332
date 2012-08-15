#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# DB server configuration management package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.packagemanagement import (get_package_db,
                                                   get_package_manager)
from hypernova.modules import (AgentRequestHandlerBase,
                               ClientRequestBuilderBase,
                               ClientResponseFormatterBase)

class AgentRequestHandler(AgentRequestHandlerBase):
    def do_install(params):
        """
        Install a DBMS server.
        """

        (pm, pdb) = (get_package_manager(), get_package_db())
        status = pm.install(pdb.resolve(params["dbms"] + "-server"))

        return AgentRequestHandlerBase._format_response(
            successful=status,
            error_code=0
        )


class ClientRequestBuilder(ClientRequestBuilderBase):
    def init_subparser(subparser, subparser_factory):
        sp = subparser_factory.add_parser("install")
        sp.add_argument("dbms")

        return subparser

    def do_install(cli_args, client):
        """
        Install a DBMS server.
        """

        return ClientRequestBuilderBase._format_request(
            ["db", "install"], {
                "dbms": cli_args.dbms,
            }
        )


class ClientResponseFormatter(ClientResponseFormatterBase):
    def do_install(cli_args, response):
        """
        Install a DBMS server.
        """

        result = "Failed: couldn't install the package"

        if response["status"]["successful"]:
            result = ""

        return result

    def do_secure(cli_args, response):
        """
        Perform post-installation security configuration.
        """

        result = "Failed: security optimisation was unsuccessful"
