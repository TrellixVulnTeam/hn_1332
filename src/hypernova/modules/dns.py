#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# DNS server configuration management package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig.dnsserver import DuplicateZoneError, \
                                                    NonexistentZoneError, \
                                                    ServerCommunicationError, \
                                                    Record, \
                                                    SoaRecord, \
                                                    Zone, \
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

    def do_add_record(params):
        """
        Add a record to an existing zone.
        """

        config = ConfigurationFactory.get('hypernova')

        server = get_authoritative_server(config['dns']['adapter'],
                                          config['dns'])

        try:
            zone = server.get_zone(params['zone'])
            record = Record(params['record']['name'],
                            params['record']['type'],
                            params['record']['content'],
                            params['record']['ttl'],
                            params['record']['priority'])
            server.add_record(zone, record)

            successful = True
            result = {'record': record.to_encodable()}
        except NonexistentZoneError:
            successful = False
            result = {'error': 'NonexistentZone'}

        return AgentRequestHandler._format_response(
            result,
            successful=successful
        )
        )

    def do_add_zone(params):
        """
        Add a zone.
        """

        config = ConfigurationFactory.get('hypernova')

        try:
            result = {'error': 'ValidationError'}

            server = get_authoritative_server(config['dns']['adapter'],
                                              config['dns'])
            zone = Zone(new_domain=params['zone']['domain'],
                        new_origin=params['zone']['origin'],
                        new_ttl=params['zone']['ttl'])
            zone.soa_record = SoaRecord(new_primary_ns=params['soa']['primary_ns'],
                                        new_responsible_person=params['soa']['responsible_person'],
                                        new_serial=params['soa']['serial'],
                                        new_refresh=params['soa']['refresh'],
                                        new_retry=params['soa']['retry'],
                                        new_expire=params['soa']['expire'],
                                        new_min_ttl=params['soa']['min_ttl'])

            try:
                server.add_zone(zone)
                successful = True
                result = {'zone': zone.to_encodable()}
            except DuplicateZoneError:
                successful = False
                result = {'error': 'DuplicateZone'}

        except ServerCommunicationError:
            successful = False
            result = {'error': 'ServerCommunicationError'}

        return AgentRequestHandler._format_response(
            result,
            successful=successful,
            error_code=0
        )

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

    # ints must be explicitly casted from str
    ZONE_ATTR_INT = ['origin', 'ttl']
    ZONE_ATTR_STR = ['domain']
    SOA_ATTR_INT  = ['serial', 'refresh', 'retry', 'expire', 'min_ttl']
    SOA_ATTR_STR  = ['primary_ns', 'responsible_person']
    RECORD_ATTR   = ['zone', 'name', 'type', 'content', 'ttl', 'priority']

    def init_subparser(subparser, subparser_factory):
        sp = subparser_factory.add_parser('add_record')
        for a in ClientRequestBuilder.RECORD_ATTR:
            sp.add_argument(a)

        sp = subparser_factory.add_parser('add_zone')
        for a in (ClientRequestBuilder.ZONE_ATTR_STR +
                  ClientRequestBuilder.ZONE_ATTR_INT):
            sp.add_argument(a)
        for a in (ClientRequestBuilder.SOA_ATTR_STR +
                  ClientRequestBuilder.SOA_ATTR_INT):
            sp.add_argument("soa_%s" %(a))

        sp = subparser_factory.add_parser('get_zone')
        sp.add_argument('domain')

        subparser_factory.add_parser('install')

        return subparser

    def do_add_record(cli_args, client):
        """
        Add a record to an existing zone.
        """

        args = {
            'zone': cli_args.zone,
            'record': {
                'name':     cli_args.name,
                'type':     cli_args.type,
                'content':  cli_args.content,
                'ttl':      int(cli_args.ttl),
                'priority': int(cli_args.priority),
            },
        }

        if args['record']['priority'] == -1:
            args['record']['priority'] = None

        return ClientRequestBuilderBase._format_request(
            ['dns', 'add_record'], args
        )

    def do_add_zone(cli_args, client):
        """
        Add a zone.
        """

        args = {'zone': {}, 'soa': {}}

        for a in ClientRequestBuilder.ZONE_ATTR_INT:
            args['zone'][a] = int(getattr(cli_args, a))
        for a in ClientRequestBuilder.ZONE_ATTR_STR:
            args['zone'][a] = getattr(cli_args, a)

        for a in ClientRequestBuilder.SOA_ATTR_INT:
            args['soa'][a] = int(getattr(cli_args, "soa_%s" %(a)))
        for a in ClientRequestBuilder.SOA_ATTR_STR:
            args['soa'][a] = getattr(cli_args, "soa_%s" %(a))

        for a in ['origin', 'ttl']:
            if args['zone'][a] == -1:
                args['zone'][a] = None

        return ClientRequestBuilderBase._format_request(
            ['dns', 'add_zone'], args
        )

    def do_get_zone(cli_args, client):
        """
        Retrieve a zone.
        """

        return ClientRequestBuilderBase._format_request(
            ['dns', 'get_zone'], {
                'domain': cli_args.domain
            }
        )

    def do_install(cli_args, client):
        """
        Install a DNS server.
        """

        return ClientRequestBuilderBase._format_request(
            ['dns', 'install']
        )


