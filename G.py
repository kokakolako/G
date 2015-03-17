#!/bin/env python3

import re, subprocess, sys, atexit, code, os, readline, yaml
from cli_colors import fg

data = { "add": [], "reset": [], "diff": [] }
files = []
branches = []

class GConsole( code.InteractiveConsole ):
    def __init__( self, locals = None, filename = "<console>" ):
        history_file = os.path.expanduser( "~/.config/G/history" )
        code.InteractiveConsole.__init__(self, locals, filename)
        self.init_history( history_file )
    def init_history( self, history_file ):
        readline.parse_and_bind( "tab: complete" )
        if hasattr( readline, "read_history_file" ):
            try:
                readline.read_history_file( history_file )
            except FileNotFoundError:
                pass
            atexit.register( self.save_history, history_file )
    def save_history( self, history_file ):
        readline.write_history_file( history_file )

def usage():
    usage = """
DESCRIPTION:

G is an interface to simplify the work with the git command line tool.

SYNTAX COMPARED TO GIT:

+------------------------------------+--------------------------+---------------------------+
| Task                               | Git syntax               | G Syntax                  |
+--------------------------------------+--------------------------+-------------------------+
| Add files to the index             | git add file1 file2      | + file1 file2             |
| Remove files from the index        | git reset file1 file2    | - file1 file2             |
| Push branch to a remote repository | git push origin master   | @master -> @origin        |
| Merge branches                     | git merge feature-branch | @feature-branch > @master |
+------------------------------------+--------------------------+---------------------------+
    """
    print(  usage )

def is_path( possible_path ):
    if re.match( "([\W~]*[\/\\\])+(\W*\/|\W*)|[\W~]*", possible_path ):
        return True
    else:
        return False

def is_branch( possible_branch ):
    if re.match( "\@\W*", possible_branch ):
        return True
    else:
        return False

def error( message ):
    print( message )
    sys.exit( 1 )

def git( cmd, files ):
    subprocess.call( [ "git", cmd ] + files )

def get_remotes():
    cwd = os.getcwd()
    settings = parse_yaml_config()
    for repository in settings:
        for key in repository.keys():
            if os.path.expanduser( key ) == os.path.expanduser( cwd ):
                    remotes = repository.get( key ).get( "remotes" )
                    return remotes

def set_remote( name, url ):
    settings = parse_yaml_config()
    cwd = os.getcwd()
    remotes = get_remotes()
    if not remotes:
        settings.append( { cwd: { "remotes": [ { name: url }] } } )
    else:
        remotes.append( { name: url } )

    for repository in settings:
        index = settings.index( repository ) - 1
        for key in repository.keys():
            if os.path.expanduser( key ) == cwd:
                settings[index][key]["remotes"] = remotes

    file = os.path.expanduser( "~/.config/G/config.yml" )
    if os.path.exists( file ):
        with open( file , "w" ) as yaml_config:
            yaml_config.write( yaml.dump( settings, default_flow_style = False ) )

def get_operator( args ):
    for arg in args:
        index = args.index( arg )
        if index == 0:
            if arg == "+":
                return "add"
            elif arg == "-":
                return "reset"
            elif arg == "~":
                return "diff"
        if arg == "=":
            return "set"
        elif arg == "->":
            return "push"
        elif arg == ">":
            return "merge"

def parse_args( operator, args ):

    global data
    global branches
    global files

    length = len( args ) - 1
    operator = get_operator( args )

    for arg in args:
        index = args.index( arg )
        if index < length:
            if index >= 0:
                if is_branch( arg ):
                    branches.append( arg[1:] )
                if is_path( arg ):
                    files.append( arg )
            elif index > 0:
                if arg == "+":
                    del args[0:index]
                    parse_args( args )
                elif arg == "-":
                    del args[0:index]
                    parse_args( args )
                elif arg == "~":
                    del args[0:index]
                    parse_args( args )
                elif is_path( arg ):
                    data[operator].append( arg )
        elif index == length:
            if operator == "push" or operator == "merge":
                branches.append( arg[1:] )
            elif is_path( arg ):
                data[operator].append( arg )

def parse_yaml_config():
    file = os.path.expanduser( "~/.config/G/config.yml" )
    if os.path.exists( file ):
        with open( file , "r" ) as yaml_config:
            settings = yaml.load( yaml_config )
    return settings

def main():

    if len( sys.argv ) == 1:
        console = GConsole()
        user_input = console.raw_input( "G " + fg.red( ">" ) + " " )
    else:
        user_input = sys.argv[1]

    args = user_input.split()
    operator = get_operator( args )

    if not args:
        usage()
    else:
        parse_args( operator, args )

    if not data.get( "add" ) == []:
        git( "add", data.get( "add" ) )
    elif not data.get( "reset" ) == []:
        git( "reset", data.get( "reset" ) )
    elif not data.get( "diff" ) == []:
        git( "diff", data.get( "diff" ) )

    if operator == "push":
        if len( branches ) == 1:
            git( "push", [ "origin", branches[0] ] )
        elif len( branches ) == 2:
            git( "push", [ branches[1], branches[0] ] )
    elif operator == "merge":
        if len( branches ) == 1:
            git( "merge", branches )
        elif len( branches ) == 2:
            git( "checkout",  [ branches[0] ]  )
            git( "merge", branches[1] )

if __name__ == "__main__":
    try:
        main()
    except BaseException:
        sys.exit(1)
