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
from builtins import object


def memoize(fun):
    """A clever way to reduce the runtime on the Mystery HELL tests by
    half"""
    dictName = "__" + fun.__name__ + "_memoizer"

    def func_wrap(self, *rest):
        if rest not in self.__dict__[dictName]:
            self.__dict__[dictName][rest] = fun(self, *rest)
        return self.__dict__[dictName][rest]

    if '__init__' not in fun.__self__.__class__.__dict__:
        fun.__self__.__class__.__dict__['__init__'] = lambda *rest: None
    oldInit = fun.__self__.__class__.__dict__['__init__']

    def init_wrap(self, *rest):
        self.__dict__[dictName] = {}
        # print "Initializing %s" % dictName
        return oldInit(self, *rest)

    fun.__self__.__class__.__dict__['__init__'] = init_wrap
    fun.__self__.__class__.__dict__[fun.__name__] = func_wrap


if __name__ == "__main__":

    class testClass(object):
        def foo(self, string):
            print(string)
            return string

    memoize(testClass.foo)
    obj = testClass()
    print("->%s" % obj.foo("Hello"))
    print("->%s" % obj.foo("Hello"))
    print("->%s" % obj.foo("Gato"))
    print("->%s" % obj.foo("Gato"))