class ClientResponseFormatter(ClientResponseFormatterBase):
    """
    DNS management response formatter component.
    """

    errors = {
        'DuplicateZone': 'a zone with the specified domain already exists',
        'NonexistentZone': 'the specified zone does not exist',
        'ServerCommunication': 'could not communicate with the DNS server',
        'UnknownError': 'an unknown error occurred within the agent',
        'ValidationError': 'a zone or record failed validation checks and couldn\'t be committed',
    }

    DIRECTIVES_FMT = "Directives:\n* Domain: %s\n* TTL: %s\n* Origin: %s"
    SOA_RECORD_FMT = "SOA record:\n* Primary nameserver: %s\n" \
                     "* Responsible person: %s\n* Serial: %s\n* Refresh: %s\n" \
                     "* Retry: %s\n* Expire: %s\n* Minimum TTL: %s"
    RECORD_FMT     = "%s IN %s %s (MX priority %s; TTL %s)"

    def _format_directives(domain, ttl, origin):
        """
        Prepare directives for printing.
        """

        directives = ClientResponseFormatter.DIRECTIVES_FMT
        return directives %(domain, ttl, origin)

    def _format_soa_record(soa_record):
        """
        Prepare SOA record for printing.
        """

        result = ClientResponseFormatter.SOA_RECORD_FMT
        return result %(soa_record['primary_ns'],
                        soa_record['responsible_person'],
                        soa_record['serial'],
                        soa_record['refresh'],
                        soa_record['retry'],
                        soa_record['expire'],
                        soa_record['min_ttl'])

    def _format_record(record):
        """
        Format a single record for printing.
        """

        result = ClientResponseFormatter.RECORD_FMT
        return result %(record['name'],
                        Record.RECORD_TYPES[record['rtype']].upper(),
                        record['content'],
                        record['priority'],
                        record['ttl'])

    def _format_records(records):
        """
        Format a set of records.
        """

        result = 'Records:'
        for r in records:
            result += "\n* %s" %(ClientResponseFormatter._format_record(r))

        return result

    def _format_zone(zone):
        """
        Format an entire zone for outputting.
        """

        return "\n\n".join([
            ClientResponseFormatter._format_directives(zone['domain'],
                                                       zone['ttl'],
                                                       zone['origin']),
            ClientResponseFormatter._format_soa_record(zone['soa_record']),
            ClientResponseFormatter._format_records(zone['records']),
        ])

    def do_add_record(cli_args, response):
        """
        Add a record to an existing zone.
        """

        result = "Failed: an error occurred processing the request"

        if response['status']['successful']:
            result = ''

        return result

    def do_add_zone(cli_args, response):
        """
        Add a zone.
        """

        result = "Failed: %s"

        if response['status']['successful']:
            zone = response['response']['zone']
            result = ClientResponseFormatter._format_zone(zone)
        else:
            try:
                seeking = response['response']['error']
            except KeyError:
                seeking = 'UnknownError'

            return (69, result %(ClientResponseFormatter.errors[seeking]))

        return result

    def do_get_zone(cli_args, response):
        """
        Retrieve a zone.
        """

        result = "Failed: %s"

        if response['status']['successful']:
            zone = response['response']['zone']
            return ClientResponseFormatter._format_zone(zone)
        else:
            try:
                seeking = response['response']['error']
            except KeyError:
                seeking = 'UnknownError'

            return (69, result %(ClientResponseFormatter.errors[seeking]))

    def do_install(cli_args, response):
        """
        Install a DNS server (just PowerDNS...for now).
        """

        result = 'Failed: package installation unsuccessful'

        if response['status']['successful']:
            result = ''

        return result
