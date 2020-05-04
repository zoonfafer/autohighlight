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
from ah.utils import Set


class Context(object):
    """A context is a set of symbols to the left, the symbol we're matching,
    and a set of symbols to the right. There may be more than one context per
    symbol, not all of which will be stored in one context."""

    def __init__(self, leftSymbols, middleSymbol, rightSymbols):
        assert (type(leftSymbols).__name__ == 'set')
        assert (type(rightSymbols).__name__ == 'set')
        self.leftSymbols = leftSymbols
        self.rightSymbols = rightSymbols
        self.middleSymbol = middleSymbol

    def __str__(self):
        return "#C<%s, %s, %s>" % (self.leftSymbols, self.middleSymbol,
                                   self.rightSymbols)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.leftSymbols != other.leftSymbols:
            return False
        if self.rightSymbols != other.rightSymbols:
            return False
        if self.middleSymbol != other.middleSymbol:
            return False
        return True

    def getLeftRegexes(self):
        """Returns a set of regexes that matches the right hand side of the expansion of the left symbols"""
        regexes = Set()
        for symbol in self.leftSymbols:
            regexes.update(symbol.getRightRegexes())
        return regexes

    def getMiddleRegexes(self):
        """Returns the set of regexes that matches the symbol we are coloring"""
        return self.middleSymbol.get_terminal_equivalent_regexes()

    def getRightRegexes(self):
        """Returns a set of regexes that matches the left hand side of the expansion of the right symbols"""
        regexes = Set()
        for symbol in self.rightSymbols:
            regexes.update(symbol.getLeftRegexes())
        return regexes
