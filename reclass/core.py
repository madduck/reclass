#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import time
#import types
import re
#import sys
import fnmatch
import shlex
from reclass.datatypes import Entity, Classes, Parameters
from reclass.errors import MappingFormatError, ClassNotFound

class Core(object):

    def __init__(self, storage, class_mappings, input_data=None):
        self._storage = storage
        self._class_mappings = class_mappings
        self._input_data = input_data

    @staticmethod
    def _get_timestamp():
        return time.strftime('%c')

    @staticmethod
    def _match_regexp(key, nodename):
        return re.search(key, nodename)

    @staticmethod
    def _match_glob(key, nodename):
        return fnmatch.fnmatchcase(nodename, key)

    @staticmethod
    def _shlex_split(instr):
        lexer = shlex.shlex(instr, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = ''
        regexp = False
        if instr[0] == '/':
            lexer.quotes += '/'
            lexer.escapedquotes += '/'
            regexp = True
        try:
            key = lexer.get_token()
        except ValueError, e:
            raise MappingFormatError('Error in mapping "{0}": missing closing '
                                     'quote (or slash)'.format(instr))
        if regexp:
            key = '/{0}/'.format(key)
        return key, list(lexer)

    def _get_class_mappings_entity(self, nodename):
        if not self._class_mappings:
            return Entity(name='empty (class mappings)')
        c = Classes()
        for mapping in self._class_mappings:
            matched = False
            key, klasses = Core._shlex_split(mapping)
            if key[0] == ('/'):
                matched = Core._match_regexp(key[1:-1], nodename)
                if matched:
                    for klass in klasses:
                        c.append_if_new(matched.expand(klass))

            else:
                if Core._match_glob(key, nodename):
                    for klass in klasses:
                        c.append_if_new(klass)

        return Entity(classes=c,
                      name='class mappings for node {0}'.format(nodename))

    def _get_input_data_entity(self):
        if not self._input_data:
            return Entity(name='empty (input data)')
        p = Parameters(self._input_data)
        return Entity(parameters=p, name='input data')

    def _recurse_entity(self, entity, merge_base=None, seen=None, nodename=None):
        if seen is None:
            seen = {}

        if merge_base is None:
            merge_base = Entity(name='empty (@{0})'.format(nodename))

        for klass in entity.classes.as_list():
            if klass not in seen:
                try:
                    class_entity = self._storage.get_class(klass)
                except ClassNotFound, e:
                    e.set_nodename(nodename)
                    raise e

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
        node_entity = self._storage.get_node(nodename)
        base_entity = Entity(name='base')
        base_entity.merge(self._get_class_mappings_entity(node_entity.name))
        base_entity.merge(self._get_input_data_entity())
        seen = {}
        merge_base = self._recurse_entity(base_entity, seen=seen,
                                          nodename=base_entity.name)
        ret = self._recurse_entity(node_entity, merge_base, seen=seen,
                                   nodename=node_entity.name)
        ret.interpolate()
        return ret

    def _nodeinfo_as_dict(self, nodename, entity):
        ret = {'__reclass__' : {'node': entity.name, 'name': nodename,
                                'uri': entity.uri,
                                'environment': entity.environment,
                                'timestamp': Core._get_timestamp()
                               },
              }
        ret.update(entity.as_dict())
        return ret

    def nodeinfo(self, nodename):
        return self._nodeinfo_as_dict(nodename, self._nodeinfo(nodename))

    def inventory(self):
        entities = {}
        for n in self._storage.enumerate_nodes():
            entities[n] = self._nodeinfo(n)

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

        return {'__reclass__' : {'timestamp': Core._get_timestamp()},
                'nodes': nodes,
                'classes': classes,
                'applications': applications
               }
