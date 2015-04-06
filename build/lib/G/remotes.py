#!/bin/env python3
# Remotes

import os

from G.cli_colors import fg
from G.settings import get_settings

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

