#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from mergers.dict import DictUpdate

class TestDictUpdate:

    def setUp(self):
        self.merger = DictUpdate()

    def test_dict_update(self):
        first = {1:1,2:3,3:2}
        second = {2:2,3:3,4:4}
        ret = self.merger.merge(first, second)
        assert len(ret) == 4
        for k,v in ret.iteritems():
            assert k == v

    def test_merge_with_none(self):
        first = {1:2,3:4}
        ret = self.merger.merge(first, None)
        assert ret == first
