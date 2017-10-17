# -*- coding: utf-8 -*-
import pytest
from pytest_fauxfactory import gen_string


def pytest_generate_tests(metafunc):
    if hasattr(metafunc.function, 'gen_string'):
        # We should have at least the first 2 arguments to gen_string
        args = metafunc.function.gen_string.args
        if len(args) < 2:
            args = (None, None)
        items, str_type = args
        kwargs = metafunc.function.gen_string.kwargs
        data = gen_string(items, str_type, *args[2:], **kwargs)
        metafunc.parametrize('value', data)


pytest_plugins = ("pytest_fauxfactory", )  # Specify the plugin so py.test finds it on Travis
