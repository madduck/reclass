#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Classes

class TestClasses:

    def test_constructor0(self):
        c = Classes()
        assert len(c) == 0

    def test_constructor1(self):
        DATA = ['one', 'two', 'three', 'four']
        c = Classes(DATA)
        assert len(c) == len(DATA)
        for i in range(0, len(c)):
            assert DATA[i] == c[i]

    def test_merge(self):
        DATA0 = ['one', 'two', 'three', 'four']
        DATA1 = ['one', 'three', 'five', 'seven']
        c = Classes(DATA0)
        c.merge(DATA1)
        assert len(c) == 6
        assert c[:4] == DATA0
        assert c[4] == DATA1[2]
        assert c[5] == DATA1[3]
