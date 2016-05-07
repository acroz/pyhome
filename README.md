# pyhome

A dotfile management and synchronisation tool.

This is a simple python utility with similar functionality to the functionality
of the `homesick` ruby utility, providing a simple interface for managing
dotfiles via git repositories.

This tool was born out of frustration at attempting to use ruby gems on HPC
systems, where I did not have administrative rights. On such systems, which are
often not the bleeding edge of ruby version, getting gems to work has proved
extremely difficult. Installation of a new ruby version with associated rubygem
was possible sometimes, but not often enough.

## Aims

This tool replicates the most basic functionalities of `homesick`, namely

1. Cloning git repositories to the appropriate location
2. Pulling repositories
3. Automatic creation of symbolic links to dotfiles in repos

## Development

Code is written to be compatible with both Python 2.6+ and 3.x, and
deliberately avoids using any modules outside the standard library, so that it
works out-of-the-box on any system with a reasonably modern Python interpreter
installed.
