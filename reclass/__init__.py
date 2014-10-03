#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

from output import OutputLoader
from storage.loader import StorageBackendLoader
from storage.memcache_proxy import MemcacheProxy

def get_storage(config, **kwargs):
    storage_class = StorageBackendLoader(config['storage_type']).load()
    return MemcacheProxy(storage_class(config['nodes_uri'],
                                       config['classes_uri'],
                                       **kwargs))


def output(data, fmt, pretty_print=False):
    output_class = OutputLoader(fmt).load()
    outputter = output_class()
    return outputter.dump(data, pretty_print=pretty_print)
