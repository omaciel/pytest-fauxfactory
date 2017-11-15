# -*- coding: utf-8 -*-
"""Provides helper methods to pytest-fauxfactory."""


def get_mark_function(metafunc):
    for key in metafunc.function.__dict__:
        if key.lower().startswith('faux'):
            return getattr(metafunc.function, key)
