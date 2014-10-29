#
# -*- coding: utf-8 -*-
#
# This file is part of python-appconfig
#
# Copyright © 2014 Contributors
# Released under the terms of the BSD license
#

'''
The opinionated config object for Python applications

'''

import os
import json
import logging
import UserDict

import yaml
from reclass.datatypes import Parameters


def _normalize_keys(items):
     '''
     Generate a new dictionary with renamed keys. All occurances of '-' are
     replaced with '_', and all keys are lowercased.

     '''
     return _dash_to_underscore(_lowercase_keys(_remove_empty_keys(items)))


def _dash_to_underscore(items):
     '''
     Generate a new dictionary with renamed keys. All occurances of '-' are
     replaced with '_'.

     '''
     return {k.replace('-', '_'):v for k,v in items.iteritems()}


def _lowercase_keys(items):
     '''
     Generate a new dictionary with renamed keys. All keys are ensured to be
     lower-cased.

     '''
     return {k.lower():v for k,v in items.iteritems()}


def _remove_empty_keys(d={}):
    '''
    Returns a dictionary, having deleted (removed) the empty keys.

    '''
    return {k:v for k,v in d.iteritems() if v is not None}


def _get_opt(opts=None, key=None):
    '''
    Attempt to retrieve the named option, Returns None if not found or an
    exception is thrown. Lookup ``opts.key`` and ``opts[key]``.

    '''
    try:
        opt = getattr(opts, key)
        return opt
    except:
        try:
            opt = opts[key]
            return opt
        except:
            return None


def _get_keys_from_env(keys=[]):
    '''
    Construct a dictionary of key/value pairs using the list of ``keys``
    provided and ``os.environ.get()`` to retrieve the key from the shell
    environment.

    Use ``_remove_empty_keys()`` to ensure there are no empty keys

    '''
    return _remove_empty_keys({k: os.environ.get(k) for k in keys})


def _merge(a, b):
    '''
    merge the contents of dictionary ``b`` into dictionary ``a``, using reclass'
    sensible form of deep-dictionary merging and interpolation.
    '''
    m = Parameters(a)
    m.merge(b)
    m.interpolate()
    return m.as_dict()


