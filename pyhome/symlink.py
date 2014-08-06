"""
pyhome.symlink

Symbolic link creation and handling.
"""

import os
import shutil
from pyhome import settings



def overwrite_prompt():
    input = raw_input('Overwrite [yn]: ')
    clean = input.strip().lower()
    if clean == 'y':
        return True
    elif clean == 'n':
        return False
    else:
        print('Invalid input: "{}"'.format(input))
        return overwrite_prompt()


def create_single_symlink(linkpath, targetpath):

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


def repo_create_symlinks(repo):

    print('Creating symlinks for repo {}'.format(repo))
    repo_home = os.path.join(settings.PYHOME_REPO, repo, 'home')

    for file in os.listdir(repo_home):
        linkpath   = os.path.join(settings.HOME, file)
        targetpath = os.path.join(repo_home, file)
        create_single_symlink(linkpath, targetpath)


def repo_clear_symlinks(repo):

    print('Removing symlinks for repo {}'.format(repo))
    repo_home = os.path.join(settings.PYHOME_REPO, repo, 'home')

    for file in os.listdir(repo_home):
        linkpath   = os.path.join(settings.HOME, file)
        targetpath = os.path.join(repo_home, file)
        clear_single_symlink(linkpath, targetpath)
