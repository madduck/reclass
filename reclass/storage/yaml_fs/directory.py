#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os
import sys
from reclass.errors import NotFoundError

SKIPDIRS = ( 'CVS', 'SCCS' )
FILE_EXTENSION = '.yml'

def vvv(msg):
    #print >>sys.stderr, msg
    pass

class Directory(object):

    def __init__(self, path, fileclass=None):
        ''' Initialise a directory object '''
        if not os.path.isdir(path):
            raise NotFoundError('No such directory: %s' % path)
        if not os.access(path, os.R_OK|os.X_OK):
            raise NotFoundError('Cannot change to or read directory: %s' % path)
        self._path = path
        self._fileclass = fileclass
        self._files = {}

    def _register_files(self, dirpath, filenames):
        for f in filter(lambda f: f.endswith(FILE_EXTENSION), filenames):
            vvv('REGISTER {0}'.format(f))
            f = os.path.join(dirpath, f)
            ptr = None if not self._fileclass else self._fileclass(f)
            self._files[f] = ptr

    files = property(lambda self: self._files)

    def walk(self, register_fn=None):
        if not callable(register_fn): register_fn = self._register_files

        def _error(exc):
            raise(exc)

        for dirpath, dirnames, filenames in os.walk(self._path,
                                                    topdown=True,
                                                    onerror=_error,
                                                    followlinks=True):
            vvv('RECURSE {0}, {1} files, {2} subdirectories'.format(
                dirpath.replace(os.getcwd(), '.'), len(filenames), len(dirnames)))
            for d in dirnames:
                if d.startswith('.') or d in SKIPDIRS:
                    vvv('   SKIP subdirectory {0}'.format(d))
                    dirnames.remove(d)
            register_fn(dirpath, filenames)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self._path)
