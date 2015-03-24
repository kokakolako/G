import os, re, subprocess

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

def is_path( possible_path ):
    """Returns True when the possible_branch is a valid path

    Arguments:
        possible_path: A string which should be checked if it is a valid path
    """
    if re.match( "(([A-Z]\:\\\)|(\~\/)|(\W*))((\W*\/)|(\W*\\\)(\W*))*", possible_path ):
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
