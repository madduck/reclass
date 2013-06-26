#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import time

def _get_timestamp():
    return time.strftime('%c')

class NodeStorageBase(object):

    def __init__(self, nodes_uri, classes_uri, applications_postfix):
        self._nodes_uri = nodes_uri
        self._classes_uri = classes_uri
        self._applications_postfix = applications_postfix

    nodes_uri = property(lambda self: self._nodes_uri)
    classes_uri = property(lambda self: self._classes_uri)

    def _read_entity(self, node, base_uri, seen={}):
        raise NotImplementedError, "Storage class not implement node info retrieval"

    def nodeinfo(self, node):
        entity, uri = self._read_nodeinfo(node, self.nodes_uri, {})
        return {'RECLASS' : {'node': node, 'node_uri': uri,
                                 'timestamp': _get_timestamp()
                                },
                'classes': list(entity.classes),
                'applications': list(entity.applications),
                'parameters': dict(entity.parameters)
               }

    def _list_inventory(self):
        raise NotImplementedError, "Storage class does not implement inventory listing"

    def inventory(self):
        entity, applications, classes = self._list_inventory()
        ret = classes
        ret.update([(k + self._applications_postfix,v) for k,v in applications.iteritems()])
        return ret

class StorageBackendLoader(object):

    def __init__(self, storage_type):
        self._name = 'reclass.storage.' + storage_type
        try:
            self._module = __import__(self._name, globals(), locals(), self._name)
        except ImportError:
            raise NotImplementedError

    def load(self, attr='ExternalNodeStorage'):
        klass = getattr(self._module, attr, None)
        if klass is None:
            raise AttributeError, \
                'Storage backend class {0} does not export "{1}"'.format(self._name, klass)
        return klass
