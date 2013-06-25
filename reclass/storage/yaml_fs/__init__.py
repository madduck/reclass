#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os
from reclass.storage import NodeStorageBase
from yamlfile import YamlFile
from directory import Directory
import reclass.errors

FILE_EXTENSION = '.yml'

class ExternalNodeStorage(NodeStorageBase):

    def __init__(self, nodes_uri, classes_uri, applications_postfix):
        super(ExternalNodeStorage, self).__init__(nodes_uri, classes_uri,
                                                  applications_postfix)

    def _read_nodeinfo(self, name, base_uri, seen, nodename=None):
        path = os.path.join(base_uri, name + FILE_EXTENSION)
        try:
            entity = YamlFile(path).entity
            seen[name] = True

            merge_base = None
            for klass in entity.classes:
                if klass not in seen:
                    ret = self._read_nodeinfo(klass, self.classes_uri, seen,
                                              name if nodename is None else nodename)[0]
                    if merge_base is None:
                        # first iteration, initialise the merge base
                        merge_base = ret
                    else:
                        # on every iteration, we merge the result of the
                        # recursive descend into what we have so far…
                        merge_base.merge(ret)

            if merge_base is None:
                # there are no parent classes, at least none we haven't
                # already seen, so we can just return the entity
                return entity, path

            # … and finally, we merge what we have at this level into the
            # result of the iteration, so that elements at the current level
            # overwrite stuff defined by parents
            merge_base.merge(entity)
            return merge_base, path

        except IOError:
            if base_uri == self.classes_uri:
                raise reclass.errors.ClassNotFound('yaml_fs', name, base_uri, nodename)
            else:
                raise reclass.errors.NodeNotFound('yaml_fs', name, base_uri)

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
