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
        if count_lines( history_file ) == settings.get( "history-length" ):
            with open( history_file, "w" ) as file:
                file.close()
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
    return re.match( r"^(([A-Z]\:\\\\)|([\/\\]*[\w]+))([\\\/]*[\w\-\.]*)*$",
            os.path.expanduser( possible_path ) )

def is_branch( possible_branch ):
    """Returns True when the possible_branch is a branch

    In "G" syntax a branch is escaped by a "@" (i.e. @name_of_branch)
    This function checks the argument "possible_branch" for exactly this syntax.

    Arguments:
        possible_branch: A string which should be checked for the branch-syntax of "G"
    """
    return re.match( r"^\@[\w\-\.\/]*$", possible_branch )

def is_empty( element ):
    return len( element ) == 0

def count_lines( path_to_file ):
    try:
        if is_path( path_to_file ):
            output = subprocess.check_output( [ "wc", "-l" ],
                    stdin = open( path_to_file, "r" ) )
            return int( output )
    except OSError:
        warning( "You need to have installed 'wc' to run 'G' proberly" )
        pass
    except FileNotFoundError:
        pass

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
        if type( operand ) == str:
            subprocess.check_call( [ "git", cmd ] + operand.split() )
        else:
            subprocess.check_call( [ "git", cmd ] + operand )
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
        return os.path.expanduser( "~/.config/G" )
    def file():
        return os.path.expanduser( "~/.config/G/config.yml" )
