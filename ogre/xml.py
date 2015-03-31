# -*- coding: utf-8 -*-
from __future__ import absolute_import
try:
    from lxml.etree import iterparse
except ImportError:
    from xml.etree.ElementTree import iterparse


def parse(fp, parser):
    """
    Parse XML data using the specified parser.

    A parser class must implement at least two methods,
    ``start_handler`` and ``end_handler``, which accept an ``Element``.
    These methods must populate an instance property ``record`` which is
    returned when parsing is complete.

    :param source: file name or file pointer containing XML data
    :param parser: parser class to use for parsing
    """

    parser = parser()
    for event, elem in iterparse(fp, events=('start', 'end')):
        if event == 'start':
            parser.start_handler(elem)
        else:
            parser.end_handler(elem)
            elem.clear()
    return parser.record


class FGDCParser(object):
    """An FGDC XML parser."""

    def __init__(self):
        #: Parsed GeoBlacklight record
        self.record = {}

    def start_handler(self, elem):
        """
        Start handler called when encountering a new element.

        No-op.
        """

        pass

    def end_handler(self, elem):
        """End handler called when encountering the end of an element."""

        if elem.tag == 'title':
            self.record['dc_title_s'] = elem.text
        elif elem.tag == 'origin':
            self.record.setdefault('dc_creator_sm', set()).add(elem.text)
        elif elem.tag == 'abstract':
            self.record['dc_description_s'] = elem.text
        elif elem.tag == 'publish':
            self.record['dc_publisher_s'] = elem.text
        elif elem.tag == 'westbc':
            self.record['_bbox_w'] = elem.text
        elif elem.tag == 'eastbc':
            self.record['_bbox_e'] = elem.text
        elif elem.tag == 'northbc':
            self.record['_bbox_n'] = elem.text
        elif elem.tag == 'southbc':
            self.record['_bbox_s'] = elem.text
        elif elem.tag == 'accconst':
            self.record['dc_rights_s'] = elem.text
        elif elem.tag == 'themekey':
            self.record.setdefault('dc_subject_sm', set()).add(elem.text)
        elif elem.tag == 'placekey':
            self.record.setdefault('dct_spatial_sm', set()).add(elem.text)
        elif elem.tag == 'direct':
            if elem.text.lower() == 'raster':
                self.record['layer_geom_type_s'] = elem.text
        elif elem.tag == 'sdtstype':
            self.record['layer_geom_type_s'] = elem.text
