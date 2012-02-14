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
                if log:
                    log.error('directory does not exist')
                return None
        
            for config_file in config_files:
        
                # Skip dotfiles
                if config_file.startswith('.'):
                    continue
        
                if log:
                    log.info('loading configuration file %s' %(config_file))
                
                config_file = os.path.join(root_dir, config_file)
                config.read_file(open(config_file, 'r'))
                
            ConfigurationFactory.configs[name] = config
                
        return ConfigurationFactory.configs[name]