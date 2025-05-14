#@+leo-ver=5-thin
#@+node:ekr.20250512061658.1: * @file tests/test.py
"""Unit tests the ekr-semantic-cache project"""
from unittest import TestCase
from leo.core import leoGlobals as g
assert g

#@+others
#@+node:ekr.20250512073231.1: ** class CacheTests
class CacheTests(TestCase):
    #@+others
    #@+node:ekr.20250512062255.1: *3* CacheTests.test_import
    def test_import(self):
        assert TestCase is not None
    #@-others
#@-others
#@-leo
