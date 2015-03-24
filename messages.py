import sys
from cli_colors import *

def error( message ):
    """Prints an error message, stops "G" and raises error code 1

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.red( message ) )
    sys.exit( 1 )

def warning( message ):
    """Prints an warning

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.yellow( message ) )

def success( message ):
    """Prints an succes message

    Arguments:
        message: The message which should be displayed to the user
    """
    print( fg.green( message ) )
