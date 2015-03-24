#!/bin/env python3

import sys, atexit, code, os, readline, yaml

from cli_colors import *
from messages import *
from manage_remotes import *
from manage_submodules import *
from helpers import *

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

def get_operator( args ):
    """Get the operator from the Arguments

    The operation which should be processed is defined by an operator.
    Possible operators are: "+", "-", "~", "=", "→", ">"

    Arguments:
        args: The arguments that need to be processed to get the operator
    """
    for arg in args:
        index = args.index( arg )
        if index == 0:
            if arg == "+":
                return "add"
            elif arg == "-":
                return "reset"
            elif arg == "~":
                return "diff"
        if arg == "=":
            return "set"
        elif arg == "→":
            return "push"
        elif arg == ">":
            return "merge"

def parse_args( args ):
    """Process all arguments recursive and store them in the operands dictionary

    When the current argument is a special operator (like "+", "-", "~", ...) the arguments
    before the operator are removed. Now the recursion begins and the function is executed again,
    when the index is greater than 0. The index must be greater then nill, because the parse_args()
    function would otherwise loop endless, because the first argument is at everytime an operator,
    when used in combination with a special operator.

    When the current argument is an operator like "push" or is an file, the argument is simply added
    to the operands list. When the current argument is a file it would also simply be added to the
    arguments list. The index of a file or a branch (@master) could also be greater or equal to the
    index 0 because normal operators does not start a recursive processing of the other arguments.

    When the index of the current argument is as long as the length of the arguments list,
    this argument is the last argument of the arguments list and is also added to the operands list.
    At this point the recursion stops, because all elements are added to the operands list.

    Arguments:
        args: The arguments that need to be parsed
    """
    length = len( args ) - 1
    operator = get_operator( args )
    for arg in args:
        index = args.index( arg )
        if index < length:
            if index >= 0:
                if is_branch( arg ):
                    operands.get( "push" ).append( arg[1:] )
                if is_path( arg ):
                    operands.get( "files" ).append( arg )
            elif index > 0:
                if arg == "+":
                    del args[0:index]
                    parse_args( args )
                elif arg == "-":
                    del args[0:index]
                    parse_args( args )
                elif arg == "~":
                    del args[0:index]
                    parse_args( args )
                elif is_path( arg ):
                    operands[operator].append( arg )
        elif index == length:
            if operator == "push" or operator == "merge":
                operands.get( "push" ).append( arg[1:] )
            elif is_path( arg ):
                operands[operator].append( arg )

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
    else:
        return sys.argv[1].split()

def get_settings():
    """Returns a dictionary which contains all settings from the config.yml file"""
    config_file = config.file()
    file = os.path.expanduser( config_file )
    if os.path.exists( file ):
        with open( file , "r" ) as yaml_config:
            return yaml.load( yaml_config )

def save_settings( settings ):
    """Store settings in the config.yml file

    This function saves settings via pyYAML in the config.yml file

    Warning:
        This function can overwrite the config.yml file, when values are not
        appended to the settings dictionary

    Arguments:
        settings: Settings that should be written to the config.yml file
    """
    config = config.file
    file = os.path.expanduser( config )
    if os.path.exists( file ):
        with open( file , "w" ) as yaml_config:
            yaml_config.write( yaml.dump( settings, default_flow_style = False ) )

def main():

    args = get_user_input()
    operator = get_operator( args )
    operands = { "add": [], "reset": [], "diff": [], "push": [] }
    files = []

    if not args:
        usage()
    else:
        parse_args( operator, args )

    if not operands.get( "add" ) == []:
        git( "add", operands.get( "add" ) )
    elif not operands.get( "reset" ) == []:
        git( "reset", operands.get( "reset" ) )
    elif not operands.get( "diff" ) == []:
        git( "diff", operands.get( "diff" ) )

    if operator == "push":
        if len( operands.get( "push" ) ) == 1:
            git( "push", [ "origin", operands.get( "push" )[0] ] )
        elif len( operands.get( "push" ) ) == 2:
            git( "push", [ operands.get( "push" )[1], branches[0] ] )
    elif operator == "merge":
        if len( operands.get( "push" ) ) == 1:
            git( "merge", operands.get( "push" ) )
        elif len( operands.get( "push" ) ) == 2:
            git( "checkout",  [ operands.get( "push" )[0] ]  )
            git( "merge", operands.get( "push" )[1] )

if __name__ == "__main__":
    """Start main() function and handle errors

    When the python file is executed this conditional starts the main() function
    The main() function loops as long, as user stops G via <C-c> or <C-d>.
    When <C-c> or <C-d> is pressed, to stop the execution, "G" raises no error code.

    When the python file is imported as a package, the settings variable is set.
    This behaviour makes it possible to use "G" a an python interface to the "Git"
    command-line program.
    """
    try:
        while True:
            main()
    except BaseException:
        sys.exit(0)
else:
    settings = get_settings()
