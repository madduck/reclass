#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass import datatypes
import yaml
import os
from reclass.errors import NotFoundError

class YamlFile(object):

    def __init__(self, path):
        ''' Initialise a yamlfile object '''
        if not os.path.isfile(path):
            raise NotFoundError('No such file: %s' % path)
        if not os.access(path, os.R_OK):
            raise NotFoundError('Cannot open: %s' % path)
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

    def get_entity(self, name=None, default_environment=None):
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

        env = self._data.get('environment', default_environment)

        if name is None:
            name = self._path

        return datatypes.Entity(classes, applications, parameters,
                                name=name, environment=env,
                                uri='yaml_fs://{0}'.format(self._path))

    def __repr__(self):
        return '<{0} {1}, {2}>'.format(self.__class__.__name__, self._path,
                                       self._data.keys())
