# -*- coding: utf-8 -*-
"""Analyse pytest-fauxfactory marks and passes arguments and keywords to
pytest's parametrize method."""
from pytest_fauxfactory.handlers import MARK_HANDLERS

from pytest_fauxfactory.helpers import generate_ids, get_mark_function


def pytest_generate_tests(metafunc):
    """Parametrize tests using `faux_string` `faux_callable` 'faux_generator'
    marks."""
    func = get_mark_function(metafunc)
    if func:
        args = func.args
        kwargs = func.kwargs
        argnames = kwargs.pop('argnames', 'value')

        data = MARK_HANDLERS[func.name](args, kwargs)

        if data:
            data = [_ for _ in data]
            metafunc.parametrize(
                argnames,
                data,
                ids=generate_ids(data, func.name))
