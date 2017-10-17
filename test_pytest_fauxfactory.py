# -*- coding: utf-8 -*-
import pytest


@pytest.mark.gen_string()
def test_gen_alpha_string_with_no_arguments(value):
    '''Passing no arguments should return a random string type.'''
    assert len(value) > 0


@pytest.mark.gen_string(4, 'alpha', length=12)
def test_gen_alpha_string_with_length(value):
    '''Generate an `alpha` string of length 12.'''
    assert len(value) == 12
