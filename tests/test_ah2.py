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
        self.ah = Autohighlight(StringIO(test1file))
        self.ah.parse()

    def checkContext(self, number):
        sym = self.ourTests[number][0]
        res = self.ourTests[number][1:]
        print("global symbol dict", self.ah.GlobalSymbolDict)
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
