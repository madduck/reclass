#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.mergers.list import SetExtend

class Classes(list):

    def __init__(self, *args, **kwargs):
        super(Classes, self).__init__(*args, **kwargs)

    def merge(self, other):
        merger = SetExtend()
        self[:] = merger.merge(self, other)

    def __repr__(self):
        return '<Classes {0}>'.format(super(Classes, self).__repr__())
