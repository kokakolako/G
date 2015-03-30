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

import os, re, sys, yaml

from helpers import *
from cli_colors import *

def main():

    args = get_user_input()
    settings = get_settings()

    if not args:
        usage()
    elif len( args ) == 1:
        arg = args[0]
        if arg == "@remotes":
            show_remotes()
        elif arg == "@submodules":
            show_submodules()
    else:
        try:
            operands = get_operands( args )
        except:
            operands = { "add": [], "reset": [], "merge": [], "push": [], "cd": [], "set": [] }
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
    length = len( args ) - 1
    operator = get_operator( args )
    for arg in args:
        index = args.index( arg )
        if index < length:
            if index >= 0:
                if index == 0:
                    operands = { "add": [], "reset": [], "merge": [], "push": [], "cd": [], "set": [] }
                if not get_operator( arg ):
                    operands.get( operator ).append( arg )
            elif index > 0:
                if arg == "+" or arg == "-" or arg == "~":
                    del args[0:index]
                    return get_operands( args )
        elif index == length:
            return operands.get( operator ).append( arg )

def get_submodules( settings = get_settings() ):
    """Returns a list of all submodules """
    submodules = settings.get( "submodules" )
    if not submodules:
        return False
    else:
        return submodules

def add_submodule( path, ignore_dirty = True ):
    """Add a submodule to the list of submodules in the config.yml file

    Arguments:
        path: The path of the submodule
        ignore_dirty: If the changes to the submodules should NOT be ignored, then set this to False
    """
    try:
        ignored_submodules = [ os.path.expanduser( module ) for module in settings.get( "ignore-submodules" ) ]
        if os.path.expanduser( path ) in ignored_submodules:
            error( "You want to add a ignored submodule" )
    except:
        pass
    if not settings.get( "submodules" ):
        settings["submodules"] = []
    submodules = settings.get( "submodules" )
    try:
        if not path in [ list( submodule.keys() )[0] for submodule in submodules ]:
            submodules.append( { path: { "ignore_dirty": ignore_dirty } } )
            save_settings( settings )
        else:
            settings["submodules"] = None
            warning( "You added the submodule with the path \"" + path + "\" already to G" )
    except TypeError:
        pass

def show_submodules():
    if get_submodules():
        print( fg.blue( "Submodules:" ) )
        for submodule in get_submodules():
            for path, values in submodule.items():
                print( "  - " + path )
    else:
        warning( "You have not added submodules to the config file \"" + config.file() + "\"" )

def find_submodules( dir = os.path.expanduser( "~" ) ):
    """Search for submodules

    Arguments:
        dir: The directory from which the function searches for submodules
    """
    ignored_submodules = settings.get( "ignore-submodules" )
    if get_submodules():
        submodules = [ submodule for submodule in settings.get( "submodules" ) ]
    for dirpath, dirnames, filenames in os.walk( dir ):
        for file in filenames:
            if file == ".gitmodules":
                submodules.append( os.path.expanduser( os.path.join( dirpath, file ) ) )
    for submodule in submodules:
        if submodule in ignored_submodules:
            submodules.remove( submodule )
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

def get_remotes( settings = get_settings() ):
    """Get all remotes, from the current repository (the current working directory)"""
    for repository in settings.get( "repositories" ):
        for path, values in repository.items():
            if os.path.expanduser( path ) == os.getcwd():
                return values.get( "remotes" )
            else:
                return False

def show_remotes():
    if get_remotes():
        print( fg.blue( "Remotes:" ) )
        for remote in get_remotes():
            for name, url in remote.items():
                print( "  - " + name + ": " + url )
    else:
        warning( "Your repository does not have any remotes, or you have not opened a repository" )

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
    repositories = settings.get( "repositories" )
    if not remotes:
        repositories.append( { cwd: { "remotes": [ { name: url }] } } )
    else:
        if not name in [ list( remote.keys() )[0] for remote in remotes ]:
            remotes.append( { name: url } )
    for repository in repositories:
        for path, values in repository.items():
            if os.path.expanduser( path ) == cwd:
                for name, url in remotes:
                        values["remotes"] = remotes
    save_settings( settings )

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
