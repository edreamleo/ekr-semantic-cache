#@+leo-ver=5-thin
#@+node:ekr.20250512061658.1: * @file tests/test.py
"""Unit tests the ekr-semantic-cache project"""
from unittest import TestCase
from leo.core import leoGlobals as g
assert g

class TestCache(TestCase):
    #@+others
    #@+node:ekr.20250512062255.1: ** TC.test_import
    def test_dummy(self):
        from test import TestCache
        assert TestCache
    #@-others
#@-leo
