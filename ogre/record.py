# -*- coding: utf-8 -*-
from __future__ import absolute_import
import arrow
import json
from six import add_metaclass

from ogre.fields import (RecordMeta, String, Enum, Dictionary, DateTime, Set,
                         Integer, Decimal)


@add_metaclass(RecordMeta)
class BaseRecord(object):
    pass


class Record(BaseRecord):
    """Defines a GeoBlacklight record.

    A record's fields (see https://github.com/geoblacklight/geoblacklight-schema)
    can be initialized through keyword arguments or set later::

        from ogre.record import Record

        record = Record(dc_title_s=u'Cambridge Libraries')
        record.dct_provenance_s = u'MIT'

    This class can be easily subclassed to create a specific kind of record::

        from ogre.record import Record
        from ogre.fields import String, Enum

        class MitRecord(Record):
            dct_provenance_s = String(default=u'MIT')
            dc_rights_s = Enum(enums=[u'Public', u'Restricted'],
                               default=u'Restricted')

    :param kwargs: initial field values
    """

    uuid = String()
    dc_identifier_s = String()
    dc_title_s = String()
    dc_description_s = String()
    dc_rights_s = Enum(enums=['Public', 'Restricted'])
    dct_provenance_s = String()
    dct_references_s = Dictionary()
    layer_id_s = String()
    layer_geom_type_s = Enum(enums=['Point', 'Line', 'Polygon', 'Raster',
                                'Scanned Map', 'Paper Map', 'Mixed'])
    layer_modified_dt = DateTime(default=arrow.now())
    layer_slug_s = String()
    solr_year_i = Integer()
    dc_creator_sm = Set()
    dc_format_s = String()
    dc_language_s = String()
    dc_publisher_s = String()
    dc_subject_sm = Set()
    dc_type_s = Enum(enums=['Dataset', 'Image', 'PhysicalObject'])
    dct_spatial_sm = Set()
    dct_temporal_sm = Set()
    dct_issued_dt = String()
    dct_isPartOf_sm = Set()

    _bbox_w = Decimal()
    _bbox_n = Decimal()
    _bbox_e = Decimal()
    _bbox_s = Decimal()
    _lat = Decimal()
    _lon = Decimal()

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def georss_box_s(self):
        bounds = (self._bbox_s, self._bbox_w, self._bbox_n, self._bbox_e)
        if None in bounds:
            return None
        return "%s %s %s %s" % bounds

    @property
    def solr_geom(self):
        bounds = (self._bbox_w, self._bbox_e, self._bbox_n, self._bbox_s)
        if None in bounds:
            return None
        return "ENVELOPE(%s, %s, %s, %s)" % bounds

    @property
    def georss_point_s(self):
        point = (self._lat, self._lon)
        if None in point:
            return None
        return "%s %s" % point

    def as_dict(self):
        """Return record as a dictionary.

        This dictionary will contain only fields present in the current
        version of the GeoBlacklight schema.

        The ``dct_references_s`` field, if not ``None``, will be
        represented as a valid JSON string.

        :rtype: dictionary
        """

        if self.dct_references_s:
            references = json.dumps(self.dct_references_s)
        else:
            references = None
        d = {
            'uuid': self.uuid,
            'dc_identifier_s': self.dc_identifier_s,
            'dc_title_s': self.dc_title_s,
            'dc_description_s': self.dc_description_s,
            'dc_rights_s': self.dc_rights_s,
            'dct_provenance_s': self.dct_provenance_s,
            'dct_references_s': references,
            'georss_box_s': self.georss_box_s,
            'layer_id_s': self.layer_id_s,
            'layer_geom_type_s': self.layer_geom_type_s,
            'layer_modified_dt': self.layer_modified_dt,
            'layer_slug_s': self.layer_slug_s,
            'solr_geom': self.solr_geom,
            'solr_year_i': self.solr_year_i,
            'dc_creator_sm': self.dc_creator_sm,
            'dc_format_s': self.dc_format_s,
            'dc_language_s': self.dc_language_s,
            'dc_publisher_s': self.dc_publisher_s,
            'dc_subject_sm': self.dc_subject_sm,
            'dc_type_s': self.dc_type_s,
            'dct_spatial_sm': self.dct_spatial_sm,
            'dct_temporal_sm': self.dct_temporal_sm,
            'dct_issued_dt': self.dct_issued_dt,
            'dct_isPartOf_sm': self.dct_isPartOf_sm,
            'georss_point_s': self.georss_point_s,
        }

        return dict((k, v) for k, v in d.items() if v)
