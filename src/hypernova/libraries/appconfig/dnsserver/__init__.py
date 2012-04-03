#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# DNS server configuration management package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

class ServerBase:
    """
    DNS server base class.
    """

    def get_zone(self, domain):
        """
        Find a zone within the server.

        Should return a Zone object with the records attribute populated with
        all corresponding records.
        """

        self._not_implemented()

    def _not_implemented(self):
        """
        Feature not implemented.
        """

        raise NotImplementedError


class AuthoritativeServerBase(ServerBase):
    """
    Authoritative DNS server.
    """

    def add_record(self, zone, record):
        """
        Add a record.

        Note: SOA records must be updated with the dedicated commit_soa_record()
        method, which ensures valid structure and data. Attempting to commit an
        SOA record with this method will raise an exception.
        """

        self._not_implemented()

    def add_soa_record(self, zone, soa_record):
        """
        Add an SOA record.
        """

        self._not_implemented()

    def add_zone(self, zone):
        """
        Add a zone.

        Beware that modifications take effect only upon the zone; any changed
        records will _not_ be implicitly updated. For this, you should use the
        commit_record() commit_soa_record() methods.
        """

        self._not_implemented()

    def rm_record(self, zone, record):
        """
        Remove a record.
        """

        self._not_implemented()

    def rm_soa_record(self, zone, record):
        """
        Remove an SOA record.
        """

    def rm_zone(self, zone):
        """
        Remove a zone.
        """

class Zone:
    """
    DNS zone.
    """

    # Domain name
    domain = None

    # Directives
    ttl    = None
    origin = None

    # SOA
    soa_record = None

    # Resource records
    records = []

    def __init__(self, new_domain=None, new_ttl=None, new_origin=None,
                 new_soa_record=None, new_records=[]):
        """
        Initialise values.
        """

        self.domain     = new_domain
        self.ttl        = new_ttl
        self.origin     = new_origin
        self.soa_record = new_soa_record
        self.records    = new_records

    def filter_records_for(self, filters):
        """
        Filter associated records for matches.
        """

        def matches(record):
            for key, value in filters.items():
                if getattr(record, key) != value:
                    return False

            return True

        matches.filters = filters

        return list(r for r in self.records if matches(r))

    def to_encodable(self):
        """
        Return a simplified representation for encoding in abstract formats.

        This is here to help the json, marshal and pickle libraries interpret
        our structures, since they're presently only able to read simple
        structures.
        """

        return {
            'domain':     self.domain,
            'ttl':        self.ttl,
            'origin':     self.origin,
            'soa_record': self.soa_record.to_encodable(),
            'records':    [r.to_encodable() for r in self.records],
        }


class Record:
    """
    DNS record.
    """

    # Resource record types
    RECORD_TYPES = [
        'a',
        'aaaa',
        'cname',
        'mx',
        'soa',
        'txt',
    ]

    # All records
    name    = ''
    rtype   = 0
    content = ''
    ttl     = 0

    # MX records only
    priority = None

    def __init__(self, new_name='', new_rtype=None, new_content=None, new_ttl=0,
                 new_priority=None):
        """
        Initialise values.
        """

        if isinstance(new_rtype, str):
            rtype = Record.RECORD_TYPES.index(new_rtype.lower())

        self.name     = new_name
        self.rtype    = new_rtype
        self.content  = new_content
        self.ttl      = new_ttl
        self.priority = new_priority

    def to_encodable(self):
        """
        See Zone.to_encodable() for details.
        """

        return {
            'name':     self.name,
            'rtype':    self.rtype,
            'content':  self.content,
            'ttl':      self.ttl,
            'priority': self.priority,
        }


class SoaRecord:
    """
    SOA (start of authority) record.
    """

    # Hostname of primary nameserver.
    #
    # The MNAME field of a record; this must always must be set as the primary
    # nameserver for the zone (the only server upon which the records are
    # modified).
    primary_ns = ''

    # Support contact.
    #
    # The email address of the person or group immediately responsible for the
    # technical administration of the zone.
    responsible_person = ''

    # Parameters
    serial  = 0
    refresh = 0
    retry   = 0
    expire  = 0
    min_ttl = 0

    def __init__(self, new_primary_ns='', new_responsible_person='',
                 new_serial=0, new_refresh=0, new_retry=0, new_expire=0,
                 new_min_ttl=0):
        """
        Initialise values.
        """

        self.primary_ns         = new_primary_ns
        self.responsible_person = new_responsible_person

        self.serial  = new_serial
        self.refresh = new_refresh
        self.retry   = new_retry
        self.expire  = new_expire
        self.min_ttl = new_min_ttl

    def to_encodable(self):
        """
        See Zone.to_encodable() for details.
        """

        return {
            'primary_ns':         self.primary_ns,
            'responsible_person': self.responsible_person,
            'serial':             self.serial,
            'refresh':            self.refresh,
            'retry':              self.retry,
            'expire':             self.expire,
            'min_ttl':            self.min_ttl,
        }


class DuplicateZoneError(Exception):
    """
    Duplicate zone error.

    Thrown whenever an attempt to create a zone fails because a zone with the
    same domain already exists.
    """

    pass


class InvalidZoneError(Exception):
    """
    Invalid zone error.

    Thrown when a zone fails validation checks.
    """

    pass


class NonexistentZoneError(Exception):
    """
    Nonexistent zone error.

    Thrown whenever operations are attempted on zones which do not exist or
    cannot be found.
    """

    pass


class ServerCommunicationError(Exception):
    """
    Broken DNS server error.

    A catch all error to throw when we're unable to communicate with the DNS
    server.
    """

    pass


def get_authoritative_server(adapter, kwargs):
    """
    Get a DNS server by its adapter name, and initialise it with the arguments
    in args.
    """

    kwargs = dict(kwargs)
    kwargs.pop('adapter')

    module_name = "hypernova.libraries.appconfig.dnsserver.%s" %(adapter)
    module = __import__(module_name, fromlist=['AuthoritativeServer'])
    Klass = getattr(module, 'AuthoritativeServer')
    return Klass(**kwargs)
