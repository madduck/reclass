#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Classes
from reclass.datatypes.classes import INVALID_CHARACTERS_FOR_CLASSNAMES
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock
from reclass.errors import InvalidClassnameError

TESTLIST1 = ['one', 'two', 'three']
TESTLIST2 = ['red', 'green', 'blue']

#TODO: mock out the underlying list

class TestClasses(unittest.TestCase):

    def test_len_empty(self):
        with mock.patch.object(Classes, 'merge_unique') as m:
            c = Classes()
            self.assertEqual(len(c), 0)
            self.assertFalse(m.called)

    def test_constructor(self):
        with mock.patch.object(Classes, 'merge_unique') as m:
            c = Classes(TESTLIST1)
            m.assert_called_once_with(TESTLIST1)

    def test_equality_list_empty(self):
        self.assertEqual(Classes(), [])

    def test_equality_list(self):
        self.assertEqual(Classes(TESTLIST1), TESTLIST1)

    def test_equality_instance_empty(self):
        self.assertEqual(Classes(), Classes())

    def test_equality_instance(self):
        self.assertEqual(Classes(TESTLIST1), Classes(TESTLIST1))

    def test_inequality(self):
        self.assertNotEqual(Classes(TESTLIST1), Classes(TESTLIST2))

    def test_construct_duplicates(self):
        c = Classes(TESTLIST1 + TESTLIST1)
        self.assertSequenceEqual(c, TESTLIST1)

    def test_append_if_new(self):
        c = Classes()
        c.append_if_new(TESTLIST1[0])
        self.assertEqual(len(c), 1)
        self.assertSequenceEqual(c, TESTLIST1[:1])

    def test_append_if_new_duplicate(self):
        c = Classes(TESTLIST1)
        c.append_if_new(TESTLIST1[0])
        self.assertEqual(len(c), len(TESTLIST1))
        self.assertSequenceEqual(c, TESTLIST1)

    def test_append_if_new_nonstring(self):
        c = Classes()
        with self.assertRaises(TypeError):
            c.append_if_new(0)

    def test_append_invalid_characters(self):
        c = Classes()
        invalid_name = ' '.join(('foo', 'bar'))
        with self.assertRaises(InvalidClassnameError):
            c.append_if_new(invalid_name)

    def test_merge_unique(self):
        c = Classes(TESTLIST1)
        c.merge_unique(TESTLIST2)
        self.assertSequenceEqual(c, TESTLIST1 + TESTLIST2)

    def test_merge_unique_duplicate1_list(self):
        c = Classes(TESTLIST1)
        c.merge_unique(TESTLIST1)
        self.assertSequenceEqual(c, TESTLIST1)

    def test_merge_unique_duplicate1_instance(self):
        c = Classes(TESTLIST1)
        c.merge_unique(Classes(TESTLIST1))
        self.assertSequenceEqual(c, TESTLIST1)

    def test_merge_unique_duplicate2_list(self):
        c = Classes(TESTLIST1)
        c.merge_unique(TESTLIST2 + TESTLIST2)
        self.assertSequenceEqual(c, TESTLIST1 + TESTLIST2)

    def test_merge_unique_duplicate2_instance(self):
        c = Classes(TESTLIST1)
        c.merge_unique(Classes(TESTLIST2 + TESTLIST2))
        self.assertSequenceEqual(c, TESTLIST1 + TESTLIST2)

    def test_merge_unique_nonstring(self):
        c = Classes()
        with self.assertRaises(TypeError):
            c.merge_unique([0,1,2])

    def test_repr_empty(self):
        c = Classes()
        self.assertEqual('%r' % c, '%s(%r)' % (c.__class__.__name__, []))

    def test_repr_contents(self):
        c = Classes(TESTLIST1)
        self.assertEqual('%r' % c, '%s(%r)' % (c.__class__.__name__, TESTLIST1))

    def test_as_list(self):
        c = Classes(TESTLIST1)
        self.assertListEqual(c.as_list(), TESTLIST1)

if __name__ == '__main__':
    unittest.main()
