#@+leo-ver=5-thin
#@+node:ekr.20250512061658.1: * @file tests/test.py
"""Unit tests the ekr-semantic-cache project"""
import os
import time
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
    #@+node:ekr.20250514060210.1: *3* CacheTests.test_times
    def test_times(self):
        # Report various times.
        from src.controller import core_path, core_names
        from src.controller import parse_ast
        assert core_path and core_names and parse_ast
        return  ### Changed.
        t1 = time.process_time()
        updated_paths: list[str] = []
        n_files = 0
        for z in core_names:
            n_files += 1
            path = f"{core_path}{os.sep}{z}.py"
            assert os.path.exists(path), repr(path)
            mod_time = os.path.getmtime(path)
            old_mod_time = self.mod_time_dict.get(path, None)
            if old_mod_time is None or mod_time > old_mod_time or 'leoCache.py' in path:
                kind = 'Create' if old_mod_time is None else 'Update'
                updated_paths.append(path)
                path_s = f"{z}.py"
                print(f"{kind} {path_s} {time.ctime(mod_time)}")
                contents = g.readFile(path)
                tree = parse_ast(contents)
                self.module_dict[path] = tree
                self.mod_time_dict[path] = mod_time
            # if 0:
                # lines = g.splitlines(dump_ast(tree))
                # for i, line in enumerate(lines[:30]):
                    # print(f"{i:2} {line.rstrip()}")
        t2 = time.process_time()
        self.stats.append(('Find changed', t2 - t1))
        return updated_paths
    #@-others
#@-others
#@-leo
