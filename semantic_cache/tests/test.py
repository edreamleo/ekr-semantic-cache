#@+leo-ver=5-thin
#@+node:ekr.20250512061658.1: * @file tests/test.py
"""Unit tests the ekr-semantic-cache project"""
import ast
import os
import time
from typing import Union
from unittest import TestCase
from leo.core import leoGlobals as g
assert g

#@+others
#@+node:ekr.20250512073231.1: ** class CacheTests
class CacheTests(TestCase):
    #@+others
    #@+node:ekr.20250512062255.1: *3* CT.test_import
    def test_import(self) -> None:
        assert TestCase is not None
    #@+node:ekr.20250514060210.1: *3* CT.test_times
    def test_times(self) -> None:
        # Report various times.
        from src.controller import core_path, core_names
        from src.controller import parse_ast
        from src.controller import CacheController
        x = CacheController()

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
    #@+node:ekr.20250515090937.1: *3* CT.test_diff (To do)
    def test_diffs(self) -> None:
        pass  ###
    #@-others
#@-others
#@-leo
