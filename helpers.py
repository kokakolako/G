#!/bin/env python3
# Helpers

import os, re, subprocess, atexit, code, readline

class GConsole( code.InteractiveConsole ):
    """Interactive Console with history and emacs short-cuts

    This class modifies the InteractiveConsole class from the "code" module to
    support a history, the history file is typically located at the following path:
        ~/.config/G/history
    """
    def __init__( self, locals = None, filename = "<console>" ):
        history_file = os.path.join( config.dir(), "history" )
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history( history_file )
    def init_history( self, history_file ):
        readline.parse_and_bind( "tab: complete" )
        if hasattr( readline, "read_history_file" ):
            try:
                readline.read_history_file( history_file )
            except FileNotFoundError:
                pass
            atexit.register( self.save_history, history_file )
    def save_history( self, history_file ):
        readline.write_history_file( history_file )


def is_path( possible_path ):
    """Returns True when the possible_branch is a valid path (POSIX/Windows)

    Arguments:
        possible_path: A string which should be checked if it is a valid path
    """
    if re.match( r"^(([A-Z]\:\\\\)|([\/\\]*[\w]+))([\\\/]*[\w\-\.]*)*$", os.path.expanduser( possible_path ) ):
        return True
    else:
        return False

def is_branch( possible_branch ):
    """Returns True when the possible_branch is a branch

    In "G" syntax a branch is escaped by a "@" (i.e. @name_of_branch)
    This function checks the argument "possible_branch" for exactly this syntax.

    Arguments:
        possible_branch: A string which should be checked for the branch-syntax of "G"
    """
    if re.match( r"^\@[\w\-\.\/]*$", possible_branch ):
        return True
    else:
        return False

def error( message ):
    """Prints an error message, stops "G" and raises error code 1

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.red( message ) )
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

def git( cmd, operand ):
    """Start a git command as a subprocess

    Arguments:
        cmd: The git command, that should to be executed. This argument must be one
        of the following: "push", "pull", "merge", "add", "reset"
        operand: Contains the files or branches, that need to be processed.
    """
    try:
        subprocess.call( [ "git", cmd ] + operand )
    except OSError:
        error( "Git need to be installed to proberly use G" )

def usage():
    """Display usage information

    When the user does not insert an argument, the usage information are displayed.
    """
    usage = """\
DESCRIPTION:

G is an interface to simplify the work with the git command line tool.

SYNTAX COMPARED TO GIT:

+------------------------------------+--------------------------+---------------------------+
| Task                               | Git syntax               | G Syntax                  |
+------------------------------------+--------------------------+---------------------------+
| Add files to the index             | git add file1 file2      | + file1 file2             |
| Remove files from the index        | git reset file1 file2    | - file1 file2             |
| Push branch to a remote repository | git push origin master   | @master -> @origin        |
| Merge branches                     | git merge feature-branch | @feature-branch > @master |
+------------------------------------+--------------------------+---------------------------+\
"""
    print( usage )

class config():
    """Get the path to the configuration directory or the configuration file

    Typicall paths for the config file / directory:
        configuration directory:    ~/.config/G
        configuration file:         ~/.config/G/config.yml

    Methods:
        dir: Returns the path to the configuration directory
        file: Returns the path to the configuration file
    """
    def __init__(  ):
        if not os.path.exists( os.path.join( os.path.expanduser( "~/.config" ), "G" )):
            os.mkdir( os.path.join( os.path.expanduser( "~/.config" ), "G" ) )
        if not os.path.isfile( os.path.expanduser( os.path.expanduser( "~/.config" ), "~/.config/G/config.yml" ) ):
            with open( os.path.expanduser( "~/.config/G/config.yml", "w" ) ) as file:
                file.close()
    def dir():
        return os.path.join( os.path.expanduser( "~/.config" ), "G" )
    def file():
        return os.path.expanduser( os.path.join( os.path.expanduser( "~/.config" ), "G/config.yml" ) )
