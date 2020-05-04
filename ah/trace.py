# autohighlighter - Automatically generate VIM and emacs coloring from BNF grammars
# Copyright (C) 2006 Scotty Allen, Scott Williams
# Copyright (C) 2020 Jeffrey Lau
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
from builtins import str
from builtins import range
indent = 0

from sys import stdout
import sys

def trprint(*args):
    global indent
    sys.stdout.write(indent * "   ")
    sys.stdout.write(*args)
    sys.stdout.write("\n")

def trenter(name):
    global indent
    trprint("ENTERING %s:" % name)
    indent += 1

def trleave(name):
    global indent
    indent -= 1
    trprint("LEAVING %s." % name)

def trace(func, printArgs):
    def inner(*args):
        global indent

        displayArgsString = '...'
        if printArgs:
            if type(printArgs).__name__ == 'list':
                displayArgs = []
                for i in range(len(args)):
                    if i in printArgs:
                        displayArgs += [str(args[i])]
                    else:
                        displayArgs += ['...']
                displayArgsString = ', '.join(displayArgs)
            else:
                displayArgsString = ', '.join( [ str(arg) for arg in args[:printArgs]] )

        trenter( "%s(%s)" % (func.__name__, displayArgsString) )
        rt = func(*args)
        trleave( "%s(%s) = %s" % (func.__name__, displayArgsString, rt) )

        return rt
    return inner

def funtrace(func, printArgs):
    """FUNTrace is one of the niftiest little utilities we wrote"""
    func.__self__.__class__.__dict__[func.__name__] = trace(func, printArgs)
    return func


