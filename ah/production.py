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
from builtins import object
class Production(object):
    """Represents a rule in the CON section of the input file."""
    def __init__(self,lhs,elements):
        self.lhs = lhs
        self.elements = elements

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return "#P<%s: %s>" % (self.lhs.defining_token.text, ' '.join([str(element.defining_token.text) for element in self.elements]))

    def __repr__(self):
        return str(self)

    def __eq__(self,other):
        if self.elements != other.elements:
            return False
        if self.lhs != other.lhs:
            return False
        return True
