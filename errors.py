#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import posix

class ReclassException(Exception):

    def __init__(self, rc=posix.EX_SOFTWARE, *args):
        super(ReclassException, self).__init__(*args)
        self._rc = rc

    def __str__(self):
        return "reclass encountered an exception, sorry!"

    message = property(lambda self: self.__str__())
    rc = property(lambda self: self._rc)


class NotFoundError(ReclassException):

    def __init__(self, rc=posix.EX_IOERR):
        super(NotFoundError, self).__init__(rc)


class NodeNotFound(NotFoundError):

    def __init__(self, storage, classname, uri):
        super(NodeNotFound, self).__init__()
        self._storage = storage
        self._name = classname
        self._uri = uri

    def __str__(self):
        return "Node '{0}' not found under {1}://{2}".format(self._name,
                                                             self._storage,
                                                             self._uri)


class ClassNotFound(NodeNotFound):

    def __init__(self, storage, classname, uri, nodename):
        super(ClassNotFound, self).__init__(storage, classname, uri)
        self._nodename = nodename

    def __str__(self):
        return "Class '{0}' (in ancestry of node {1}) not found under {2}://{3}" \
                .format(self._name, self._nodename, self._storage, self._uri)
