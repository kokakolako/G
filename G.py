#!/bin/env python3

import re, subprocess, sys
from os.path import basename

try:
    userInput = input( "G: " )
except BaseException:
    sys.exit( 1 )

args = userInput.split()
data = { "add": [], "reset": [] }
operator = ""
branches = []

# try:
#     subprocess.check_call( "git symbolic-ref HEAD", shell=True )
#     currentBranch = basename(  )

def showUsage():
    usage = """
DESCRIPTION:

G is an interface to simplify the work with the git command line tool.

SYNTAX:

- Add files to the index:
    Git standard syntax:                G Syntax:
        git add file1 file2                 + file1 file2

- Remove files from the index:
    Git standard syntax:                G Syntax:
        git reset file1 file2               - file1 file2

- Push branches to a remote repository:
    Git Standard Syntax:                G Syntax:
        git push origin master              @master -> @origin

- Merge branches:
    Git standard syntax:                G Syntax:
        git merge feature-branch            @feature-branch > @master
    """
    print( usage )

def isPath( possiblePath ):
    if re.match( "([\W~]*[\/\\\])+(\W*\/|\W*)|[\W~]*", possiblePath ):
        return True
    else:
        return False

def isBranch( possibleBranch ):
    if re.match( "\@\W*", possibleBranch ):
        return True
    else:
        return False

def git( cmd, files ):
    try:
        subprocess.call( [ "git", cmd ] + files )
    except BaseException:
        sys.exit(1)

def parseArgs( args ):

    global data
    global operator
    global branches

    length = len( args ) - 1

    for arg in args:
        index = args.index( arg )
        if index < length:
            if index == 0:
                if arg == "+":
                    operator = "add"
                elif arg == "-":
                    operator = "reset"
            elif index >= 0:
                if arg == "->":
                    operator = "push"
                elif arg == ">":
                    operator = "merge"
                elif isBranch( arg ):
                    branches.append( arg[1:] )
            elif index > 0:
                if arg == "+":
                    del args[0:index]
                    parseArgs( args )
                elif arg == "-":
                    del args[0:index]
                    parseArgs( args )
                elif isPath( arg ):
                    data[operator].append( arg )
        elif index == length:
            if operator == "push":
                branches.append( arg[1:] )
            elif operator == "merge":
                branches.append( arg[1:] )
            elif isPath( arg ):
                data[operator].append( arg )

if not args:
    showUsage()
else:
    parseArgs( args )

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
