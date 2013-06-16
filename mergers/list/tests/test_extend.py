#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from mergers.list import ListExtend

class TestListExtend:

    def setUp(self):
        self.merger = ListExtend()

    def _test_merge(self, one, two, target):
        res = self.merger.merge(one, two)
        print res, target
        return res == target

    def test_merge_scalars(self):
        assert self._test_merge(1, 2, [1,2])

    def test_merge_tuples(self):
        t1 = (1,2,3)
        t2 = (6,5,4)
        target = [t1, t2]
        assert self._test_merge(t1, t2, target)

    def test_merge_lists(self):
        l1 = [1,2,3]
        l2 = [6,5,4]
        target = l1 + l2
        assert self._test_merge(l1, l2, target)

    def test_merge_scalar_tuple(self):
        s = 'one'
        t = (2,3)
        target = [s, t]
        assert self._test_merge(s, t, target)

    def test_merge_scalar_list(self):
        s = 'foo'
        l = [1,2,3]
        target = [s]
        target.extend(l)
        assert self._test_merge(s, l, target)

    def test_merge_list_scalar(self):
        l = [1,2,3]
        s = 'bar'
        target = l[:]
        target.append(s)
        assert self._test_merge(l, s, target)

    def test_merge_duplicates_scalar(self):
        s1 = 2
        s2 = 2
        target = [2,2]
        assert self._test_merge(s1, s2, target)

    def test_merge_duplicates_list(self):
        l1 = [1,2,3]
        l2 = [3,2,1]
        target = l1 + l2
        assert self._test_merge(l1, l2, target)

    def test_merge_with_none(self):
        first = [1,2,3]
        ret = self.merger.merge(first, None)
        assert ret == first
