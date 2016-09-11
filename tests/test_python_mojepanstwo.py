#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_python_mojepanstwo
----------------------------------

Tests for `python_mojepanstwo` module.
"""


import sys
import unittest
from . import my_vcr

from python_mojepanstwo import mojepanstwo


class TestPython_mojepanstwo(unittest.TestCase):

    @my_vcr.use_cassette()
    def test_example_list(self):
        conditions = {'twitter_accounts.name': "Michał Boni"}
        response = mojepanstwo().twitter_accounts_list(conditions=conditions)
        self.assertEqual(len(response), 1)
        dataobject = response[0]
        self.assertEqual(dataobject.twitter_accounts__twitter_name, 'MichalBoni')

    @my_vcr.use_cassette()
    def test_example_detail(self):
        response = mojepanstwo().twitter_accounts_detail(pk=133)
        self.assertEqual(response.twitter_accounts__twitter_name, 'MichalBoni')

    @my_vcr.use_cassette()
    def test_refresh_dataset(self):
        client = mojepanstwo()
        client.DATASET_ENUM = []
        client.refresh_dataset()
        self.assertNotEqual(client.DATASET_ENUM, [])
        self.assertTrue('sejm_druki' in client.DATASET_ENUM)


if __name__ == '__main__':
    sys.exit(unittest.main())
