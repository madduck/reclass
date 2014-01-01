#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
class OutputterBase(object):

    def __init__(self):
        pass

    def dump(self, data, pretty_print=False):
        raise NotImplementedError, "dump() method not yet implemented"


class OutputLoader(object):

    def __init__(self, outputter):
        self._name = 'reclass.output.' + outputter + '_outputter'
        try:
            self._module = __import__(self._name, globals(), locals(), self._name)
        except ImportError:
            raise NotImplementedError

    def load(self, attr='Outputter'):
        klass = getattr(self._module, attr, None)
        if klass is None:
            raise AttributeError, \
                'Outputter class {0} does not export "{1}"'.format(self._name, klass)
        return klass
