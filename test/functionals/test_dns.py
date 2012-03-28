#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent DNS module unit tests
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from functionals import ModuleFunctionalTestCase
import re

class TestGetZone(ModuleFunctionalTestCase):

    def test_with_no_domain(self):

        result = self.doRequest('dns', 'get_zone')

        self.assertNonZero(result[0])

        regex = re.compile('error: too few arguments')
        self.assertIsNotNone(regex.search(result[2]))

    def test_with_nonexistent_domain(self):

        result = self.doRequest('dns', 'get_zone', {
            'domain': 'nonexistent.domain',
        })

        self.assertNonZero(result[0])
