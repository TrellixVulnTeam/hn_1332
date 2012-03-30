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

    SELECT_ZONE = "SELECT d.id, d.name " \
                  "FROM domains d " \
                  "WHERE d.name = ? " \
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
          * The comment field PowerDNS adds to records is _not_ supported by
            this libary. Inserted rows won't contain this field, and there's a
            chance that modifications will alter it.
        """

        db = oursql.connect(**self.credentials)

        try:
            cursor = db.cursor(oursql.DictCursor)
            cursor.execute(self.SELECT_ZONE, [main_domain,])
            zone_meta = cursor.fetchone()
            cursor.close()

            cursor = db.cursor()
            try:
                cursor.execute(self.SELECT_ZONE_RECORDS, [zone_meta['id'],])
            except TypeError:
                raise dns.NonexistentZoneError()

            records = []
            for r in cursor:
                if r[1].lower() == 'soa':
                    soa_record = dns.SoaRecord(*r[2].split())
                else:
                    records.append(dns.Record(*r))
            cursor.close()

        finally:
            db.close()

        return dns.Zone(zone_meta['name'],
                        new_soa_record=soa_record, new_records=records)
