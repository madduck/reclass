#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Parameters
from reclass.defaults import PARAMETER_INTERPOLATION_SENTINELS
from reclass.errors import InfiniteRecursionError
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

SIMPLE = {'one': 1, 'two': 2, 'three': 3}

class TestParameters(unittest.TestCase):

    def _construct_mocked_params(self, iterable=None, delimiter=None):
        p = Parameters(iterable, delimiter)
        self._base = base = p._base
        p._base = mock.MagicMock(spec_set=dict, wraps=base)
        p._base.__repr__ = mock.MagicMock(autospec=dict.__repr__,
                                          return_value=repr(base))
        return p, p._base

    def test_len_empty(self):
        p, b = self._construct_mocked_params()
        l = 0
        b.__len__.return_value = l
        self.assertEqual(len(p), l)
        b.__len__.assert_called_with()

    def test_constructor(self):
        p, b = self._construct_mocked_params(SIMPLE)
        l = len(SIMPLE)
        b.__len__.return_value = l
        self.assertEqual(len(p), l)
        b.__len__.assert_called_with()

    def test_repr_empty(self):
        p, b = self._construct_mocked_params()
        b.__repr__.return_value = repr({})
        self.assertEqual('%r' % p, '%s(%r, %r)' % (p.__class__.__name__, {},
                                                   Parameters.DEFAULT_PATH_DELIMITER))
        b.__repr__.assert_called_once_with()

    def test_repr(self):
        p, b = self._construct_mocked_params(SIMPLE)
        b.__repr__.return_value = repr(SIMPLE)
        self.assertEqual('%r' % p, '%s(%r, %r)' % (p.__class__.__name__, SIMPLE,
                                                   Parameters.DEFAULT_PATH_DELIMITER))
        b.__repr__.assert_called_once_with()

    def test_repr_delimiter(self):
        delim = '%'
        p, b = self._construct_mocked_params(SIMPLE, delim)
        b.__repr__.return_value = repr(SIMPLE)
        self.assertEqual('%r' % p, '%s(%r, %r)' % (p.__class__.__name__, SIMPLE, delim))
        b.__repr__.assert_called_once_with()

    def test_equal_empty(self):
        p1, b1 = self._construct_mocked_params()
        p2, b2 = self._construct_mocked_params()
        b1.__eq__.return_value = True
        self.assertEqual(p1, p2)
        b1.__eq__.assert_called_once_with(b2)

    def test_equal_default_delimiter(self):
        p1, b1 = self._construct_mocked_params(SIMPLE)
        p2, b2 = self._construct_mocked_params(SIMPLE,
                                        Parameters.DEFAULT_PATH_DELIMITER)
        b1.__eq__.return_value = True
        self.assertEqual(p1, p2)
        b1.__eq__.assert_called_once_with(b2)

    def test_equal_contents(self):
        p1, b1 = self._construct_mocked_params(SIMPLE)
        p2, b2 = self._construct_mocked_params(SIMPLE)
        b1.__eq__.return_value = True
        self.assertEqual(p1, p2)
        b1.__eq__.assert_called_once_with(b2)

    def test_unequal_content(self):
        p1, b1 = self._construct_mocked_params()
        p2, b2 = self._construct_mocked_params(SIMPLE)
        b1.__eq__.return_value = False
        self.assertNotEqual(p1, p2)
        b1.__eq__.assert_called_once_with(b2)

    def test_unequal_delimiter(self):
        p1, b1 = self._construct_mocked_params(delimiter=':')
        p2, b2 = self._construct_mocked_params(delimiter='%')
        b1.__eq__.return_value = False
        self.assertNotEqual(p1, p2)
        b1.__eq__.assert_called_once_with(b2)

    def test_unequal_types(self):
        p1, b1 = self._construct_mocked_params()
        self.assertNotEqual(p1, None)
        self.assertEqual(b1.__eq__.call_count, 0)

    def test_construct_wrong_type(self):
        with self.assertRaises(TypeError):
            self._construct_mocked_params('wrong type')

    def test_merge_wrong_type(self):
        p, b = self._construct_mocked_params()
        with self.assertRaises(TypeError):
            p.merge('wrong type')

    def test_get_dict(self):
        p, b = self._construct_mocked_params(SIMPLE)
        self.assertDictEqual(p.as_dict(), SIMPLE)

    def test_merge_scalars(self):
        p1, b1 = self._construct_mocked_params(SIMPLE)
        mergee = {'five':5,'four':4,'None':None,'tuple':(1,2,3)}
        p2, b2 = self._construct_mocked_params(mergee)
        p1.merge(p2)
        for key, value in mergee.iteritems():
            # check that each key, value in mergee resulted in a get call and
            # a __setitem__ call against b1 (the merge target)
            self.assertIn(mock.call(key), b1.get.call_args_list)
            self.assertIn(mock.call(key, value), b1.__setitem__.call_args_list)

    def test_stray_occurrence_overwrites_during_interpolation(self):
        p1 = Parameters({'r' : mock.sentinel.ref, 'b': '${r}'})
        p2 = Parameters({'b' : mock.sentinel.goal})
        p1.merge(p2)
        p1.interpolate()
        self.assertEqual(p1.as_dict()['b'], mock.sentinel.goal)

