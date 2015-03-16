#!/bin/env python3

import re, subprocess, sys

data = { "add": [], "reset": [] }
branches = []

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
    print( usage )

def is_path( possiblePath ):
    if re.match( "([\W~]*[\/\\\])+(\W*\/|\W*)|[\W~]*", possiblePath ):
        return True
    else:
        return False

def is_branch( possibleBranch ):
    if re.match( "\@\W*", possibleBranch ):
        return True
    else:
        return False

def git( cmd, files ):
    subprocess.call( [ "git", cmd ] + files )

def get_operator( args ):
    for arg in args:
        index = args.index( arg )
        if index == 0:
            if arg == "+":
                return "add"
            elif arg == "-":
                return "reset"
        elif index >= 0:
            if arg == "=":
                return "set"
            if arg == "->":
                return "push"
            elif arg == ">":
                return "merge"

def parse_args( operator, args ):

    global data
    global branches

    length = len( args ) - 1
    operator = get_operator( args )

    for arg in args:
        index = args.index( arg )
        if index < length:
            if index >= 0:
                if is_branch( arg ) and not operator  == "set":
                    branches.append( arg[1:] )
            elif index > 0:
                if arg == "+":
                    del args[0:index]
                    parse_args( args )
                elif arg == "-":
                    del args[0:index]
                    parse_args( args )
                elif is_path( arg ):
                    data[operator].append( arg )
        elif index == length:
            if operator == "push" or operator == "merge":
                branches.append( arg[1:] )
            elif is_path( arg ):
                data[operator].append( arg )

def main():

    if len( sys.argv ) == 1:
        user_input = input( "G: " )
    else:
        user_input = sys.argv[1]

    args = user_input.split()
    operator = get_operator( args )

    if not args:
        usage()
    else:
        parse_args( operator, args )

    if data.get( "add" ) != []:
        git( "add", data.get( "add" ) )
    elif data.get( "reset" ) != []:
        git( "reset", data.get( "reset" ) )

    if operator == "push":
        if len( branches ) == 1:
            git( "push", [ "origin", branches[0] ] )
        elif len( branches ) == 2:
            git( "push", [ branches[1], branches[0] ] )
    elif operator == "merge":
        if len( branches ) == 1:
            git( "merge", [ branches[0] ] )
        elif len( branches ) == 2:
            git( "checkout",  [ branches[0] ]  )
            git( "merge", branches[1] )

if __name__ == "__main__":
    try:
        main()
    except BaseException:
        sys.exit(1)
