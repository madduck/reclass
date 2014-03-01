#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import re

from reclass.utils.dictpath import DictPath
from reclass.defaults import PARAMETER_INTERPOLATION_SENTINELS, \
        PARAMETER_INTERPOLATION_DELIMITER
from reclass.errors import IncompleteInterpolationError, \
        UndefinedVariableError

_SENTINELS = [re.escape(s) for s in PARAMETER_INTERPOLATION_SENTINELS]
_RE = '{0}\s*(.+?)\s*{1}'.format(*_SENTINELS)

class RefValue(object):
    '''
    Isolates references in string values

    RefValue can be used to isolate and eventually expand references to other
    parameters in strings. Those references can then be iterated and rendered
    in the context of a dictionary to resolve those references.

    RefValue always gets constructed from a string, because templating
    — essentially this is what's going on — is necessarily always about
    strings. Therefore, generally, the rendered value of a RefValue instance
    will also be a string.

    Nevertheless, as this might not be desirable, RefValue will return the
    referenced variable without casting it to a string, if the templated
    string contains nothing but the reference itself.

    For instance:

      mydict = {'favcolour': 'yellow', 'answer': 42, 'list': [1,2,3]}
      RefValue('My favourite colour is ${favolour}').render(mydict)
      → 'My favourite colour is yellow'      # a string

      RefValue('The answer is ${answer}').render(mydict)
      → 'The answer is 42'                   # a string

      RefValue('${answer}').render(mydict)
      → 42                                   # an int

      RefValue('${list}').render(mydict)
      → [1,2,3]                              # an list

    The markers used to identify references are set in reclass.defaults, as is
    the default delimiter.
    '''

    INTERPOLATION_RE = re.compile(_RE)

    def __init__(self, string, delim=PARAMETER_INTERPOLATION_DELIMITER):
        self._strings = []
        self._refs = []
        self._delim = delim
        self._parse(string)

    def _parse(self, string):
        parts = RefValue.INTERPOLATION_RE.split(string)
        self._refs = parts[1:][::2]
        self._strings = parts[0:][::2]
        self._check_strings(string)

    def _check_strings(self, orig):
        for s in self._strings:
            pos = s.find(PARAMETER_INTERPOLATION_SENTINELS[0])
            if pos >= 0:
                raise IncompleteInterpolationError(orig,
                                                   PARAMETER_INTERPOLATION_SENTINELS[1])

    def _resolve(self, ref, context):
        path = DictPath(self._delim, ref)
        try:
            return path.get_value(context)
        except KeyError as e:
            raise UndefinedVariableError(ref)

    def has_references(self):
        return len(self._refs) > 0

    def get_references(self):
        return self._refs

    def _assemble(self, resolver):
        if not self.has_references():
            return self._strings[0]

        if self._strings == ['', '']:
            # preserve the type of the referenced variable
            return resolver(self._refs[0])

        # reassemble the string by taking a string and str(ref) pairwise
        ret = ''
        for i in range(0, len(self._refs)):
            ret += self._strings[i] + str(resolver(self._refs[i]))
        if len(self._strings) > len(self._refs):
            # and finally append a trailing string, if any
            ret += self._strings[-1]
        return ret

    def render(self, context):
        resolver = lambda s: self._resolve(s, context)
        return self._assemble(resolver)

    def __repr__(self):
        do_not_resolve = lambda s: s.join(PARAMETER_INTERPOLATION_SENTINELS)
        return 'RefValue(%r, %r)' % (self._assemble(do_not_resolve),
                                     self._delim)
