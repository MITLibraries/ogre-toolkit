# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json

import pytest

from ogre.record import Record
from ogre.exceptions import InvalidDataError


def testRecordInitializesFromData():
    r = Record(dc_rights_s='Public')
    assert r.dc_rights_s == 'Public'


def testEnumRaisesExceptionForUnknownValue():
    with pytest.raises(InvalidDataError):
        Record(dc_rights_s='Level 8')


def testRecordHasOptionalFields():
    r = Record()
    assert r.dc_creator_sm is None


def testSolrGeomConstructsGeomString():
    r = Record()
    r.solr_geom = '-20.5', '20', '10.0', '-10'
    assert r.solr_geom == 'ENVELOPE(-20.5, 20, 10.0, -10)'


def testSetFieldRemovesDuplicates():
    r = Record(dc_creator_sm=['Bubbles', 'Bubbles'])
    assert r.dc_creator_sm == set(['Bubbles'])
