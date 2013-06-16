#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from test_extend import TestListExtend
from mergers.list import SetExtend

class TestSetExtend(TestListExtend):

    def setUp(self):
        self.merger = SetExtend()

    def test_merge_duplicates_scalar(self):
        s1 = 2
        s2 = 2
        target = [2]
        assert self._test_merge(s1, s2, target)

    def test_merge_duplicates_list(self):
        l1 = [1,2,3]
        l2 = [3,2,1]
        target = l1
        assert self._test_merge(l1, l2, target)

    def test_merge_with_none(self):
        first = [1,2,3]
        ret = self.merger.merge(first, None)
        assert ret == first
