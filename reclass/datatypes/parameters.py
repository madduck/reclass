#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import types

from reclass.defaults import PARAMETER_INTERPOLATION_DELIMITER
from reclass.utils.dictpath import DictPath
from reclass.utils.refvalue import RefValue
from reclass.errors import InfiniteRecursionError, UndefinedVariableError

class Parameters(object):
    '''
    A class to hold nested dictionaries with the following specialities:

      1. "merging" a dictionary (the "new" dictionary) into the current
         Parameters causes a recursive walk of the new dict, during which

         - scalars (incl. tuples) are replaced with the value from the new
           dictionary;
         - lists are extended, not replaced;
         - dictionaries are updated (using dict.update), not replaced;

      2. "interpolating" a dictionary means that values within the dictionary
         can reference other values in the same dictionary. Those references
         are collected during merging and then resolved during interpolation,
         which avoids having to walk the dictionary twice. If a referenced
         value contains references itself, those are resolved first, in
         topological order. Therefore, deep references work. Cyclical
         references cause an error.

    To support these specialities, this class only exposes very limited
    functionality and does not try to be a really mapping object.
    '''
    DEFAULT_PATH_DELIMITER = PARAMETER_INTERPOLATION_DELIMITER

    def __init__(self, mapping=None, delimiter=None):
        if delimiter is None:
            delimiter = Parameters.DEFAULT_PATH_DELIMITER
        self._delimiter = delimiter
        self._base = {}
        self._refs = {}
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

    def _register_ref_occurrence(self, path, ref):
        self._refs[path] = ref

    def _update_scalar(self, cur, new, path):
        if self.delimiter is None or not isinstance(new, types.StringTypes):
            return new

        else:
            ret = RefValue(new, self.delimiter)
            if not ret.has_references():
                # do not replace with RefValue instance if there are no
                # references
                return new

            self._register_ref_occurrence(path, ret)
            return ret

    def _extend_list(self, cur, new, path):
        if isinstance(cur, list):
            ret = cur
        else:
            ret = [cur]
        for i in xrange(len(new)):
            ret.append(self._merge_recurse(None, new[i], path.new_subpath(i)))
        return ret

    def _merge_dict(self, cur, new, path):
        if isinstance(cur, dict):
            ret = cur
        else:
            # nothing sensible to do
            raise TypeError('Cannot merge dict into {0} '
                            'objects'.format(type(cur)))

        if self.delimiter is None:
            # a delimiter of None indicates that there is no value
            # processing to be done, and since there is no current
            # value, we do not need to walk the new dictionary:
            ret.update(new)
            return ret

        for key, newvalue in new.iteritems():
            ret[key] = self._merge_recurse(ret.get(key), newvalue,
                                           path.new_subpath(key))
        return ret

    def _merge_recurse(self, cur, new, path=None):
        if path is None:
            path = DictPath(self.delimiter)

        if isinstance(new, dict):
            if cur is None:
                cur = {}
            return self._merge_dict(cur, new, path)

        elif isinstance(new, list):
            if cur is None:
                cur = []
            return self._extend_list(cur, new, path)

        else:
            return self._update_scalar(cur, new, path)

    def merge(self, other):
        if isinstance(other, dict):
            self._base = self._merge_recurse(self._base, other, None)

        elif isinstance(other, self.__class__):
            self._base = self._merge_recurse(self._base, other._base,
                                             None)
            self._refs.update(other._refs)

        else:
            raise TypeError('Cannot merge %s objects into %s' % (type(other),
                            self.__class__.__name__))

    def interpolate(self):
        while len(self._refs) > 0:
            path, refvalue = self._refs.iteritems().next()
            self._interpolate_inner(path, refvalue)

    def _interpolate_inner(self, path, refvalue):
        self._refs[path] = None
        for ref in refvalue.get_references():
            path_from_ref = DictPath(self.delimiter, ref)
            try:
                refvalue_inner = self._refs[path_from_ref]
                if refvalue_inner is None:
                    # every call to _interpolate_inner replaces the value of
                    # the saved occurrences of a reference with None.
                    # Therefore, if we encounter None instead of a refvalue,
                    # it means that we have already processed it and are now
                    # faced with a cyclical reference.
                    raise InfiniteRecursionError(path, ref)
                self._interpolate_inner(path_from_ref, refvalue_inner)
            except KeyError as e:
                pass
        try:
            new = refvalue.render(self._base)
            path.set_value(self._base, new)
            del self._refs[path]
        except UndefinedVariableError as e:
            raise UndefinedVariableError(e.var, path)

