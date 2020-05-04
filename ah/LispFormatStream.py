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
from future import standard_library
standard_library.install_aliases()
from io import StringIO

class LispFormatStream (StringIO):
    def __init__(self): self.buffer, self.indent = StringIO(), [0]
    def getvalue(self): return self.buffer.getvalue()
    def prin(self, str):
        col = self.indent[-1]
        #self.buffer.write(" "*col)
        for char in str:
            self.buffer.write(char)
            if char == "(":
                self.indent += [col]
            elif char == ")":
                self.indent = self.indent
            col += 1
        self.buffer.write("\n")

if __name__ == "__main__":
    import unittest
    class LispFormatStreamTest(unittest.TestCase):
        def setUp(self):
            self.lfs = LispFormatStream()
        def testEasy(self):
            self.lfs.prin("(plain)")
            self.lfs.prin("(plain)")
            self.assertEqual("(plain)\n(plain)\n", self.lfs.getvalue())
        def testBreakOpen(self):
            self.lfs.prin("(plain")
            self.lfs.prin("(plain))")
            self.assertEqual("(plain\n  (plain)\n", self.lfs.getvalue())
        def testBreakOpenSecond(self):
            self.lfs.prin("(plain second")
            self.lfs.prin("foo)")
            self.assertEqual("(plain second\n       foo)\n", self.lfs.getvalue())
        def testBreakDoubleOpen(self):
            self.lfs.prin("'((foo bar)")
            self.lfs.prin("(foo bar))")
            self.assertEqual("'((foo bar)\n  (foo bar))\n", self.lfs.getvalue())
    unittest.main()
