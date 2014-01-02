#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.storage.loader import StorageBackendLoader

import unittest

class TestLoader(unittest.TestCase):

    def test_load(self):
        loader = StorageBackendLoader('yaml_fs')
        from reclass.storage.yaml_fs import ExternalNodeStorage as YamlFs
        self.assertEqual(loader.load(), YamlFs)

if __name__ == '__main__':
    unittest.main()
