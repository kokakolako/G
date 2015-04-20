#!/bin/env python3
# Helpers

import os, re, subprocess, atexit, code, readline

from config import history_file

class GConsole( code.InteractiveConsole ):
    """Interactive Console with history and emacs short-cuts

    This class modifies the InteractiveConsole class from the "code" module to
    support a history, the history file is typically located at the following path:
        ~/.config/G/history
    """
    def __init__( self, locals = None, filename = "<console>",
            histfile = history_file() ):
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history( histfile )
    def init_history( self, histfile ):
        readline.parse_and_bind( "tab: complete" )
        if hasattr( readline, "read_history_file" ):
            try:
                readline.read_history_file( histfile )
            except FileNotFoundError:
                pass
            atexit.register( self.save_history, histfile )
    def save_history( self, histfile ):
        readline.write_history_file( histfile )

def emend_path( path_to_emend ):
    """This function convert a string to an OS independent path"""
    path = re.split( r"[\\\/]", os.path.expanduser( path_to_emend ) )
    if re.match( r"([\/\\]|[^~])", path_to_emend[0:1] ):
        return path.insert( 0, os.sep )
    else:
        return os.getcwd() + os.sep + os.path.join( *path )

def is_path( possible_path ):
    """Returns True when the possible_branch is a valid path (POSIX/Windows)

    Arguments:
        possible_path: A string which should be checked if it is a valid path
    """
    if re.match( r"^(([A-Z]\:\\\\)|([\/\\]*[\w]+))([\\\/]*[\w\-\.]*)*$",
            os.path.expanduser( possible_path ) ):
        return True
    else:
        return False

def is_variable( possible_variable ):
    """Returns True when the possible_variable is a branch

    In "G" syntax a variable is escaped by a "@" (i.e. @name_of_branch)
    This function checks the argument "possible_variable" for exactly this syntax.

    Arguments:
        possible_variable: A string which should be checked for the branch-syntax of "G"
    """
    if re.match( r"^\@[\w\-\.\/]*$", possible_variable ):
        return True
    else:
        return False

def is_repository( possible_repository = os.getcwd() ):
    for file in os.listdir( possible_repository ):
        if file == ".git":
            return True
        else:
            return False

def is_empty( element ):
    return len( element ) == 0

def git( cmd, operand = None  ):
    """Start a git command as a subprocess

    Arguments:
        cmd: The git command, that should to be executed. This argument must be one
        of the following: "push", "pull", "merge", "add", "reset"
        operand: Contains the files or branches, that need to be processed.
    """
    try:
        if not operand:
            subprocess.check_call( [ "git", cmd ] )
        elif type( operand ) == str:
            subprocess.check_call( [ "git", cmd ] + operand.split() )
        else:
            subprocess.check_call( [ "git", cmd ] + operand )
    except OSError:
        error( "Git need to be installed to proberly use G" )

def get_current_branch():
    current_branch = subprocess.check_output( "git rev-parse --abbrev-ref HEAD".split() )
    # Convert the byte-string to utf-8
    current_branch = current_branch.decode( "utf-8" )
    # Return the current branch without the newline character ("\n")
    return current_branch[:-1]
