#!/bin/env python3
# Configuration

import os

def version():
    return "0.0.1"

def config_dir():
    dir = os.path.join( os.path.expanduser( "~" ), ".config", "G" )
    if not os.path.exists( dir ):
        os.makedirs ( dir, exists_ok = True )
    return dir

def config_file():
    config = os.path.join( os.path.expanduser( "~" ), ".config", "G", "config.yml" )
    if not os.path.isfile( config ):
        with open( config, "w" ) as file:
            file.close()
    return config

def history_file():
    history = os.path.join( os.path.expanduser( "~" ), ".config", "G", "history" )
    if not os.path.isfile( history ):
        if count_lines( history ) == settings.get( "history-length" ):
            with open( history, "w" ) as file:
                file.close()
    return history
