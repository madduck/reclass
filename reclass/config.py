#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import yaml, os, optparse, posix, sys

import errors
from defaults import *
from constants import MODE_NODEINFO, MODE_INVENTORY

def make_db_options_group(parser, defaults={}):
    ret = optparse.OptionGroup(parser, 'Database options',
                               'Configure from where {0} collects data'.format(parser.prog))
    ret.add_option('-s', '--storage-type', dest='storage_type',
                   default=defaults.get('storage_type', OPT_STORAGE_TYPE),
                   help='the type of storage backend to use [%default]')
    ret.add_option('-b', '--inventory-base-uri', dest='inventory_base_uri',
                   default=defaults.get('inventory_base_uri',
                                        OPT_INVENTORY_BASE_URI),
                   help='the base URI to prepend to nodes and classes [%default]'),
    ret.add_option('-u', '--nodes-uri', dest='nodes_uri',
                   default=defaults.get('nodes_uri', OPT_NODES_URI),
                   help='the URI to the nodes storage [%default]'),
    ret.add_option('-c', '--classes-uri', dest='classes_uri',
                   default=defaults.get('classes_uri', OPT_CLASSES_URI),
                   help='the URI to the classes storage [%default]')
    return ret


def make_output_options_group(parser, defaults={}):
    ret = optparse.OptionGroup(parser, 'Output options',
                               'Configure the way {0} prints data'.format(parser.prog))
    ret.add_option('-o', '--output', dest='output',
                   default=defaults.get('output', OPT_OUTPUT),
                   help='output format (yaml or json) [%default]')
    ret.add_option('-y', '--pretty-print', dest='pretty_print',
                   action="store_true",
                   default=defaults.get('pretty_print', OPT_PRETTY_PRINT),
                   help='try to make the output prettier [%default]')
    return ret


def make_modes_options_group(parser, inventory_shortopt, inventory_longopt,
                             inventory_help, nodeinfo_shortopt,
                             nodeinfo_longopt, nodeinfo_dest, nodeinfo_help):

    def _mode_checker_cb(option, opt_str, value, parser):
        if hasattr(parser.values, 'mode'):
            raise optparse.OptionValueError('Cannot specify multiple modes')

        if option == parser.get_option(nodeinfo_longopt):
            setattr(parser.values, 'mode', MODE_NODEINFO)
            setattr(parser.values, nodeinfo_dest, value)
        else:
            setattr(parser.values, 'mode', MODE_INVENTORY)
            setattr(parser.values, nodeinfo_dest, None)

    ret = optparse.OptionGroup(parser, 'Modes',
                               'Specify one of these to determine what to do.')
    ret.add_option(inventory_shortopt, inventory_longopt,
                   action='callback', callback=_mode_checker_cb,
                   help=inventory_help)
    ret.add_option(nodeinfo_shortopt, nodeinfo_longopt,
                   default=None, dest=nodeinfo_dest, type='string',
                   action='callback', callback=_mode_checker_cb,
                   help=nodeinfo_help)
    return ret


def make_parser_and_checker(name, version, description,
                            inventory_shortopt='-i',
                            inventory_longopt='--inventory',
                            inventory_help='output the entire inventory',
                            nodeinfo_shortopt='-n',
                            nodeinfo_longopt='--nodeinfo',
                            nodeinfo_dest='nodename',
                            nodeinfo_help='output information for a specific node',
                            add_options_cb=None,
                            defaults={}):

    parser = optparse.OptionParser(version=version)
    parser.prog = name
    parser.version = version
    parser.description = description.capitalize()
    parser.usage = '%prog [options] ( {0} | {1} {2} )'.format(inventory_longopt,
                                                             nodeinfo_longopt,
                                                             nodeinfo_dest.upper())
    parser.epilog = 'Exactly one mode has to be specified.'

    db_group = make_db_options_group(parser, defaults)
    parser.add_option_group(db_group)

    output_group = make_output_options_group(parser, defaults)
    parser.add_option_group(output_group)

    if callable(add_options_cb):
        add_options_cb(parser, defaults)

    modes_group = make_modes_options_group(parser, inventory_shortopt,
                                           inventory_longopt, inventory_help,
                                           nodeinfo_shortopt,
                                           nodeinfo_longopt, nodeinfo_dest,
                                           nodeinfo_help)
    parser.add_option_group(modes_group)

    def option_checker(options, args):
        if len(args) > 0:
            parser.error('No arguments allowed')
        elif not hasattr(options, 'mode') \
                or options.mode not in (MODE_NODEINFO, MODE_INVENTORY):
            parser.error('You need to specify exactly one mode '\
                         '({0} or {1})'.format(inventory_longopt,
                                               nodeinfo_longopt))
        elif options.mode == MODE_NODEINFO \
                and not getattr(options, nodeinfo_dest, None):
            parser.error('Mode {0} needs {1}'.format(nodeinfo_longopt,
                                                     nodeinfo_dest.upper()))
        elif options.inventory_base_uri is None and options.nodes_uri is None:
            parser.error('Must specify --inventory-base-uri or --nodes-uri')
        elif options.inventory_base_uri is None and options.classes_uri is None:
            parser.error('Must specify --inventory-base-uri or --classes-uri')

    return parser, option_checker


def path_mangler(inventory_base_uri, nodes_uri, classes_uri):

    if inventory_base_uri is None:
        # if inventory_base is not given, default to current directory
        inventory_base_uri = os.getcwd()

    nodes_uri = nodes_uri or 'nodes'
    classes_uri = classes_uri or 'classes'

    def _path_mangler_inner(path):
        ret = os.path.join(inventory_base_uri, path)
        ret = os.path.expanduser(ret)
        return os.path.abspath(ret)

    n, c = map(_path_mangler_inner, (nodes_uri, classes_uri))
    if n == c:
        raise errors.DuplicateUriError(n, c)
    common = os.path.commonprefix((n, c))
    if common == n or common == c:
        raise errors.UriOverlapError(n, c)

    return n, c


def get_options(name, version, description,
                            inventory_shortopt='-i',
                            inventory_longopt='--inventory',
                            inventory_help='output the entire inventory',
                            nodeinfo_shortopt='-n',
                            nodeinfo_longopt='--nodeinfo',
                            nodeinfo_dest='nodename',
                            nodeinfo_help='output information for a specific node',
                            add_options_cb=None,
                            defaults={}):

    parser, checker = make_parser_and_checker(name, version, description,
                                              inventory_shortopt,
                                              inventory_longopt,
                                              inventory_help,
                                              nodeinfo_shortopt,
                                              nodeinfo_longopt, nodeinfo_dest,
                                              nodeinfo_help,
                                              add_options_cb,
                                              defaults=defaults)
    options, args = parser.parse_args()
    checker(options, args)

    options.nodes_uri, options.classes_uri = \
            path_mangler(options.inventory_base_uri, options.nodes_uri,
                         options.classes_uri)

    return options


def vvv(msg):
    #print >>sys.stderr, msg
    pass


def find_and_read_configfile(filename=CONFIG_FILE_NAME,
                             dirs=CONFIG_FILE_SEARCH_PATH):
    for d in dirs:
        f = os.path.join(d, filename)
        if os.access(f, os.R_OK):
            vvv('Using config file: {0}'.format(f))
            return yaml.safe_load(file(f))
        elif os.path.isfile(f):
            raise PermissionsError('cannot read %s' % f)
    return {}
