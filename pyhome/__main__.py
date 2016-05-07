
from __future__ import print_function

import os
import sys
import shutil
import argparse
from glob import glob

from pyhome import settings, git, symlink

def repo_list():
    """
    Return list of all git repos in repodir
    """
    
    # Assuming all git repos contain a .git folder
    pattern = os.path.join(settings.PYHOME_REPO, '*', '.git')
    
    # Do some extra checks
    repos = []
    for path in glob(pattern):
        # .git should be a folder
        if not os.path.isdir(path):
            continue
        repo_root = os.path.dirname(path)
        repos.append(os.path.basename(repo_root))

    return sorted(repos)


def list(args):
    """
    List all existing repos in your pyhome
    """

    print('Current pyhome repos:')
    for repo in repo_list():
        print('    {}'.format(repo))
    

def clone(args):
    """
    Clone a new repo to your pyhome
    """

    # Make sure repo dir exists
    if not os.path.exists(settings.PYHOME_REPO):
        os.makedirs(settings.PYHOME_REPO)
    
    print('Cloning repo from {} ...'.format(args.url))
    git.clone(settings.PYHOME_REPO, args.url, args.name, args.submodules)


def remove(args):
    """
    Remove a repo from your pyhome
    """

    repopath = os.path.join(settings.PYHOME_REPO, args.repo)

    if not os.path.exists(repopath):
        print('No repo "{}" found.'.format(args.repo))
        # This is an error
        sys.exit(1)

    if not args.force:
        # Make sure of no accidental deletions
        tpl = 'Really remove "{}"? Run again with "-f" to confirm.'
        print(tpl.format(repopath))

    else:
        # Actually delete the thing
        print('Removing repo {} ...'.format(repopath))
        print(' - Unlinking ...')
        symlink.repo_clear_symlinks(repopath)
        print(' - Removing directory ...')
        shutil.rmtree(repopath)


def pull(args):
    """
    Pull a repo and optionally update its submodules
    """

    for r in repos_from_arguments(args):
        print('\nPulling repo in {} ...'.format(r))
        git.pull(r, args.submodules)


def link(args):
    """
    Generate links for this repo in your $HOME folder
    """

    for r in repos_from_arguments(args):
        print('\nCreating symlinks for repo {} ...'.format(r))
        symlink.repo_create_symlinks(r)


def unlink(args):
    """
    Remove links for this repo in your $HOME folder
    """

    for r in repos_from_arguments(args):
        print('\nRemoving symlinks for repo {} ...'.format(r))
        symlink.repo_clear_symlinks(r)


def parser_add_repo_options(parser):
    """
    Add some standard options for selecting repos to a parser
    """

    parser.add_argument('repos', nargs='*', help='repos to link')
    parser.add_argument('-a', '--all', action='store_true',
                        help='link all repos')


def repos_from_arguments(args):
    """
    Build a list of repos rom the arguments defined in parser_add_repo_options
    """
    
    if args.all:
        repos = repo_list()

        if len(repos) == 0:
            print('No repos have yet been cloned to your pyhome')
            sys.exit(1)

    else:
        repos = args.repos

        if len(repos) == 0:
            print('Either specify repos on the command line or use --all')
            sys.exit(1)
    
    return [os.path.join(settings.PYHOME_REPO, r) for r in repos]


def main():
    """
    Execute the main command line interface.
    """

    # Define the CLI
    description = 'A dotfile management and synchronisation tool.'
    parser = argparse.ArgumentParser(description=description)
    subparsers = parser.add_subparsers()

    # Fix for issue #9253
    # http://bugs.python.org/issue9253#msg186387
    subparsers.required = True
    subparsers.dest = 'subcommand'

    def add(func):
        sub = subparsers.add_parser(func.__name__, help=func.__doc__,
                                    description=func.__doc__)
        sub.set_defaults(func=func)
        return sub

    # List existing repos
    list_parser = add(list)
   
    # Clone a repo
    clone_parser = add(clone)
    clone_parser.add_argument('url',
                              help='URL of git repo to clone')
    clone_parser.add_argument('name',
                              nargs='?',
                              help='optionally specify name of cloned repo')
    clone_parser.add_argument('--no-submodules',
                              action='store_false', dest='submodules',
                              help='do not update submodules')

    # Remove a repo
    rm_parser = add(remove)
    rm_parser.add_argument('repo',
                           help='name of the repo to remove')
    rm_parser.add_argument('-f', '--force',
                           action='store_true',
                           help='confirm the removal of the repo')

    # Pull a repo/repos
    pull_parser = add(pull)
    parser_add_repo_options(pull_parser)
    pull_parser.add_argument('--no-submodules',
                             action='store_false', dest='submodules',
                             help='do not update submodules')
    
    # Set up symlinks
    link_parser = add(link)
    parser_add_repo_options(link_parser)

    # Clear symlinks
    unlink_parser = add(unlink)
    parser_add_repo_options(unlink_parser)

    args = parser.parse_args()
    args.func(args)


# Enable script execution with 'python -m pyhome'
if __name__ == '__main__':
    main()
