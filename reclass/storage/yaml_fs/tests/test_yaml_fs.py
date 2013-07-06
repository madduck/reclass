#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass.storage.yaml_fs import ExternalNodeStorage

import os

POSTFIX = '_hosts'
PWD = os.path.dirname(__file__)
HOSTS = ['red', 'blue', 'green']
APPLICATIONS = {'apt': HOSTS,
                'motd': HOSTS,
                'firewall': HOSTS[:2],
                'lighttpd': HOSTS[:2],
                'postfix': HOSTS[1:],
                'blues': HOSTS[1:2]
               }
CLASSES = {'basenode': HOSTS,
           'debiannode': HOSTS,
           'debiannode@sid': HOSTS[0:1],
           'debiannode@wheezy': HOSTS[2:3],
           'debiannode@squeeze': HOSTS[1:2],
           'hosted@munich': HOSTS[1:2],
           'hosted@zurich': [HOSTS[0], HOSTS[2]],
           'mailserver': HOSTS[1:],
           'webserver': HOSTS[:2]
          }

class TestYamlFs:

    def setUp(self):
        self._storage = ExternalNodeStorage(os.path.join(PWD, 'nodes'),
                                            os.path.join(PWD, 'classes'))
        self._inventory = self._storage.inventory()

    def test_inventory_setup(self):
        assert isinstance(self._inventory, dict)
        assert 'applications' in self._inventory
        assert 'classes' in self._inventory

    def test_inventory_applications(self):
        assert len(self._inventory['applications']) == len(APPLICATIONS)
        for i in APPLICATIONS.iterkeys():
            assert i in self._inventory['applications']
        for app, members in self._inventory['applications'].iteritems():
            for i in APPLICATIONS[app]:
                assert i in members
        for app, members in APPLICATIONS.iteritems():
            for i in self._inventory['applications'][app]:
                assert i in members

    def test_inventory_classes(self):
        assert len(self._inventory['classes']) == len(CLASSES)
        for i in CLASSES.iterkeys():
            assert i in self._inventory['classes']
        for klass, members in self._inventory['classes'].iteritems():
            for i in CLASSES[klass]:
                assert i in members
        for klass, members in CLASSES.iteritems():
            for i in self._inventory['classes'][klass]:
                assert i in members

    def test_host_meta(self):
        for n in HOSTS:
            node = self._storage.nodeinfo(n)
            assert '__reclass__' in node

    def test_host_entities(self):
        for n in HOSTS:
            node = self._storage.nodeinfo(n)
            assert 'applications' in node
            assert 'classes' in node
            assert 'parameters' in node

    def test_merge_empty_dict(self):
        node = self._storage.nodeinfo(HOSTS[0])
        assert 'apt' in node['parameters']
        assert node['parameters']['apt'] is not None

    def test_merge_parameters(self):
        node = self._storage.nodeinfo(HOSTS[1])
        assert node['parameters']['apt']['mirror_base'] == 'uni-erlangen'
