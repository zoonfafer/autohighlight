#!/usr/bin/python
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

from __future__ import print_function
from ah.autohighlight import Autohighlight
import hotshot
import hotshot.stats
from ah.memoize import memoize
import sys
import getopt
import re
from ah.symbol import Symbol
from ah.vimoutputter import VimOutputter
from ah.EmacsOutputter import EmacsOutputter
from ah.utils import Set


def usage():
    print("""Usage: python ah.py [OPTION]... [FILE]
Generates the specified syntax highlighting files from the given input FILE.

Options:
  -h, --help  Prints this help
      --vim   Generates a vim syntax highlighting file
      --emacs Generates an emacs font locking file
      --error-checking Highlight all symbols not currently being colored as errors (currently works for vim only)
""")


def strip_filename(filename):
    return re.sub(r'\.ah$', '', filename)


def generate_vim(filename, error_checking):
    output_filename = strip_filename(filename) + '.vim'
    print('Generating vim file %s\n' % output_filename)
    ah = Autohighlight(filename)
    ah.parse()
    outputter = VimOutputter(error_checking)
    open(output_filename, 'w').write(ah.output(outputter))


def generate_emacs(filename):
    import os.path
    output_filename = strip_filename(filename) + '.el'
    ah = Autohighlight(filename)
    ah.parse()
    outputter = EmacsOutputter(os.path.basename(strip_filename(filename)))
    open(output_filename, 'w').write(ah.output(outputter))
    print("Wrote %s\n" % output_filename)


def main_interface():
    profile = False
    help, vim, emacs, error_checking = False, False, False, False
    opts, args = getopt.getopt(
        sys.argv[1:-1], "h",
        ["help", "vim", "emacs", "error-checking", "memoize", "profile"])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help = True
        elif opt == '--vim':
            vim = True
        elif opt == '--memoize':
            memoize(Symbol.get_terminal_equivalent_regexes)
            memoize(Symbol.getRightRegexes)
            memoize(Symbol.getLeftRegexes)
            memoize(Symbol.get_contexts)
        elif opt == '--profile':
            profile = True
        elif opt == '--emacs':
            emacs = True
        elif opt == '--error-checking':
            error_checking = True

    filename = sys.argv[-1]

    def do_it():
        if (help):
            usage()
            sys.exit()

        if (vim):
            generate_vim(filename, error_checking)

        if (emacs):
            generate_emacs(filename)

        if (not emacs and not vim):
            usage()
            sys.exit(2)

    if profile:
        fn = "sample%s.prof" % "".join(sys.argv[1:-1])
        prof = hotshot.Profile(fn)
        prof.runcall(do_it)
        prof.close()
        stats = hotshot.stats.load(fn)
        stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats()
    else:
        do_it()


if __name__ == "__main__":
    main_interface()
