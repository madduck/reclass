#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.mergers.list import SetExtend

class ApplicationsMerger(SetExtend):

    def __init__(self, negater='~'):
        self._negater=negater

    def _combine(self, first, second):
        for i in second:
            remove = False
            if i.startswith('~'):
                i = i[1:]
                remove = True
            if i not in first:
                if not remove:
                    first.append(i)
            elif remove:
                first.remove(i)
        return first


class Applications(list):

    def __init__(self, *args, **kwargs):
        super(Applications, self).__init__(*args, **kwargs)

    def merge(self, other, negater='~'):
        merger = ApplicationsMerger(negater)
        self[:] = merger.merge(self, other)

    def __repr__(self):
        return '<Applications {0}>'.format(super(Applications, self).__repr__())
