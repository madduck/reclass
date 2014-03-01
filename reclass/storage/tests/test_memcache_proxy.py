#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.storage.memcache_proxy import MemcacheProxy
from reclass.storage import NodeStorageBase

import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

class TestMemcacheProxy(unittest.TestCase):

    def setUp(self):
        self._storage = mock.MagicMock(spec_set=NodeStorageBase)

    def test_no_nodes_caching(self):
        p = MemcacheProxy(self._storage, cache_nodes=False)
        NAME = 'foo'; NAME2 = 'bar'; RET = 'baz'
        self._storage.get_node.return_value = RET
        self.assertEqual(p.get_node(NAME), RET)
        self.assertEqual(p.get_node(NAME), RET)
        self.assertEqual(p.get_node(NAME2), RET)
        self.assertEqual(p.get_node(NAME2), RET)
        expected = [mock.call(NAME), mock.call(NAME),
                    mock.call(NAME2), mock.call(NAME2)]
        self.assertListEqual(self._storage.get_node.call_args_list, expected)

    def test_nodes_caching(self):
        p = MemcacheProxy(self._storage, cache_nodes=True)
        NAME = 'foo'; NAME2 = 'bar'; RET = 'baz'
        self._storage.get_node.return_value = RET
        self.assertEqual(p.get_node(NAME), RET)
        self.assertEqual(p.get_node(NAME), RET)
        self.assertEqual(p.get_node(NAME2), RET)
        self.assertEqual(p.get_node(NAME2), RET)
        expected = [mock.call(NAME), mock.call(NAME2)] # called once each
        self.assertListEqual(self._storage.get_node.call_args_list, expected)

    def test_no_classes_caching(self):
        p = MemcacheProxy(self._storage, cache_classes=False)
        NAME = 'foo'; NAME2 = 'bar'; RET = 'baz'
        self._storage.get_class.return_value = RET
        self.assertEqual(p.get_class(NAME), RET)
        self.assertEqual(p.get_class(NAME), RET)
        self.assertEqual(p.get_class(NAME2), RET)
        self.assertEqual(p.get_class(NAME2), RET)
        expected = [mock.call(NAME), mock.call(NAME),
                    mock.call(NAME2), mock.call(NAME2)]
        self.assertListEqual(self._storage.get_class.call_args_list, expected)

    def test_classes_caching(self):
        p = MemcacheProxy(self._storage, cache_classes=True)
        NAME = 'foo'; NAME2 = 'bar'; RET = 'baz'
        self._storage.get_class.return_value = RET
        self.assertEqual(p.get_class(NAME), RET)
        self.assertEqual(p.get_class(NAME), RET)
        self.assertEqual(p.get_class(NAME2), RET)
        self.assertEqual(p.get_class(NAME2), RET)
        expected = [mock.call(NAME), mock.call(NAME2)] # called once each
        self.assertListEqual(self._storage.get_class.call_args_list, expected)

    def test_nodelist_no_caching(self):
        p = MemcacheProxy(self._storage, cache_nodelist=False)
        p.enumerate_nodes()
        p.enumerate_nodes()
        expected = [mock.call(), mock.call()]
        self.assertListEqual(self._storage.enumerate_nodes.call_args_list, expected)

    def test_nodelist_caching(self):
        p = MemcacheProxy(self._storage, cache_nodelist=True)
        p.enumerate_nodes()
        p.enumerate_nodes()
        expected = [mock.call()] # once only
        self.assertListEqual(self._storage.enumerate_nodes.call_args_list, expected)


if __name__ == '__main__':
    unittest.main()
