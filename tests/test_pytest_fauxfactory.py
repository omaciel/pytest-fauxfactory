# -*- coding: utf-8 -*-
"""Tests the `faux_string` mark."""
import fauxfactory
import pytest


def is_numeric(value):
    """Check if value is numeric."""
    return value.isnumeric()


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
    assert 'Mark expected an integer' in result.stdout.str()
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


def test_generator_mark_without_arguments(testdir):
    """Check that missing arguments is detected."""
    testdir.makepyfile("""
        import pytest
        @pytest.mark.faux_generator()
        def test_foo_without_args(value):
            assert True
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Missing arguments' in result.stdout.str()
    assert result.ret == 2


def test_generator_mark_with_incorrect_argument_type(testdir):
    """Check that non generator arg is detected."""
    testdir.makepyfile("""
        import pytest
        def gen_string():
            yield 'some string'
        @pytest.mark.faux_generator(gen_string(), 'I am not a generator')
        def test_something(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(error=1)
    assert 'Argument with index 1 is not a generator' in result.stdout.str()
    assert result.ret == 2


def test_generator_mark_number_of_tests_generated(testdir):
    """check that the number of tests generated is correct."""
    testdir.makepyfile("""
        import fauxfactory
        import pytest
        def gen_strings(items=1):
            for _ in range(items):
                yield fauxfactory.gen_alpha()
        @pytest.mark.faux_generator(gen_strings(10))
        def test_generator_test_number(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=10)
    assert result.ret == 0


def test_generator_mark_combined_gens_number_of_tests_generated(testdir):
    """check that using combined generators, generates the correct number of
     tests."""
    testdir.makepyfile("""
        import fauxfactory
        import pytest
        def gen_strings(items=1):
            for _ in range(items):
                yield fauxfactory.gen_alpha()
        @pytest.mark.faux_generator(
            (fauxfactory.gen_alpha() for _ in range(5)),
             gen_strings(5)
        )
        def test_generator_test_number(value):
            assert value
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=10)
    assert result.ret == 0


def alpha_strings_generator(items=1, length=10):
    """Generate alpha string value at each iteration."""
    for _ in range(items):
        yield fauxfactory.gen_alpha(length=length)


@pytest.mark.faux_generator(alpha_strings_generator(items=3, length=12))
def test_generator_alpha_strings(value):
    """Test function generator with kwargs"""
    assert len(value) == 12


list_of_integers = [fauxfactory.gen_integer(min_value=0) for _ in range(4)]


@pytest.mark.faux_generator(int_val for int_val in list_of_integers)
def test_generator_expression(value):
    """Test generator expression"""
    assert isinstance(value, int)
    assert value >= 0


def foo_generator():
    """Returns different values: first, a string 'foo'; second iteration, a
    list of integers."""
    yield 'foo'
    yield [1, 2, 3]


@pytest.mark.faux_generator(foo_generator())
def test_generator_foo_generator(value):
    """Test diffrent types values"""
    if isinstance(value, list):
        assert value == [1, 2, 3]
    else:
        assert value == 'foo'


@pytest.mark.faux_generator(
    alpha_strings_generator(items=3, length=12),
    (int_val for int_val in list_of_integers),
    foo_generator()
)
def test_generator_combined(value):
    """Test combined generators"""
    if isinstance(value, list):
        assert value == [1, 2, 3]
    elif isinstance(value, int):
        assert value >= 0
    else:
        assert value.isalpha()
