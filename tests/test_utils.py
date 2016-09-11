#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_python_mojepanstwo
----------------------------------

Tests for `utils` module.
"""


import sys
import unittest

from python_mojepanstwo.utils import urlencode_php


class TestPython_urlencode_php(unittest.TestCase):

    def _test(self, input, expected_output):
        self.assertEqual(urlencode_php(input), expected_output)

    def test_simple_key_value(self):
        self._test({'x': 'x'}, "x=x")

    def test_simple_key_value_quotable(self):
        self._test({'x': 'x '}, "x=x%20")

    def test_multiple_keys(self):
        self._test({'x': 'x', 'z': 'z'}, "x=x&z=z")

    def test_encoding_dict(self):
        self._test({'x': {'y': 'v'}, 'z': 'z'}, "x[y]=v&z=z")

    def test_encoding_list(self):
        self._test({'x': ['1', '2']}, "x[]=1&x[]=2")


if __name__ == '__main__':
    sys.exit(unittest.main())
