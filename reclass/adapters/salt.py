#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import os, sys, posix

from reclass import get_nodeinfo, get_inventory, output
from reclass.errors import ReclassException
from reclass.config import find_and_read_configfile, get_options
from reclass.constants import MODE_NODEINFO
from reclass.defaults import *
from reclass.version import *

def ext_pillar(minion_id, pillar,
               storage_type=OPT_STORAGE_TYPE,
               inventory_base_uri=OPT_INVENTORY_BASE_URI,
               nodes_uri=OPT_NODES_URI,
               classes_uri=OPT_CLASSES_URI):

    data = get_nodeinfo(storage_type, inventory_base_uri, nodes_uri,
                        classes_uri, minion_id)
    params = data.get('parameters', {})
    params['__reclass__'] = {}
    params['__reclass__']['applications'] = data['applications']
    params['__reclass__']['classes'] = data['classes']
    return params


def top(minion_id, storage_type=OPT_STORAGE_TYPE,
        inventory_base_uri=OPT_INVENTORY_BASE_URI, nodes_uri=OPT_NODES_URI,
        classes_uri=OPT_CLASSES_URI):

    env = 'base'
    # TODO: node environments

    # if the minion_id is not None, then return just the applications for the
    # specific minion, otherwise return the entire top data (which we need for
    # CLI invocations of the adapter):
    if minion_id is not None:
        data = get_nodeinfo(storage_type, inventory_base_uri, nodes_uri,
                            classes_uri, minion_id)
        applications = data.get('applications', [])
        return {env: applications}

    else:
        data = get_inventory(storage_type, inventory_base_uri, nodes_uri,
                            classes_uri)
        nodes = {}
        for node_id, node_data in data['nodes'].iteritems():
            nodes[node_id] = node_data['applications']

        return {env: nodes}


def cli():
    try:
        inventory_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        defaults = {'pretty_print' : True,
                    'output' : 'yaml',
                    'inventory_base_uri': inventory_dir
                   }
        defaults.update(find_and_read_configfile())
        options = get_options(RECLASS_NAME, VERSION, DESCRIPTION,
                              inventory_shortopt='-t',
                              inventory_longopt='--top',
                              inventory_help='output the state tops (inventory)',
                              nodeinfo_shortopt='-p',
                              nodeinfo_longopt='--pillar',
                              nodeinfo_dest='nodename',
                              nodeinfo_help='output pillar data for a specific node',
                              defaults=defaults)

        if options.mode == MODE_NODEINFO:
            data = ext_pillar(options.nodename, {},
                              storage_type=options.storage_type,
                              inventory_base_uri=options.inventory_base_uri,
                              nodes_uri=options.nodes_uri,
                              classes_uri=options.classes_uri)
        else:
            data = top(minion_id=None,
                       storage_type=options.storage_type,
                       inventory_base_uri=options.inventory_base_uri,
                       nodes_uri=options.nodes_uri,
                       classes_uri=options.classes_uri)

        print output(data, options.output, options.pretty_print)

    except ReclassException, e:
        e.exit_with_message(sys.stderr)

    sys.exit(posix.EX_OK)

if __name__ == '__main__':
    cli()
