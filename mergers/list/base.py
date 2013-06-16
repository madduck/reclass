#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from mergers.base import BaseMerger

class BaseListMerger(BaseMerger):

    def merge(self, first, second):
        first = [first] if not isinstance(first, list) else first[:]
        if second is None:
            return first
        second = [second] if not isinstance(second, list) else second[:]
        return self._combine(first, second)
