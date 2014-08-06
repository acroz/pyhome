"""
pyhome.dircontext

Directory context manager for the safe execution of a function with a temporary
changed working directory.
"""

import os

class dircontext(object):
    """
    Simple context manager for the execution of a code block inside another
    directory.
    """

    def __init__(self, dir):
        """ Store current and temp directories """
        self._orig_dir = os.getcwd()
        self._temp_dir = os.path.abspath(dir)

    def __enter__(self):
        """ Change to temporary directory """
        os.chdir(self._temp_dir)

    def __exit__(self, *args, **kwargs):
        """ Reset directory to original dir """
        os.chdir(self._orig_dir)
