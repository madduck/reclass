#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–14 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import posix, sys
import traceback

from reclass.defaults import PARAMETER_INTERPOLATION_SENTINELS

class ReclassException(Exception):

    def __init__(self, rc=posix.EX_SOFTWARE, msg=None):
        super(ReclassException, self).__init__()
        self._rc = rc
        self._msg = msg
        self._traceback = traceback.format_exc()

    message = property(lambda self: self._get_message())
    rc = property(lambda self: self._rc)

    def _get_message(self):
        if self._msg:
            return self._msg
        else:
            return 'No error message provided.'

    def exit_with_message(self, out=sys.stderr):
        print >>out, self.message
        if self._traceback:
            print >>out, self._traceback
        sys.exit(self.rc)


class PermissionError(ReclassException):

    def __init__(self, msg, rc=posix.EX_NOPERM):
        super(PermissionError, self).__init__(rc=rc, msg=msg)


class InvocationError(ReclassException):

    def __init__(self, msg, rc=posix.EX_USAGE):
        super(InvocationError, self).__init__(rc=rc, msg=msg)


class ConfigError(ReclassException):

    def __init__(self, msg, rc=posix.EX_CONFIG):
        super(ConfigError, self).__init__(rc=rc, msg=msg)


class DuplicateUriError(ConfigError):

    def __init__(self, nodes_uri, classes_uri):
        super(DuplicateUriError, self).__init__(msg=None)
        self._nodes_uri = nodes_uri
        self._classes_uri = classes_uri

    def _get_message(self):
        return "The inventory URIs must not be the same " \
               "for nodes and classes: {0}".format(self._nodes_uri)


class UriOverlapError(ConfigError):

    def __init__(self, nodes_uri, classes_uri):
        super(UriOverlapError, self).__init__(msg=None)
        self._nodes_uri = nodes_uri
        self._classes_uri = classes_uri

    def _get_message(self):
        msg = "The URIs for the nodes and classes inventories must not " \
              "overlap, but {0} and {1} do."
        return msg.format(self._nodes_uri, self._classes_uri)


class NotFoundError(ReclassException):

    def __init__(self, msg, rc=posix.EX_IOERR):
        super(NotFoundError, self).__init__(rc=rc, msg=msg)


class NodeNotFound(NotFoundError):

    def __init__(self, storage, nodename, uri):
        super(NodeNotFound, self).__init__(msg=None)
        self._storage = storage
        self._name = nodename
        self._uri = uri

    def _get_message(self):
        msg = "Node '{0}' not found under {1}://{2}"
        return msg.format(self._name, self._storage, self._uri)


class ClassNotFound(NotFoundError):

    def __init__(self, storage, classname, uri, nodename=None):
        super(ClassNotFound, self).__init__(msg=None)
        self._storage = storage
        self._name = classname
        self._uri = uri
        self._nodename = nodename

    def _get_message(self):
        if self._nodename:
            msg = "Class '{0}' (in ancestry of node '{1}') not found " \
                  "under {2}://{3}"
        else:
            msg = "Class '{0}' not found under {2}://{3}"
        return msg.format(self._name, self._nodename, self._storage, self._uri)

    def set_nodename(self, nodename):
        self._nodename = nodename


class InterpolationError(ReclassException):

    def __init__(self, msg, rc=posix.EX_DATAERR):
        super(InterpolationError, self).__init__(rc=rc, msg=msg)


class UndefinedVariableError(InterpolationError):

    def __init__(self, var, context=None):
        super(UndefinedVariableError, self).__init__(msg=None)
        self._var = var
        self._context = context
    var = property(lambda self: self._var)
    context = property(lambda self: self._context)

    def _get_message(self):
        msg = "Cannot resolve " + self._var.join(PARAMETER_INTERPOLATION_SENTINELS)
        if self._context:
            msg += ' in the context of %s' % self._context
        return msg

    def set_context(self, context):
        self._context = context


class IncompleteInterpolationError(InterpolationError):

    def __init__(self, string, end_sentinel):
        super(IncompleteInterpolationError, self).__init__(msg=None)
        self._ref = string.join(PARAMETER_INTERPOLATION_SENTINELS)
        self._end_sentinel = end_sentinel

    def _get_message(self):
        msg = "Missing '{0}' to end reference: {1}"
        return msg.format(self._end_sentinel, self._ref)


class InfiniteRecursionError(InterpolationError):

    def __init__(self, path, ref):
        super(InfiniteRecursionError, self).__init__(msg=None)
        self._path = path
        self._ref = ref.join(PARAMETER_INTERPOLATION_SENTINELS)

    def _get_message(self):
        msg = "Infinite recursion while resolving {0} at {1}"
        return msg.format(self._ref, self._path)


class MappingError(ReclassException):

    def __init__(self, msg, rc=posix.EX_DATAERR):
        super(MappingError, self).__init__(rc=rc, msg=msg)


class MappingFormatError(MappingError):

    def __init__(self, msg):
        super(MappingFormatError, self).__init__(msg)


class NameError(ReclassException):

    def __init__(self, msg, rc=posix.EX_DATAERR):
        super(NameError, self).__init__(rc=rc, msg=msg)


class InvalidClassnameError(NameError):

    def __init__(self, invalid_character, classname):
        super(InvalidClassnameError, self).__init__(msg=None)
        self._char = invalid_character
        self._classname = classname

    def _get_message(self):
        msg = "Invalid character '{0}' in class name '{1}'."
        return msg.format(self._char, classname)


class DuplicateNodeNameError(NameError):

    def __init__(self, storage, name, uri1, uri2):
        super(DuplicateNodeNameError, self).__init__(msg=None)
        self._storage = storage
        self._name = name
        self._uris = (uri1, uri2)

    def _get_message(self):
        msg = "{0}: Definition of node '{1}' in '{2}' collides with " \
              "definition in '{3}'. Nodes can only be defined once " \
              "per inventory."
        return msg.format(self._storage, self._name, self._uris[1], self._uris[0])
