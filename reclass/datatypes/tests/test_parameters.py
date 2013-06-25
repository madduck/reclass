#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Parameters

class TestParameters:

    def test_constructor0(self):
        c = Parameters()
        assert len(c) == 0

    def test_constructor1(self):
        DATA = {'blue':'white', 'black':'yellow'}
        c = Parameters(DATA)
        assert len(c) == len(DATA)
        for i in c.iterkeys():
            assert DATA[i] == c[i]
