#
# -*- coding: utf-8 -*-
#
# This file is part of reclass (http://github.com/madduck/reclass)
#
# Copyright © 2007–13 martin f. krafft <madduck@madduck.net>
# Released under the terms of the Artistic Licence 2.0
#

import posix, sys

from reclass.defaults import PARAMETER_INTERPOLATION_SENTINELS

class ReclassException(Exception):

    def __init__(self, msg, rc=posix.EX_SOFTWARE, *args):
        super(ReclassException, self).__init__(msg, *args)
        self._rc = rc

    def __str__(self):
        return self.message

    rc = property(lambda self: self._rc)

    def exit_with_message(self, out=sys.stderr):
        print >>out, self.message
        sys.exit(self.rc)


class PermissionError(ReclassException):

    def __init__(self, msg, rc=posix.EX_NOPERM):
        super(PermissionError, self).__init__(msg, rc)


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


class InterpolationError(ReclassException):

    def __init__(self, msg, rc=posix.EX_DATAERR):
        super(InterpolationError, self).__init__(msg, rc)


class UndefinedVariableError(InterpolationError):

    def __init__(self, var, context=None):
        self._var = var
        msg = "Cannot resolve " + var.join(PARAMETER_INTERPOLATION_SENTINELS)
        if context:
            msg += ' in the context of %s' % context
        super(UndefinedVariableError, self).__init__(msg)

    var = property(lambda x: x._var)


class IncompleteInterpolationError(InterpolationError):

    def __init__(self, string, end_sentinel):
        msg = "Missing '%s' to end reference: %s" % \
                (end_sentinel, string.join(PARAMETER_INTERPOLATION_SENTINELS))
        super(IncompleteInterpolationError, self).__init__(msg)


class InfiniteRecursionError(InterpolationError):

    def __init__(self, path, ref):
        msg = "Infinite recursion while resolving %s at %s" \
                % (ref.join(PARAMETER_INTERPOLATION_SENTINELS), path)
        super(InfiniteRecursionError, self).__init__(msg)
