# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
import pytest
import arrow
import json

from ogre.record import Record
from ogre.exceptions import InvalidDataError


class RecordTestCase(unittest.TestCase):
    def testRecordInitializesFromData(self):
        r = Record(dc_rights_s='Public')
        self.assertEqual(r.dc_rights_s, 'Public')

    def testEnumRaisesExceptionForUnknownValue(self):
        with pytest.raises(InvalidDataError):
            Record(dc_rights_s='Level 8')

    def testStringFieldStripsWhitespaceByDefault(self):
        r = Record(dc_title_s='Geothermal resources of New Mexico ')
        self.assertEqual(r.dc_title_s, 'Geothermal resources of New Mexico')

    def testGeoRssConstructsRssString(self):
        r = Record(_bbox_w='-20.5', _bbox_e='20', _bbox_s='-10',
                      _bbox_n='10.0')
        self.assertEqual(r.georss_box_s, '-10 -20.5 10.0 20')

    def testDateTimeConstructsDateTime(self):
        r = Record(layer_modified_dt='2015-01-01T12:12:12Z')
        self.assertEqual(r.layer_modified_dt.year, 2015)

    def testModifiedUsesDefaultDatetime(self):
        r = Record()
        self.assertEqual(r.layer_modified_dt.year, arrow.now().year)

    def testSolrGeomConstructsGeomString(self):
        r = Record(_bbox_w='-20.5', _bbox_e='20', _bbox_s='-10',
                      _bbox_n='10.0')
        self.assertEqual(r.solr_geom, 'ENVELOPE(-20.5, 20, 10.0, -10)')

    def testIntegerFieldConvertsToInteger(self):
        r = Record(solr_year_i='1999')
        self.assertEqual(r.solr_year_i, 1999)

    def testSetFieldRemovesDuplicates(self):
        r = Record(dc_creator_sm=['Bubbles', 'Bubbles'])
        self.assertEqual(r.dc_creator_sm, set(['Bubbles']))

    def testGeoRssPointConstructsRssString(self):
        r = Record(_lat='45', _lon='-180')
        self.assertEqual(r.georss_point_s, '45 -180')

    def testAsDictReturnsReferencesAsJson(self):
        references = {
            'http://schema.org/Person': 'Britney Spears',
        }
        r = Record(dct_references_s=references)
        self.assertEqual(r.as_dict().get('dct_references_s'),
                         json.dumps(references))

    def testAsDictRemovesEmptyFields(self):
        r = Record(uuid='123')
        assert 'dc_title_s' not in r.as_dict()

    def testRecordCanBeRepresentedAsDictionary(self):
        time = arrow.now()
        r = Record(uuid='0-8-3', dc_title_s='Today, in the world of cats',
                      _lat='-23', _lon='97', layer_modified_dt=time)
        self.assertEqual(r.as_dict(),
            {'uuid': '0-8-3', 'dc_title_s': 'Today, in the world of cats',
             'georss_point_s': '-23 97', 'layer_modified_dt': time})
