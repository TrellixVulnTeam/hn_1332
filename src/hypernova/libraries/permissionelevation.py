#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Permission elevation library
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from hypernova.libraries.configuration import ConfigurationFactory

def elevate_cmd(cmd):
    """
    Return an elevated command, ready for execution.

    When cmd is a list, we prepend the options necessary for the command to run
    as the system's root/administrative user as seperate, self-contained
    arguments. When it's a string, we prepend to the string the space-delimited
    parameters.

    If the object is of any other type, a TypeError will be thrown.
    """

    config = ConfigurationFactory.get('hypernova')['elevation']

    if config['method'] == 'elevator':
        prefix = [config['binary']]

    if isinstance(cmd, list):
        prefix.extend(cmd)
        cmd = prefix
    elif isinstance(cmd, str):
        cmd = '%s %s' %(' '.join(prefix), cmd)
    else:
        raise TypeError('list or str expected')

    return cmd
