#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import types
import os
from reclass.errors import InvalidClassnameError

INVALID_CHARACTERS_FOR_CLASSNAMES = ' ' + os.sep

class Classes(object):
    '''
    A very limited ordered set of strings with O(n) uniqueness constraints. It
    is neither a proper list or a proper set, on purpose, to keep things
    simple.
    '''
    def __init__(self, iterable=None):
        self._items = []
        if iterable is not None:
            self.merge_unique(iterable)

    def __len__(self):
        return len(self._items)

    def __eq__(self, rhs):
        if isinstance(rhs, list):
            return self._items == rhs
        else:
            try:
                return self._items == rhs._items
            except AttributeError as e:
                return False

    def __ne__(self, rhs):
        return not self.__eq__(rhs)

    def as_list(self):
        return self._items[:]

    def merge_unique(self, iterable):
        if isinstance(iterable, self.__class__):
            iterable = iterable.as_list()
        # Cannot just call list.extend here, as iterable's items might not
        # be unique by themselves, or in the context of self.
        for i in iterable:
            self.append_if_new(i)

    def _assert_is_string(self, item):
        if not isinstance(item, types.StringTypes):
            raise TypeError('%s instances can only contain strings, '\
                            'not %s' % (self.__class__.__name__, type(item)))

    def _assert_valid_characters(self, item):
        for c in INVALID_CHARACTERS_FOR_CLASSNAMES:
            if c in item:
                raise InvalidClassnameError(c, item)

    def _append_if_new(self, item):
        if item not in self._items:
            self._items.append(item)

    def append_if_new(self, item):
        self._assert_is_string(item)
        self._assert_valid_characters(item)
        self._append_if_new(item)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__,
                           self._items)
