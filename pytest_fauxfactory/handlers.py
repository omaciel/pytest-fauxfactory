# -*- coding: utf-8 -*-
"""Methods to handle specific pytest marks."""
from inspect import isgenerator

import pytest

from pytest_fauxfactory.constants import STRING_TYPES
from pytest_fauxfactory.marks import faux_callable, faux_generator, faux_string


def callable_mark_handler(args, kwargs):
    """"pytest faux_callable mark handler"""
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


def generator_mark_handler(args, kwargs=None):
    """"pytest faux_generator mark handler."""
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


def string_mark_handler(args, kwargs):
    """"pytest faux_string mark handler"""
    # We should have at least the first 2 arguments to faux_string
    if len(args) == 0:
        args = (1, None)
    elif len(args) == 1:
        if isinstance(args[0], int):
            args = (args[0], None)
        elif isinstance(args[0], str):
            if args[0] in STRING_TYPES:
                args = (1, args[0])
            else:
                raise pytest.UsageError(
                    'String type {} is not supported.'.format(args[0])
                )
    items, str_type = args[0:2]

    if items < 1:
        raise pytest.UsageError(
            'Mark expected an integer greater than 0, got {}'.format(
                items))

    return faux_string(items, str_type, *args[2:], **kwargs)


MARK_HANDLERS = {
    'faux_callable': callable_mark_handler,
    'faux_generator': generator_mark_handler,
    'faux_string': string_mark_handler,
}
