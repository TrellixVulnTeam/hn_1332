#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Test harness
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

import os
import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    tests = loader.discover(os.path.dirname(__file__))
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)
