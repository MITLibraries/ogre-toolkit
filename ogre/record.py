# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json

from jsonschema.validators import validator_for

from ogre.fields import Enum, optional


def create_validator(schema):
    validator = validator_for(schema)
    validator.check_schema(schema)
    return validator(schema).validate


class Record(object):
    dc_description_s = None
    dc_identifier_s = None
    dc_language_s = None
    dc_publisher_s = None
    dc_title_s = None
    dct_issued_dt = None
    dct_provenance_s = None
    geoblacklight_version = None
    layer_id_is = None
    layer_modified_dt = None
    layer_slug_s = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    @optional
    def dc_creator_sm(self):
        return self._dc_creator_sm

    @dc_creator_sm.setter
    def dc_creator_sm(self, value):
        self._dc_creator_sm = set(value)

    @property
    @optional
    def dc_format_s(self):
        return self._dc_format_s

    @dc_format_s.setter
    def dc_format_s(self, value):
        self._dc_format_s = value

    @property
    def dc_rights_s(self):
        return self._dc_rights_s

    @dc_rights_s.setter
    @Enum('Public', 'Restricted')
    def dc_rights_s(self, value):
        self._dc_rights_s = value

    @property
    @optional
    def dc_source_sm(self):
        return self._dc_source_sm

    @dc_source_sm.setter
    def dc_source_sm(self, value):
        self._dc_source_dm = set(value)

    @property
    @optional
    def dc_subject_sm(self):
        return self._dc_subject_sm

    @dc_subject_sm.setter
    def dc_subject_sm(self, value):
        self._dc_subject_sm = set(value)

    @property
    @optional
    def dc_type_s(self):
        return self._dc_type_s

    @dc_type_s.setter
    @Enum('Dataset', 'Image', 'PhysicalObject')
    def dc_type_s(self, value):
        self._dc_type_s = value

    @property
    @optional
    def dct_isPartOf_sm(self):
        return self._dct_isPartOf_sm

    @dct_isPartOf_sm.setter
    def dct_isPartOf_sm(self, value):
        self._dct_isPartOf_sm = set(value)

    @property
    def dct_references_s(self):
        return self._dct_references_s

    @dct_references_s.setter
    def dct_references_s(self, value):
        self._dct_references_s = dict(value)

    @property
    @optional
    def dct_spatial_sm(self):
        return self._dct_spatial_sm

    @dct_spatial_sm.setter
    def dct_spatial_sm(self, value):
        self._dct_spatial_sm = set(value)

    @property
    @optional
    def dct_temporal_sm(self):
        return self._dct_temporal_sm

    @dct_temporal_sm.setter
    def dct_temporal_sm(self, value):
        self._dct_temporal_sm = set(value)

    @property
    def layer_geom_type_s(self):
        return self._layer_geom_type_s

    @layer_geom_type_s.setter
    @Enum('Point', 'Line', 'Polygon', 'Raster', 'Scanned Map', 'Mixed')
    def layer_geom_type_s(self, value):
        self._layer_geom_type_s = value

    @property
    def solr_geom(self):
        return self._solr_geom

    @solr_geom.setter
    def solr_geom(self, values):
        """W,E,N,S"""
        self._solr_geom = "ENVELOPE({}, {}, {}, {})".format(*values)

    def as_dict(self):
        record = {
            'dc_creator_sm': list(self.dc_creator_sm or []),
            'dc_description_s': self.dc_description_s,
            'dc_format_s': self.dc_format_s,
            'dc_identifier_s': self.dc_identifier_s,
            'dc_language_s': self.dc_language_s,
            'dc_publisher_s': self.dc_publisher_s,
            'dc_rights_s': self.dc_rights_s,
            'dc_source_sm': list(self.dc_source_sm or []),
            'dc_subject_sm': list(self.dc_subject_sm or []),
            'dc_title_s': self.dc_title_s,
            'dc_type_s': self.dc_type_s,
            'dct_isPartOf_sm': list(self.dct_isPartOf_sm or []),
            'dct_issued_dt': self.dct_issued_dt,
            'dct_provenance_s': self.dct_provenance_s,
            'dct_references_s': json.dumps(self.dct_references_s),
            'dct_spatial_sm': list(self.dct_spatial_sm or []),
            'dct_temporal_sm': list(self.dct_temporal_sm or []),
            'geoblacklight_version': self.geoblacklight_version,
            'layer_geom_type_s': self.layer_geom_type_s,
            'layer_id_s': self.layer_id_s,
            'layer_modified_dt': self.layer_modified_dt,
            'layer_slug_s': self.layer_slug_s,
            'solr_geom': self.solr_geom,
        }
        return {k: v for k, v in record.items() if v}

    def to_json(self):
        return json.dumps(self.as_dict())
