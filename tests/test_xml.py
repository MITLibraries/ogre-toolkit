# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest
from mock import Mock
import io

from ogre.xml import parse, FGDCParser


class ParseTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = Mock()
        self.xml = io.BytesIO(u'<root><child/></root>'.encode('utf-8'))

    def testParseCallsStartHandlerWithElement(self):
        parse(self.xml, Mock(return_value=self.parser))
        self.assertEqual(self.parser.start_handler.call_args[0][0].tag, 'child')

    def testParseCallsEndHandlerWithElement(self):
        parse(self.xml, Mock(return_value=self.parser))
        self.assertEqual(self.parser.end_handler.call_args[0][0].tag, 'root')

    def testParseReturnsRecord(self):
        record = parse(self.xml, Mock(return_value=self.parser))
        self.assertEqual(record, self.parser.record)


class FgdcParserTestCase(unittest.TestCase):
    def test_parser_skips_empty_elements(self):
        record = parse(
            io.BytesIO(u'<metadata><title/></metadata>'.encode('utf-8')),
            FGDCParser)
        assert 'dc_title_s' not in record

    def testParserReturnsThemeKeywordsAsSet(self):
        record = parse(io.open('tests/fixtures/repo/foo/bar/fgdc.xml', 'rb'),
                       FGDCParser)
        self.assertEqual(record['dc_subject_sm'],
                         set(['point', 'names', 'features']))
