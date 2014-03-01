#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Applications, Classes
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

TESTLIST1 = ['one', 'two', 'three']
TESTLIST2 = ['red', 'green', '~two', '~three']
GOALLIST = ['one', 'red', 'green']

#TODO: mock out the underlying list

class TestApplications(unittest.TestCase):

    def test_inheritance(self):
        a = Applications()
        self.assertIsInstance(a, Classes)

    def test_constructor_negate(self):
        a = Applications(TESTLIST1 + TESTLIST2)
        self.assertSequenceEqual(a, GOALLIST)

    def test_merge_unique_negate_list(self):
        a = Applications(TESTLIST1)
        a.merge_unique(TESTLIST2)
        self.assertSequenceEqual(a, GOALLIST)

    def test_merge_unique_negate_instance(self):
        a = Applications(TESTLIST1)
        a.merge_unique(Applications(TESTLIST2))
        self.assertSequenceEqual(a, GOALLIST)

    def test_append_if_new_negate(self):
        a = Applications(TESTLIST1)
        a.append_if_new(TESTLIST2[2])
        self.assertSequenceEqual(a, TESTLIST1[::2])

    def test_repr_empty(self):
        negater = '%%'
        a = Applications(negation_prefix=negater)
        self.assertEqual('%r' % a, "%s(%r, '%s')" % (a.__class__.__name__, [], negater))

    def test_repr_contents(self):
        negater = '%%'
        a = Applications(TESTLIST1, negation_prefix=negater)
        self.assertEqual('%r' % a, "%s(%r, '%s')" % (a.__class__.__name__, TESTLIST1, negater))

    def test_repr_negations(self):
        negater = '~'
        a = Applications(TESTLIST2, negation_prefix=negater)
        self.assertEqual('%r' % a, "%s(%r, '%s')" % (a.__class__.__name__, TESTLIST2, negater))

    def test_repr_negations_interspersed(self):
        l = ['a', '~b', 'a', '~d']
        a = Applications(l)
        is_negation = lambda x: x.startswith(a.negation_prefix)
        GOAL = filter(lambda x: not is_negation(x), set(l)) + filter(is_negation, l)
        self.assertEqual('%r' % a, "%s(%r, '~')" % (a.__class__.__name__, GOAL))

if __name__ == '__main__':
    unittest.main()
