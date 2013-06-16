#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from datatypes import Entity, Classes, Parameters, Applications

class TestEntity:

    def test_constructor0(self):
        e = Entity()
        assert isinstance(e.classes, Classes)
        assert len(e.classes) == 0
        assert isinstance(e.parameters, Parameters)
        assert len(e.parameters) == 0
        assert isinstance(e.applications, Applications)
        assert len(e.applications) == 0

    def test_constructor1(self):
        c = Classes(['one', 'two'])
        p = Parameters({'blue':'white', 'black':'yellow'})
        a = Applications(['three', 'four'])
        e = Entity(c, a, p)
        assert e.classes == c
        assert e.parameters == p
        assert e.applications == a
