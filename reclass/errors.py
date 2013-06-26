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

    def __init__(self, msg, rc=posix.EX_SOFTWARE, *args):
        super(ReclassException, self).__init__(msg, *args)
        self._rc = rc

    def __str__(self):
        return self.message

    rc = property(lambda self: self._rc)


class InvocationError(ReclassException):

    def __init__(self, msg, rc=posix.EX_USAGE):
        super(InvocationError, self).__init__(msg, rc)


class NotFoundError(ReclassException):

    def __init__(self, msg, rc=posix.EX_IOERR):
        super(NotFoundError, self).__init__(msg, rc)


class NodeNotFound(NotFoundError):

    def __init__(self, storage, classname, uri):
        self._storage = storage
        self._name = classname
        self._uri = uri
        msg = "Node '{0}' not found under {1}://{2}".format(self._name,
                                                            self._storage,
                                                            self._uri)
        super(NodeNotFound, self).__init__(msg)


class ClassNotFound(NotFoundError):

    def __init__(self, storage, classname, uri, nodename):
        self._storage = storage
        self._name = classname
        self._uri = uri
        self._nodename = nodename
        msg = "Class '{0}' (in ancestry of node {1}) not found under {2}://{3}" \
                .format(self._name, self._nodename, self._storage, self._uri)
        super(ClassNotFound, self).__init__(msg)
