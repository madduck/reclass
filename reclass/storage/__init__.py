#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

class NodeStorageBase(object):

    def __init__(self, name):
        self._name = name

    name = property(lambda self: self._name)

    def get_node(self, name, merge_base=None):
        msg = "Storage class '{0}' does not implement node entity retrieval."
        raise NotImplementedError(msg.format(self.name))

    def get_class(self, name):
        msg = "Storage class '{0}' does not implement class entity retrieval."
        raise NotImplementedError(msg.format(self.name))

    def enumerate_nodes(self):
        msg = "Storage class '{0}' does not implement node enumeration."
        raise NotImplementedError(msg.format(self.name))
