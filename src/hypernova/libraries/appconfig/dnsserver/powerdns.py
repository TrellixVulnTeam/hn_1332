#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# PowerDNS adapter for DNS management
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

"""
A few things:

  * PowerDNS is a bit strange and refers to DNS zones as "domains". Don't confuse
    the PowerAdmin "zones" table with actual zones; it just expresses ownership
    over domains!
  * Unlike most DNS servers, where resource records can use @ to represent the
    domain they belong to, PowerDNS uses the domain itself and doesn't suffix
    the domains with a full stop, as is considered standard.
  * Duplicate records are considered acceptable by this adapter. This is
    more than likely a bad thing that should be rectified in the future.
"""

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

    INSERT_RECORD = "INSERT INTO records (domain_id, name, type, content, ttl, prio) " \
                    "VALUES (?, ?, ?, ?, ?, ?)"

    INSERT_ZONE = "INSERT INTO domains (name, type) " \
                  "VALUES (?, ?)"

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

    def _soa_content(self, soa_record):
        """
        Concatenate the attributes of an SOA record.
        """

        return ' '.join((soa_record.primary_ns,
                         soa_record.responsible_person,
                         str(soa_record.serial),
                         str(soa_record.refresh),
                         str(soa_record.retry),
                         str(soa_record.expire),
                         str(soa_record.min_ttl)))

    def add_record(self, zone, record):
        """
        See the documentation for AuthoritativeServerBase.add_record() for
        details.
        """

        db = oursql.connect(**self.credentials)

        try:
            if not hasattr(zone, 'id'):
                with db as cursor:
                    cursor.execute(self.SELECT_ZONE, (zone.domain,))
                    zone.id = cursor.fetchone()[0]

            with db as cursor:
                cursor.execute(self.INSERT_RECORD, (zone.id,
                                                    record.name,
                                                    record.rtype.upper(),
                                                    record.content,
                                                    record.ttl,
                                                    record.priority))
        finally:
            db.close()

        return cursor.lastrowid

    def add_soa_record(self, zone, soa_record):
        """
        See the documentation for AuthoritativeServerBase.add_soa_record() for
        details.
        """

        db = oursql.connect(**self.credentials)

        try:
            if not hasattr(zone, 'id'):
                with db as cursor:
                    cursor.execute(self.SELECT_ZONE, (zone.domain,))
                    zone.id = cursor.fetchone()[0]

            with db as cursor:
                cursor.execute(self.INSERT_RECORD, (zone.id,
                                                    zone.domain,
                                                    'SOA',
                                                    self._soa_content(soa_record),
                                                    None,
                                                    None))
        finally:
            db.close()

    def add_zone(self, zone):
        """
        See the documentation for AuthoritativeServerBase.add_zone() for
        details.
        """

        db = oursql.connect(**self.credentials)

        try:
            with db as cursor:
                cursor.execute(self.INSERT_ZONE, (zone.domain, 'NATIVE'))
        except oursql.IntegrityError:
            raise dns.DuplicateZoneError()
        finally:
            db.close()

        self.add_soa_record(zone, zone.soa_record)

        zone.id = cursor.lastrowid
        return cursor.lastrowid
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
                # Normalise the record type with a numerical value for easier
                # processing later
                r = list(r)
                r[1] = dns.Record.RECORD_TYPES.index(r[1].lower())

                if r[1] == dns.Record.RECORD_TYPES.index('soa'):
                    soa_record = dns.SoaRecord(*r[2].split())
                else:
                    records.append(dns.Record(*r))
            cursor.close()

        finally:
            db.close()

        return dns.Zone(zone_meta['name'],
                        new_soa_record=soa_record, new_records=records)
