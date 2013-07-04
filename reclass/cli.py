#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import sys, os, posix

from reclass import get_nodeinfo, get_inventory, output
from reclass.config import find_and_read_configfile, get_options
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
        options = get_options(RECLASS_NAME, VERSION, DESCRIPTION,
                              defaults=defaults)
        if options.mode == MODE_NODEINFO:
            data = get_nodeinfo(options.storage_type,
                                options.inventory_base_uri, options.nodes_uri,
                                options.classes_uri, options.nodename)
        else:
            data = get_inventory(options.storage_type,
                                 options.inventory_base_uri,
                                 options.nodes_uri, options.classes_uri)

        print output(data, options.output, options.pretty_print)

    except ReclassException, e:
        e.exit_with_message(sys.stderr)

    sys.exit(posix.EX_OK)

if __name__ == '__main__':
    main()
