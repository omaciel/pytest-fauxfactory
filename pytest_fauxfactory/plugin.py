# -*- coding: utf-8 -*-
"""Analyse pytest-fauxfactory marks and passes arguments and keywords to
pytest's parametrize method."""
from pytest_fauxfactory.handlers import MARK_HANDLERS

from pytest_fauxfactory.helpers import (
    extract_arguments,
    extract_keyword_arguments,
    get_mark_function,
)


def pytest_generate_tests(metafunc):
    """Parametrize tests using `faux_string` `faux_callable` 'faux_generator'
    marks."""
    func = get_mark_function(metafunc)
    if func:
        args = extract_arguments(func)
        kwargs = extract_keyword_arguments(func)

        data = MARK_HANDLERS[func.name](args, kwargs)

        if data:
            metafunc.parametrize('value', data)
