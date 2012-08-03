#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Factory wrapper for the python_gnupg module
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import gnupg

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

