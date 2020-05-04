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
from builtins import object
class Outputter(object):
    """An abstract class defining the interface to the outputter
    classes."""
    def appendColorDefinition(self, color):
        raise NotImplemented()

    def appendLiteral(self, color, literal):
        raise NotImplemented()

    def appendMapping(self, color, contexts): # contexts: List<Context>
        raise NotImplemented()

    def getBuffer(self):
        raise NotImplemented()
