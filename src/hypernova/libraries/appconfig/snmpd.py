#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# SNMPd configuration management
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.appconfig import AppConfigBase, AppProvisionerBase
from hypernova.libraries import environment
import os
from shutil import rmtree

COMM_RW = 'rw_community'

class AppConfig(AppConfigBase):

    _module_name = 'snmpd'

    __templ_community = '%s %s %s'
    __templ_disk      = 'disk %s %.2f'
    __templ_load      = 'load %.2f %.2f %.2f'
    __templ_sys       = 'syslocation %s\nsyscontact %s'

    # Disks to monitor
    #
    # Multiple disks can be specified in the list. Each list item is itself
    # either a list or a tuple containing two values, the mountpoint of the disk
    # and the number of GBs left on the volume before issuing a warning about
    # disk space:
    #
    # [
    #     ('/mount/point', 10)
    # ]
    disks = []

    # Load average to panic about
    #
    # A list or tuple containing three values; the 1 minute, 5 minute and 15
    # minute system load averages considered harmful or detrimental.
    #
    # (1.0, 0.8, 0.6)
    load = ()

    # The location of the machine; usually a company or domain name
    sys_location = ''

    # An administrative contact who'll be mailed when error conditions are met
    sys_contact = ''

    # Read/write communities
    #
    # Multiple read/write communities can be specified in the following format:
    #
    # [
    #     ('community_name', 'host.name')
    # ]
    rw_communities = []

    def __str__(self):
        opts = []

        opts.append(self.__sys_to_snmpd(self.sys_contact, self.sys_location))
        opts.append(self.__communities_to_snmpd(self.rw_communities))
        opts.append(self.__load_to_snmpd(self.load))
        opts.append(self.__disks_to_snmpd(self.disks))

        return '\n'.join(opts)

    def __communities_to_snmpd(self, communities, comm_type=COMM_RW):
        """
        Convert communities list/dict objects into snmpd.conf directives.
        """

        opts = []
        for c in communities:
            opts.append(self.__templ_community %(comm_type, c[0], c[1]))
        return '\n'.join(opts)

    def __disks_to_snmpd(self, disks):
        """
        Convert disks list into snmpd.conf directives.
        """

        opts = []
        for d in disks:
            opts.append(self.__templ_disk %(d[0], d[1]))
        return '\n'.join(opts)

    def __load_to_snmpd(self, load):
        """
        Convert load sequence into snmpd.conf directive.
        """

        return self.__templ_load %(float(load[0]), float(load[1]),
                                   float(load[2]))

    def __sys_to_snmpd(self, sys_contact, sys_location):
        """
        Convert the system contact/location metadata into snmpd directives.
        """

        return self.__templ_sys %(sys_location, sys_contact)


class AppProvisioner(AppProvisionerBase):

    _module_name = 'snmpd'

    _packages  = ['snmpd']
    _snmpd_conf = '/etc/snmp/snmpd.conf'

    _sys_service  = 'snmpd'

    def _provision(self, snmpd_conf):

        self.install_packages()

        self.service_ctl(environment.CTL_STOP)

        if os.path.isdir('/etc/snmp'):
            rmtree('/etc/snmp')
        os.mkdir('/etc/snmp')

        with open(self._snmpd_conf, 'w+') as c:
            c.write(str(snmpd_conf))

        self.service_ctl(environment.CTL_START)
