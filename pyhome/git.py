"""
pyhome.git

Provides functional interface to git by running shell commands through the
subprocess module.
"""

from subprocess import check_output, STDOUT, CalledProcessError
from pyhome.dircontext import dircontext

class GitException(Exception):
    pass

def git(*args):
    """
    Run a git command.
    """
    
    # Construct command list
    cmd = ['git'] + list(args)
    
    # Attempt command and handle errors
    try:
        output = check_output(cmd, stderr=STDOUT)
    except OSError:
        raise GitException('git command not found')
    except CalledProcessError as e:
        raise GitException(e.output.strip())

    print(output.strip())

def clone(pyhome_dir, url, name=None):
    """
    Clone a git repo.
    """

    with dircontext(pyhome_dir):

        if name is None:
            git('clone', url)

        else:
            assert isinstance(name, str), GitException('Specified repo name invalid')
            assert len(name) > 0, GitException('Specified repo name invalid')

            git('clone', url, name)

def submodule_update(repo_root):
    """
    Update all submodules in a repo.
    """

    with dircontext(repo_root):
        git('submodule', 'update', '--init')
