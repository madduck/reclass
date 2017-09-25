#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–17 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import sys, os, posix

from reclass import get_storage, output
from reclass.core import Core
from reclass.config import find_and_read_configfile, get_options, \
        make_modes_options_group
from reclass.errors import ReclassException
from reclass.defaults import *
from reclass.constants import MODE_NODEINFO
from reclass.version import *

def main():
    try:
        defaults = {'pretty_print' : OPT_PRETTY_PRINT,
                    'output' : OPT_OUTPUT
                   }
        defaults.update(find_and_read_configfile())

        modesdata = dict(
            inventory_shortopt='-i',
            inventory_longopt='--inventory',
            inventory_help='output the entire inventory',
            nodeinfo_shortopt='-n',
            nodeinfo_longopt='--nodeinfo',
            nodeinfo_dest='nodename',
            nodeinfo_help='output information for a specific node',
        )

        def parser_cb(parser, defaults):
            parser.usage = '%prog [options] ( {inventory_longopt} ' \
                           '| {nodeinfo_longopt} {0} )'.\
                    format(modesdata['nodeinfo_dest'].upper(), **modesdata)
            parser.epilog = 'Exactly one mode has to be specified.'

            g, c = make_modes_options_group(parser, **modesdata)
            parser.add_option_group(g)
            return c

        options, args = get_options(RECLASS_NAME, VERSION, DESCRIPTION,
                                    parser_cb, defaults=defaults)

        storage = get_storage(options.storage_type, options.nodes_uri,
                              options.classes_uri, default_environment='base')
        class_mappings = defaults.get('class_mappings')
        reclass = Core(storage, class_mappings)

        if options.mode == MODE_NODEINFO:
            data = reclass.nodeinfo(options.nodename)

        else:
            data = reclass.inventory()

        print output(data, options.output, options.pretty_print)

    except ReclassException, e:
        e.exit_with_message(sys.stderr)

    sys.exit(posix.EX_OK)

if __name__ == '__main__':
    main()
