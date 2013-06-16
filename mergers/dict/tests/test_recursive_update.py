#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from test_update import TestDictUpdate
from mergers.dict import DictRecursiveUpdate

class TestDictRecursiveUpdate(TestDictUpdate):

    def setUp(self):
        self.merger = DictRecursiveUpdate()

    def test_simple_recursive_dict_update(self):
        first = {'one':{1:1,2:3,3:2}}
        second = {'one':{2:2,3:3,4:4}}
        ret = self.merger.merge(first, second)
        assert len(ret) == 1
        for k,v in ret['one'].iteritems():
            assert k == v

    def test_complex_recursive_dict_update(self):
        first = {'one': 1,
                 'two': {'a':92,'b':94},
                 'three': {'third':0.33,'two thirds':0.67},
                 'four': {1:{1:1},2:{2:2},3:{3:4}}
                }
        second = {'five': 5,
                  'one': 1,
                  'two': {'b':93,'c':94},
                  'four': {4:{4:4}, 3:{3:3}},
                 }
        ret = self.merger.merge(first, second)
        assert ret['one'] == 1
        assert len(ret['two']) == 3
        assert ret['two']['b'] == 93
        assert len(ret['three']) == 2
        assert len(ret['four']) == 4
        for i in range(1,4):
            assert len(ret['four'][i]) == 1
            for k,v in ret['four'][i].iteritems():
                assert k == v

    def test_merge_with_none(self):
        first = {1:2,3:4}
        ret = self.merger.merge(first, None)
        assert ret == first
