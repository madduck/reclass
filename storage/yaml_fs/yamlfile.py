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
    path = property(lambda self: self._path)

    def _read(self):
        fp = file(self._path)
        data = yaml.safe_load(fp)
        if data is not None:
            self._data = data
        fp.close()

    def _get_entity(self):
        classes = self._data.get('classes')
        if classes is None:
            classes = []
        classes = datatypes.Classes(classes)

        applications = self._data.get('applications')
        if applications is None:
            applications = []
        applications = datatypes.Applications(applications)

        parameters = self._data.get('parameters')
        if parameters is None:
            parameters = {}
        parameters = datatypes.Parameters(parameters)

        return datatypes.Entity(classes, applications, parameters)
    entity = property(lambda self: self._get_entity())

    def __repr__(self):
        return '<{0} {1}, {2}>'.format(self.__class__.__name__, self._path,
                                       self._data.keys())
