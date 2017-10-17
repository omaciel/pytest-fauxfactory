# -*- coding: utf-8 -*-
"""Provides FauxFactory helper methods."""
import fauxfactory

STRING_TYPES = (
    'alpha',
    'alphanumeric',
    'cjk',
    'html',
    'latin1',
    'numeric',
    'utf8',
    'punctuation',
)


def gen_string(items=None, str_type=None, *args, **kwargs):
    """Generate a new string type."""
    item = 0

    if items is None:
        items = 1
    if str_type is None:
        str_type = fauxfactory.gen_choice(STRING_TYPES)

    while item < items:
        yield fauxfactory.gen_string(str_type, *args, **kwargs)
        item += 1
