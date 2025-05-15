#@+leo-ver=5-thin
#@+node:ekr.20250426050140.1: * @file src/controller.py
"""The main program for the semantic cacher"""
#@+<< semantic_cache: imports >>
#@+node:ekr.20250426051119.1: ** << semantic_cache: imports >>
# pylint: disable=reimported,wrong-import-position
import ast
import os
import pickle
import sqlite3
import sys
import time
from typing import Any, Callable, Generator, Optional
import zlib

leo_path = r'C:\Repos\leo-editor'
if leo_path not in sys.path:
    sys.path.insert(0, leo_path)

from leo.core import leoGlobals as g  # type:ignore[import-not-found]
from leo.core.leoCache import SqlitePickleShare  # type:ignore[import-not-found]
#@-<< semantic_cache: imports >>
#@+<< semantic_cache: annotations >>
#@+node:ekr.20250426055357.1: ** << semantic_cache: annotations >>
Node = ast.AST
Value = Any
#@-<< semantic_cache: annotations >>
#@+<< semantic_cache: file names >>
#@+node:ekr.20250426054838.1: ** << semantic_cache: file names >>
core_path = r'c:\Repos\leo-editor\leo\core'

core_names = (
    # leoAPI, leoAtFile,  # leoAst,
    'leoApp',
    'leoBackground',  # 'leoBridge', # 'leoBeautify',
    'leoCache', 'leoChapters', 'leoColor', 'leoColorizer',
    'leoCommands', 'leoConfig',  # 'leoCompare', 'leoDebugger',
    'leoExternalFiles',
    'leoFileCommands', 'leoFind', 'leoFrame',
    'leoGlobals', 'leoGui',
    'leoHistory', 'leoImport',  # 'leoJupytext',
    'leoKeys', 'leoMarkup', 'leoMenu',
    'leoNodes',
    'leoPlugins',  # 'leoPersistence', 'leoPrinting', 'leoPymacs',
    'leoQt',
    'leoRst',  # leoRope,
    'leoSessions', 'leoShadow',
    # leoTest2', leoTips', leoTokens,
    'leoUndo', 'leoVersion',  # 'leoVim'
)

#@-<< semantic_cache: file names >>

#@+others
#@+node:ekr.20250426055254.1: ** --- top-level functions
#@+node:ekr.20250426055745.1: *3* function: dump_ast & helper
annotate_fields = False
include_attributes = False
indent_ws = ' '

def dump_ast(node: Optional[Node], level: int = 0) -> str:
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
#@+node:ekr.20250426054003.1: *3* function: parse_ast
def parse_ast(contents: str) -> Optional[ast.AST]:
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
#@+node:ekr.20250515155334.1: *3* function: ast_context
def ast_context(method: Callable) -> Callable:
    """A a decorator for ast contexts."""

    def wrapper(self: Any, node: Node) -> None:
        self.parent_context = self.context_stack[-1] if self.context_stack else None
        self.context_stack.append(node)
        # g.printObj(self.context_stack, tag=method.__name__)
        method(self, node)
        self.context_stack.pop()
        self.parent_context = self.context_stack[-1] if self.context_stack else None

    return wrapper
#@+node:ekr.20250427052951.1: ** class SemanticCache(SqlitePickleShare)
class SemanticCache(SqlitePickleShare):
    """The persistent cache object"""
    #@+others
    #@+node:ekr.20250427053445.1: *3* SemanticCache.__init__
    def __init__(self, root: str) -> None:  # pylint: disable=super-init-not-called
        """ctor for the SemanticCache object."""
        self.root = root  # For traces.
        dbfile = ':memory:' if g.unitTesting else root
        self.conn = sqlite3.connect(dbfile)
        self.init_dbtables(self.conn)

        def loadz(data: Value) -> Optional[Value]:
            if data:
                # Retain this code for maximum compatibility.
                try:
                    val = pickle.loads(zlib.decompress(data))
                except(ValueError, TypeError):
                    g.es("Unpickling error - Python 3 data accessed from Python 2?")
                    return None
                return val
            return None

        def dumpz(val: Value) -> Value:
            try:
                # Use Python 2's highest protocol, 2, if possible
                data = pickle.dumps(val, protocol=2)
            except Exception:
                # Use best available if that doesn't work (unlikely)
                data = pickle.dumps(val, pickle.HIGHEST_PROTOCOL)
            return sqlite3.Binary(zlib.compress(data))

        self.loader = loadz
        self.dumper = dumpz
        self.reset_protocol_in_values()
    #@-others

    def _makedirs(self, fn: str, mode: int = 0o777) -> None:
        raise NotImplementedError

    def _walkfiles(self, s: str, pattern: Any = None) -> None:
        raise NotImplementedError
