# -*- coding: utf-8 -*-
"""
The Ogre Toolkit provides a declarative API for defining a
:class:`~ogre.record.Record`. Use the fields documented here to
create new kinds of records.
"""

from __future__ import absolute_import
import decimal
import arrow

from ogre.exceptions import InvalidDataError


class RecordMeta(type):
    def __new__(cls, clsname, bases, methods):
        for k, v in methods.items():
            if isinstance(v, Descriptor):
                v.name = k
        return type.__new__(cls, clsname, bases, methods)


class Descriptor(object):
    def __init__(self, name=None, **opts):
        self.name = name
        for k, v in opts.items():
            setattr(self, k, v)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value


class Default(object):
    """A field type mixin that supports default values.

    Fields using this can define a default value::

        from ogre.record import Record
        from ogre.fields import Default

        class MyField(Default):
            pass

        class MyRecord(Record):
            default_field = MyField(default='Is this dress blue and black?')

        record = MyRecord()
        record.default_field # 'Is this dress blue and black?'
    """

    def __get__(self, instance, owner):
        try:
            return instance.__dict__.get(self.name, self.default)
        except AttributeError:
            return instance.__dict__.get(self.name)


class Enum(Descriptor, Default):
    """
    Enumerable field type.

    This defines a field that accepts values from a predetermined list.
    A mapper function can be passed that is called on the value being
    set right before it is set. For example::

        from ogre.record import Record
        from ogre.fields import Enum

        class MyRecord(Record):
            places = Enum(enums=['MFA', 'MOBA'], mapper=lambda x: x.upper())

        record = MyRecord(places='moba')
        record.places # MOBA

    :param enums: list of valid values
    :param mapper: mapper function
    """

    def __init__(self, name=None, **opts):
        defaults = {'mapper': lambda x: x}
        defaults.update(opts)
        super(Enum, self).__init__(name, **defaults)

    def __set__(self, instance, value):
        mapped = self.mapper(value)
        if mapped in self.enums:
            super(Enum, self).__set__(instance, mapped)
        else:
            raise InvalidDataError(self.name, mapped)


class String(Descriptor, Default):
    """
    A string field type.

    By default, white space will be removed from the beginning and end
    of the string. Set ``strip_ws`` to ``False`` to disable this behavior.

    :param strip_ws: remove white space from string, default is ``True``
    """

    def __init__(self, name=None, **opts):
        defaults = {'strip_ws': True}
        defaults.update(opts)
        super(String, self).__init__(name, **defaults)

    def __set__(self, instance, value):
        if self.strip_ws: value = value.strip()
        super(String, self).__set__(instance, value)


class Decimal(Descriptor, Default):
    """
    A decimal field type.

    Calls ``decimal.Decimal()`` on any value being set.
    """

    def __set__(self, instance, value):
        super(Decimal, self).__set__(instance, decimal.Decimal(value))


class DateTime(Descriptor, Default):
    """An `arrow <https://github.com/crsmithdev/arrow>`_ datetime field."""

    def __set__(self, instance, value):
        super(DateTime, self).__set__(instance, arrow.get(value))


class Integer(Descriptor, Default):
    """
    An integer field type.

    Calls ``int()`` on any value being set.
    """

    def __set__(self, instance, value):
        super(Integer, self).__set__(instance, int(value))


class Set(Descriptor):
    """A ``set`` field type.

    Example usage::

        from ogre.record import Record

        record = Record()
        record.dct_spatial_sm.add("Boston")
        record.dct_spatial_sm.update(["Cambridge", "Boston"])
        record.dct_spatial_sm # set(["Boston", "Cambridge"])

    """

    def __set__(self, instance, value):
        super(Set, self).__set__(instance, set(value))

    def __get__(self, instance, owner):
        if instance.__dict__.get(self.name) is None:
            self.__set__(instance, set())
        return instance.__dict__.get(self.name)


class Dictionary(Descriptor):
    """A ``dict`` field type."""

    def __get__(self, instance, owner):
        if instance.__dict__.get(self.name) is None:
            self.__set__(instance, dict())
        return instance.__dict__.get(self.name)
