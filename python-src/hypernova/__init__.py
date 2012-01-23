#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Package (egg) definition
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import gnupg

__author__        = 'The Development Manager Ltd'
__author_email__  = 'luke.carrier@tdm.info'
__description__   = 'HyperNova server agent'
__friendly_name__ = 'HyperNova'
__url__           = 'http://hypernova.cloudnova.net/'
__version__       = '0.1.0'


class GPG(gnupg.GPG):
    """
    gnupg.GPG instance factory.
    """

    instances = {}

    def get_gpg(gpgbinary='gpg', gnupghome=None, verbose=False,
                 use_agent=False, keyring=None, instancename=None):

        if not instancename:
            instancename = str(locals())

        if instancename not in GPG.instances:
            GPG.instances[instancename] = GPG(gpgbinary, gnupghome, verbose,
                                              use_agent, keyring)

        return GPG.instances[instancename]
