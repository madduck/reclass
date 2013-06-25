#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.storage.yaml_fs import directory
import os, sys

TESTDIR = os.path.join(sys.path[0], 'classes')
FILECOUNT = 10

class TestDirectory:

    def setUp(self):
        self._dir = directory.Directory(TESTDIR)

    def test_walk_registry(self):
        def count_fn(d, f):
            count_fn.c += len(f)
        count_fn.c = 0
        self._dir.walk(register_fn=count_fn)
        assert count_fn.c == FILECOUNT

    def test_walk(self):
        self._dir.walk()
        assert len(self._dir.files) == FILECOUNT

