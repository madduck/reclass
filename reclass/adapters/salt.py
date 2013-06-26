#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
from reclass import config, get_data
from reclass.errors import InvocationError

def _check_storage_params(storage_type, inventory_base_uri, nodes_uri,
                          classes_uri):
    nodes_uri, classes_uri = config.path_mangler(inventory_base_uri,
                                                 nodes_uri, classes_uri)

    if nodes_uri is None:
        raise InvocationError('missing nodes_uri or inventory_base_uri parameters')

    if classes_uri is None:
        raise InvocationError('missing classes_uri or inventory_base_uri parameters')

    if storage_type is None:
        storage_type = 'yaml_fs'   # TODO: should be obtained from config

    return storage_type, nodes_uri, classes_uri


def _get_data(storage_type, inventory_base_uri, nodes_uri, classes_uri, node):

    storage_type, nodes_uri, classes_uri = _check_storage_params(storage_type,
                                                                 inventory_base_uri,
                                                                 nodes_uri,
                                                                 classes_uri)
    return get_data(storage_type, nodes_uri, classes_uri, node)


def ext_pillar(pillar, storage_type=None, inventory_base_uri=None,
               nodes_uri=None, classes_uri=None):

    node = opts.get('id')
    if node is None:
        raise InvocationError('no node ID provided')

    data = _get_data(storage_type, inventory_base_uri, nodes_uri, classes_uri,
                     node)
    params = data.get('parameters', {})
    params['__reclass__'] = {}
    params['__reclass__']['applications'] = data['applications']
    params['__reclass__']['classes'] = data['classes']

    # TODO: template interpolation?
    return params


def top(salt, opts, grains):
    reclass_opts = opts.get('master_tops', {}).get('reclass')
    if reclass_opts is None:
         raise InvocationError('no configuration provided')

    storage_type = reclass_opts.get('storage_type')
    inventory_base_uri = reclass_opts.get('inventory_base_uri')
    nodes_uri = reclass_opts.get('nodes_uri')
    classes_uri = reclass_opts.get('classes_uri')

    data = _get_data(storage_type, inventory_base_uri, nodes_uri, classes_uri,
                     node=None)
    env = 'base'
    top = {env: {}}
    # TODO: node environments
    for node_id, node_data in data['nodes'].iteritems():
        #env = data.environment
        #if env not in top:
        #    top[env] = {}
        top[env][node_id] = node_data['applications']

    return top
