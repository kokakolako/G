#!/bin/env python3
# Submodules

import os, threading

from settings import get_settings, save_settings
from cli_colors import fg
from helpers import git

def get_submodules( settings = get_settings() ):
    """Returns a list of all submodules """
    submodules = settings.get( "submodules" )
    if not submodules:
        return False
    else:
        return submodules

def add_submodule( path, ignore_dirty = True, verbose = False, settings = get_settings() ):
    """Add a submodule to the list of submodules in the config.yml file

    Arguments:
        path: The path of the submodule
        ignore_dirty: If the changes to the submodules should NOT be ignored, then set this to False
        verbose: Don't show error messages, when this value is set to True.
    """
    try:
        ignored_submodules = [ os.path.expanduser( module ) for module in settings.get( "ignore-submodules" ) ]
        if os.path.expanduser( path ) in ignored_submodules:
            if not verbose:
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
            if not verbose:
                warning( "You added the submodule with the path \"" + path + "\" already to G" )
    except TypeError:
        pass

def show_submodules():
    if get_submodules():
        print( fg.green( "Submodules:" ) )
        for submodule in get_submodules():
            for path, values in submodule.items():
                print( "  - " + path )
    else:
        warning( "You have not added submodules to the config.config_file \"" + config.file() + "\"" )

def find_submodules( dir = os.path.expanduser( "~" ), settings = get_settings() ):
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
    for submodule in submodules:
        add_submodule( submodule, verbose = True )
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

def update_submodules( submodules = get_settings().get( "submodules" ) ):
    for submodule in submodules:
        path_to_submodule = os.path.dirname( list( submodule.keys() )[0] )
        os.chdir( path_to_submodule )
        git( "submodule", "foreach git pull origin master" )
