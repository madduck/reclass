#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import time, sys
from reclass.datatypes import Entity

def _get_timestamp():
    return time.strftime('%c')

def vvv(msg):
    print >>sys.stderr, msg
    pass

class NodeStorageBase(object):

    def __init__(self, nodes_uri, classes_uri):
        self._nodes_uri = nodes_uri
        self._classes_uri = classes_uri
        self._classes_cache = {}

    nodes_uri = property(lambda self: self._nodes_uri)
    classes_uri = property(lambda self: self._classes_uri)

    def _get_storage_name(self):
        raise NotImplementedError, "Storage class does not have a name"

    def _get_node(self, name, merge_base=None):
        raise NotImplementedError, "Storage class not implement node entity retrieval"

    def _get_class(self, name):
        raise NotImplementedError, "Storage class not implement class entity retrieval"

    def _recurse_entity(self, entity, merge_base=None, seen=None, nodename=None):
        if seen is None:
            seen = {}

        if merge_base is None:
            merge_base = Entity(name='empty (@{0})'.format(nodename))

        for klass in entity.classes.as_list():
            if klass not in seen:
                try:
                    class_entity = self._classes_cache[klass]
                except KeyError, e:
                    class_entity, uri = self._get_class(klass)
                    self._classes_cache[klass] = class_entity

                descent = self._recurse_entity(class_entity, seen=seen,
                                               nodename=nodename)
                # on every iteration, we merge the result of the recursive
                # descent into what we have so far…
                merge_base.merge(descent)
                seen[klass] = True

        # … and finally, we merge what we have at this level into the
        # result of the iteration, so that elements at the current level
        # overwrite stuff defined by parents
        merge_base.merge(entity)
        return merge_base

    def _nodeinfo(self, nodename):
        node_entity, uri = self._get_node(nodename)
        merge_base = Entity(name='merge base for {0}'.format(nodename))
        ret = self._recurse_entity(node_entity, merge_base, nodename=nodename)
        ret.interpolate()
        return ret, uri

    def _nodeinfo_as_dict(self, nodename, entity, uri):
        ret = {'__reclass__' : {'node': nodename, 'uri': uri,
                                'timestamp': _get_timestamp()
                                },
              }
        ret.update(entity.as_dict())
        return ret

    def nodeinfo(self, nodename):
        return self._nodeinfo_as_dict(nodename, *self._nodeinfo(nodename))

    def _list_inventory(self):
        raise NotImplementedError, "Storage class does not implement inventory listing"

    def inventory(self):
        entities = self._list_inventory()

        nodes = {}
        applications = {}
        classes = {}
        for f, (nodeinfo, uri) in entities.iteritems():
            d = nodes[f] = self._nodeinfo_as_dict(f, nodeinfo, uri)
            for a in d['applications']:
                if a in applications:
                    applications[a].append(f)
                else:
                    applications[a] = [f]
            for c in d['classes']:
                if c in classes:
                    classes[c].append(f)
                else:
                    classes[c] = [f]

        return {'__reclass__' : {'timestamp': _get_timestamp()},
                'nodes': nodes,
                'classes': classes,
                'applications': applications
               }


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
