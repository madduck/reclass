#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import datatypes
import yaml

class YamlFile(object):

    def __init__(self, path):
        ''' Initialise a yamlfile object '''
        self._path = path
        self._data = dict()
        self._read()

    def _read(self):
        fp = file(self._path)
        self._data = yaml.safe_load(fp)
        self._name = self._data.get('name', self._path)
        fp.close()

    name = property(lambda self: self._name)

    def _get_entity(self):
        classes = datatypes.Classes(self._data.get('classes', []))
        parameters = datatypes.Parameters(self._data.get('parameters', {}))
        applications = datatypes.Applications(self._data.get('applications', []))
        return datatypes.Entity(classes, parameters, applications)
    entity = property(lambda self: self._get_entity())

    def __repr__(self):
        return '<{0} {1}, {2}>'.format(self.__class__.__name__, self._name,
                                       self._data.keys())
