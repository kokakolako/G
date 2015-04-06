#!/bin/env python3

# G -- An interactive shell for Git
# -------------------------------------------------------------------------
#
# Copyright (C) 2015  Niklas Köhler
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os, sys

from G.cli_colors import fg
from G.config import history_file
from G.helpers import *
from G.messages import usage
from G.remotes import show_remotes, add_remote
from G.settings import get_settings
from G.submodules import show_submodules, add_submodule

def main( args ):

    settings = get_settings()
    operands = get_operands( args )

    if not args:
        usage()
    elif len( args ) == 1:
        arg = args[0]
        if arg == "@remotes":
            show_remotes()
        elif arg == "@submodules":
            show_submodules()

    for operator, parameter in operands.items():
        if not is_empty( parameter ):
            if operator == "add" or operator == "reset":
                git( operator, parameter )
            elif operator == "push":
                if len( parameter ) == 1:
                    git( "push", [ "origin", parameter[0][1:] ] )
                elif len( parameter ) == 2:
                    git( "push", [ parameter[1][1:], parameter[0][1:] ] )
            elif operator == "merge":
                if len( parameter ) == 1:
                    git( "merge", parameter[0][1:] )
                elif len( parameter ) == 2:
                    git( "checkout",  [ parameter[0][1:] ]  )
                    git( "merge", parameter[1][1:] )
            elif operator == "cd":
                os.chdir( os.path.expanduser( parameter[0] ) )
            elif operator == "set":
                if is_submodule( parameter[0] ):
                    add_submodule( parameter[0][1:], parameter[1] )

def get_user_input( args = sys.argv ):
    """Returns the arguments in an list which are typed-in by the user

    When the user defines an argument via the command-line, "G" directly interprets the argument.
    The argument must be escaped by quotation marks ("), otherwhise they would not be processed.

    When the user simply invakes G witouh an argument, an interacitve shell session is started:
    The history is saved and some Emacs editing keys are working.
    """
    if len( args ) == 1:
        console = GConsole()
        return console.raw_input( "G " + fg.red( ">" ) + " " ).split()
    if len( args ) == 2:
        if type( args[1] ) == str:
            return args[1].split()
    else:
        return args

def get_operator( args ):
    """Get the operator from the Arguments

    The operation which should be processed is defined by an operator. Possible operators
    are: "+", "-", "~", "=", "→", ">"

    Arguments:
        args: The arguments that need to be processed to get the operator
    """

    if type( args ) == str:
        args = [ args ]

    for arg in args:
        index = args.index( arg )
        if index >= 0:
            if arg == "=":
                return "set"
            elif arg == "->":
                return "push"
            elif arg == ">":
                return "merge"
            elif arg == "cd":
                return "cd"
        if index == 0:
            if arg == "+":
                return "add"
            elif arg == "-":
                return "reset"
    return False

def get_operands( args ):
    """Returns all operands as an dictionary

    When the current argument is a special operator (like "+", "-", ...) the arguments
    before the operator are removed. Now the recursion begins and the function is executed again,
    when the index is greater than 0. The index must be greater then nill, because the get_operands()
    function would otherwise loop endless, because the first argument is at everytime an operator,
    when used in combination with a special operator.

    When the current argument is an operator like "push" or "merge" or is an file, the argument is added
    to the operands dictionary. When the current argument is a file it would also added to the
    arguments list. The index of a file or a branch (@master) could also be greater or equal to the
    index 0 because normal operators does not start a recursive processing of the other arguments.

    When the index of the current argument is as long as the length of the arguments list,
    this argument is the last argument of the arguments list and is also added to the operands list.
    At this point the recursion stops, because all elements are added to the operands list.

    Arguments:
        args: The arguments that need to be checked for operands
    """
    # The index number of the last element in the args list

    length = len( args ) - 1
    operator = get_operator( args )

    for arg in args:
        # The index of the current argument (arg)
        index = args.index( arg )
        if index < length:
            if index == 0:
                operands = { "add": [], "reset": [], "merge": [], "push": [], "cd": [], "set": [] }
            if index >= 0:
                if not get_operator( arg ):
                    operands.get( operator ).append( arg )
            elif index > 0:
                if arg == "+" or arg == "-" or arg == "~":
                    del args[0:index]
                    return get_operands( args )
        # Return all operands when the index is equally to the length of the
        # arguments array, the recursiomn stops at this pint (also append the
        elif index == length:
            operands.get( operator ).append( arg )
            return operands

# Check if the program is started via the executable
if __name__ == "__main__":
    """Start main() function and handle errors

    When the python file is executed this conditional starts the main() function The main() function
    loops as long, as user stops G via <C-c> or <C-d>.  When <C-c> or <C-d> is pressed, to stop the
    execution, "G" raises no error code.

    When the python file is imported as a package, the settings variable is set. This behaviour makes
    it possible to use "G" a an python module.
    """

    # Check if the history is longer than "history-length"
    # The initialization of G would be otherwise VERY slow
    history_file()

    # Parse optional arguments
    if len( sys.argv ) > 1:
        # Start G in debug mode ( main is executed one single time,
        # errors become printed to stderr )
        if sys.argv[1] == "-d" or sys.argv[1] == "--debug":
            args = sys.argv
            # Remove the debug parameter
            args.remove( args[1] )
            main( get_user_input( args ) )
    # Loop main() as long as the user does not stop G via <C-c>
    # or <C-d>, handle runtime errors via exceptions.
    else:
        while True:
            try:
                # Get user input and redirect the arguments to the
                # main() function
                args = get_user_input()
                main( args )
            except BaseException:
                sys.exit( 0 )
# If the user starts G as a script (i.e. importing G via python),
# get settings from the config file (instead of get the settings via
# a user input
else:
    settings = get_settings()
