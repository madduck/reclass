#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

'''
Argh-compatible Commands for Shell Scripts
------------------------------------------

Here we define the basic commands (functions) dispatched by ``argh``. Define
arguments and build our option parser with function decorators, it is simple
and clear.

'''
import logging

from argh.decorators import arg, aliases

from reclass.core import Core
from reclass.config import Config
from reclass.logs import init_logger


@arg('-o', '--output', help='output format (yaml or json)')
@arg('-d', '--debug', default=False, help='Flag to enable debug logging')
@arg('-i', '--inventory-base-uri', default=None,
     help='The base URI to prepend to nodes and classes')
# this is registered as a positional, required argument
@arg('nodename', help='Name of the node to query for')
# this is not working for some reason..
@aliases('info')
def nodeinfo(**options):
    logger = init_logger(debug=options['debug'])
    logger.debug('parsed options: %s' % options)
    # config parsing
    config = Config(opts=options)
    # instantiate reclass core, loads storage/etc from config
    reclass = Core(config)
    # retrieve and print data
    data = reclass.nodeinfo(options['nodename'])
    print reclass.output(data)


@arg('-o', '--output', help='output format (yaml or json)')
@arg('-d', '--debug', default=False, help='Flag to enable debug logging')
@arg('-i', '--inventory-base-uri', default=None,
     help='The base URI to prepend to nodes and classes')
@aliases('inv')
def inventory(**options):
    '''
    List the complete Reclass inventory given the ``options`` and configuration
    provided/referencred.

    '''
    logger = init_logger(debug=options['debug'])
    logger.debug('parsed options: %s' % options)
    # config parsing
    config = Config(opts=options)
    # instantiate reclass core, loads storage/etc from config
    reclass = Core(config)
    # retrieve and print data
    data = reclass.inventory()
    print reclass.output(data)


#@arg('--test', default=False, help='Flag to enable test/noop mode')
def salt(options):
    '''
    Placeholder argh-compatible command for use with the reclass-salt script
    and SaltAdapter().

    '''
    pass


#@arg('--test', default=False, help='Flag to enable test/noop mode')
def ansible(options):
    '''
    Placeholder argh-compatible command for use with the reclass-ansible script
    and AnsibleAdapter().

    '''
    pass
