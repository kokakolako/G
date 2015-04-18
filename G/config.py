#!/bin/env python3
# Configuration

import os

def version():
    return "0.0.1"

def config_dir():
    config_dir = os.path.join( os.path.expanduser( "~" ), ".config", "G" )
    if not os.path.exists( config_dir ):
        os.makedirs ( config_dir, exists_ok = True )
    return config_dir

def config_file():
    config_file = os.path.join( os.path.expanduser( "~" ), ".config", "G", "config.yml" )
    if not os.path.isfile( config_file ):
        with open( config_file, "w" ) as file:
            file.close()
    return config_file

def history_file():
    history_file = os.path.join( os.path.expanduser( "~" ), ".config", "G", "history" )
    if not os.path.isfile( history_file ):
        if count_lines( history_file ) == settings.get( "history-length" ):
            with open( history_file, "w" ) as file:
                file.close()
    return history_file

def count_lines( file ):
    try:
        if os.path.isfile( file ):
            output = subprocess.check_output( [ "wc", "-l" ],
                    stdin = open( file, "r" ) )
            return int( output )
    except OSError:
        warning( "You need to have installed 'wc' to run 'G' proberly" )
        pass
    except FileNotFoundError:
        pass

