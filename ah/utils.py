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
def Set(*rest):
    """Using python's built-in "set" function is dangerous!! if you
    pass it a string on accident, it produces a set of all the
    characters in the string, instead of producing a set containing a
    string."""
    if len(rest) == 1 and type(rest[0]).__name__ == 'list':
        return set(rest[0])
    return set(rest)
