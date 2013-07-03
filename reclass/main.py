#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# reclass — recursive external node classifier
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from version import __name__, __description__ , __version__, \
        __author__, __copyright__, __licence__

import sys, os, posix
import reclass.config
from reclass.output import OutputLoader
from reclass.storage import StorageBackendLoader
import reclass.errors
from reclass import get_data, output

def _error(msg, rc):
    print >>sys.stderr, msg
    sys.exit(rc)

def run():
    config_file = None
    for d in (os.getcwd(), os.path.dirname(sys.argv[0])):
        f = os.path.join(d, __name__ + '-config.yml')
        if os.access(f, os.R_OK):
            config_file = f
            break
    try:
        defaults = { 'pretty_print' : True, 'output' : 'yaml' }
        options = reclass.config.get_options(__name__, __version__,
                                             __description__, config_file,
                                             defaults)
        nodes_uri, classes_uri = reclass.config.path_mangler(options.inventory_base_uri,
                                                                options.nodes_uri,
                                                                options.classes_uri)
        data = get_data(options.storage_type, nodes_uri, classes_uri,
                        options.node)
        print output(data, options.output, options.pretty_print)
        sys.exit(posix.EX_OK)

    except reclass.errors.ReclassException, e:
        _error(e.message, e.rc)
