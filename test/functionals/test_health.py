#!/usr/bin/env python3.2

#
# HyperNova server management framework
#
# Agent health module unit tests
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

from functionals import ModuleFunctionalTestCase
import re

class TestLoadAverages(ModuleFunctionalTestCase):
    """
    Health module unit test case.
    """

    def test_load_averages(self):
        """
        Test the health.load_averages action.
        """

        result = self.doRequest('health', 'load_averages')
        self.assertZero(result[0])

        avgs = result[1].split("\n")
        for entry in ['', 'Load averages:']:
            avgs.remove(entry)

        regex = re.compile('^\* (1|5|15)m: ([0-9])*.([0-9])*$')

        for avg in avgs:
            self.assertIsNotNone(regex.match(avg))
