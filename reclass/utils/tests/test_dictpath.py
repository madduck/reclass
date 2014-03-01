#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.utils.dictpath import DictPath
import unittest

class TestDictPath(unittest.TestCase):

    def test_constructor0(self):
        p = DictPath(':')
        self.assertListEqual(p._parts, [])

    def test_constructor_list(self):
        l = ['a', 'b', 'c']
        p = DictPath(':', l)
        self.assertListEqual(p._parts, l)

    def test_constructor_str(self):
        delim = ':'
        s = 'a{0}b{0}c'.format(delim)
        l = ['a', 'b', 'c']
        p = DictPath(delim, s)
        self.assertListEqual(p._parts, l)

    def test_constructor_str_escaped(self):
        delim = ':'
        s = 'a{0}b\{0}b{0}c'.format(delim)
        l = ['a', 'b\\{0}b'.format(delim), 'c']
        p = DictPath(delim, s)
        self.assertListEqual(p._parts, l)

    def test_constructor_invalid_type(self):
        with self.assertRaises(TypeError):
            p = DictPath(':', 5)

    def test_equality(self):
        delim = ':'
        s = 'a{0}b{0}c'.format(delim)
        l = ['a', 'b', 'c']
        p1 = DictPath(delim, s)
        p2 = DictPath(delim, l)
        self.assertEqual(p1, p2)

    def test_inequality_content(self):
        delim = ':'
        s = 'a{0}b{0}c'.format(delim)
        l = ['d', 'e', 'f']
        p1 = DictPath(delim, s)
        p2 = DictPath(delim, l)
        self.assertNotEqual(p1, p2)

    def test_inequality_delimiter(self):
        l = ['a', 'b', 'c']
        p1 = DictPath(':', l)
        p2 = DictPath('%', l)
        self.assertNotEqual(p1, p2)

    def test_repr(self):
        delim = '%'
        s = 'a:b\:b:c'
        p = DictPath(delim, s)
        self.assertEqual('%r' % p, 'DictPath(%r, %r)' % (delim, s))

    def test_str(self):
        s = 'a:b\:b:c'
        p = DictPath(':', s)
        self.assertEqual(str(p), s)

    def test_path_accessor(self):
        l = ['a', 'b', 'c']
        p = DictPath(':', l)
        self.assertListEqual(p.path, l)

    def test_new_subpath(self):
        l = ['a', 'b', 'c']
        p = DictPath(':', l[:-1])
        p = p.new_subpath(l[-1])
        self.assertListEqual(p.path, l)

    def test_get_value(self):
        v = 42
        l = ['a', 'b', 'c']
        d = {'a':{'b':{'c':v}}}
        p = DictPath(':', l)
        self.assertEqual(p.get_value(d), v)

    def test_get_value_escaped(self):
        v = 42
        l = ['a', 'b:b', 'c']
        d = {'a':{'b:b':{'c':v}}}
        p = DictPath(':', l)
        self.assertEqual(p.get_value(d), v)

    def test_get_value_listindex_list(self):
        v = 42
        l = ['a', 1, 'c']
        d = {'a':[None, {'c':v}, None]}
        p = DictPath(':', l)
        self.assertEqual(p.get_value(d), v)

    def test_get_value_listindex_str(self):
        v = 42
        s = 'a:1:c'
        d = {'a':[None, {'c':v}, None]}
        p = DictPath(':', s)
        self.assertEqual(p.get_value(d), v)

    def test_set_value(self):
        v = 42
        l = ['a', 'b', 'c']
        d = {'a':{'b':{'c':v}}}
        p = DictPath(':', l)
        p.set_value(d, v+1)
        self.assertEqual(d['a']['b']['c'], v+1)

    def test_set_value_escaped(self):
        v = 42
        l = ['a', 'b:b', 'c']
        d = {'a':{'b:b':{'c':v}}}
        p = DictPath(':', l)
        p.set_value(d, v+1)
        self.assertEqual(d['a']['b:b']['c'], v+1)

    def test_set_value_escaped_listindex_list(self):
        v = 42
        l = ['a', 1, 'c']
        d = {'a':[None, {'c':v}, None]}
        p = DictPath(':', l)
        p.set_value(d, v+1)
        self.assertEqual(d['a'][1]['c'], v+1)

    def test_set_value_escaped_listindex_str(self):
        v = 42
        s = 'a:1:c'
        d = {'a':[None, {'c':v}, None]}
        p = DictPath(':', s)
        p.set_value(d, v+1)
        self.assertEqual(d['a'][1]['c'], v+1)

    def test_get_nonexistent_value(self):
        l = ['a', 'd']
        p = DictPath(':', l)
        with self.assertRaises(KeyError):
            p.get_value(dict())

    def test_set_nonexistent_value(self):
        l = ['a', 'd']
        p = DictPath(':', l)
        with self.assertRaises(KeyError):
            p.set_value(dict(), 42)

if __name__ == '__main__':
    unittest.main()
