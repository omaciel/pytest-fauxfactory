# -*- coding: utf-8 -*-
"""Provides helper methods to pytest-fauxfactory."""


def extract_arguments(func):
    """Extract arguments passed to a function."""
    return func.args


def extract_keyword_arguments(func):
    """Extract keyword arguments passed to a function."""
    return func.kwargs


def get_mark_function(metafunc):
    for key in metafunc.function.__dict__:
        if key.lower().startswith('faux'):
            return getattr(metafunc.function, key)
