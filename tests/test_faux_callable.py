# -*- coding: utf-8 -*-
"""Test the `faux_callable` mark."""
import pytest

import fauxfactory

from pytest_fauxfactory.marks import faux_callable


def is_numeric(value):
    """Check if value is numeric."""
    return value.isnumeric()


def test_faux_callable_with_none_items():
    """Test that None items return always one iteration"""
    def simple_callable():
        # simple callable that return True
        return True
    values = [value for value in faux_callable(None, simple_callable)]
    assert len(values) == 1
    assert values[0] is True


def test_callable_mark_without_arguments(testdir):
    """Check that missing arguments is detected."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_callable()
        def test_foo_without_args(value):
            assert True
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Missing arguments' in result.stdout.str()
    assert result.ret == 2


def test_callable_mark_without_callable_function(testdir):
    """Check that missing callable function is detected."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_callable(1)
        def test_foo_without_callable_function(value):
            assert True
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Missing arguments' in result.stdout.str()
    assert result.ret == 2


def test_callable_mark_incorrect_items_argument_type(testdir):
    """Check that first argument to mark is numeric."""
    testdir.makepyfile("""
        import fauxfactory
        import pytest
        @pytest.mark.faux_callable('1', fauxfactory.gen_alpha)
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Mark expected an integer' in result.stdout.str()
    assert result.ret == 2


def test_callable_mark_incorrect_items_argument(testdir):
    """Check that first argument to mark is numeric."""
    testdir.makepyfile("""
        import fauxfactory
        import pytest
        @pytest.mark.faux_callable(0, fauxfactory.gen_alpha)
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Mark expected an integer greater than 0' in result.stdout.str()
    assert result.ret == 2


def test_callable_mark_incorrect_callable_argument_type(testdir):
    """Check that second argument to mark is callable."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_callable(1, 'I am not a callable')
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Mark expected a callable function' in result.stdout.str()
    assert result.ret == 2


def test_callable_mark_number_of_tests_generated(testdir):
    """check that the number of tests generated is correct."""
    testdir.makepyfile("""
        import fauxfactory
        import pytest
        @pytest.mark.faux_callable(10, fauxfactory.gen_alpha)
        def test_callable_as_first_argument(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=10)
    assert result.ret == 0


def test_callable_mark_incorrect_value(testdir):
    """Check that argument `value` is not being used for callable mark."""
    testdir.makepyfile("""
        import fauxfactory
        import pytest
        @pytest.mark.faux_callable(10, fauxfactory.gen_alpha)
        def test_something(foo):
            assert foo
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'uses no argument \'value\'' in result.stdout.str()
    assert result.ret == 2


@pytest.mark.faux_callable(2, fauxfactory.gen_boolean)
def test_callable_without_kwargs_callable_without_argument(value):
    """test callable that should not accept argument"""
    assert value in (True, False)


@pytest.mark.faux_callable(2, fauxfactory.gen_alphanumeric)
def test_callable_without_kwargs_callable_with_kwargs_default_values(value):
    """Test callable that has kwargs with default values"""
    # gen_alphanumeric length default value = 10
    assert len(value) == 10


@pytest.mark.faux_callable(
    1,
    fauxfactory.gen_special,
    length=12,
    validator=is_numeric,
    default='1')
def test_callable_with_kwargs(value):
    """Call `fauxfactory.gen_special` with kwargs that returns default of `1`.
    """
    assert value == '1'


def generic_func(*args, **kwargs):
    """generic function that return args and kwargs"""
    return args, kwargs


@pytest.mark.faux_callable(1, generic_func, 'arg_0', 'arg_1',
                           kwarg_0='kwarg_0', kwarg_1='kwarg_1')
def test_callable_with_args_and_kwargs(value):
    """Call generic function with args and kwargs"""
    assert isinstance(value, tuple)
    assert len(value) == 2
    args, kwargs = value
    assert args == ('arg_0', 'arg_1')
    assert kwargs == dict(kwarg_0='kwarg_0', kwarg_1='kwarg_1')


@pytest.mark.faux_callable(4, fauxfactory.gen_integer, min_value=0,
                           max_value=100)
def test_callable_generate_integers(value):
    """Test function that return generated integer"""
    assert isinstance(value, int)
    assert 0 <= value <= 100


def generate_alpha_strings(number=1, length=10):
    """function that return a tuple of generated alpha string"""
    return tuple(fauxfactory.gen_alpha(length=length) for _ in range(number))


@pytest.mark.faux_callable(5, generate_alpha_strings, 3, length=12)
def test_callable_generate_from_custom_function(value):
    """Test generic function that return a tuple of generated strings"""
    assert isinstance(value, tuple)
    assert len(value) == 3
    # we can also unpack
    location, organization, cv = value
    for str_alpha in (location, organization, cv):
        assert len(str_alpha) == 12
    assert location != organization
    assert location != cv


def generate_rgb(number=1):
    """Generate random RGB values."""
    return tuple(fauxfactory.gen_integer(0, 255) for _ in range(number))


@pytest.mark.faux_callable(4, generate_rgb, number=3)
def test_callable_generate_from_custom_function_rgb(value):
    """Test generic function that return a tuple of rgb integers"""
    assert isinstance(value, tuple)
    assert len(value) == 3
    for rgb_int in value:
        assert 0 <= rgb_int <= 255


def generate_person():
    """Generate a random person record."""
    return {
        'name': fauxfactory.gen_alpha(length=12),
        'age': fauxfactory.gen_integer(min_value=12, max_value=100)
    }


@pytest.mark.faux_callable(3, generate_person)
def test_callable_generate_person(value):
    """Test generic function that return a dict"""
    assert isinstance(value, dict)
    assert 'name' in value
    assert 'age' in value
    assert len(value['name']) == 12
    assert 12 <= value['age'] <= 100


def generate_person_in_tuple():
    """Generate a random person record in a tuple (name, age)."""
    return (
        fauxfactory.gen_alpha(length=12),
        fauxfactory.gen_integer(min_value=12, max_value=100)
    )


@pytest.mark.faux_callable(3, generate_person_in_tuple, argnames='name, age')
def test_callable_generate_with_custom_args(name, age):
    """Test generic function with custom arguments."""
    assert len(name) == 12
    assert 12 <= age <= 100
