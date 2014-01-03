#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.datatypes import Entity, Classes, Parameters, Applications
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

@mock.patch.multiple('reclass.datatypes', autospec=True, Classes=mock.DEFAULT,
                     Applications=mock.DEFAULT,
                     Parameters=mock.DEFAULT)
class TestEntity(unittest.TestCase):

    def _make_instances(self, Classes, Applications, Parameters):
        return Classes(), Applications(), Parameters()

    def test_constructor_default(self, **mocks):
        # Actually test the real objects by calling the default constructor,
        # all other tests shall pass instances to the constructor
        e = Entity()
        self.assertEqual(e.name, '')
        self.assertEqual(e.uri, '')
        self.assertIsInstance(e.classes, Classes)
        self.assertIsInstance(e.applications, Applications)
        self.assertIsInstance(e.parameters, Parameters)

    def test_constructor_empty(self, **types):
        instances = self._make_instances(**types)
        e = Entity(*instances)
        self.assertEqual(e.name, '')
        self.assertEqual(e.uri, '')
        cl, al, pl = [getattr(i, '__len__') for i in instances]
        self.assertEqual(len(e.classes), cl.return_value)
        cl.assert_called_once_with()
        self.assertEqual(len(e.applications), al.return_value)
        al.assert_called_once_with()
        self.assertEqual(len(e.parameters), pl.return_value)
        pl.assert_called_once_with()

    def test_constructor_empty_named(self, **types):
        name = 'empty'
        e = Entity(*self._make_instances(**types), name=name)
        self.assertEqual(e.name, name)

    def test_constructor_empty_uri(self, **types):
        uri = 'test://uri'
        e = Entity(*self._make_instances(**types), uri=uri)
        self.assertEqual(e.uri, uri)

    def test_constructor_empty_env(self, **types):
        env = 'not base'
        e = Entity(*self._make_instances(**types), environment=env)
        self.assertEqual(e.environment, env)

    def test_equal_empty(self, **types):
        instances = self._make_instances(**types)
        self.assertEqual(Entity(*instances), Entity(*instances))
        for i in instances:
            i.__eq__.assert_called_once_with(i)

    def test_equal_empty_named(self, **types):
        instances = self._make_instances(**types)
        self.assertEqual(Entity(*instances), Entity(*instances))
        name = 'empty'
        self.assertEqual(Entity(*instances, name=name),
                         Entity(*instances, name=name))

    def test_unequal_empty_uri(self, **types):
        instances = self._make_instances(**types)
        uri = 'test://uri'
        self.assertNotEqual(Entity(*instances, uri=uri),
                            Entity(*instances, uri=uri[::-1]))
        for i in instances:
            i.__eq__.assert_called_once_with(i)

    def test_unequal_empty_named(self, **types):
        instances = self._make_instances(**types)
        name = 'empty'
        self.assertNotEqual(Entity(*instances, name=name),
                            Entity(*instances, name=name[::-1]))
        for i in instances:
            i.__eq__.assert_called_once_with(i)

    def test_unequal_types(self, **types):
        instances = self._make_instances(**types)
        self.assertNotEqual(Entity(*instances, name='empty'),
                            None)
        for i in instances:
            self.assertEqual(i.__eq__.call_count, 0)

    def _test_constructor_wrong_types(self, which_replace, **types):
        instances = self._make_instances(**types)
        instances[which_replace] = 'Invalid type'
        e = Entity(*instances)

    def test_constructor_wrong_type_classes(self, **types):
        self.assertRaises(TypeError, self._test_constructor_wrong_types, 0)

    def test_constructor_wrong_type_applications(self, **types):
        self.assertRaises(TypeError, self._test_constructor_wrong_types, 1)

    def test_constructor_wrong_type_parameters(self, **types):
        self.assertRaises(TypeError, self._test_constructor_wrong_types, 2)

    def test_merge(self, **types):
        instances = self._make_instances(**types)
        e = Entity(*instances)
        e.merge(e)
        for i, fn in zip(instances, ('merge_unique', 'merge_unique', 'merge')):
            getattr(i, fn).assert_called_once_with(i)

    def test_merge_newname(self, **types):
        instances = self._make_instances(**types)
        newname = 'newname'
        e1 = Entity(*instances, name='oldname')
        e2 = Entity(*instances, name=newname)
        e1.merge(e2)
        self.assertEqual(e1.name, newname)

    def test_merge_newuri(self, **types):
        instances = self._make_instances(**types)
        newuri = 'test://uri2'
        e1 = Entity(*instances, uri='test://uri1')
        e2 = Entity(*instances, uri=newuri)
        e1.merge(e2)
        self.assertEqual(e1.uri, newuri)

    def test_merge_newenv(self, **types):
        instances = self._make_instances(**types)
        newenv = 'new env'
        e1 = Entity(*instances, environment='env')
        e2 = Entity(*instances, environment=newenv)
        e1.merge(e2)
        self.assertEqual(e1.environment, newenv)

    def test_as_dict(self, **types):
        instances = self._make_instances(**types)
        entity = Entity(*instances, name='test', environment='test')
        comp = {}
        comp['classes'] = instances[0].as_list()
        comp['applications'] = instances[1].as_list()
        comp['parameters'] = instances[2].as_dict()
        comp['environment'] = 'test'
        d = entity.as_dict()
        self.assertDictEqual(d, comp)


if __name__ == '__main__':
    unittest.main()
