"""
Provides functional interface to git by running shell commands through the
subprocess module.
"""

import os
import locale
from subprocess import check_output, STDOUT, CalledProcessError
from pyhome.dircontext import dircontext

# Determine system encoding from locale
SYSENC = locale.getpreferredencoding()

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
    except OSError as e:
        raise GitException('git command not found')
    except CalledProcessError as e:
        raise GitException(e.output.decode(SYSENC).strip())
    finally:
        pass
    
    out = output.decode(SYSENC).strip()
    if len(out) > 0:
        print(out)

def reponame(url, name=None):
    """
    Determine a repo's cloned name from its URL.
    """
    if name is not None:
        return name
    name = os.path.basename(url)
    if name.endswith('.git'):
        name = name[:-4]
    return name

def clone(parent, url, name=None, submodules=True):
    """
    Clone a git repo.
    """

    subcmd = ['clone', url]
    
    if name is not None:
        subcmd.append(name)

    with dircontext(parent):
        git(*subcmd)

        if submodules:
            with dircontext(reponame(url, name)):
                git('submodule', 'update', '--init')

def pull(repo, submodules=True):
    """
    Update a repo.
    """
    with dircontext(repo):
        git('pull')
        if submodules:
            git('submodule', 'update', '--init')
