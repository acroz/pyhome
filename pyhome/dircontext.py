"""
Directory context manager for the safe execution of a function with a temporary
changed working directory.
"""

import os
from contextlib import contextmanager

@contextmanager
def dircontext(directory):
    """
    Context manager for the execution of a code block inside another directory.
    """

    # Store the current directory
    orig_dir = os.getcwd()

    try:
        # Change the working directory
        os.chdir(directory)
        yield

    finally:
        # Resotre the original directory
        os.chdir(orig_dir)
