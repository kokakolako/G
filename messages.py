#!/bin/env python3
# Messages

from cli_colors import fg
import sys

def error( message ):
    """Prints an error message, stops "G" and raises error code 1

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.red( "Error: " + message ) )
    sys.exit( 1 )

def warning( message ):
    """Prints an warning

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.yellow( message ) )

def success( message ):
    """Prints an succes message

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.green( message ) )

def usage():
    """Display usage information

    When the user does not insert an argument, the usage information are displayed.
    """
    usage = """\
DESCRIPTION:

G is an interface to simplify the work with the git command line tool.

SYNTAX COMPARED TO GIT:

+-----------------------------+----------------------------------------------+---------------------------+
| Task                        | Git syntax                                   | G Syntax                  |
+-----------------------------+----------------------------------------------+---------------------------+
| Add files to the index      | git add file1 file2                          | + file1 file2             |
| Remove files from the index | git reset file1 file2                        | - file1 file2             |
| Push to a remote repository | git push origin master                       | @master -> @origin        |
| Merge branches              | git merge feature-branch                     | @feature-branch > @master |
| Update all submodules       | git submodule foreach git pull origin master | update                    |
+-----------------------------+----------------------------------------------+---------------------------+\
"""
    print( usage )
