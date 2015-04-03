# -*- coding: utf-8 -*-
from __future__ import absolute_import
from jsonschema import validate, Draft4Validator

import requests

class Validator(object):
    """Defines a Validator for objects.

    :param str schema_url: url to file that contains json-schema object
    :raises AttributeError: when missing schema_url
    """
    def __init__(self, schema_url):
        self._schema = self._get_schema(schema_url)
        self._types = {
            "array": (list, set)
        }
        
        self._validator = Draft4Validator(schema=self._schema, types=self._types)

    def _get_schema(self, schema_url):
        r = requests.get(schema_url)
        r.raise_for_status()

        return r.json()

    def is_valid(self, obj):
        for key, value in obj.items():
            if value is None:
                del obj[key]

        self._validator.validate(obj)