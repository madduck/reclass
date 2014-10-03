#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os, sys
from version import RECLASS_NAME

# defaults for the command-line options
OPT_STORAGE_TYPE = 'yaml_fs'
OPT_INVENTORY_BASE_URI = os.path.join('/etc', RECLASS_NAME)
OPT_NODES_URI = 'nodes'
OPT_CLASSES_URI = 'classes'
OPT_PRETTY_PRINT = True
OPT_OUTPUT = 'yaml'

CONFIG_FILE_SEARCH_PATH = [os.getcwd(),                 # current directory
                           os.path.expanduser('~'),     # user home
                           OPT_INVENTORY_BASE_URI,      # /etc/reclass
                           os.path.dirname(sys.argv[0]) # path to reclass script
                          ]

CONFIG_FILE_NAME = RECLASS_NAME + '-config.yml'

DEFAULT_CONFIG_LIST = [
    os.path.join(d, CONFIG_FILE_NAME) for d in CONFIG_FILE_SEARCH_PATH
]

DEFAULT_CONFIG = {
    'storage_type': OPT_STORAGE_TYPE,
    'inventory_base_uri': OPT_INVENTORY_BASE_URI,
    'nodes_uri': OPT_NODES_URI,
    'classes_uri': OPT_CLASSES_URI,
    'pretty_print': OPT_PRETTY_PRINT,
    'output': OPT_OUTPUT,
    'debug': False,
    'class_mappings': None,
}


PARAMETER_INTERPOLATION_SENTINELS = ('${', '}')
PARAMETER_INTERPOLATION_DELIMITER = ':'
