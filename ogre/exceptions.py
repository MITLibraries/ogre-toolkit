# -*- coding: utf-8 -*-


class InvalidDataError(Exception):
    def __init__(self, field, value):
        self.field = field
        self.value = value
