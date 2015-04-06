#!/bin/env python3
# Settings

import yaml

from G.config import config_file

def get_settings():
    """Returns a dictionary which contains all settings from the config.yml file"""
    with open( config_file() , "r" ) as yaml_config:
        return yaml.load( yaml_config )

def save_settings( new_settings ):
    """Store settings via pyYAML in the config.config_file

    __Warning__:
        This function can overwrite the config.yml file, when values are not **appended** to the
        settings dictionary

    Arguments:
        new_settings: Settings that should be written to the config.yml file
    """
    with open( config_file() , "w" ) as yaml_config:
        yaml_config.write( yaml.dump( new_settings, default_flow_style = False ) )
