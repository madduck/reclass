#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from classes import Classes
from applications import Applications
from parameters import Parameters

class Entity(object):
    '''
    A collection of Classes, Parameters, and Applications, mainly as a wrapper
    for merging. The name and uri of an Entity will be updated to the name and
    uri of the Entity that is being merged.
    '''
    def __init__(self, classes=None, applications=None, parameters=None,
                 uri=None, name=None, environment=None):
        if classes is None: classes = Classes()
        self._set_classes(classes)
        if applications is None: applications = Applications()
        self._set_applications(applications)
        if parameters is None: parameters = Parameters()
        self._set_parameters(parameters)
        self._uri = uri or ''
        self._name = name or ''
        self._environment = environment or ''

    name = property(lambda s: s._name)
    uri = property(lambda s: s._uri)
    environment = property(lambda s: s._environment)
    classes = property(lambda s: s._classes)
    applications = property(lambda s: s._applications)
    parameters = property(lambda s: s._parameters)

    def _set_classes(self, classes):
        if not isinstance(classes, Classes):
            raise TypeError('Entity.classes cannot be set to '\
                            'instance of type %s' % type(classes))
        self._classes = classes

    def _set_applications(self, applications):
        if not isinstance(applications, Applications):
            raise TypeError('Entity.applications cannot be set to '\
                            'instance of type %s' % type(applications))
        self._applications = applications

    def _set_parameters(self, parameters):
        if not isinstance(parameters, Parameters):
            raise TypeError('Entity.parameters cannot be set to '\
                            'instance of type %s' % type(parameters))
        self._parameters = parameters

    def merge(self, other):
        self._classes.merge_unique(other._classes)
        self._applications.merge_unique(other._applications)
        self._parameters.merge(other._parameters)
        self._name = other.name
        self._uri = other.uri
        self._environment = other.environment

    def interpolate(self):
        self._parameters.interpolate()

    def __eq__(self, other):
        return isinstance(other, type(self)) \
                and self._applications == other._applications \
                and self._classes == other._classes \
                and self._parameters == other._parameters \
                and self._name == other._name \
                and self._uri == other._uri

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%r, %r, %r, uri=%r, name=%r)" % (self.__class__.__name__,
                                                    self.classes,
                                                    self.applications,
                                                    self.parameters,
                                                    self.uri,
                                                    self.name)

    def as_dict(self):
        return {'classes': self._classes.as_list(),
                'applications': self._applications.as_list(),
                'parameters': self._parameters.as_dict(),
                'environment': self._environment
               }
