#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent application package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from configparser import SafeConfigParser
import os

class ConfigurationFactory():
    """
    Initialise a SafeConfigParser object from files in a specified directory.
    """

    configs = {}

    def get(name, root_dir=None, log=None):

        if name not in ConfigurationFactory.configs:
            config = SafeConfigParser()

            try:
                config_files = os.listdir(root_dir)
                config_files.sort()

                for config_file in config_files:

                    # Skip dotfiles and directories
                    if config_file.startswith('.'):
                        if log:
                            log.warn('skipping hidden item %s' %(config_file))

                        continue

                    if log:
                        log.info('loading configuration file %s' %(config_file))

                    config_file = os.path.join(root_dir, config_file)
                    try:
                        with open(config_file, 'r') as f:
                            config.read_file(f)
                    except IOError:
                        if log:
                            log.warn('failed to load file %s; is it a directory?'
                                     %(config_file))

            except OSError:
                if not os.path.isfile(root_dir):
                    if log:
                        log.error('directory does not exist')

                    raise LoadError

                with open(root_dir, 'r') as f:
                    config.read_file(f)

            ConfigurationFactory.configs[name] = config

        return ConfigurationFactory.configs[name]


class LoadError(Exception):
    pass
