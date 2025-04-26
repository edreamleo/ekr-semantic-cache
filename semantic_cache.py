#@+leo-ver=5-thin
#@+node:ekr.20250426050140.1: * @file semantic_cache.py
"""The main program for the semantic cacher"""

#@+<< semantic_cache: imports >>
#@+node:ekr.20250426051119.1: ** << semantic_cache: imports >>
# pylint: disable=reimported,unused-import,wrong-import-position

import ast
import sys

leo_path = r'C:\Repos\leo-editor'
if leo_path not in sys.path:
    sys.path.insert(0, leo_path)

from leo.core import leoGlobals as g
from leo.core import (
    leoAPI, leoApp, leoAtFile,  # leoAst,
    leoBackground,  # leoBridge, # leoBeautify,
    leoCache, leoChapters, leoColor, leoColorizer,
    leoCommands, leoConfig,  # leoCompare, leoDebugger,
    leoExternalFiles,
    leoFileCommands, leoFind, leoFrame,
    leoGlobals, leoGui,
    leoHistory, leoImport,  # leoJupytext,
    leoKeys, leoMarkup, leoMenu,
    leoNodes,
    leoPlugins,  # leoPersistence, leoPrinting, leoPymacs,
    leoQt,
    leoRst,  # leoRope,
    leoSessions, leoShadow,
    # leoTest2, leoTips, leoTokens,
    leoUndo, leoVersion,  # leoVim
)
#@-<< semantic_cache: imports >>

#@+others
#@+node:ekr.20250426052508.1: ** function: main
def main():
    g.trace()
#@-others

if __name__ == "__main__":
    main()

#@@language python
#@@tabwidth -4
#@-leo
