# -*- coding: utf-8 -*-


class InvalidDataError(Exception):
    def __init__(self, field, value):
        super(InvalidDataError, self).__init__(field, value)
        self.field = field
        self.value = value
