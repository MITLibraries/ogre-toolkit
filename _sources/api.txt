API
===

Repository
----------

.. automodule:: ogre.repository
    :members:

Record
------

.. autoclass:: ogre.record.Record
    :members:

Fields
------

.. automodule:: ogre.fields

    .. autoclass:: Default(default=None)
    .. autoclass:: String(strip_ws=True)
        :show-inheritance:
    .. autoclass:: Decimal()
        :show-inheritance:
    .. autoclass:: Integer()
        :show-inheritance:
    .. autoclass:: DateTime()
        :show-inheritance:
    .. autoclass:: Set()
        :show-inheritance:
    .. autoclass:: Enum(enums, mapper=lambda x: x)
        :show-inheritance:
    .. autoclass:: Dictionary()
        :show-inheritance:

XML Parsers
-----------

.. automodule:: ogre.xml
    :members:
