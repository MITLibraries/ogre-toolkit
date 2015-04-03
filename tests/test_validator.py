# -*- coding: utf-8 -*-
from __future__ import absolute_import
from jsonschema import ValidationError
from mock import patch, Mock
from ogre.validator import Validator

import unittest

class ValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.fakeSchemaUrl = 'http://fake-url.json'
        self.testSchema = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "required": [
                "uuid"
            ],
            "type": "object",
            "properties": {
                "uuid": { 
                    "type": "string"

                },
                "layer_geom_type_s": { 
                    "type": "string",
                    "enum": [
                        "Line",
                        "Mixed",
                        "Paper Map",
                        "Point",
                        "Polygon",
                        "Raster",
                        "Scanned Map"
                    ]

                },
                "solr_year_i": { 
                    "type": "integer"
                },
                "dc_creator_sm": { 
                    "type": "array",
                    "items": {
                         "type": "string"
                     }

                }
            }
        }

        self.schema_mock_response = Mock()
        self.schema_mock_response.json.return_value = self.testSchema

        with patch('requests.get') as self.schema_mock_request:
            self.schema_mock_request.return_value = self.schema_mock_response

            self.validator = Validator(self.fakeSchemaUrl)


    def testSchemaIsRequestedAndReturned(self):
        self.schema_mock_request.assert_called_once_with(self.fakeSchemaUrl)
        self.schema_mock_response.json.assert_called_once()
        self.assertEqual(self.validator._schema, self.testSchema)

    def testValidDataPasses(self):
        testData = {
            'uuid': '12345'
        }

        self.validator.is_valid(testData)

    def testInvalidDataThrowsValidationError(self):
        testData = {
            'id': 12345
        }

        self.assertRaises(ValidationError, self.validator.is_valid, testData)
