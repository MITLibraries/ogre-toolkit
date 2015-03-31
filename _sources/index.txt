Welcome to the Ogre Toolkit Documentation!
==========================================

The Ogre Toolkit is designed to make working with `OpenGeoMetadata <https://github.com/OpenGeoMetadata>`_ repositories a bit easier for Python projects.


Repositories
-------------------------

A :class:`~ogre.repository.Repository` is a collection of items. Each item provides access to its associated metadata files::

    from ogre.repository import Repository

    repo = Repository('local/repo', 'remote/repo')
    for item in repo:
        with open(item.fgdc) as fp:
            fp.read() # <?xml version="1.0"?><metadata>...


Parsers
-------

Parsers (currently only FGDC) are provided to handle various metadata formats that might appear in a repository. A parser will parse a file into a dictionary whose keys match the current GeoBlacklight schema::

    from ogre.xml import parse, FGDCParser

    metadata = parse(item.fgdc, FGDCParser)
    print metadata['dc_title_s']


Records
--------------------

A :class:`~ogre.record.Record` is a container object for GeoBlacklight metadata (see: https://github.com/geoblacklight/geoblacklight-schema). Fields can be
provided as arguments to the constructor or set later::

    from ogre.record import Record

    record = Record(dc_title_s='Some GIS data')
    print record.dc_title_s  # 'Some GIS data'

    record.dct_provenance_s = 'MIT'

Fields are typed and provide some basic normalization and authority control::

    record.dc_description_s = '  Abstract   '
    print record.dc_description_s  # 'Abstract'

    record.dc_rights_s = 'Bogus rights'  # raises InvalidDataError

A record can be represented as a dictionary::

    record.as_dict() # {'dc_title_s': 'Some GIS data'...

You can easily create your own kind of ``Record`` with, for example, default field values::

    from ogre.record import Record
    from ogre.fields import *

    class MITRecord(Record):
        dct_provenance_s = String(default='MIT')

    r = MITRecord()
    print r.dct_provenance_s  # 'MIT'


API Reference
-------------

For detailed information on the API refer to the following documentation:

.. toctree::
    :maxdepth: 2

    api
