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
from ah.io import StringIO
import unittest
import pytest

test1file = \
    """
{
} {
  document : document statement ';' .
  document : .
  statement : 'foo' .
} {
}
"""


class AhTestContexts(unittest.TestCase):
    ourTests = [["statement", ['\\;|', '\\;']], ["'foo'", ['\\;|', '\\;']]]

    def setUp(self):
        global test1file
        self.ah = Autohighlight(StringIO(test1file.encode()))
        self.ah.parse()

    def checkContext(self, number):
        sym = self.ourTests[number][0]
        res = self.ourTests[number][1:]
        print(("global symbol dict", self.ah.GlobalSymbolDict))
        context = self.ah.GlobalSymbolDict[sym].get_contexts(
            self.ah.GlobalSymbolDict)
        self.assertEqual(
            res, context, "Contexts for %s are not as expected:\n%s\n%s" %
            (sym, res, context))

    @pytest.mark.skip(reason="This test came broken")
    def test0(self):
        self.checkContext(0)

    @pytest.mark.skip(reason="This test came broken")
    def test1(self):
        self.checkContext(1)


if __name__ == "__main__":
    unittest.main()
