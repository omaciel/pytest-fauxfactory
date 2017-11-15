# -*- coding: utf-8 -*-
"""Analyse pytest-fauxfactory marks and passes arguments and keywords to
pytest's parametrize method."""
from pytest_fauxfactory.handlers import MARK_HANDLERS

from pytest_fauxfactory.helpers import get_mark_function


def pytest_generate_tests(metafunc):
    """Parametrize tests using `faux_string` `faux_callable` 'faux_generator'
    marks."""
    func = get_mark_function(metafunc)
    if func:
        # import pdb; pdb.set_trace()
        args = func.args
        kwargs = func.kwargs
        argnames = kwargs.pop('argnames', 'value')
        # if not isinstance(argnames, (tuple, list)):
        #     argnames = [x.strip() for x in argnames.split(",") if x.strip()]

        data = MARK_HANDLERS[func.name](args, kwargs)

        if data:
            metafunc.parametrize(argnames, data)
