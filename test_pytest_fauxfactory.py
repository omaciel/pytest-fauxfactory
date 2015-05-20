# -*- coding: utf-8 -*-
import pytest


def test_namespace_presence():
    pytest.faux


def test_function_works():
    assert len(pytest.faux.gen_alphanumeric()) > 0