class ConfigBase(UserDict.UserDict):
    '''
    Base class that provides a meaningful (opinionated) foundation to build an
    object suitable for all of an Application's configuration. It is meant to be
    dict-like in nature, subclassing ``UserDict.UserDict``.

    Current Bugs:

     * we don't normalize keys retrieved from JSON/YAML files
     * it would be awesome to enable/disable normalizing keys
     * specifying the files to load is cumbersome, incomplete, imperfect.
     * we ought to print out more info about the Exception encountered when
       handling files.

    '''
    # a place to store the config keys (data)
    data = {}
    # write the whole config out to this file
    file_path = os.path.join(os.getcwd(), 'config.yaml')
    # supported file-types: json/yaml
    file_format = 'yaml'
    # list of keys to extract from the environment
    _env_keys = []
    # list of opt attributes to extract from an OptionParser object
    _opts_list = []
    # a place to store defaults
    _defaults = {}
    # list of files to search and load YAML/JSON config from
    _filelist = []
    # a place to stash a logging.logger instance we can rely on internally
    logger = None
    # flag to enable SUPER verbose debug
    _vvv = False


    def __init__(self, rt={}, opts=None, lgr=None, files=[], *args, **kwargs):
        '''
        '''
        # ensure we have a logger we can use
        self._init_logger(lgr)
        # init config structure with defaults
        self.merge(self._defaults)
        # load data loaded from file, update config with the result
        self.merge(self._load_files())
        # load config keys from the environment, if provided
        self.merge(self._parse_env())
        # parse options, if provided, extracting the keys we want
        if opts:
            self.merge(self._parse_opts(opts))
        # finally, merge in the custom/runtime config keys
        self.merge(rt)
        msg = ('config object init complete, the result: %s' % self.data)
        self.logger.debug(msg)


    def _init_logger(self, lgr=None):
        '''
        Initialize a logger the config instance can rely on. Set ``self.logger``
        to ``lgr`` if provided, or setup our own. For now, we default to enabling
        debug mode when providing our own. Maybe in the future we'll use an env
        variable or something sneaky like that.

        '''
        if lgr:
            self.logger = lgr
        elif not self.logger:
            logging.basicConfig(format='%(levelname)s: %(name)s %(message)s',
                                level=logging.DEBUG)
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel('DEBUG')
        else: # there's a logger in place, we don't have a new on, leave it be
            pass


    def _parse_env(self):
        '''
        Using the list of keys provided by ``self._env_keys``, attempt to
        retrieve each key from the shell environment. Returns the dictionary
        compiled out of the keys retrieved.

        '''
        msg = ('retrieving keys from the shell environment: %s' % self._env_keys)
        self.logger.debug(msg)
        return _normalize_keys(_get_keys_from_env(self._env_keys))


    def _parse_opts(self, opts):
        '''
        Provided an ``OptionParser``-like object ``opts``, use the list of
        attributes defined in ``self._opts_list`` to extract a specific list of
        keys. Use ``_get_opts()`` to retrieve the key, or None. Generate a
        dictionary with these extracted keys and return the result. Use
        ``_remove_empty_keys()`` to ensure the result is concise.

        '''
        msg = ('retrieving keys from the option parser: %s' % opts)
        self.logger.debug(msg)
        return _normalize_keys({o: _get_opt(opts, o) for o in self._opts_list})


    def _load_files(self):
        '''
        Using the list of file paths provided by ``self._filelist``, look up each
        file to be loaded, parsed to a dictionary, and merged together. The file
        is parsed as either YAML or JSON based on the file extension.

        '''
        for config in self._filelist:
            if os.path.exists(config):
                # merge with {} to ensure we interpolate what we load from files
                return _merge({}, self._load_file(config))
	# return empty {} if no files are found/readable
	return {}


    def _load_file(self, fpath):
        '''
        Provided the full file path to a file, ``fpath``, attempt to load and
        parse this file as either YAML or JSON. Return the result as a
        dictionary.

        '''
        def _determine_filetype(fpath, default='yaml', sfx=None):
            '''
            return ``yaml`` or ``json`` based on the suffix of ``fpath``.

            '''
            if fpath.endswith('.yaml') or fpath.endswith('.yml'):
                sfx = 'yaml'
            elif fpath.endswith('.json'):
                sfx = 'json'
            return sfx or default

        # figure out the file type based on the suffix
        ftype = _determine_filetype(fpath)
        self.logger.debug('attempting to load data from %s' % fpath)
        # only try to open and parse the file if it exists
        if os.path.exists(fpath):
            with open(fpath, 'r') as f:
                contents = f.read()
            # if ftype is not supported/found, we return data {}
            if ftype == 'yaml':
                data = yaml.safe_load(contents)
            elif ftype == 'json':
                data = json.loads(contents)
            msg = ('loaded and parsed data from %s as %s: %s' % (fpath, ftype, data))
            self.logger.debug(msg)
        else:
            self.logger.debug('cannot open config %s' % fpath)
        # return an empty dict to prevent returning None
        return data or {}


    def merge(self, data):
        '''
        Merge the dictionary provided ``data``, into ``self.data``.

        '''
        if self._vvv:
            self.logger.debug('merging %s into %s' % (data, self.data))
        self.data = _merge(self.data, data)


    def save(self, fpath=None):
        '''
        If ``fpath`` is provided, update ``self.file_path`` and attempt to write
        out the contents of the config dictionary to that file. Returns ``True``
        on success and ``False`` if there is an Exception in opening or dumping
        data to the file.

        '''
        if fpath:
            self.logger.debug('updated file path to %s' % fpath)
            self.file_path = fpath
        try:
            with open(self.file_path, 'w') as config:
                msg = ('writing %s file to %s with contents %s' %
                          (self.file_format, self.file_path, self.data))
                self.logger.debug(msg)
                if self.file_format == 'json':
                    json.dump(self.data, config, indent=2)
                else:
                    yaml.safe_dump(self.data, config)
                return True
        except:
            # ensure this is correct, and includes the error message
            #msg = ('failed to open and write to %s, error: %s' % (self.file_path))
            #self.logger.error(msg)
            return False


    def load_from(self, fl=[]):
        '''
        Provided a list of filesystem paths, update ``self._filelist`` and load
        these files into the configuration dictionary.

        '''
        self.logger.debug('filelist is %s, updating to %s' % (self._filelist, fl))
        self._filelist = fl
        self.merge(self._load_files())


    def set_verbose_debug(self, enable=False):
        '''
        Set ``self._vvv`` (very, very, verbose debug output) based on ``enable``

        '''
        self._vvv = enable
