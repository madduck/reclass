#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from test_recursive_update import TestDictRecursiveUpdate
from mergers.dict import DictRecursivePolicyUpdate

class TestDictRecursivePolicyUpdate(TestDictRecursiveUpdate):

    def setUp(self):
        self.merger = DictRecursivePolicyUpdate()

    def test_nested_lists_extend(self):
        first = {'one': [1,2],
                 'two': {'one': [1,2]}}
        second = {'one': [3,4], 
                  'two': {'one': [3,4]}}
        ret = self.merger.merge(first, second)
        assert len(ret['one']) == 4
        assert ret['one'][2] == 3
        assert len(ret['two']['one']) == 4
        assert ret['two']['one'][3] == 4

    def test_merge_with_none(self):
        first = {1:2,3:4}
        ret = self.merger.merge(first, None)
        assert ret == first
