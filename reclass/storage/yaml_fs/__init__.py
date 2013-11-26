#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os, sys
import fnmatch
from reclass.storage import NodeStorageBase
from yamlfile import YamlFile
from directory import Directory
from reclass.datatypes import Entity
import reclass.errors

FILE_EXTENSION = '.yml'

def vvv(msg):
    #print >>sys.stderr, msg
    pass

class ExternalNodeStorage(NodeStorageBase):

    def __init__(self, nodes_uri, classes_uri, class_mappings):
        super(ExternalNodeStorage, self).__init__(nodes_uri, classes_uri,
                                                  class_mappings)

        def _handle_node_duplicates(name, uri1, uri2):
            raise reclass.errors.DuplicateNodeNameError(self._get_storage_name(),
                                                        name, uri1, uri2)
        self._nodes = self._enumerate_inventory(nodes_uri,
                                                duplicate_handler=_handle_node_duplicates)
        self._classes = self._enumerate_inventory(classes_uri)

    def _get_storage_name(self):
        return 'yaml_fs'

    def _enumerate_inventory(self, basedir, duplicate_handler=None):
        ret = {}
        def register_fn(dirpath, filenames):
            filenames = fnmatch.filter(filenames, '*{0}'.format(FILE_EXTENSION))
            vvv('REGISTER {0} in path {1}'.format(filenames, dirpath))
            for f in filenames:
                name = os.path.splitext(f)[0]
                uri = os.path.join(dirpath, f)
                if name in ret and callable(duplicate_handler):
                    duplicate_handler(name, os.path.join(basedir, ret[name]), uri)
                ret[name] = os.path.relpath(uri, basedir)

        d = Directory(basedir)
        d.walk(register_fn)
        return ret

    def _get_node(self, name):
        vvv('GET NODE {0}'.format(name))
        try:
            path = os.path.join(self.nodes_uri, self._nodes[name])
        except KeyError, e:
            raise reclass.errors.NodeNotFound(self._get_storage_name(),
                                              name, self.nodes_uri)
        entity = YamlFile(path).entity
        return entity

    def _get_class(self, name, nodename=None):
        vvv('GET CLASS {0}'.format(name))
        try:
            path = os.path.join(self.classes_uri, self._classes[name])
        except KeyError, e:
            raise reclass.errors.ClassNotFound(self._get_storage_name(),
                                               name, self.classes_uri,
                                               nodename)
        entity = YamlFile(path).entity
        return entity

    def _list_inventory(self):
        entities = {}
        for n in self._nodes.iterkeys():
            entities[n] = self._nodeinfo(n)
        return entities
