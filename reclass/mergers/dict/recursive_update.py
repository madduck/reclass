#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from base import BaseDictMerger

class DictRecursiveUpdate(BaseDictMerger):

    def merge(self, first, second):
        if second is None:
            return first

        ret = first.copy()
        for k,v in second.iteritems():
            if k in ret:
                if isinstance(ret[k], dict):
                    if isinstance(v, (list, tuple)):
                        v = dict(v)
                    ret[k] = self.merge(ret[k], v)
                else:
                    ret[k] = v
            else:
                ret[k] = v
        return ret
