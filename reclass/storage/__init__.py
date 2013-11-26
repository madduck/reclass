#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import time
import types
import re
import sys
import fnmatch
from reclass.datatypes import Entity, Classes

def _get_timestamp():
    return time.strftime('%c')

def vvv(msg):
    print >>sys.stderr, msg
    pass

class NodeStorageBase(object):

    def __init__(self, nodes_uri, classes_uri, class_mappings):
        self._nodes_uri = nodes_uri
        self._classes_uri = classes_uri
        self._classes_cache = {}
        self._class_mappings = class_mappings

    nodes_uri = property(lambda self: self._nodes_uri)
    classes_uri = property(lambda self: self._classes_uri)
    class_mappings = property(lambda self: self._class_mappings)

    def _match_regexp(self, key, nodename):
        return re.search(key, nodename)

    def _match_glob(self, key, nodename):
        return fnmatch.fnmatchcase(nodename, key)

    def _populate_with_class_mappings(self, nodename):
        c = Classes()
        for key, value in self.class_mappings.iteritems():
            match = False
            if key.startswith('/') and key.endswith('/'):
                match = self._match_regexp(key[1:-1], nodename)
            else:
                match = self._match_glob(key, nodename)
            if match:
                if isinstance(value, (types.ListType, types.TupleType)):
                    for v in value:
                        c.append_if_new(v)
                else:
                    c.append_if_new(value)

        return Entity(classes=c,
                      name='class mappings for node {0}'.format(nodename))

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
                    class_entity = self._get_class(klass)
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
        node_entity = self._get_node(nodename)
        merge_base = self._populate_with_class_mappings(nodename)
        ret = self._recurse_entity(node_entity, merge_base, nodename=nodename)
        ret.interpolate()
        return ret

    def _nodeinfo_as_dict(self, nodename, entity):
        ret = {'__reclass__' : {'node': nodename, 'uri': entity.uri,
                                'timestamp': _get_timestamp()
                               },
              }
        ret.update(entity.as_dict())
        return ret

    def nodeinfo(self, nodename):
        return self._nodeinfo_as_dict(nodename, self._nodeinfo(nodename))

    def _list_inventory(self):
        raise NotImplementedError, "Storage class does not implement inventory listing"

    def inventory(self):
        entities = self._list_inventory()

        nodes = {}
        applications = {}
        classes = {}
        for f, nodeinfo in entities.iteritems():
            d = nodes[f] = self._nodeinfo_as_dict(f, nodeinfo)
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
