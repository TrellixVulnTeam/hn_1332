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

    def get_zone(domain):
        """
        Find a zone within the server.

        Should return a Zone object with the records attribute populated with
        all corresponding records.
        """

        raise NotImplementedError


class AuthoritativeServerBase(ServerBase):
    """
    Authoritative DNS server.
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

    def __init__(self, domain=None, ttl=None, origin=None, soa_record=None,
                 records=[]):
        """
        Initialise values.
        """

        self.domain     = domain
        self.ttl        = ttl
        self.origin     = origin
        self.soa_record = soa_record
        self.records    = records

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
            'soa_record': self.soa_record.__dict__,
            'records':    [r.to_encodable() for r in self.records],
        }


class Record:
    """
    DNS record.
    """

    # Resource record types
    RECORD_TYPES = (
        'a',
        'aaaa',
        'cname',
        'mx',
        'soa',
        'txt',
    )

    # All records
    name    = ''
    rtype   = 0
    content = ''
    ttl     = 0

    # MX records only
    priority = None

    def __init__(self, name='', rtype=None, content=None, ttl=0, priority=None):
        """
        Initialise values.
        """

        if isinstance(rtype, str):
            rtype = Record.RECORD_TYPES.index(rtype.lower())

        self.name     = name
        self.rtype    = rtype
        self.content  = content
        self.ttl      = 0
        self.priority = priority

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

    def __init__(self, primary_ns='', responsible_person='', serial=0,
                 refresh=0, retry=0, expire=0, min_ttl=0):
        """
        Initialise values.
        """

        self.primary_ns         = primary_ns
        self.responsible_person = responsible_person

        self.serial  = serial
        self.refresh = refresh
        self.retry   = retry
        self.expire  = expire
        self.min_ttl = min_ttl

    def to_encodable(self):
        """
        See Zone.to_encodable() for details.
        """

        return {
            'primary_ns':         self.primary_ns,
            'responsible_person': self.responsible_name,
            'serial':             self.serial,
            'refresh':            self.refresh,
            'retry':              self.retry,
            'expire':             self.expire,
            'min_ttl':            self.min_ttl,
        }


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
