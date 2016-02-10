# pyhome

A simple python utility replicating the basic functionality of the `homesick`
ruby utility, providing a simple interface for managing dotfiles via git repos.

This tool was born out of frustration at attempting to use ruby gems on
systems where I do not have administrative rights. On such systems, which are
often not the bleeding edge of ruby version, getting gems to work has proved
extremely difficult. Installation of a new ruby version with associated rubygem
was possible some, but not all of the time.

## Aim

This tool replicates the most basic functionalities of `homesick`, namely

1. Cloning repos to the appropriate location
2. Commit/push/pull of repos
3. Automatic creation of symbolic links to files in repos

Code is written to be compatible with both Python 2.6+ and 3.x.
