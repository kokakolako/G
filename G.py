#!/bin/env python3

import re, subprocess, sys, atexit, code, os, readline, yaml
from cli_colors import *
from messages import *

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
            os.mkdir( os.path.join( xdg_conf, "G" ) )
        if not os.path.isfile( os.path.expanduser( os.path.expanduser( "~/.config" ), "~/.config/G/config.yml" ) ):
            with open( os.path.expanduser( "~/.config/G/config.yml", "w" ) ) as file:
                file.close()
    def dir():
        return os.path.join( os.path.expanduser( "~/.config" ), "G" )
    def file():
        return os.path.expanduser( os.path.join( os.path.expanduser( "~/.config" ), "G/config.yml" ) )

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
    """Returns True when the possible_branch is a valid path

    Arguments:
        possible_path: A string which should be checked if it is a valid path
    """
    if re.match( "(([A-Z]\:\\\\)|(\~[\/]))((\W*\/)|(\W*\\)(\W*))*", possible_path ):
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
    if re.match( "\@\W*", possible_branch ):
        return True
    else:
        return False

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

def get_remotes():
    """Get all remotes, from the current repository (the current working directory)"""
    for repository in settings.get( "repositories" ):
        for key in repository.keys():
            if os.path.expanduser( key ) == os.path.expanduser( os.getcwd() ):
                    return repository.get( key ).get( "remotes" )

def add_remote( name, url ):
    """Add a new remote to the config.yml file

    When no remotes are defined in the current repository into the config.yml file.
    This function adds a new remote to the current repository. The current working
    directory is used as the name for the current repository.

    Arguments:
        name: The name for the remote (i.e. origin)
        url: The url to the remote repository (i.e. git@github.com:kokakolako/G.git)
    """
    cwd = os.getcwd()
    remotes = get_remotes()
    if not remotes:
        settings.get( "repositories" ).append( { cwd: { "remotes": [ { name: url }] } } )
    for repository in settings.get( "repositories" ):
        for key in repository.keys():
            if os.path.expanduser( key ) == os.path.expanduser( cwd ):
                    remotes = repository.get( key ).get( "remotes" )
    else:
        # Check if name is contained in all remotes
        if not name in [ list( remote.keys() )[0] for remote in remotes ]:
            remotes.append( { name: url } )
    for repository in settings.get( "repositories" ):
        index = settings.get( "repositories" ).index( repository ) - 1
        for key in repository.keys():
            if os.path.expanduser( key ) == cwd:
                settings["repositories"][index][key]["remotes"] = remotes
    save_settings( settings )

def get_submodules():
    """Returns a list of all submodules """
    ignored_submodules = [ os.path.expanduser( module ) for module in settings.get( "ignore-submodules" ) ]
    try:
        submodules = find_submodules()
    except TypeError:
        warning( "No submodules are defined in the configuration file: \"" + config.file() + "\"" )
        return None
    for submodule in submodules:
        for ignored_submodule in ignored_submodules:
            if re.match( ignored_submodule, submodule ):
                submodules.remove( submodule )
    return submodules

def add_submodule( name, path, ignore_dirty = True ):
    """Add a submodule to the list of submodules in the config.yml file

    Arguments:
        name: Specify a name for the submodule
        path: The path to the specific submodule
        ignore_dirty: If the changes to the submodules should NOT be ignored, then set this to False
    """
    submodules = get_submodules()
    if not submodules:
        settings.get( "submodules" ).append( { name: path, "ignore_dirty": ignore_dirty } )
        return settings

def find_submodules( dir = os.path.expanduser( "~" ) ):
    """Search for submodules

    Arguments:
        dir: The directory from which the function searches for submodules
    """
    submodules = ( submodule for submodule in settings.get( "submodules" ))
    for dirpath, dirnames, filenames in os.walk( dir ):
        for file in filenames:
            if file == ".gitmodules":
                submodules.append( os.path.expanduser( os.path.join( dirpath, file ) ) )
    return submodules

def ignore_submodule( path_to_submodule ):
    """Ignore a specific path to a submodule which will be ignored by "G"

    Arguments:
        path_to_submodule: A path to a submodule which should be ignored by "G"
    """
    ignored_submodules = [ os.path.expanduser( module ) for module in settings.get( "ignore-submodules" ) ]
    if not path_to_submodule in ignored_submodules:
        ignored_submodules.append( os.expanduser( path_to_submodule ) )
    save_settings( settings )

def git( operator, operand ):
    """Start a git command as a subprocess

    Arguments:
        operator: The operator defines the git command, that needs to be executed.
        This argument must be one of the following: "push", "pull", "merge", "add", "reset"
        operand: Contains the files or branches, that need to be processed.
    """
    try:
        subprocess.call( [ "git", operator ] + operand )
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
| Push branch to a remote repository | git push origin master   | @master → @origin        |
| Merge branches                     | git merge feature-branch | @feature-branch > @master |
| Diff files                         | git diff file1 file 2    | ~ file1 file2             |
+------------------------------------+--------------------------+---------------------------+\
"""
    print( usage )

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
elif __name__ == "G":
    settings = get_settings()
