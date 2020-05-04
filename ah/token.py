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
import re
import pprint


class Token(object):
    """A token contains a bit of text and the text coordinate where it
    came from."""
    text = ""
    line = 0
    col = 0

    def __init__(self, line, col, text):
        self.col = col
        self.line = line
        self.text = text

    def __str__(self):
        pp = pprint.PrettyPrinter()
        a = self.__dict__.copy()
        a['a-type-tag'] = "Token"
        return pp.pformat(a)

    def __repr__(self):
        return str(self)

    def must_be(self, str):
        if self.text != str:
            raise Exception("%d:%d: Expected '%s', got '%s'." %
                            (self.line, self.col, str, self.text))

    def must_match(self, rex, expected):
        if not re.compile(rex).match(self.text):
            raise Exception("%d:%d: Expected a %s, got '%s' instead." %
                            (self.line, self.col, expected, self.text))

    def __eq__(self, other):
        if other.__class__.__name__ == 'Token' and \
           other.col == self.col and \
           other.line == self.line and \
           other.text == self.text:
            return True
        return False

    def assert_symbol_name(self):
        if self.text[0] == "'":
            return True
        if not re.compile('^[a-zA-Z0-9_]+$').match(self.text):
            raise Exception("%d:%d: Expected a symbol, got %s." %
                            (self.line, self.col, self.text))
