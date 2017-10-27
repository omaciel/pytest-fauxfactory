# -*- coding: utf-8 -*-
"""Tests the `gen_string` mark."""
import pytest


def is_numeric(value):
    """Check if value is numeric."""
    return value.isnumeric()


def test_mark_plain(testdir):
    """Check that mark `gen_string` adds 10 iterations to test."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.gen_string(10)
        def test_something(value):
            assert 1 == 1
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=10)
    assert result.ret == 0


def test_mark_correct_value(testdir):
    """Check that argument `value` is being used to pass random data."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.gen_string(10)
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=10)
    assert result.ret == 0


def test_mark_incorrect_value(testdir):
    """Check that argument `value` is not being used."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.gen_string(10)
        def test_something(foo):
            assert foo
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'uses no argument \'value\'' in result.stdout.str()
    assert result.ret == 2


def test_mark_incorrect_argument(testdir):
    """Check that first argument to mark is numeric."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.gen_string('1')
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Mark expected an integer' in result.stdout.str()
    assert result.ret == 2


def test_mark_invalid_integer(testdir):
    """Check that first argument to mark is valid integer."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.gen_string(0)
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Mark expected an integer greater than 0' in result.stdout.str()
    assert result.ret == 2


@pytest.mark.gen_string()
def test_gen_alpha_string_with_no_arguments(value):
    """Passing no arguments should return a random string type."""
    assert len(value) > 0


@pytest.mark.gen_string(1)
def test_gen_alpha_string_with_limit_arguments(value):
    """Passing limit argument should return a random string type."""
    assert len(value) > 0


@pytest.mark.gen_string(4, 'alpha', length=12)
def test_gen_alpha_string_with_length(value):
    """Generate an `alpha` string of length 12."""
    assert len(value) == 12


@pytest.mark.gen_string(
    1,
    'punctuation',
    length=12,
    validator=is_numeric,
    default='1')
def test_gen_alpha_string_with_validator(value):
    """Call `gen_string` with validator that returns default of `1`."""
    assert value == '1'
