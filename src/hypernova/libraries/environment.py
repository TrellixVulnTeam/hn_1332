#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# System environment library
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.permissionelevation import elevate_cmd
import os
import subprocess

CTL_START   = 'start'
CTL_STOP    = 'stop'
CTL_RESTART = 'restart'
CTL_RELOAD  = 'reload'

def service_ctl(service, action, require_elevation=True, raise_exc=True):
    """
    Perform a service control action.

    Tolerant of both RHEL and Debian-style configurations.
    """

    try:
        service_util = where_is('service')
    except UtilityNotFoundError:
        try:
            service_util = where_is('invoke-rc.d')
        except UtilityNotFoundError:
            service_util = None

    if service_util:
        cmd = [service_util, service, action]
    else:
        cmd = ['/etc/init.d/%s' %(service), action]

    if require_elevation:
        cmd = elevate_cmd(cmd)

    result = subprocess.check_call(cmd)

    if result == 0:
        return True

    if raise_exc:
        raise ServiceControlError(service, action)


def where_is(binary, raise_exc=True, path=None):
    """
    Find a binary on a specified (or the system's path).

    Seek a binary on the specified set of colon-separated paths. If this string
    isn't set, default to the system's PATH environment variable. If this isn't
    set either, try a sane default of /bin:/usr/bin.

    Returns the path to the binary on success, None if it cannot be found.
    """

    if not path:
        path = os.getenv('PATH', '/bin:/usr/bin')
    paths = path.split(':')

    for path in paths:
        abs_path = os.path.join(path, binary)

        if os.path.isfile(abs_path):
            return abs_path

    if raise_exc:
        raise UtilityNotFoundError(binary, paths)

    return None

class ServiceControlError(Exception):

    service = None
    action  = None

    def __init__(self, service, action):
        self.service = service
        self.action  = action

        self.value = 'Action "%s" on service "%s" failed'


class UtilityNotFoundError(Exception):

    utility = None
    paths   = None

    def __init__(self, utility, paths):
        self.utility = utility
        self.paths   = ', '.join(paths)

        self.value = 'Unable to find "%s" in %s' %(utility, paths)
