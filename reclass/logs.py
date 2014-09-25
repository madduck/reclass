#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import logging.config

from reclass.defaults import RECLASS_NAME


RECLASS_LOGGER = RECLASS_NAME

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
            'level': 'ERROR',
        }
    }
}


def init_logger(debug=False, config={}):
    '''
    Initialize and return an instance of ``logging.logger``, using ``config``
    as a dictionary config, if provided, else use the internal default
    ``LOGGING_CONFIG`` for Reclass. If ``debug`` is ``True``, update the log
    level to ``DEBUG``

    '''
    if not config:
        config = LOGGING_CONFIG
    logging.config.dictConfig(config)
    logger = logging.getLogger(RECLASS_LOGGER)
    if debug:
        logger.setLevel(logging.DEBUG)
    logger.debug('Enabling debug log messages')
    return logger
