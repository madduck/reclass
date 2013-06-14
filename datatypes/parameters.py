#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from mergers.dict import DictRecursivePolicyUpdate

class Parameters(dict):

    def __init__(self, *args, **kwargs):
        super(Parameters, self).__init__(*args, **kwargs)

    def merge(self, other, merger=DictRecursivePolicyUpdate()):
        self.update(merger.merge(self, other))

    def __repr__(self):
        return '<Parameters {0}>'.format(super(Parameters, self).__repr__())
