"""
Pygaze patcher
Import this module first before importing pygaze.

Written by D. H. Kim
"""


def patch_pygaze_libtime():

    import sys
    import time
    from pygaze._time import pygametime  # NOQA

    # Patch time module first
    time.clock = time.perf_counter

    # Get original class from target module
    old_class = pygametime.PyGameTime

    # Make new constructor
    def new_constructor(self):
        old_class.__init__(self)  # call super constructor
        # On Windows, time.clock() (-> time.perf_counter() ) provides higher accuracy than time.time().
        if sys.platform == "win32":
            self._cpu_time = time.perf_counter
        else:
            self._cpu_time = time.time

    # Make new class dynamically by type
    new_class = type('PyGameTime', (old_class, ), {'__init__': new_constructor})

    # Patch with new class
    pygametime.PyGameTime = new_class


patch_pygaze_libtime()
