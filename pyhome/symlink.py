"""
Symbolic link creation and handling.
"""

from __future__ import print_function

import os
import shutil
from pyhome import settings

# Python 2/3 compatability
try:
    input = raw_input
except NameError:
    pass

# Files to search for that may contain subdir definitions
SUBDIR_FILENAMES = ['.subdir',
                    '.pyhome_subdir',
                    '.homesick_subdir']

def overwrite_prompt():
    userinput = input('Overwrite [yn]: ')
    clean = userinput.strip().lower()
    if clean == 'y':
        return True
    elif clean == 'n':
        return False
    else:
        print('Invalid input: "{}"'.format(input))
        return overwrite_prompt()

def create_single_symlink(linkpath, targetpath):
    """
    Create a symbolic link, printing status messages and prompting if needed.
    """

    create = True

    # Check current file status
    if os.path.exists(linkpath):

        # Is it a link already
        if os.path.islink(linkpath):

            # Does it point to the right place?
            if os.path.samefile(linkpath, targetpath):
                print('Unchanged: {} -> {}'.format(linkpath, targetpath))
                return

            else:
                print('Conflict: {} -> {}'.format(linkpath, targetpath))
                print('          {}'.format(linkpath))
                print('              currently points to')
                print('          {}'.format(os.readlink(linkpath)))

                if overwrite_prompt():
                    os.unlink(linkpath)
                else:
                    create = False

        else:
            print('Conflict: {} -> {}'.format(linkpath, targetpath))
            print('          {}'.format(linkpath))

            if os.path.isdir(linkpath):
                print('              exists and is a directory')
                if overwrite_prompt():
                    shutil.rmtree(linkpath)
                else:
                    create = False

            else:
                print('              exists')
                if overwrite_prompt():
                    os.remove(linkpath)
                else:
                    create = False

    if create:
        os.symlink(targetpath, linkpath)
        print('Linked:   {} -> {}'.format(linkpath, targetpath))


def clear_single_symlink(linkpath, targetpath):
    """
    Remove a symbolic link, printing status messages and prompting if needed.
    """

    if not os.path.exists(linkpath):
        # Skip quietly
        pass

    elif not os.path.islink(linkpath):
        print('Skipping: {} -> {}'.format(linkpath, targetpath))
        print('          {}'.format(linkpath))
        print('              is not a link')
    
    elif not os.path.samefile(linkpath, targetpath):
        print('Skipping: {} -> {}'.format(linkpath, targetpath))
        print('          {}'.format(linkpath))
        print('              does not point to')
        print('          {}'.format(os.readlink(linkpath)))

    else:
        os.unlink(linkpath)
        print('Unlinked: {} -> {}'.format(linkpath, targetpath))

def splitall(path):
    """
    Split a path into its constituent parts.

    From the Python Cookbook: https://goo.gl/ooy0sx
    """

    allparts = []

    while 1:
        parts = os.path.split(path)

        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break

        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break

        else:
            path = parts[0]
            allparts.insert(0, parts[1])

    return allparts

def linkable_files(directory, subdirs=[]):
    """
    Generate a list of linkable files in the directory, accounting for subdir
    definitions.
    """

    # Get the first directory of each subdir
    subdir_top = [splitall(sd)[0] for sd in subdirs]

    for file in os.listdir(directory):

        if file in subdir_top:

            # Get any children
            children = []
            for top, sd in zip(subdir_top, subdirs):
                if file == top:
                    remaining = splitall(sd)[1:]
                    if len(remaining) > 0:
                        children.append(os.path.join(*remaining))

            for subfile in linkable_files(os.path.join(directory, file),
                                          children):
                yield os.path.join(file, subfile)

        else:
            yield file


def load_subdirs(repo):
    """
    Load any subdir definitions for this repo.
    """

    subdirs = []

    # Iterate over all possible subdir files
    for filename in SUBDIR_FILENAMES:
        fullpath = os.path.join(repo, filename)
        if os.path.exists(fullpath):

            # Load the subdirs
            with open(fullpath) as fp:
                for line in fp:
                    line = line.strip()
                    if len(line) > 0:
                        subdirs.append(line)

    return subdirs


def repo_symlink_map(repo, function):
    """
    Map a function to all linkable file (from, to) pairs in this repo.
    """

    home = os.path.join(repo, 'home')

    for fname in linkable_files(home, load_subdirs(repo)):
        linkpath   = os.path.join(settings.HOME, fname)
        targetpath = os.path.join(home, fname)
        function(linkpath, targetpath)


def repo_create_symlinks(repo):
    """
    Generate symbolic links for this repo.
    """
    repo_symlink_map(repo, create_single_symlink)


def repo_clear_symlinks(repo):
    """
    Remove symbolic links for this repo.
    """
    repo_symlink_map(repo, clear_single_symlink)
