pytest-fauxfactory
==================

.. image:: https://img.shields.io/pypi/v/pytest-fauxfactory.svg
    :target: https://pypi.python.org/pypi/pytest-fauxfactory

.. image:: https://img.shields.io/pypi/l/pytest-fauxfactory.svg
    :target: https://pypi.python.org/pypi/pytest-fauxfactory

.. image:: https://img.shields.io/pypi/pyversions/pytest-fauxfactory.svg
    :target: https://pypi.python.org/pypi/pytest-fauxfactory

.. image:: https://travis-ci.org/omaciel/pytest-fauxfactory.svg?branch=master
    :target: https://travis-ci.org/omaciel/pytest-fauxfactory

---------------

**pytest-fauxfactory** is a **Pytest** plugin that helps you pass random data to your automated tests, leveraging the
power of `FauxFactory https://github.com/omaciel/fauxfactory`.

Features
--------

pytest-fauxfactory let's you create parameterized automated tests, providing:

- Randomically generated strings via **FauxFactory**
- Allowing you to provide a `callable` method to return the type and number of data items to be used by your tests
- Allowing you to provide a `generator` method to return the type and number of data items to be used by your tests

Installation
------------


::

    $ pip install pytest-fauxfactory


Usage Examples
--------------


Generating Random Strings: faux_string
++++++++++++++++++++++++++++++++++++++
Let's say you need to generate a random string value (identified as **author**) for a test

.. code-block:: python

    @pytest.mark.faux_string()
    def test_generate_alpha_strings():
        assert value

The allowed types of strings that can be generated are:

- alpha
- alphanumeric
- cjk
- html
- latin1
- numeric
- utf8
- punctuation

Using the `faux_string` mark without any arguments will generate a single random string for your test.

::

    test_generate_alpha_strings[faux_string_0] PASSED


Suppose you want to generate **4** random **alpha** strings (identified as **book**) for a test:

.. code-block:: python

    @pytest.mark.faux_string(4, 'alpha')
    def test_generate_alpha_strings(value):
        assert value.isalpha()


You will then have 4 tests, each with different values:

::

    test_generate_alpha_strings[faux_string_0] PASSED
    test_generate_alpha_strings[faux_string_1] PASSED
    test_generate_alpha_strings[faux_string_2] PASSED
    test_generate_alpha_strings[faux_string_3] PASSED

Now, suppose you also want to make sure that all strings have exactly 43 characters:

.. code-block:: python

    @pytest.mark.faux_string(4, 'alpha', length=43)
    def test_generate_alpha_strings(value):
        assert len(value) == 43

Additionally, you can run tests with different string lengths by passing in a list of lengths:

.. code-block:: python

    @pytest.mark.faux_string(4, 'alpha', length=[5, 15])
    def test_gen_alpha_string_with_variable_length(value):
        """Generate an `alpha` string of length of either 5 or 15."""
        assert len(value) == 5 or len(value) == 15

This will generate 4 new tests

::

    tests/test_faux_string.py::test_gen_alpha_string_with_variable_length[faux_string_0] PASSED                                                                                                                                          [ 91%]
    tests/test_faux_string.py::test_gen_alpha_string_with_variable_length[faux_string_1] PASSED                                                                                                                                [ 92%]
    tests/test_faux_string.py::test_gen_alpha_string_with_variable_length[faux_string_2] PASSED                                                                                                                                          [ 93%]
    tests/test_faux_string.py::test_gen_alpha_string_with_variable_length[faux_string_3] PASSED

Similarly, you can run tests with different string types by passing in a list of types:

.. code-block:: python

    @pytest.mark.faux_string(4, ['alpha', 'alphanumeric'], length=[5, 10])
    def test_gen_alpha_string_with_variable_types(value):
        """Generate alpha strings with length 5, alphanumeric with length 10."""
        if len(value) == 5:
            assert not contains_number(value)
        else:
            assert contains_number(value)

This will generate 4 new tests

::

    tests/test_faux_string.py::test_gen_alpha_string_with_variable_types[faux_string_0] PASSED                                                                                                                                           [ 96%]
    tests/test_faux_string.py::test_gen_alpha_string_with_variable_types[faux_string_1] PASSED                                                                                                                                      [ 97%]
    tests/test_faux_string.py::test_gen_alpha_string_with_variable_types[faux_string_2] PASSED                                                                                                                                           [ 98%]
    tests/test_faux_string.py::test_gen_alpha_string_with_variable_types[faux_string_3] PASSED


Using Custom Functions: faux_callable
+++++++++++++++++++++++++++++++++++++
Now imagine that you have a custom function that generates values of any type instead of the default types used by
`faux_string`. Using `fauxfactory.gen_integer` for example:

.. code-block:: python

    import fauxfactory
    import pytest

    @pytest.mark.faux_callable(4, fauxfactory.gen_integer)
    def test_callable_generate_integers(value):
        """Test function that return generated integer"""
        assert isinstance(value, int)


