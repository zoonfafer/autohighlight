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
from __future__ import unicode_literals
import unittest
from ah.io import StringIO
from ah.tokenizer import *


class TokenizerTestCase(unittest.TestCase):
    def tokenList(self, string):
        try:
            tokenizer = Tokenizer(StringIO(string.encode()))
            return [token for token in tokenizer]
        except TokenizerException as e:
            return e

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testTokenizeString(self):
        """Checks for correct basic string tokenization"""
        self.assertEqual([Token(1, 0, "'abcd'")], self.tokenList("'abcd'"))

    def testTokenizeEscapedString(self):
        tl = self.tokenList("'abc\\'de'")
        self.assertEqual([Token(1, 0, "'abc\\'de'")], tl)

    def testTokenizeUnfinishedString(self):
        """Is an error signalled for unfinished strings?"""
        tl = self.tokenList("'abc")
        self.assertEqual("EofInString", tl.__class__.__name__)

    def testFloatsParsedAsTwoIntegers(self):
        """There are no floats, so things that look like floats should
        parse like integers"""
        tl = self.tokenList("5.6")
        self.assertEqual(
            [Token(1, 0, "5"),
             Token(1, 1, "."),
             Token(1, 2, "6")], tl)

    def testIntegerFollowedByPeriod(self):
        """5. => "5" ".": This seems to cause trouble"""
        tl = self.tokenList("5.")
        self.assertEqual([Token(1, 0, "5"), Token(1, 1, ".")], tl)

    def testNewlineDelimitedIntegers(self):
        """5\n6 => "5" "6": Another edge case"""
        tl = self.tokenList("5\n6")
        self.assertEqual([Token(1, 0, "5"), Token(2, 0, "6")], tl)

    def testIntegerFollowedByIdentifier(self):
        """5a => "5" "a": Another state transition edge case"""
        tl = self.tokenList("5a")
        self.assertEqual([Token(1, 0, "5"), Token(1, 1, "a")], tl)

    def testIdFollowedByInteger(self):
        """a. => "a" ".": Edge case similar to previous"""
        tl = self.tokenList("a.")
        self.assertEqual([Token(1, 0, "a"), Token(1, 1, ".")], tl)

    def testTokenizeMashedIdAndRegex(self):
        """id$foo => "id" "foo" """
        tl = self.tokenList("id$foo")
        self.assertEqual([Token(1, 0, "id"), Token(1, 2, "$foo")], tl)

    def testTokenizeMashedIdsAndPunct(self):
        """This should return 5 symbols"""
        tl = self.tokenList("id.def.foo")
        want = [
            Token(1, 0, "id"),
            Token(1, 2, "."),
            Token(1, 3, "def"),
            Token(1, 6, "."),
            Token(1, 7, "foo")
        ]
        self.assertEqual(want, tl)

    def testInteger(self):
        tl = self.tokenList("12")
        self.assertEqual([Token(1, 0, "12")], tl)

    def testPunctuationAfterWhitespace(self):
        tl = self.tokenList("\n.")[0]
        self.assertEqual(2, tl.line)
        self.assertEqual(0, tl.col)

    def testValidStartTokens(self):
        valid = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        valid += "{}[].:0123456789"
        for inichar in valid:
            self.assertEqual([Token(1, 0, inichar)], self.tokenList(inichar))

    def testInvalidStartTokens(self):
        invalid = r"-_`~!@#%^&*()+=\|?<>,"
        for badchar in invalid:
            tl = self.tokenList(badchar)
            self.assertEqual("UnexpectedCharacter", tl.__class__.__name__)


if __name__ == "__main__":
    unittest.main()