#@+node:ekr.20250427190248.1: ** class CacheController
class CacheController:
    """The driver class for the semantic caching project."""

    #@+others
    #@+node:ekr.20250428100117.1: *3* CC.do_semanctics (To do)
    def do_semantics(self, updated_files: list[str]) -> None:
        """
        Do all semantics on updated files:
        - Recompute diffs,
        - Recompute gives/takes (defs/refs) data.
        """
        t1 = time.perf_counter()

        # Get the original tree (in the cache)
        path = updated_files[0]
        old_tree = self.old_tree_dict[path]
        new_tree = self.new_tree_dict[path]

        # Get the new tree, from the changed file.
        if 0:
            print(dump_ast(old_tree))
            print(dump_ast(new_tree))
            print('')

        # Visit all the nodes in the new tree.
        Visitor(controller=self).visit(new_tree)  # type:ignore

        t2 = time.perf_counter()
        self.stats.append(('Semantics', t2 - t1))
    #@+node:ekr.20250427190307.1: *3* CC.get_changed_files
    def get_changed_files(self) -> list[str]:
        """
        Update the tree and modification file for all new and changed files.
        """
        trace = False
        t1 = time.perf_counter()
        updated_paths: list[str] = []
        for path in self.paths:
            mod_time = os.path.getmtime(path)
            old_mod_time = self.mod_time_dict.get(path, None)
            if old_mod_time is not None and mod_time > old_mod_time:
                if trace:
                    kind = 'Create' if old_mod_time is None else 'Update'
                    print(f"{kind} {path} {time.ctime(mod_time)}")
                updated_paths.append(path)
                contents = g.readFile(path)
                tree = parse_ast(contents)
                self.new_tree_dict[path] = tree
                self.mod_time_dict[path] = mod_time
            else:
                self.new_tree_dict[path] = self.new_tree_dict[path]
        t2 = time.perf_counter()
        self.stats.append(('Find changed', t2 - t1))
        if trace and updated_paths:
            g.printObj(updated_paths, tag='Updated files')
        return updated_paths
    #@+node:ekr.20250515083553.1: *3* CC.init
    def init(self) -> None:

        # The list of all paths to be considered.
        self.paths: list[str] = [
            f"{core_path}{os.sep}{z}.py"
            for z in core_names if os.path.exists(z)
        ]

        # Init stats.
        self.stats: list[tuple[str, float]] = []

        # Load the cache.
        self.cache = self.load_cache()

        # Load dictionaries from the cache.
        self.old_tree_dict: dict[str, Optional[Node]] = self.cache.get('old_tree_dict') or {}
        self.new_tree_dict: dict[str, Optional[Node]] = {}
        self.mod_time_dict: dict[str, float] = self.cache.get('mod_time_dict') or {}
    #@+node:ekr.20250514055617.1: *3* CC.main (entry)
    def main(self) -> None:
        assert g.app is None, repr(g.app)
        assert g.unitTesting is False
        t1 = time.perf_counter()
        self.init()
        updated_files = self.get_changed_files()
        if updated_files:
            self.do_semantics(updated_files)
            self.write_cache()
            self.commit_cache()
        self.close_cache()
        t2 = time.perf_counter()
        self.stats.append(('Total', t2 - t1))
        self.print_stats(updated_files)
    #@+node:ekr.20250427200712.1: *3* CC: Cache methods
    #@+node:ekr.20250515104457.1: *4* CC.clear_cache (unit testing)
    def clear_cache(self) -> None:
        assert g.unitTesting
        self.cache['old_tree_dict'] = {}
        self.cache['mod_time_dict'] = {}
    #@+node:ekr.20250515084324.1: *4* CC.commit_cache
    def commit_cache(self) -> None:
        """Commit the cache."""
        t1 = time.perf_counter()
        self.cache.conn.commit()
        t2 = time.perf_counter()
        self.stats.append(('Commit cache', t2 - t1))

    #@+node:ekr.20250515084325.1: *4* CC.close_cache
    def close_cache(self) -> None:
        """Close the cache."""
        t1 = time.perf_counter()
        self.cache.conn.close()
        t2 = time.perf_counter()
        self.stats.append(('Close cache', t2 - t1))
    #@+node:ekr.20250428034510.1: *4* CC.dump_cache
    def dump_cache(self) -> None:
        """Dump the contents of the data to be written to the cache."""

        # Dump the modification times
        print('Dump of mod_time_dict...')
        for key, val in self.mod_time_dict.items():
            print(f"{val:<18} {key}")
    #@+node:ekr.20250515084143.1: *4* CC.load_cache
    def load_cache(self) -> SemanticCache:
        """Load the persistent cache."""
        t1 = time.perf_counter()
        cache = SemanticCache('semantic_cache.db')
        t2 = time.perf_counter()
        self.stats.append(('Load cache', (t2 - t1)))
        return cache
    #@+node:ekr.20250427194628.1: *4* CC.write_cache
    def write_cache(self) -> None:
        """Update the persistent cache with all data."""

        # All keys are full path names.
        t1 = time.perf_counter()
        self.cache['old_tree_dict'] = self.new_tree_dict
        self.cache['mod_time_dict'] = self.mod_time_dict
        t2 = time.perf_counter()
        self.stats.append(('Write cache', (t2 - t1)))
    #@+node:ekr.20250515084512.1: *3* CC: Stats
    #@+node:ekr.20250428071526.1: *4* CC.print_stats
    def print_stats(self, updated_files: list[str]) -> None:

        # Get the max length of all keys.
        pad_n = 5  # A reasonable default.
        for key, value in self.stats:
            pad_n = max(pad_n, len(key))

        def pad(key: str) -> str:
            pad_s = max(0, pad_n - len(key))
            return pad_s * ' ' + key

        # Print the stats.
        n = len(updated_files)
        print('')
        print(f"{n} updated file{g.plural(n)}")
        for key, value in self.stats:
            print(f"{pad(key)} {value:.2f} sec.")
    #@-others
