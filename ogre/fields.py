# -*- coding: utf-8 -*-
"""
The Ogre Toolkit provides a declarative API for defining a
:class:`~ogre.record.Record`. Use the fields documented here to
create new kinds of records.
"""

from __future__ import absolute_import

from ogre.exceptions import InvalidDataError


class Enum(object):
    def __init__(self, *args):
        self.enums = args

    def __call__(self, f):
        def wrapped(*args):
            for arg in args[1:]:
                if arg not in self.enums:
                    raise InvalidDataError(f.__name__, arg)
            f(*args)
        return wrapped


def optional(f):
    def wrapped(self):
        try:
            return f(self)
        except AttributeError:
            return None
    return wrapped
