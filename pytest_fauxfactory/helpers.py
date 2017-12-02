# -*- coding: utf-8 -*-
"""Provides helper methods to pytest-fauxfactory."""


def generate_ids(data, func_name):
    """Generate IDs for parametrize method."""
    return [
        '{}_{}'.format(func_name, idx)
        for idx
        in range(len(data))
    ]


def get_mark_function(metafunc):
    """Extract the name of the function being called."""
    for key in metafunc.function.__dict__:
        if key.lower().startswith('faux'):
            return getattr(metafunc.function, key)
