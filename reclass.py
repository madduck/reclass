#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# reclass — recursive external node classifier
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
__prog__ = 'reclass'
__description__ = 'classify nodes based on an external data source'
__version__ = '1.0'
__author__ = 'martin f. krafft <madduck@madduck.net>'
__copyright__ = 'Copyright © 2007–13 ' + __author__
__licence__ = 'Artistic Licence 2.0'

import sys, os, posix, time
import config
from output import OutputLoader
from storage import StorageBackendLoader
import errors

def get_options(config_file=None):
    return config.get_options(__name__, __version__, __description__, config_file)

def get_data(storage_type, nodes_uri, classes_uri, applications_postfix, node):
    storage_class = StorageBackendLoader(storage_type).load()
    storage = storage_class(os.path.abspath(os.path.expanduser(nodes_uri)),
                            os.path.abspath(os.path.expanduser(classes_uri)),
                            applications_postfix
                           )
    if node is False:
        ret = storage.inventory()
    else:
        ret = storage.nodeinfo(node)
        ret['RECLASS']['timestamp'] = time.strftime('%c')

    return ret

def output(data, fmt, pretty_print=False):
    output_class = OutputLoader(fmt).load()
    outputter = output_class()
    return outputter.dump(data, pretty_print=pretty_print)

def _error(msg, rc):
    print >>sys.stderr, msg
    sys.exit(rc)

if __name__ == '__main__':
    __name__ = __prog__
    config_file = None
    for d in (os.getcwd(), os.path.dirname(sys.argv[0])):
        f = os.path.join(d, __name__ + '-config.yml')
        if os.access(f, os.R_OK):
            config_file = f
            break
    try:
        options = get_options(config_file)
        data = get_data(options.storage_type, options.nodes_uri,
                        options.classes_uri, options.applications_postfix,
                        options.node)
        print output(data, options.output, options.pretty_print)
        sys.exit(posix.EX_OK)

    except errors.ReclassException, e:
        _error(e.message, e.rc)
