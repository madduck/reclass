#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import logging.config

from reclass.config import get_options
from reclass.defaults import RECLASS_NAME
from reclass.version import VERSION, DESCRIPTION


RECLASS_LOGGER = 'reclass'

options = get_options(RECLASS_NAME, VERSION, DESCRIPTION)
LOG_LEVEL = 'ERROR'
if options.debug:
    LOG_LEVEL = 'DEBUG'


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        }
    },
    'loggers': {
        RECLASS_LOGGER: {
            'handlers': ['stderr'],
            'level': LOG_LEVEL,
        }
    }
}


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(RECLASS_LOGGER)
logger.debug('Enabling debug log messages')
