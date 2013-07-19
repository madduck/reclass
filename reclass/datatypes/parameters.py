#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
class Parameters(object):
    '''
    A class to hold nested dictionaries with the following speciality:

    "merging" a dictionary (the "new" dictionary) into the current Parameters
    causes a recursive walk of the new dict, during which

       - scalars (incl. tuples) are replaced with the value from the new
         dictionary;
       - lists are extended, not replaced;
       - dictionaries are updated (using dict.update), not replaced;

    To support this speciality, this class only exposes very limited
    functionality and does not try to be a really mapping object.
    '''
    DEFAULT_PATH_DELIMITER = ':'  # useful default for YAML

    def __init__(self, mapping=None, delimiter=None):
        if delimiter is None:
            delimiter = Parameters.DEFAULT_PATH_DELIMITER
        self._delimiter = delimiter
        self._base = {}
        if mapping is not None:
            # we initialise by merging, otherwise the list of references might
            # not be updated
            self.merge(mapping)

    delimiter = property(lambda self: self._delimiter)

    def __len__(self):
        return len(self._base)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self._base,
                               self.delimiter)

    def __eq__(self, other):
        return self._base == other._base \
                and self._delimiter == other._delimiter

    def __ne__(self, other):
        return not self.__eq__(other)

    def as_dict(self):
        return self._base.copy()

    def _update_scalar(self, cur, new, delim, parent):
        if delim is None:
            return new

        else:
            return new #TODO

    def _extend_list(self, cur, new, delim, parent):
        if isinstance(cur, list):
            ret = cur
        else:
            ret = [cur]
        for i in new:
            ret.append(self._merge_recurse(None, i, delim, parent))
        return ret

    def _merge_dict(self, cur, new, delim, parent):
        if isinstance(cur, dict):
            ret = cur
        else:
            # nothing sensible to do
            raise TypeError('Cannot merge dict into {0} '
                            'objects'.format(type(cur)))

        if delim is None:
            # a delimiter of None indicates that there is no value
            # processing to be done, and since there is no current
            # value, we do not need to walk the new dictionary:
            ret.update(new)
            return ret

        for key, newvalue in new.iteritems():
            ret[key] = self._merge_recurse(ret.get(key), newvalue, delim,
                                           (ret, key))
        return ret

    def _merge_recurse(self, cur, new, delim, parent=None):
        if isinstance(new, dict):
            if cur is None:
                cur = {}
            return self._merge_dict(cur, new, delim, parent)

        elif isinstance(new, list):
            if cur is None:
                cur = []
            return self._extend_list(cur, new, delim, parent)

        else:
            return self._update_scalar(cur, new, delim, parent)

    def merge(self, other):
        if isinstance(other, dict):
            self._base = self._merge_recurse(self._base, other, None)

        elif isinstance(other, self.__class__):
            self._base = self._merge_recurse(self._base, other._base,
                                             other.delimiter)

        else:
            raise TypeError('Cannot merge %s objects into %s' % (type(other),
                            self.__class__.__name__))