This will generate 4 new tests

::

    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_2] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_3] PASSED


faux_callable can also transfer arguments to the callable function:

.. code-block:: python

    import fauxfactory
    import pytest

    @pytest.mark.faux_callable(4, fauxfactory.gen_integer, min_value=0,
                               max_value=100)
    def test_callable_generate_integers(value):
        """Test function that return generated integer with kwargs"""
        assert isinstance(value, int)
        assert 0 <= value <= 100

This will generate 4 new tests

::

    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_2] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[faux_callable_3] PASSED


Of course the generated values can be of any type! For example, let's generate values as a tuple of alpha strings:

.. code-block:: python

    import fauxfactory
    import pytest

    def generate_alpha_strings(number=1, length=10):
        """function that return a tuple of generated alpha string"""
        return tuple(fauxfactory.gen_alpha(length=length) for _ in range(number))

    @pytest.mark.faux_callable(5, generate_alpha_strings, number=3, length=12)
    def test_callable_generate_from_custom_function(value):
        """Test generic function that return a tuple of generated strings"""
        assert isinstance(value, tuple)
        assert len(value) == 3
        # unpack
        location, organization, cv = value
        for str_alpha in (location, organization, cv):
            assert len(str_alpha) == 12
            assert location != organization
            assert location != cv

This will generate 5 new tests

::

    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[faux_callable_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[faux_callable_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[faux_callable_2] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[faux_callable_3] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[faux_callable_4] PASSED


Let's now generate values from a custom function that returns a dictionary:

.. code-block:: python

    import fauxfactory
    import pytest

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

This will generate 3 new tests

::

    tests/test_pytest_fauxfactory.py::test_generate_person[faux_callable_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_person[faux_callable_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_person[faux_callable_2] PASSED


Using Generators: faux_generator
++++++++++++++++++++++++++++++++
Now instead of using a callable function, we want to generate tests with values
of any type from a generator function or generator expression.
For this purpose we can use the "faux_generator" mark:


.. code-block:: python

    def alpha_strings_generator(items=1, length=10):
        """Generate alpha string value at each iteration."""
        for _ in range(items):
            yield fauxfactory.gen_alpha(length=length)


    @pytest.mark.faux_generator(alpha_strings_generator(items=3, length=12))
    def test_generator_alpha_strings(value):
        """Test function generator with kwargs."""
        assert len(value) == 12

This will generate 3 new tests

::

    tests/test_pytest_fauxfactory.py::test_generator_alpha_strings[faux_generator_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_alpha_strings[faux_generator_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_alpha_strings[faux_generator_2] PASSED

We can also use a generator expression:

.. code-block:: python

    list_of_integers = [fauxfactory.gen_integer(min_value=0) for _ in range(4)]


    @pytest.mark.faux_generator(int_val for int_val in list_of_integers)
    def test_generator_expression(value):
        """Test generator expression."""
        assert isinstance(value, int)
        assert value >= 0

This will generate 4 tests

::

    tests/test_pytest_fauxfactory.py::test_generator_expression[faux_generator_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_expression[faux_generator_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_expression[faux_generator_2] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_expression[faux_generator_3] PASSED


Of course the returned values can be of any type:


.. code-block:: python

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


This will generate 2 tests

::

    tests/test_pytest_fauxfactory.py::test_generator_foo_generator[faux_generator_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_foo_generator[faux_generator_1] PASSED

We can also combine all the above generators:

.. code-block:: python

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

This will generate 9 tests

::

    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_0] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_1] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_2] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_3] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_4] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_5] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_6] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_7] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[faux_generator_8] PASSED

Custom test arguments usage
___________________________

Using the argnames keyword in any of the above decorators, we can customize the arguments used for the test function, to use "name" argument instead of "value":

.. code-block:: python

    @pytest.mark.faux_string(2, 'alpha', argnames='name')
    def test_gen_alpha_string_with_custom_arg_name(name):
        """Generate default alpha strings with custom argument."""
        assert len(name) == 10

This will generate 2 tests

::

    tests/test_faux_string.py::test_gen_alpha_string_with_custom_arg_name[faux_string_0] PASSED                                                                                                                          [ 50%]
    tests/test_faux_string.py::test_gen_alpha_string_with_custom_arg_name[faux_string_1] PASSED                                                                                                                          [100%]

We can also use multiple custom arguments:

.. code-block:: python

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

This will generate 3 tests

::

    tests/test_faux_callable.py::test_callable_generate_with_custom_args[faux_callable_0] PASSED
    tests/test_faux_callable.py::test_callable_generate_with_custom_args[faux_callable_1] PASSED
    tests/test_faux_callable.py::test_callable_generate_with_custom_args[faux_callable_2] PASSED

Documentation
-------------

Documentation is in the works but we would love to get help from the community!
