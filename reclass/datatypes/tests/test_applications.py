#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Applications

class TestApplications:

    def test_constructor0(self):
        c = Applications()
        assert len(c) == 0

    def test_constructor1(self):
        DATA = ['one', 'two', 'three', 'four']
        c = Applications(DATA)
        assert len(c) == len(DATA)
        for i in range(0, len(c)):
            assert DATA[i] == c[i]

    def test_merge(self):
        DATA0 = ['one', 'two', 'three', 'four']
        DATA1 = ['one', 'three', 'five', 'seven']
        c = Applications(DATA0)
        c.merge(DATA1)
        assert len(c) == 6
        assert c[:4] == DATA0
        assert c[4] == DATA1[2]
        assert c[5] == DATA1[3]

    def test_merge_negate(self):
        negater = '~'
        DATA0 = ['red', 'green', 'blue']
        DATA1 = [negater + 'red', 'yellow', 'black']
        c = Applications(DATA0)
        c.merge(DATA1, negater)
        assert len(c) == len(DATA0)-1 + len(DATA1)-1
        assert c[0] == DATA0[1]
        assert c[1] == DATA0[2]
        assert c[2] == DATA1[1]
        assert c[3] == DATA1[2]

    def test_merge_negate_default(self):
        c = Applications(['red'])
        c.merge(['~red'])
        assert len(c) == 0

    def test_merge_negate_nonexistent(self):
        c = Applications(['blue'])
        c.merge(['~red'])
        assert len(c) == 1
        assert 'red' not in c
        assert '~red' not in c
        assert 'blue' in c
