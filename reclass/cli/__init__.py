#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import sys, os, posix

from reclass.core import Core
from reclass.config import get_options, Config
from reclass.errors import ReclassException
from reclass.defaults import *
from reclass.constants import MODE_NODEINFO
from reclass.logs import init_logger
from reclass.version import *

def main():
    try:
        # option parsing
        options = get_options(RECLASS_NAME, VERSION, DESCRIPTION)
        logger = init_logger(debug=options.debug)
        logger.debug('parsed options: %s' % options)
        # config parsing
        config = Config(opts=options)
        # instantiate reclass core, loads storage/etc from config
        reclass = Core(config)

        # are we looking up a specific node or inventory?
        if options.mode == MODE_NODEINFO:
            data = reclass.nodeinfo(options.nodename)
        else:
            data = reclass.inventory()

        print reclass.output(data)

    except ReclassException, e:
        e.exit_with_message(sys.stderr)

    sys.exit(posix.EX_OK)

if __name__ == '__main__':
    main()
