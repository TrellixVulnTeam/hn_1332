#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# DNS server configuration management package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig.dnsserver import NonexistentZoneError, \
                                                    ServerCommunicationError, \
                                                    Record, \
                                                    get_authoritative_server
from hypernova.libraries.configuration import ConfigurationFactory
from hypernova.libraries.packagemanagement import get_package_db, \
                                                  get_package_manager
from hypernova.modules import AgentRequestHandlerBase, \
                              ClientRequestBuilderBase, \
                              ClientResponseFormatterBase

class AgentRequestHandler(AgentRequestHandlerBase):
    """
    DNS management component for the agent.
    """

    def do_add_zone(params):
        """
        Add a zone.
        """

    def do_get_zone(params):
        """
        Get a zone.
        """

        config = ConfigurationFactory.get('hypernova')

        try:
            server = get_authoritative_server(config['dns']['adapter'],
                                              config['dns'])

            try:
                successful = True
                result     = {
                    'zone': server.get_zone(params['domain']).to_encodable(),
                }
            except NonexistentZoneError:
                successful = False
                result     = {'error': 'NonexistentZone'}
        except ServerCommunicationError:
            successful = False
            result     = {'error': 'ServerCommunication'}

        return AgentRequestHandler._format_response(
            result,
            successful=successful,
            error_code=0
        )

    def do_install(params):
        """
        Install a DNS server.
        """

        pm  = get_package_manager()
        pdb = get_package_db()

        status = pm.install(pdb.resolve('powerdns-authoritative'))

        return AgentRequestHandler._format_response(
            successful=status,
            error_code=0
        )


class ClientRequestBuilder(ClientRequestBuilderBase):
    """
    DNS management request generation component.
    """

    def init_subparser(subparser, subparser_factory):
        sp = subparser_factory.add_parser('add_zone')
        sp.add_argument('domain')
        sp = subparser_factory.add_parser('get_zone')
        sp.add_argument('domain')

        subparser_factory.add_parser('install')
        return subparser

    def do_add_zone(cli_args, client):
        return ClientRequestBuilderBase._format_request(
            ['dns', 'add_zone'],
            {

            }
        )

    def do_get_zone(cli_args, client):
        return ClientRequestBuilderBase._format_request(
            ['dns', 'get_zone'],
            {
                'domain': cli_args.domain
            }
        )

    def do_install(cli_args, client):
        return ClientRequestBuilderBase._format_request(
            ['dns', 'install']
        )


class ClientResponseFormatter(ClientResponseFormatterBase):
    """
    DNS management response formatter component.
    """

    errors = {
        'NonexistentZone': 'the specified zone does not exist',
        'ServerCommunication': 'could not communicate with the DNS server',
        'UnknownError': 'an unknown error occurred within the agent',
    }

    directives_fmt = "Directives:\n* Domain: %s\n* TTL: %s\n* Origin: %s"
    soa_record_fmt = "SOA record:\n* Primary nameserver: %s\n" \
                     "* Responsible person: %s\n* Serial: %s\n* Refresh: %s\n" \
                     "* Retry: %s\n* Expire: %s\n* Minimum TTL: %s"
    record_fmt     = "%s IN %s %s (MX priority %s; TTL %s)"

    def do_get_zone(cli_args, response):
        result = 'Failed: %s'

        if response['status']['successful']:
            zone = response['response']['zone']

            directives = ClientResponseFormatter.directives_fmt
            directives = directives %(zone['domain'],
                                      zone['ttl'],
                                      zone['origin'])

            soa_record = ClientResponseFormatter.soa_record_fmt
            soa_record = soa_record %(zone['soa_record']['primary_ns'],
                                      zone['soa_record']['responsible_person'],
                                      zone['soa_record']['serial'],
                                      zone['soa_record']['refresh'],
                                      zone['soa_record']['retry'],
                                      zone['soa_record']['expire'],
                                      zone['soa_record']['min_ttl'])

            records = 'Records:'
            record_content = ClientResponseFormatter.record_fmt
            for record in zone['records']:
                records += "\n* "
                records += record_content %(record['name'],
                                            Record.RECORD_TYPES[record['rtype']].upper(),
                                            record['content'],
                                            record['priority'],
                                            record['ttl'])

            return "%s\n\n%s\n\n%s" %(directives, soa_record, records)
        else:
            try:
                seeking = response['response']['error']
            except KeyError:
                seeking = 'UnknownError'

            return (69, result %(ClientResponseFormatter.errors[seeking]))

    def do_install(cli_args, response):
        result = 'Failed: package installation unsuccessful'

        if response['status']['successful']:
            result = ''

        return result
