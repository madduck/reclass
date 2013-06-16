#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from base import BaseDictMerger

class DictRecursivePolicyUpdate(BaseDictMerger):

    def __init__(self, policy=None):
        super(DictRecursivePolicyUpdate, self).__init__()
        if policy is None:
            policy = {(dict,dict) : self.merge,
                      (list,list) : lambda x,y: x+y,
                      (dict,list) : lambda x,y: self.merge(x, dict(y)),
                      None        : lambda x,y: y
                     }
        self._policy = policy

    def merge(self, first, second):
        if second is None:
            return first

        ret = first.copy()
        for k,v in second.iteritems():
            if k in ret:
                pfn = self._policy.get((type(ret[k]), type(v)),
                                       self._policy.get(None))
                ret[k] = pfn(ret[k], v)
            else:
                ret[k] = v
        return ret
