#!/bin/env python3
# G

import os, re, sys, yaml

from helpers import *
from manage_submodules import *
from manage_remotes import *
from cli_colors import *

def main():

    args = get_user_input()
    operands = get_operands( args )
    settings = get_settings()

    if not args:
        usage()

    for operator, files in operands:
        if not is_empty( files ):
            if operator == "add" or operator == "reset":
                git( operator, files )
            elif operator == "push":
                if len( files ) == 1:
                    git( "push", [ "origin", files[0] ] )
                elif len( files ) == 2:
                    git( "push", [ files[1], files[0] ] )
            elif operator == "merge":
                if len( files ) == 1:
                    git( "merge", files[0] )
                elif len( files ) == 2:
                    git( "checkout",  [ files[0] ]  )
                    git( "merge", files[1] )

def get_user_input():
    """Returns the arguments in an list which are typed-in by the user

    When the user defines an argument via the command-line, "G" directly interprets the argument.
    The argument must be escaped by quotation marks ("), otherwhise they would not be processed.

    When the user simply invakes G witouh an argument, an interacitve shell session is started:
    The history is saved and some Emacs editing keys are working.
    """
    if len( sys.argv ) == 1:
        console = GConsole()
        return console.raw_input( "G " + fg.red( ">" ) + " " ).split()
    if len( sys.argv ) == 2:
        if type( sys.argv[1] ) == str:
            return sys.argv[1].split()
    else:
        return sys.argv

def get_settings():
    """Returns a dictionary which contains all settings from the config.yml file"""
    with open( config.file() , "r" ) as yaml_config:
        return yaml.load( yaml_config )

def save_settings( settings ):
    """Store settings via pyYAML in the config file

    __Warning__:
        This function can overwrite the config.yml file, when values are not **appended** to the
        settings dictionary

    Arguments:
        settings: Settings that should be written to the config.yml file
    """
    with open( config.file() , "w" ) as yaml_config:
        yaml_config.write( yaml.dump( settings, default_flow_style = False ) )

def get_operator( args ):
    """Get the operator from the Arguments

    The operation which should be processed is defined by an operator. Possible operators
    are: "+", "-", "~", "=", "→", ">"

    Arguments:
        args: The arguments that need to be processed to get the operator
    """
    for arg in args:
        index = args.index( arg )
        if index >= 0:
            if arg == "=":
                return "set"
            elif arg == "->":
                return "push"
            elif arg == ">":
                return "merge"
        if index == 0:
            if arg == "+":
                return "add"
            elif arg == "-":
                return "reset"

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
    length = len( args ) - 1
    operator = get_operator( args )
    for arg in args:
        index = args.index( arg )
        if index < length:
            if index >= 0:
                if index == 0:
                    operands = { "add": [], "reset": [], "merge": [], "push": [] }
                if is_path( arg ):
                    operands.get( operator ).append( arg )
                elif is_branch( arg ):
                    operands.get( operator ).append( arg[1:] )
            elif index > 0:
                if arg == "+" or arg == "-" or arg == "~":
                    del args[0:index]
                    return get_operands( args )
        elif index == length:
            if is_path( arg ):
                operands.get( operator ).append( arg )
            elif is_branch( arg ):
                operands.get( operator ).append( arg[1:] )
            return operands

if __name__ == "__main__":
    """Start main() function and handle errors

    When the python file is executed this conditional starts the main() function The main() function
    loops as long, as user stops G via <C-c> or <C-d>.  When <C-c> or <C-d> is pressed, to stop the
    execution, "G" raises no error code.

    When the python file is imported as a package, the settings variable is set. This behaviour makes
    it possible to use "G" a an python module.
    """
    try:
        while True:
            main()
    except BaseException:
        sys.exit(0)
else:
    settings = get_settings()
