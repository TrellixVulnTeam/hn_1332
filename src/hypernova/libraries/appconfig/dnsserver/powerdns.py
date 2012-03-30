#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# PowerDNS adapter for DNS management
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig import dnsserver as dns
import oursql

class AuthoritativeServer(dns.AuthoritativeServerBase):

    credentials = {}

    SELECT_ZONE = "SELECT z.id, d.name " \
                  "FROM zones z, domains d " \
                  "WHERE d.name = ? " \
                  "AND z.domain_id = d.id " \
                  "LIMIT 1"

    SELECT_ZONE_RECORDS = "SELECT r.name, r.type, r.content, r.ttl, r.prio " \
                          "FROM records r " \
                          "WHERE r.domain_id = ?"

    def __init__(self, host, username, password, db):
        """
        Initialise the connection.
        """

        self.credentials = {
            'host':   host,
            'user':   username,
            'passwd': password,
            'db':     db
        }

    def get_zone(self, main_domain):
        """
        See the documentation for ServerBase.get_zone() for details.

        Known quirks:

          * PowerDNS doesn't support directives, as implemented by BIND. As a
            result, the ttl and origin fields of each zone are always set to
            None.
        """

        db = oursql.connect(**self.credentials)

        try:
            cursor = db.cursor(oursql.DictCursor)
            cursor.execute(self.SELECT_ZONE, [main_domain,])
            zone_meta = cursor.fetchone()
            cursor.close()

            zone = dns.Zone(zone_meta['name'])

            cursor = db.cursor()
            cursor.execute(self.SELECT_ZONE_RECORDS, [zone_meta['id'],])

            for r in cursor:
                if r[1].lower() == 'soa':
                    zone.soa_record = dns.SoaRecord(*r[2].split())
                else:
                    zone.records.append(dns.Record(*r))
            cursor.close()

        finally:
            db.close()

        return zone
