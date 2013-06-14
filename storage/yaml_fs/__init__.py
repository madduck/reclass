#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os
from storage import NodeStorageBase
from yamlfile import YamlFile
from directory import Directory

FILE_EXTENSION = '.yml'

class ExternalNodeStorage(NodeStorageBase):

    def __init__(self, nodes_uri, classes_uri):
        super(ExternalNodeStorage, self).__init__(nodes_uri, classes_uri)

    def _read_nodeinfo(self, name, base_uri, seen):
        path = os.path.join(base_uri, name + FILE_EXTENSION)
        entity = YamlFile(path).entity
        seen[name] = True
        for klass in entity.classes:
            if klass not in seen:
                ret = self._read_nodeinfo(klass, self.classes_uri, seen)[0]
                ret.merge(entity)
                entity = ret
        return entity, path

    def _list_inventory(self):
        d = Directory(self.nodes_uri)

        entities = {}

        def register_fn(dirpath, filenames):
            for f in filter(lambda f: f.endswith(FILE_EXTENSION), filenames):
                name = f[:-len(FILE_EXTENSION)]
                nodeinfo = self.nodeinfo(name)
                entities[name] = nodeinfo

        d.walk(register_fn)

        applications = {}
        classes = {}
        for f, nodeinfo in entities.iteritems():
            for a in nodeinfo['applications']:
                if a in applications:
                    applications[a].append(f)
                else:
                    applications[a] = [f]
            for c in nodeinfo['classes']:
                if c in classes:
                    classes[c].append(f)
                else:
                    classes[c] = [f]

        return entities, applications, classes
