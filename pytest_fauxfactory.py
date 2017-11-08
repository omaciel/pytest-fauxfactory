# -*- coding: utf-8 -*-
"""Provides FauxFactory helper methods."""
import fauxfactory
import pytest

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


def faux_string(items=None, str_type=None, *args, **kwargs):
    """Generate a new string type."""
    item = 0

    if items is None:
        items = 1
    if str_type is None:
        str_type = fauxfactory.gen_choice(STRING_TYPES)

    while item < items:
        yield fauxfactory.gen_string(str_type, *args, **kwargs)
        item += 1


def pytest_generate_tests(metafunc):
    """Parametrize tests using `faux_string` mark."""
    if hasattr(metafunc.function, 'faux_string'):
        # We should have at least the first 2 arguments to faux_string
        args = metafunc.function.faux_string.args
        if len(args) == 0:
            args = (1, None)
        elif len(args) == 1:
            args = (args[0], None)
        items, str_type = args
        if not isinstance(items, int):
            raise pytest.UsageError(
                'Mark expected an integer, got a {}: {}'.format(
                    type(items), items))
        if items < 1:
            raise pytest.UsageError(
                'Mark expected an integer greater than 0, got {}'.format(
                    items))
        kwargs = metafunc.function.faux_string.kwargs
        data = faux_string(items, str_type, *args[2:], **kwargs)
        metafunc.parametrize('value', data)
