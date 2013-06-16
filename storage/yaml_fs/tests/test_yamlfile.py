#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import storage.yaml_fs.yamlfile as yamlfile
import os, sys
from datatypes import Entity, Classes, Parameters, Applications

TESTFILE = os.path.join(sys.path[0], 'nodes', 'blue.yml')
EMPTYFILE = os.path.join(sys.path[0], 'nodes', 'empty.yml')
NULLFILE = os.path.join(sys.path[0], 'nodes', 'null.yml')

class TestYamlFile:

    def setUp(self):
        self._file = yamlfile.YamlFile(TESTFILE)

    def test_path_property(self):
        assert self._file.path == TESTFILE

    def test_data(self):
        e = self._file.entity
        c = e.classes
        assert len(c) == 4
        assert hasattr(c, 'merge')
        p = e.parameters
        assert len(p) == 2
        assert 'motd' in p
        assert 'colour' in p
        assert hasattr(p, 'merge')
        a = e.applications
        assert len(a) == 1
        assert 'blues' in a
        assert hasattr(a, 'merge')

    def test_empty_file(self):
        e = yamlfile.YamlFile(EMPTYFILE).entity
        assert isinstance(e, Entity)
        assert isinstance(e.classes, Classes)
        assert len(e.classes) == 0
        assert isinstance(e.parameters, Parameters)
        assert len(e.parameters) == 0
        assert isinstance(e.applications, Applications)
        assert len(e.applications) == 0

    def test_null_file(self):
        e = yamlfile.YamlFile(NULLFILE).entity
        assert isinstance(e, Entity)
        assert isinstance(e.classes, Classes)
        assert len(e.classes) == 0
        assert isinstance(e.parameters, Parameters)
        assert len(e.parameters) == 0
        assert isinstance(e.applications, Applications)
        assert len(e.applications) == 0
