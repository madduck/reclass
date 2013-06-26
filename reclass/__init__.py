#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

from output import OutputLoader
from storage import StorageBackendLoader

def get_data(storage_type, nodes_uri, classes_uri, applications_postfix, node):
    storage_class = StorageBackendLoader(storage_type).load()
    storage = storage_class(nodes_uri, classes_uri, applications_postfix)
    if node is False:
        ret = storage.inventory()
    else:
        ret = storage.nodeinfo(node)

    return ret

def output(data, fmt, pretty_print=False):
    output_class = OutputLoader(fmt).load()
    outputter = output_class()
    return outputter.dump(data, pretty_print=pretty_print)
