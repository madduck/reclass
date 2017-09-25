#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–17 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import os, sys, posix

from reclass import get_storage, output
from reclass.core import Core
from reclass.errors import ReclassException
from reclass.config import find_and_read_configfile, get_options
from reclass.constants import MODE_NODEINFO
from reclass.defaults import *
from reclass.version import *

def nodeinfo(nodename,
             storage_type=OPT_STORAGE_TYPE,
             inventory_base_uri=OPT_INVENTORY_BASE_URI,
             nodes_uri=OPT_NODES_URI,
             classes_uri=OPT_CLASSES_URI,
             class_mappings=None):

    storage = get_storage(storage_type, nodes_uri, classes_uri,
                          default_environment='production')

    reclass = Core(storage, class_mappings)

    return reclass.nodeinfo(nodename)


def cli():
    try:
        defaults = {'pretty_print' : True,
                    'output' : 'yaml',
                   }
        defaults.update(find_and_read_configfile())

        def parser_cb(parser, defaults):
            parser.usage = '%prog [options] HOSTNAME'
            parser.epilog = ''

            def arg_checker(options, args):
                if len(args) != 1:
                    parser.error('Need exactly one host name')
                elif options.inventory_base_uri is None and options.nodes_uri is None:
                    parser.error('Must specify --inventory-base-uri or --nodes-uri')
                elif options.inventory_base_uri is None and options.classes_uri is None:
                    parser.error('Must specify --inventory-base-uri or --classes-uri')

            return arg_checker

        options, args = get_options(RECLASS_NAME, VERSION, DESCRIPTION,
                                    parser_cb, defaults=defaults)
        class_mappings = defaults.get('class_mappings')

        data = nodeinfo(args[0],
                        storage_type=options.storage_type,
                        inventory_base_uri=options.inventory_base_uri,
                        nodes_uri=options.nodes_uri,
                        classes_uri=options.classes_uri,
                        class_mappings=class_mappings)

        print output(data, options.output, options.pretty_print)

    except ReclassException, e:
        e.exit_with_message(sys.stderr)

    sys.exit(posix.EX_OK)

if __name__ == '__main__':
    cli()
