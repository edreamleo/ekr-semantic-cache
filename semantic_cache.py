#@+leo-ver=5-thin
#@+node:ekr.20250426050140.1: * @file semantic_cache.py
"""The main program for the semantic cacher"""

#@+<< semantic_cache: imports >>
#@+node:ekr.20250426051119.1: ** << semantic_cache: imports >>
# pylint: disable=reimported,unused-import,wrong-import-position

import ast
import os
import sys
from typing import Generator

leo_path = r'C:\Repos\leo-editor'
if leo_path not in sys.path:
    sys.path.insert(0, leo_path)

from leo.core import leoGlobals as g

# from leo.core import (
    # leoAPI, leoApp, leoAtFile,  # leoAst,
    # leoBackground,  # leoBridge, # leoBeautify,
    # leoCache, leoChapters, leoColor, leoColorizer,
    # leoCommands, leoConfig,  # leoCompare, leoDebugger,
    # leoExternalFiles,
    # leoFileCommands, leoFind, leoFrame,
    # leoGlobals, leoGui,
    # leoHistory, leoImport,  # leoJupytext,
    # leoKeys, leoMarkup, leoMenu,
    # leoNodes,
    # leoPlugins,  # leoPersistence, leoPrinting, leoPymacs,
    # leoQt,
    # leoRst,  # leoRope,
    # leoSessions, leoShadow,
    # # leoTest2, leoTips, leoTokens,
    # leoUndo, leoVersion,  # leoVim
# )
#@-<< semantic_cache: imports >>
#@+<< semantic_cache: annotations >>
#@+node:ekr.20250426055357.1: ** << semantic_cache: annotations >>
Node = ast.AST
#@-<< semantic_cache: annotations >>
#@+<< semantic_cache: data >>
#@+node:ekr.20250426054838.1: ** << semantic_cache: data >>
core_path = r'c:\Repos\leo-editor\leo\core'

core_names = (
    # leoAPI, leoAtFile,  # leoAst,
    'leoApp',
    # leoBackground,  # leoBridge, # leoBeautify,
    # leoCache, leoChapters, leoColor, leoColorizer,
    # leoCommands, leoConfig,  # leoCompare, leoDebugger,
    # leoExternalFiles,
    # leoFileCommands, leoFind, leoFrame,
    # leoGlobals, leoGui,
    # leoHistory, leoImport,  # leoJupytext,
    # leoKeys, leoMarkup, leoMenu,
    # leoNodes,
    # leoPlugins,  # leoPersistence, leoPrinting, leoPymacs,
    # leoQt,
    # leoRst,  # leoRope,
    # leoSessions, leoShadow,
    # # leoTest2, leoTips, leoTokens,
    # leoUndo, leoVersion,  # leoVim
)
#@-<< semantic_cache: data >>

#@+others
#@+node:ekr.20250426055254.1: ** --- top-level functions
#@+node:ekr.20250426055745.1: *3* function: dump_ast & helper
annotate_fields = False
include_attributes = False
indent_ws = ' '

def dump_ast(node: Node, level: int = 0) -> str:
    """
    Dump an ast tree. Adapted from ast.dump.
    """
    sep1 = '\n%s' % (indent_ws * (level + 1))
    if isinstance(node, ast.AST):
        fields = [(a, dump_ast(b, level + 1)) for a, b in get_fields(node)]
        if include_attributes and node._attributes:
            fields.extend([(a, dump_ast(getattr(node, a), level + 1))
                for a in node._attributes])
        if annotate_fields:
            aList = ['%s=%s' % (a, b) for a, b in fields]
        else:
            aList = [b for a, b in fields]
        name = node.__class__.__name__
        sep = '' if len(aList) <= 1 else sep1
        return '%s(%s%s)' % (name, sep, sep1.join(aList))
    if isinstance(node, list):
        sep = sep1
        return 'LIST[%s]' % ''.join(
            ['%s%s' % (sep, dump_ast(z, level + 1)) for z in node])
    return repr(node)
#@+node:ekr.20250426055745.2: *4* dumper.get_fields
def get_fields(node: Node) -> Generator:
    return (
        (a, b) for a, b in ast.iter_fields(node)
            if a not in ['ctx',] and b not in (None, [])
    )
#@+node:ekr.20250426052508.1: *3* function: main
def main():
    for z in core_names:
        path = f"{core_path}{os.sep}{z}.py"
        assert os.path.exists(path), repr(path)
        contents = g.readFile(path)
        tree = parse_ast(contents)
        lines = g.splitlines(dump_ast(tree))
        print(f"{z}.py...")
        for i, line in enumerate(lines[:30]):
            print(f"{i:2} {line.rstrip()}")
#@+node:ekr.20250426054003.1: *3* function: parse_ast
def parse_ast(contents: str) -> ast.AST:
    """
    Parse string s, catching & reporting all exceptions.
    Return the ast node, or None.
    """

    def oops(message: str) -> None:
        print('')
        print(f"parse_ast: {message}")
        g.printObj(contents)
        print('')

    try:
        s1 = g.toEncodedString(contents)
        tree = ast.parse(s1, filename='before', mode='exec')
        return tree
    except IndentationError:
        oops('Indentation Error')
    except SyntaxError:
        oops('Syntax Error')
    except Exception:
        oops('Unexpected Exception')
        g.es_exception()
    return None
#@+node:ekr.20250426053702.1: ** class class_cache
class class_cache:
    """A class containing all cached data from one Python class."""
#@+node:ekr.20250426053807.1: ** class module_cache
class module_cache:
    """A class containing all cached data from one Python module."""
#@-others

if __name__ == "__main__":
    main()

#@@language python
#@@tabwidth -4
#@-leo
