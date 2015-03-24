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
