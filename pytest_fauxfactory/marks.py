# -*- coding: utf-8 -*-
"""FauxFactory specific marks methods."""
from itertools import chain

import fauxfactory

from pytest_fauxfactory.constants import STRING_TYPES


def faux_callable(items, callable_func, *args, **kwargs):
    """Generate new values from callable object."""
    if items is None:
        items = 1
    for _ in range(items):
        yield callable_func(*args, **kwargs)


def faux_generator(*args):
    """Generate values from generators passed as arguments."""
    return chain.from_iterable(args)


def faux_string(items, str_type=None, *args, **kwargs):
    """Generate a new string type."""
    item = 0

    if str_type is None:
        str_type = fauxfactory.gen_choice(STRING_TYPES)

    while item < items:
        yield fauxfactory.gen_string(str_type, *args, **kwargs)
        item += 1
