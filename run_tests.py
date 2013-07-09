#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import unittest
tests = unittest.TestLoader().discover('reclass')
unittest.TextTestRunner(verbosity=1).run(tests)
