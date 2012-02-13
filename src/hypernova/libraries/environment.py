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
