# -*- coding: utf-8 -*-
"""Provides FauxFactory helper methods."""
from inspect import isgenerator
from itertools import chain

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


def faux_callable(items, callable_func, *args, **kwargs):
    """Generate new values from callable object."""
    if items is None:
        items = 1
    for _ in range(items):
        yield callable_func(*args, **kwargs)


def faux_generator(*args):
    """Generate values from generators passed as arguments."""
    return chain.from_iterable(args)


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


def _pytest_faux_callable_mark_handler(metafunc):
    """"pytest faux_callable mark handler"""
    args = metafunc.function.faux_callable.args
    kwargs = metafunc.function.faux_callable.kwargs

    usage_message = (
        'usage: faux_callable(items, callable_function, *args, **kwargs)'
    )

    if len(args) < 2:
        raise pytest.UsageError(
            'Missing arguments: {0}'.format(usage_message)
        )

    items, callable_function = args[0:2]
    if not isinstance(items, int):
        raise pytest.UsageError(
            'Mark expected an integer, got a {}: {}'.format(
                type(items), items))
    if items < 1:
        raise pytest.UsageError(
            'Mark expected an integer greater than 0, got {}'.format(
                items))
    if not callable(callable_function):
        raise pytest.UsageError(
            'Mark expected a callable function, got a {}: {}'.format(
                type(callable_function), callable_function))

    return faux_callable(items, callable_function, *args[2:], **kwargs)


def _pytest_faux_generator_mark_handler(metafunc):
    """"pytest faux_generator mark handler."""
    args = metafunc.function.faux_generator.args
    usage_message = 'usage: faux_generator(generator)'

    if len(args) == 0:
        raise pytest.UsageError(
            'Missing arguments, {0}'.format(usage_message)
        )
    for index, arg in enumerate(args):
        if not isgenerator(arg):
            raise pytest.UsageError(
                'Argument with index {0} is not a generator, {1}'
                .format(index, usage_message)
            )

    return faux_generator(*args)


def _pytest_faux_string_mark_handler(metafunc):
    """"pytest faux_string mark handler"""
    # We should have at least the first 2 arguments to faux_string
    args = metafunc.function.faux_string.args
    if len(args) == 0:
        args = (1, None)
    elif len(args) == 1:
        args = (args[0], None)
    items, str_type = args[0:2]
    if not isinstance(items, int):
        raise pytest.UsageError(
            'Mark expected an integer, got a {}: {}'.format(
                type(items), items))
    if items < 1:
        raise pytest.UsageError(
            'Mark expected an integer greater than 0, got {}'.format(
                items))
    kwargs = metafunc.function.faux_string.kwargs

    return faux_string(items, str_type, *args[2:], **kwargs)


def pytest_generate_tests(metafunc):
    """Parametrize tests using `faux_string` `faux_callable` 'faux_generator'
    marks."""
    data = None
    if hasattr(metafunc.function, 'faux_string'):
        data = _pytest_faux_string_mark_handler(metafunc)
    elif hasattr(metafunc.function, 'faux_callable'):
        data = _pytest_faux_callable_mark_handler(metafunc)
    elif hasattr(metafunc.function, 'faux_generator'):
        data = _pytest_faux_generator_mark_handler(metafunc)

    if data:
        metafunc.parametrize('value', data)
