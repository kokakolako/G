import os

from G import *

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
        if not name in [ list( remote.keys() )[0] for remote in remotes ]:
            remotes.append( { name: url } )
    for repository in settings.get( "repositories" ):
        index = settings.get( "repositories" ).index( repository ) - 1
        for key in repository.keys():
            if os.path.expanduser( key ) == cwd:
                settings["repositories"][index][key]["remotes"] = remotes
    save_settings( settings )