class TestParametersNoMock(unittest.TestCase):

    def test_merge_scalars(self):
        p = Parameters(SIMPLE)
        mergee = {'five':5,'four':4,'None':None,'tuple':(1,2,3)}
        p.merge(mergee)
        goal = SIMPLE.copy()
        goal.update(mergee)
        self.assertDictEqual(p.as_dict(), goal)

    def test_merge_scalars_overwrite(self):
        p = Parameters(SIMPLE)
        mergee = {'two':5,'four':4,'three':None,'one':(1,2,3)}
        p.merge(mergee)
        goal = SIMPLE.copy()
        goal.update(mergee)
        self.assertDictEqual(p.as_dict(), goal)

    def test_merge_lists(self):
        l1 = [1,2,3]
        l2 = [2,3,4]
        p1 = Parameters(dict(list=l1[:]))
        p2 = Parameters(dict(list=l2))
        p1.merge(p2)
        self.assertListEqual(p1.as_dict()['list'], l1+l2)

    def test_merge_list_into_scalar(self):
        l = ['foo', 1, 2]
        p1 = Parameters(dict(key=l[0]))
        p1.merge(Parameters(dict(key=l[1:])))
        self.assertListEqual(p1.as_dict()['key'], l)

    def test_merge_scalar_over_list(self):
        l = ['foo', 1, 2]
        p1 = Parameters(dict(key=l[:2]))
        p1.merge(Parameters(dict(key=l[2])))
        self.assertEqual(p1.as_dict()['key'], l[2])

    def test_merge_dicts(self):
        mergee = {'five':5,'four':4,'None':None,'tuple':(1,2,3)}
        p = Parameters(dict(dict=SIMPLE))
        p.merge(Parameters(dict(dict=mergee)))
        goal = SIMPLE.copy()
        goal.update(mergee)
        self.assertDictEqual(p.as_dict(), dict(dict=goal))

    def test_merge_dicts_overwrite(self):
        mergee = {'two':5,'four':4,'three':None,'one':(1,2,3)}
        p = Parameters(dict(dict=SIMPLE))
        p.merge(Parameters(dict(dict=mergee)))
        goal = SIMPLE.copy()
        goal.update(mergee)
        self.assertDictEqual(p.as_dict(), dict(dict=goal))

    def test_merge_dicts_override(self):
        """Validate that tilde merge overrides function properly."""
        mergee = {'~one': {'a': 'alpha'},
                  '~two': ['gamma']}
        base = {'one': {'b': 'beta'},
                'two': ['delta']}
        goal = {'one': {'a': 'alpha'},
                'two': ['gamma']}
        p = Parameters(dict(dict=base))
        p.merge(Parameters(dict(dict=mergee)))
        self.assertDictEqual(p.as_dict(), dict(dict=goal))

    def test_merge_dict_into_scalar(self):
        p = Parameters(dict(base='foo'))
        with self.assertRaises(TypeError):
            p.merge(Parameters(dict(base=SIMPLE)))

    def test_merge_scalar_over_dict(self):
        p = Parameters(dict(base=SIMPLE))
        mergee = {'base':'foo'}
        p.merge(Parameters(mergee))
        self.assertDictEqual(p.as_dict(), mergee)

    def test_interpolate_single(self):
        v = 42
        d = {'foo': 'bar'.join(PARAMETER_INTERPOLATION_SENTINELS),
             'bar': v}
        p = Parameters(d)
        p.interpolate()
        self.assertEqual(p.as_dict()['foo'], v)

    def test_interpolate_multiple(self):
        v = '42'
        d = {'foo': 'bar'.join(PARAMETER_INTERPOLATION_SENTINELS) + 'meep'.join(PARAMETER_INTERPOLATION_SENTINELS),
             'bar': v[0],
             'meep': v[1]}
        p = Parameters(d)
        p.interpolate()
        self.assertEqual(p.as_dict()['foo'], v)

    def test_interpolate_multilevel(self):
        v = 42
        d = {'foo': 'bar'.join(PARAMETER_INTERPOLATION_SENTINELS),
             'bar': 'meep'.join(PARAMETER_INTERPOLATION_SENTINELS),
             'meep': v}
        p = Parameters(d)
        p.interpolate()
        self.assertEqual(p.as_dict()['foo'], v)

    def test_interpolate_list(self):
        l = [41,42,43]
        d = {'foo': 'bar'.join(PARAMETER_INTERPOLATION_SENTINELS),
             'bar': l}
        p = Parameters(d)
        p.interpolate()
        self.assertEqual(p.as_dict()['foo'], l)

    def test_interpolate_infrecursion(self):
        v = 42
        d = {'foo': 'bar'.join(PARAMETER_INTERPOLATION_SENTINELS),
             'bar': 'foo'.join(PARAMETER_INTERPOLATION_SENTINELS)}
        p = Parameters(d)
        with self.assertRaises(InfiniteRecursionError):
            p.interpolate()

if __name__ == '__main__':
    unittest.main()
