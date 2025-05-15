#@+leo-ver=5-thin
#@+node:ekr.20250512061658.1: * @file tests/test.py
"""Unit tests the ekr-semantic-cache project"""
import ast
import os
import time
from typing import Union
from unittest import TestCase
from leo.core import leoGlobals as g
from src.controller import CacheController, parse_ast
assert g

#@+others
#@+node:ekr.20250512073231.1: ** class CacheTests
class CacheTests(TestCase):

    def setUp(self) -> None:
        super().setUp()
        g.unitTesting = True
        self.cc = CacheController()
        self.cc.init()

    def tearDown(self) -> None:
        super().tearDown()
        g.unitTesting = False
        self.cc = None

    #@+others
    #@+node:ekr.20250514060210.1: *3* CT.test_times
    def test_times(self) -> None:

        self.skipTest('Passed')
        x = self.cc

        # Report various times.
        from src.controller import core_path, core_names

        # Precheck.
        paths = [f"{core_path}{os.sep}{z}.py" for z in core_names]
        for path in paths:
            assert os.path.exists(path), repr(path)

        # Time to get all modification times.
        t1 = time.perf_counter()
        mod_time_dict: dict[str, Union[float, None]] = {}
        for path in paths:
            mod_time_dict[path] = os.path.getmtime(path)

        # Time to parse all files.
        t2 = time.perf_counter()
        contents_dict: dict[str, str] = {}
        for path in paths:
            contents_dict[path] = g.readFile(path)

        # Time to parse all files.
        t3 = time.perf_counter()
        tree_dict: dict[str, Union[ast.AST, None]] = {}
        for path in paths:
            tree_dict[path] = parse_ast(contents_dict[path])

        # Totals.
        t4 = time.perf_counter()
        x.stats.append(('Read all mod times', t2 - t1))
        x.stats.append(('Read all files', t3 - t2))
        x.stats.append(('Parse all files', t4 - t3))
        # x.stats.append(('Test', 2.61))
        x.print_stats(paths)
    #@+node:ekr.20250515090937.1: *3* CT.test_semantics
    def test_semantics(self) -> None:

        x = self.cc
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, 'dummy_test_program.py')
        assert os.path.exists(path)

        # Set old_tree_dict from the *old* contents.
        old_contents = g.readFile(path)
        x.old_tree_dict[path] = parse_ast(old_contents)

        # Set new_tree_dict from the *new) contents.
        new_contents = old_contents.replace('# [update] ', '')
        x.new_tree_dict[path] = parse_ast(new_contents)

        # Run do_semantics.
        x.do_semantics([path])
    #@-others
#@-others
#@-leo
