#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from base import BaseListMerger

class ListExtend(BaseListMerger):

    def _combine(self, first, second):
        if second is not None:
            if isinstance(second, list):
                first.extend(second)
            else:
                first.append(second)
        return first
