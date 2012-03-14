#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent application package
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from configparser import ConfigParser
import os

class ConfigurationFactory():
    """
    Initialise a ConfigParser object from files in a specified directory.
    """

    configs = {}

    def get(name, root_dir=None, log=None):

        if name not in ConfigurationFactory.configs:
            config = ConfigParser()

            try:
                config_files = os.listdir(root_dir)
                config_files.sort()
            except OSError:
                if os.path.isfile(root_dir):
                    config_files = [root_dir]
                else:
                    if log:
                        log.error('directory does not exist')

                    raise LoadError

            for config_file in config_files:

                # Skip dotfiles
                if config_file.startswith('.'):
                    continue

                if log:
                    log.info('loading configuration file %s' %(config_file))

                config_file = os.path.join(root_dir, config_file)
                with open(config_file, 'r') as f:
                    config.read_file(f)

            ConfigurationFactory.configs[name] = config

        return ConfigurationFactory.configs[name]


class LoadError(Exception):
    pass
