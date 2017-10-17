# -*- coding: utf-8 -*-
import pytest
from pytest_fauxfactory import gen_string


def pytest_generate_tests(metafunc):
    if hasattr(metafunc.function, 'gen_string'):
        # We should have at least the first 2 arguments to gen_string
        args = metafunc.function.gen_string.args
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
            raise pytest.UsageError('Mark expected an integer greater than 0, got {}'.format(items))
        kwargs = metafunc.function.gen_string.kwargs
        data = gen_string(items, str_type, *args[2:], **kwargs)
        metafunc.parametrize('value', data)


pytest_plugins = ("pytest_fauxfactory", )  # Specify the plugin so py.test finds it on Travis
