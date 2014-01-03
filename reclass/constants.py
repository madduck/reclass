#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

class _Constant(object):

    def __init__(self, displayname):
        self._repr = displayname

    __str__ = __repr__ = lambda self: self._repr

MODE_NODEINFO = _Constant('NODEINFO')
MODE_INVENTORY = _Constant('INVENTORY')
