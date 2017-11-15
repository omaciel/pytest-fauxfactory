# -*- coding: utf-8 -*-
"""Test the `faux_generator` mark."""
import pytest

import fauxfactory


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
    """Check that the number of tests generated is correct."""
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
    """Check that using combined generators generates the correct number of
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
    """Test function generator with kwargs."""
    assert len(value) == 12


list_of_integers = [fauxfactory.gen_integer(min_value=0) for _ in range(4)]


@pytest.mark.faux_generator(int_val for int_val in list_of_integers)
def test_generator_expression(value):
    """Test generator expression."""
    assert isinstance(value, int)
    assert value >= 0


def foo_generator():
    """Returns different values: first, a string 'foo'; second iteration, a
    list of integers."""
    yield 'foo'
    yield [1, 2, 3]


@pytest.mark.faux_generator(foo_generator())
def test_generator_foo_generator(value):
    """Test diffrent type values."""
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
    """Test combined generators."""
    if isinstance(value, list):
        assert value == [1, 2, 3]
    elif isinstance(value, int):
        assert value >= 0
    else:
        assert value.isalpha()
