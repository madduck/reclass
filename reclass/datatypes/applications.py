#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

from classes import Classes

class Applications(Classes):
    '''
    Extends Classes with the possibility to let specially formatted items
    remove earlier occurences of the item. For instance, if the "negater" is
    '~', then "adding" an element "~foo" to a list causes a previous element
    "foo" to be removed. If no such element exists, nothing happens, but
    a reference of the negation is kept, in case the instance is later used to
    extend another instance, in which case the negations should apply to the
    instance to be extended.
    '''
    DEFAULT_NEGATION_PREFIX = '~'

    def __init__(self, iterable=None,
                 negation_prefix=DEFAULT_NEGATION_PREFIX):
        self._negation_prefix = negation_prefix
        self._offset = len(negation_prefix)
        self._negations = []
        super(Applications, self).__init__(iterable)

    def _get_negation_prefix(self):
        return self._negation_prefix
    negation_prefix = property(_get_negation_prefix)

    def append_if_new(self, item):
        self._assert_is_string(item)
        if item.startswith(self._negation_prefix):
            item = item[self._offset:]
            self._negations.append(item)
            try:
                self._items.remove(item)
            except ValueError:
                pass
        else:
            super(Applications, self)._append_if_new(item)

    def merge_unique(self, iterable):
        if isinstance(iterable, self.__class__):
            # we might be extending ourselves to include negated applications,
            # in which case we need to remove our own content accordingly:
            for negation in iterable._negations:
                try:
                    self._items.remove(negation)
                except ValueError:
                    pass
            iterable = iterable.as_list()
        for i in iterable:
            self.append_if_new(i)

    def __repr__(self):
        contents = self._items + \
                ['%s%s' % (self._negation_prefix, i) for i in self._negations]
        return "%s(%r, %r)" % (self.__class__.__name__, contents,
                               self._negation_prefix)
