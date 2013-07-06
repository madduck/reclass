#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from classes import Classes
from parameters import Parameters
from applications import Applications

class Entity(object):

    def __init__(self, classes=None, applications=None, parameters=None,
                 name=None):
        if applications is None: applications = Applications()
        self._applications = applications
        if classes is None: classes = Classes()
        self._classes = classes
        if parameters is None: parameters = Parameters()
        self._parameters = parameters
        self._name = name

    applications = property(lambda self: self._applications)
    classes = property(lambda self: self._classes)
    parameters = property(lambda self: self._parameters)
    name = property(lambda self: self._name)

    def merge(self, other):
        self.classes.merge(other.classes)
        self.applications.merge(other.applications)
        self.parameters.merge(other.parameters)
        self._name = other.name

    def __eq__(self, other):
        return self.applications == other.applications \
                and self.classes == other.classes \
                and self.parameters == other.parameters \
                and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return '<Entity{0} classes:{1} applications:{2}, parameters:{3}>'.format(
            '' if not self.name else " '%s'" % self.name,
            len(self.classes), len(self.applications), len(self.parameters))
