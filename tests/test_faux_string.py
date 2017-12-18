# -*- coding: utf-8 -*-
"""Test the `faux_string` mark."""
import pytest


def is_numeric(value):
    """Check if value is numeric."""
    return value.isnumeric()


def contains_number(value):
    """Check to see if the string contains a number."""
    return any(char.isnumeric() for char in value)


def test_mark_plain(testdir):
    """Check that mark `faux_string` adds 10 iterations to test."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_string(10)
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
        @pytest.mark.faux_string(10)
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
        @pytest.mark.faux_string(10)
        def test_something(foo):
            assert foo
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'uses no argument \'value\'' in result.stdout.str()
    assert result.ret == 2


def test_mark_str_type_argument(testdir):
    """Check that passing only str_type argument works."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_string('alpha')
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == 0


def test_mark_incorrect_str_type_argument(testdir):
    """Check that passing incorrect str_type argument raises error."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_string('alphabet')
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'String type alphabet is not supported' in result.stdout.str()
    assert result.ret == 2


def test_mark_incorrect_argument(testdir):
    """Check that first argument to mark is numeric."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_string('1')
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'String type 1 is not supported' in result.stdout.str()
    assert result.ret == 2


def test_mark_invalid_integer(testdir):
    """Check that first argument to mark is valid integer."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_string(0)
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Mark expected an integer greater than 0' in result.stdout.str()
    assert result.ret == 2


@pytest.mark.faux_string()
def test_gen_alpha_string_with_no_arguments(value):
    """Passing no arguments should return a random string type."""
    assert len(value) > 0


@pytest.mark.faux_string(1)
def test_gen_alpha_string_with_limit_arguments(value):
    """Passing limit argument should return a random string type."""
    assert len(value) > 0


@pytest.mark.faux_string(4, 'alpha', length=12)
def test_gen_alpha_string_with_length(value):
    """Generate an `alpha` string of length 12."""
    assert len(value) == 12


@pytest.mark.faux_string(
    1,
    'punctuation',
    length=12,
    validator=is_numeric,
    default='1')
def test_gen_alpha_string_with_validator(value):
    """Call `faux_string` with validator that returns default of `1`."""
    assert value == '1'


@pytest.mark.faux_string(4, 'alpha', length=[5, 15])
def test_gen_alpha_string_with_variable_length(value):
    """Generate an `alpha` string of length of either 5 or 15."""
    assert len(value) == 5 or len(value) == 15


@pytest.mark.faux_string(4, [], length=[5, 30])
def test_gen_alpha_string_with_empty_types(value):
    """Generate default alpha strings with length 5 and 30 characters."""
    assert len(value) >= 5


@pytest.mark.faux_string(4, ['alpha', 'alphanumeric'], length=[])
def test_gen_alpha_string_with_empty_length(value):
    """Generate default alpha strings with length as empty list."""
    assert len(value) == 10


@pytest.mark.faux_string(4, [], length=[])
def test_gen_alpha_string_with_empty_types_and_length(value):
    """Generate default alpha strings with types and length as empty lists."""
    assert len(value) >= 10


@pytest.mark.faux_string(4, ['alpha', 'numeric'], length=[5, 30])
def test_gen_alpha_string_with_variable_types(value):
    """Generate alpha strings with length 5, alphanumeric with length 30."""
    if len(value) == 5:
        assert not contains_number(value)
    else:
        assert contains_number(value)


@pytest.mark.faux_string(2, 'alpha', argnames='name')
def test_gen_alpha_string_with_custom_arg_name(name):
    """Generate default alpha strings with custom argument."""
    assert len(name) == 10
