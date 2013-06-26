#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os, sys, posix, stat

import reclass.config
from reclass.errors import InvocationError, ReclassException
from reclass import get_data, output

def ansible_adapter(ansible_dir, exc_handler):
    try:
        if len(sys.argv) == 1:
            raise InvocationError('Need to specify --list or --host.',
                                  posix.EX_USAGE)

        # The adapter resides in the Ansible directory, so let's look there
        # for an optional configuration file called reclass-config.yml.
        options = {'output':'json', 'pretty_print':True}
        config_path = os.path.join(ansible_dir, 'reclass-config.yml')
        if os.path.exists(config_path) and os.access(config_path, os.R_OK):
            options.update(reclass.config.read_config_file(config_path))

        # Massage options into shape
        if 'storage_type' not in options:
            options['storage_type'] = 'yaml_fs'

        if 'nodes_uri' not in options:
            nodes_uri = os.path.join(ansible_dir, 'nodes')
            if stat.S_ISDIR(os.stat(nodes_uri).st_mode):
                options['nodes_uri'] = nodes_uri
            else:
                raise InvocationError('nodes_uri not specified',
                                      posix.EX_USAGE)

        if 'classes_uri' not in options:
            classes_uri = os.path.join(ansible_dir, 'classes')
            if not stat.S_ISDIR(os.stat(classes_uri).st_mode):
                classes_uri = options['nodes_uri']
            options['classes_uri'] = classes_uri

        if 'applications_postfix' not in options:
            options['applications_postfix'] = '_hosts'

        # Invoke reclass according to what Ansible wants.
        # If the 'node' option is set, we want node information. If the option
        # is False instead, we print the inventory. Yeah for option abuse!
        if sys.argv[1] == '--list':
            if len(sys.argv) > 2:
                raise InvocationError('Unknown arguments: ' + \
                                    ' '.join(sys.argv[2:]), posix.EX_USAGE)
            options['node'] = False

        elif sys.argv[1] == '--host':
            if len(sys.argv) < 3:
                raise InvocationError('Missing hostname.', posix.EX_USAGE)
            elif len(sys.argv) > 3:
                raise InvocationError('Unknown arguments: ' + \
                                    ' '.join(sys.argv[3:]), posix.EX_USAGE)
            options['node'] = sys.argv[2]

        else:
            raise InvocationError('Unknown mode (--list or --host required).',
                                  posix.EX_USAGE)

        data = get_data(options['storage_type'], options['nodes_uri'],
                        options['classes_uri'],
                        options['applications_postfix'], options['node'])

        if options['node']:
            # Massage and shift the data like Ansible wants it
            data['parameters']['RECLASS'] = data['RECLASS']
            for i in ('classes', 'applications'):
                data['parameters']['RECLASS'][i] = data[i]
            data = data['parameters']

        print output(data, options['output'], options['pretty_print'])

    except ReclassException, e:
        exc_handler(e.message, e.rc)
