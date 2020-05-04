from __future__ import unicode_literals
from ah.utils import Set
from ah.autohighlight import Autohighlight
from ah.io import StringIO
from ah.context import Context
import unittest
from ah.utils import Set
import re

test1file = \
    """
{
} {
    t: 't' .
    s: '(' x ')' .
    x: x t ',' .
    x: .
} {
}
"""


class AhTestContexts(unittest.TestCase):
    def setUp(self):
        global test1file
        self.ah = Autohighlight(StringIO(test1file.encode()))
        self.ah.parse()

    def testGetContextsForT(self):
        gsd = self.ah.GlobalSymbolDict
        expected = [Context(Set([gsd["x"]]), gsd['t'], Set([gsd["','"]]))]
        contexts = gsd['t'].get_contexts()
        self.assertEqual(
            contexts, expected,
            "Contexts for %s are not as expected:\n%s\n%s" %
            ('t', contexts, expected))

    def testGetRegexesForT(self):
        gsd = self.ah.GlobalSymbolDict
        # print("gsd: %s" % gsd)
        #expected = [Context(Set([gsd["x"]]),gsd['t'],Set([gsd["','"]])) ]
        # left_expected = Set('\\,', '\\(')
        # right_expected = Set('\\,')
        left_expected = Set(list(map(lambda x: re.escape(x), [',', '('])))
        right_expected = Set(list(map(lambda x: re.escape(x), [','])))
        for sym in list(self.ah.GlobalSymbolDict.values()):
            sym.GlobalSymbolDict = gsd
        # print("gsd['t']: %s" % gsd['t'])
        contexts = gsd['t'].get_contexts()
        # print("context : %s" % contexts)
        # print("context0: %s" % contexts[0])
        # print("context0.getLeft: %s" % contexts[0].getLeftRegexes())
        left_regex = contexts[0].getLeftRegexes()
        self.assertEqual(
            left_regex, left_expected,
            "Left regex for %s is not as left_expected:\n%s\n%s" %
            ('t', left_regex, left_expected))
        right_regex = contexts[0].getRightRegexes()
        self.assertEqual(
            right_regex, right_expected,
            "Right regex for %s is not as expected:\n%s\n%s" %
            ('t', right_regex, right_expected))
        self.assertEqual(contexts[0].getMiddleRegexes(), Set('t'))

    def testGetContextsForX(self):
        gsd = self.ah.GlobalSymbolDict
        symbol = gsd['x']
        expected = [
            Context(Set([gsd["'('"]]), gsd['x'], Set([gsd["')'"]])),
            Context(Set([gsd["'('"]]), gsd['x'], Set([gsd["t"]]))
        ]
        contexts = symbol.get_contexts()
        self.assertEqual(
            contexts, expected,
            "Contexts for %s are not as expected:\n%s\n%s" %
            (symbol.defining_token.text, contexts, expected))

    def testGetContextsForProductionForX(self):
        gsd = self.ah.GlobalSymbolDict
        symbol = gsd['x']
        symbol.GlobalSymbolDict = gsd
        expected = [Context(Set([gsd["'('"]]), gsd['x'], Set([gsd["t"]]))]
        contexts = symbol.get_contexts_for_production(symbol.productions[0])
        self.assertEqual(
            contexts, expected,
            "Contexts for production 0 for %s are not as expected:\n%s\n%s" %
            (symbol.defining_token.text, contexts, expected))


if __name__ == "__main__":
    unittest.main()
