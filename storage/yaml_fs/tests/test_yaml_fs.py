#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from storage.yaml_fs import ExternalNodeStorage

import os

PWD = os.path.dirname(__file__)
HOSTS = ['red', 'blue', 'green']
MEMBERSHIPS = {'apt_hosts': HOSTS,
               'motd_hosts': HOSTS,
               'firewall_hosts': HOSTS[:2],
               'lighttpd_hosts': HOSTS[:2],
               'postfix_hosts': HOSTS[1:],
               'basenode': HOSTS,
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
        assert len(self._inventory) == len(MEMBERSHIPS)
        for i in MEMBERSHIPS.iterkeys():
            assert i in self._inventory

    def test_inventory_memberships(self):
        for app, members in self._inventory.iteritems():
            for i in MEMBERSHIPS[app]:
                print i
                assert i in members
        for app, members in MEMBERSHIPS.iteritems():
            for i in self._inventory[app]:
                print i
                assert i in members

    def test_host_meta(self):
        for n in HOSTS:
            node = self._storage.nodeinfo(n)
            assert 'RECLASS' in node

    def test_host_entity(self):
        for n in HOSTS:
            node = self._storage.nodeinfo(n)
            assert 'applications' in node
            assert 'classes' in node
            assert 'parameters' in node
