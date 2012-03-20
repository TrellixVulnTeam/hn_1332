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
import subprocess

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

        regex = re.compile('(1|5|15)m: ([0-9]).([0-9])*')
        avgs = result[1].split("\n")
        avgs.remove('')
        for avg in avgs:
            regex.match(avg)

