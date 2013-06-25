#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#
import os
import sys

SKIPDIRS = ( '.git' , '.svn' , 'CVS', 'SCCS', '.hg', '_darcs' )
FILE_EXTENSION = '.yml'

def vvv(msg):
    #print >>sys.stderr, msg
    pass

class Directory(object):

    def __init__(self, path, fileclass=None):
        ''' Initialise a directory object '''
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
        def _error(error):
            raise Exception('{0}: {1} ({2})'.format(error.filename, error.strerror, error.errno))
        if not callable(register_fn): register_fn = self._register_files
        for dirpath, dirnames, filenames in os.walk(self._path,
                                                      topdown=True,
                                                      onerror=_error,
                                                      followlinks=True):
            vvv('RECURSE {0}, {1} files, {2} subdirectories'.format(
                dirpath.replace(os.getcwd(), '.'), len(filenames), len(dirnames)))
            for d in SKIPDIRS:
                if d in dirnames:
                    vvv('   SKIP subdirectory {0}'.format(d))
                    dirnames.remove(d)
            register_fn(dirpath, filenames)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self._path)
