#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# System environment library
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import os
import platform

def get_os():
    """
    Attempt to guess the OS type and release.

    This hacky function attempts to guess the OS type based on the presence of a
    few specific files.

    Returns None of the OS name/version metadata cannot be found, else returns
    a tuple containing the (name, version, release_title).
    """

    return platform.dist()

def get_package_manager(releaseinfo):
    """
    Attempt to guess the package manager.
    """

    if releaseinfo[0].lower() in ('centos', 'fedora'):
        return ('rpm', 'yum')

    return None

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

class UtilityNotFoundError(Exception):

    utility = None
    paths   = None

    def __init__(self, utility, paths):
        self.utility = utility
        self.paths   = ', '.join(paths)

        self.value = 'Unable to find "%s" in %s' %(utility, paths)

    def __str__(self):
        return repr(self.value)
