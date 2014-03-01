#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

from reclass.utils.refvalue import RefValue
from reclass.defaults import PARAMETER_INTERPOLATION_SENTINELS, \
        PARAMETER_INTERPOLATION_DELIMITER
from reclass.errors import UndefinedVariableError, \
        IncompleteInterpolationError
import unittest

def _var(s):
    return '%s%s%s' % (PARAMETER_INTERPOLATION_SENTINELS[0], s,
                       PARAMETER_INTERPOLATION_SENTINELS[1])

CONTEXT = {'favcolour':'yellow',
           'motd':{'greeting':'Servus!',
                   'colour':'${favcolour}'
                  },
           'int':1,
           'list':[1,2,3],
           'dict':{1:2,3:4},
           'bool':True
          }

def _poor_mans_template(s, var, value):
    return s.replace(_var(var), value)

class TestRefValue(unittest.TestCase):

    def test_simple_string(self):
        s = 'my cat likes to hide in boxes'
        tv = RefValue(s)
        self.assertFalse(tv.has_references())
        self.assertEquals(tv.render(CONTEXT), s)

    def _test_solo_ref(self, key):
        s = _var(key)
        tv = RefValue(s)
        res = tv.render(CONTEXT)
        self.assertTrue(tv.has_references())
        self.assertEqual(res, CONTEXT[key])

    def test_solo_ref_string(self):
        self._test_solo_ref('favcolour')

    def test_solo_ref_int(self):
        self._test_solo_ref('int')

    def test_solo_ref_list(self):
        self._test_solo_ref('list')

    def test_solo_ref_dict(self):
        self._test_solo_ref('dict')

    def test_solo_ref_bool(self):
        self._test_solo_ref('bool')

    def test_single_subst_bothends(self):
        s = 'I like ' + _var('favcolour') + ' and I like it'
        tv = RefValue(s)
        self.assertTrue(tv.has_references())
        self.assertEqual(tv.render(CONTEXT),
                         _poor_mans_template(s, 'favcolour',
                                             CONTEXT['favcolour']))

    def test_single_subst_start(self):
        s = _var('favcolour') + ' is my favourite colour'
        tv = RefValue(s)
        self.assertTrue(tv.has_references())
        self.assertEqual(tv.render(CONTEXT),
                         _poor_mans_template(s, 'favcolour',
                                             CONTEXT['favcolour']))

    def test_single_subst_end(self):
        s = 'I like ' + _var('favcolour')
        tv = RefValue(s)
        self.assertTrue(tv.has_references())
        self.assertEqual(tv.render(CONTEXT),
                         _poor_mans_template(s, 'favcolour',
                                             CONTEXT['favcolour']))

    def test_deep_subst_solo(self):
        var = PARAMETER_INTERPOLATION_DELIMITER.join(('motd', 'greeting'))
        s = _var(var)
        tv = RefValue(s)
        self.assertTrue(tv.has_references())
        self.assertEqual(tv.render(CONTEXT),
                         _poor_mans_template(s, var,
                                             CONTEXT['motd']['greeting']))

    def test_multiple_subst(self):
        greet = PARAMETER_INTERPOLATION_DELIMITER.join(('motd', 'greeting'))
        s = _var(greet) + ' I like ' + _var('favcolour') + '!'
        tv = RefValue(s)
        self.assertTrue(tv.has_references())
        want = _poor_mans_template(s, greet, CONTEXT['motd']['greeting'])
        want = _poor_mans_template(want, 'favcolour', CONTEXT['favcolour'])
        self.assertEqual(tv.render(CONTEXT), want)

    def test_multiple_subst_flush(self):
        greet = PARAMETER_INTERPOLATION_DELIMITER.join(('motd', 'greeting'))
        s = _var(greet) + ' I like ' + _var('favcolour')
        tv = RefValue(s)
        self.assertTrue(tv.has_references())
        want = _poor_mans_template(s, greet, CONTEXT['motd']['greeting'])
        want = _poor_mans_template(want, 'favcolour', CONTEXT['favcolour'])
        self.assertEqual(tv.render(CONTEXT), want)

    def test_undefined_variable(self):
        s = _var('no_such_variable')
        tv = RefValue(s)
        with self.assertRaises(UndefinedVariableError):
            tv.render(CONTEXT)

    def test_incomplete_variable(self):
        s = PARAMETER_INTERPOLATION_SENTINELS[0] + 'incomplete'
        with self.assertRaises(IncompleteInterpolationError):
            tv = RefValue(s)

if __name__ == '__main__':
    unittest.main()
