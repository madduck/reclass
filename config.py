#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import yaml, os, optparse, posix, sys

def _make_parser(name, version, description, defaults={}):
    parser = optparse.OptionParser(version=version)
    parser.prog = name
    parser.version = version
    parser.description = description
    parser.usage = '%prog [options] ( --inventory | --nodeinfo <nodename> )'

    options_group = optparse.OptionGroup(parser, 'Options',
                                         'Configure the way {0} works'.format(name))
    options_group.add_option('-t', '--storage-type', dest='storage_type',
                             default=defaults.get('storage_type', 'yaml_fs'),
                             help='the type of storage backend to use [%default]')
    options_group.add_option('-u', '--nodes-uri', dest='nodes_uri',
                             default=defaults.get('nodes_uri', None),
                             help='the URI to the nodes storage [%default]'),
    options_group.add_option('-c', '--classes-uri', dest='classes_uri',
                             default=defaults.get('classes_uri', None),
                             help='the URI to the classes storage [%default]')
    options_group.add_option('-o', '--output', dest='output',
                             default=defaults.get('output', 'yaml'),
                             help='output format (yaml or json) [%default]')
    options_group.add_option('-p', '--pretty-print', dest='pretty_print',
                             default=defaults.get('pretty_print', False),
                             action="store_true",
                             help='try to make the output prettier [%default]')
    options_group.add_option('--applications-postfix', dest='applications_postfix',
                             default=defaults.get('applications_postfix', '_hosts'),
                             help="the postfix to apply to groups made from applications ['%default']")
    parser.add_option_group(options_group)

    run_modes = optparse.OptionGroup(parser, 'Modes',
                                     'Specify one of these to determine what to do.')
    run_modes.add_option('-i', '--inventory', action='store_false', dest='node',
                         help='output the entire inventory')
    run_modes.add_option('-n', '--nodeinfo', action='store', dest='node',
                         default=None,
                         help='output information for a specific node')
    parser.add_option_group(run_modes)

    return parser

def _parse_and_check_options(parser):
    options, args = parser.parse_args()

    def usage_error(msg):
        sys.stderr.write(msg + '\n\n')
        parser.print_help(sys.stderr)
        sys.exit(posix.EX_USAGE)

    if len(args) > 0:
        usage_error('No arguments allowed')
    elif options.node is None:
        usage_error('You need to either pass --inventory or --nodeinfo <nodename>')
    elif options.output not in ('json', 'yaml'):
        usage_error('Unknown output format: {0}'.format(options.output))
    elif options.nodes_uri is None:
        usage_error('Must specify at least --nodes-uri')

    options.classes_uri = options.classes_uri or options.nodes_uri

    return options

def read_config_file(path):
    if os.path.exists(path):
        return yaml.safe_load(file(path))
    else:
        return {}

def get_options(name, version, description, config_file=None):
    config_data = {}
    if config_file is not None:
        config_data.update(read_config_file(config_file))
    parser = _make_parser(name, version, description, config_data)
    return _parse_and_check_options(parser)