#@+node:ekr.20250426053702.1: ** class class_cache
class class_cache:
    """A class containing all cached data from one Python class."""
#@+node:ekr.20250426053807.1: ** class module_cache
class module_cache:
    """A class containing all cached data from one Python module."""
#@+node:ekr.20250515125921.1: ** class Visitor (ast.NodeVisitor)
class Visitor(ast.NodeVisitor):
    """A visitor class to create refs/defs data."""

    def __init__(self, controller: CacheController) -> None:
        super().__init__()
        self.controller = controller
        self.context: list[Node] = []
        self.context_stack: list[Node] = []
        self.parent_context: Optional[Node] = None

    #@+others
    #@+node:ekr.20250515173146.1: *3* v.set_def & set_ref
    def set_def(self, node: Node) -> None:
        assert self.parent_context, g.callers()
        if 1:
            name = getattr(node, 'name', '<no name>')
            parent_name = getattr(self.parent_context, 'name', self.parent_context.__class__.__name__)
            print(f"Def: {parent_name:>20}::{name}")
        defs = getattr(self.parent_context, 'defs', [])
        defs.append(node)

    def set_ref(self, node: Node) -> None:
        assert self.parent_context, g.callers()
        if 1:
            name = getattr(node, 'name', '<no name>')
            parent_name = getattr(self.parent_context, 'name', self.parent_context.__class__.__name__)
            print(f"Ref: {parent_name:>20}::{name}")
        refs = getattr(self.parent_context, 'refs', [])
        refs.append(node)
    #@+node:ekr.20250515130057.1: *3* v.visit_ClassDef
    @ast_context
    def visit_ClassDef(self, node: Node) -> None:
        # tag_s = f"class {node.name}"
        # print(f"{tag_s:>20} parent_context: {self.parent_context.__class__.__name__}")
        self.set_def(node)
        self.generic_visit(node)
    #@+node:ekr.20250515130541.1: *3* v.visit_FunctionDef
    @ast_context
    def visit_FunctionDef(self, node: Node) -> None:
        # tag_s = f"def {node.name}"
        # print(f"{tag_s:>20} parent_context: {self.parent_context.__class__.__name__}")
        self.set_def(node)
        self.generic_visit(node)
    #@+node:ekr.20250515131258.1: *3* v.visit_Module
    @ast_context
    def visit_Module(self, node: Node) -> None:
        self.generic_visit(node)
    #@-others
#@-others

if __name__ == "__main__":
    CacheController().main()

#@@language python
#@@tabwidth -4
#@-leo
