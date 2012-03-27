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
from sqlalchemy import create_engine, exc, \
                       Column, MetaData, Integer, String, Table
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_

class AuthoritativeServer(dns.AuthoritativeServerBase):

    ADDR_FMT = '%s+%s://%s:%s@%s/%s'

    engine = None
    conn   = None
    meta   = None
    tables = {}

    def __init__(self, host, username, password, db, dialect='mysql',
                 engine='oursql'):
        """
        Initialise the connection.
        """

        addr = self.ADDR_FMT %(dialect, engine, username, password, host, db)
        self._init_db_conn(addr)
        self._init_db_ddl()

    def _init_db_conn(self, addr):
        """
        Prepare the database connection.
        """

        self.engine = create_engine(addr)

        try:
            self.conn   = self.engine.connect()
        except exc.DBAPIError:
            raise dns.ServerCommunicationError('failed to connect')

    def _init_db_ddl(self):
        """
        Initialise table metadata (data definition).

        We declare the tables we're interested in, as per
            http://docs.sqlalchemy.org/en/latest/core/schema.html
        """

        self.meta = MetaData()

        self.tables['domains'] = Table('domains', self.meta,
            Column('id',              Integer(11), nullable=False, primary_key=True, autoincrement=True),
            Column('name',            String(255), nullable=False, unique=True                         ),
            Column('master',          String(128), nullable=True                                       ),
            Column('last_check',      Integer(11), nullable=True                                       ),
            Column('type',            String(6),   nullable=False                                      ),
            Column('notified_serial', Integer(11), nullable=True                                       ),
            Column('account',         String(40),  nullable=True                                       )
        )

        self.tables['records'] = Table('records', self.meta,
            Column('id',          Integer(11), nullable=False, primary_key=True, autoincrement=True),
            Column('domain_id',   Integer(11), nullable=True                                       ),
            Column('name',        String(255), nullable=True                                       ),
            Column('type',        String(6),   nullable=True                                       ),
            Column('content',     String(255), nullable=True                                       ),
            Column('ttl',         Integer(11), nullable=True                                       ),
            Column('prio',        Integer(11), nullable=True                                       ),
            Column('change_date', Integer(11), nullable=True                                       ),
        )

        self.tables['zone_templ'] = Table('zone_templ', self.meta,
            Column('id',    Integer(20),  nullable=False, primary_key=True, autoincrement=True),
            Column('name',  String(128),  nullable=False                                      ),
            Column('descr', String(1024), nullable=False                                      ),
            Column('owner', Integer(20),  nullable=False                                      )
        )

        self.tables['zone_templ_records'] = Table('zone_templ_records', self.meta,
            Column('id',            Integer(20), nullable=False, primary_key=True, autoincrement=True),
            Column('zone_templ_id', Integer(20), nullable=False                                      ),
            Column('name',          String(255), nullable=False                                      ),
            Column('type',          String(6),   nullable=False                                      ),
            Column('content',       String(255), nullable=False                                      ),
            Column('ttl',           Integer(20), nullable=False                                      ),
            Column('prio',          Integer(20), nullable=False                                      )
        )

        self.tables['zones'] = Table('zones', self.meta,
            Column('id',            Integer(11),  nullable=False, primary_key=True, autoincrement=True),
            Column('domain_id',     Integer(11),  nullable=False                                      ),
            Column('owner',         Integer(11),  nullable=False                                      ),
            Column('comment',       String(1024), nullable=False                                      ),
            Column('zone_templ_id', Integer(11),  nullable=False                                      )
        )

    def get_zone(self, main_domain):
        """
        See the documentation for ServerBase.get_zone() for details.

        Known quirks:

          * PowerDNS doesn't support directives, as implemented by BIND. As a
            result, the ttl and origin fields of each zone are always set to
            None.

          * These queries should really be rolled into one, but SQLAlchemy is
            pretty scary.
        """

        # Find the zone
        query = select(
            [
                self.tables['zones'].c.id,
                self.tables['domains'].c.name,
            ],
            and_(
                self.tables['domains'].c.name == main_domain,
                self.tables['zones'].c.domain_id == self.tables['domains'].c.id,
            )
        )
        proxy = self.conn.execute(query)
        zone_meta = proxy.fetchone()
        proxy.close()

        zone = dns.Zone(zone_meta['name'])

        # Find the records
        query = select(
            [
                self.tables['records'].c.name,
                self.tables['records'].c.type,
                self.tables['records'].c.content,
                self.tables['records'].c.ttl,
                self.tables['records'].c.prio,
            ],
            and_(
                self.tables['records'].c.domain_id == zone_meta['id']
            )
        )
        proxy = self.conn.execute(query)

        # Add the records to the zone
        for record in proxy:
            if record['type'].lower() == 'soa':
                zone.soa_record = dns.SoaRecord(*record['content'].split())
            else:
                zone.records.append(dns.Record(record['name'], record['type'],
                                               record['content'], record['ttl'],
                                               record['prio']))
        proxy.close()

        return zone
