#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import sys, os, posix

from reclass import get_storage, output
from reclass.core import Core
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
