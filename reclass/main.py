#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from version import *

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
        f = os.path.join(d, RECLASS_NAME + '-config.yml')
        if os.access(f, os.R_OK):
            config_file = f
            break
    try:
        defaults = { 'pretty_print' : True, 'output' : 'yaml' }
        options = reclass.config.get_options(RECLASS_NAME, VERSION, DESCRIPTION,
                                             config_file, defaults)
        nodes_uri, classes_uri = reclass.config.path_mangler(options.inventory_base_uri,
                                                                options.nodes_uri,
                                                                options.classes_uri)
        data = get_data(options.storage_type, nodes_uri, classes_uri,
                        options.node)
        print output(data, options.output, options.pretty_print)
        sys.exit(posix.EX_OK)

    except reclass.errors.ReclassException, e:
        _error(e.message, e.rc)
