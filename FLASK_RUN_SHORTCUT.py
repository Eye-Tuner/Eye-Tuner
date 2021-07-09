"""Shortcut for flask server."""

if __name__ == '__main__':
    import os
    import sys
    import runpy
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'flask', 'project'))
    runpy.run_module('app', run_name='__main__')
