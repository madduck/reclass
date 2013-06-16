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

    def __init__(self, classes=Classes(), applications=Applications(),
                 parameters=Parameters()):
        self._applications = applications
        self._classes = classes
        self._parameters = parameters

    applications = property(lambda self: self._applications)
    classes = property(lambda self: self._classes)
    parameters = property(lambda self: self._parameters)

    def merge(self, other):
        self.applications.merge(other.applications)
        self.classes.merge(other.classes)
        self.parameters.merge(other.parameters)

    def __repr__(self):
        return '<Entity classes:{0} applications:{1}, parameters:{2}>'.format(
            len(self.classes), len(self.applications), len(self.parameters))
