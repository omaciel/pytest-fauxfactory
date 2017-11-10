pytest-fauxfactory
==================

Now you pass random data to your tests using this **Pytest** plugin for `FauxFactory https://github.com/omaciel/fauxfactory`.

The easiest way to use it is to decorate your test with the `faux_string` mark and write a test that expects a `value` argument:

.. code-block:: python

    @pytest.mark.faux_string()
    def test_generate_alpha_strings(value):
        assert value

By default a single random string will be generated for your test.

::

    test_generate_alpha_strings[:<;--{#+,&] PASSED


Suppose you want to generate **4** random strings (identified as **value**) for a test:

.. code-block:: python

    @pytest.mark.faux_string(4, 'alpha')
    def test_generate_alpha_strings(value):
        assert value.isalpha()


You will then have 4 tests, each with different values:

::

    test_generate_alpha_strings[EiOKPHSXNYfv] PASSED
    test_generate_alpha_strings[BBATlPxwmHaP] PASSED
    test_generate_alpha_strings[kXIGIIXOyZyv] PASSED
    test_generate_alpha_strings[eqHxEFneSKNC] PASSED


Now, suppose you also want to make sure that all strings have exactly 43 characters:

.. code-block:: python

    @pytest.mark.faux_string(4, 'alpha', length=43)
    def test_generate_alpha_strings(value):
        assert len(value) == 43


You can also get random types of strings by excluding the second argument:

.. code-block:: python

    @pytest.mark.faux_string(4)
    def test_generate_alpha_strings(value):
        assert len(value) > 0


Now imagine that you have a custom function that generates values of any type instead of the default types used in faux_string. For that you can use the "faux_callable" mark:

.. code-block:: python

    import fauxfactory
    import pytest

    @pytest.mark.faux_callable(4, fauxfactory.gen_integer)
    def test_callable_generate_integers(value):
        """Test function that return generated integer"""
        assert isinstance(value, int)


This will generate 4 new tests

::

    tests/test_pytest_fauxfactory.py::test_generate_integers[-40777152258153876] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[9141141773039816881] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[-2876033762618571864] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[2679201549842738042] PASSED


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

    tests/test_pytest_fauxfactory.py::test_generate_integers[99] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[78] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[86] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_integers[68] PASSED


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

    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value0] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value1] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value2] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value3] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value4] PASSED


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

This will generate 5 new tests

::

    tests/test_pytest_fauxfactory.py::test_generate_person[value0] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_person[value1] PASSED
    tests/test_pytest_fauxfactory.py::test_generate_person[value2] PASSED

Now instead of using a callable function, we want to generate tests with values
of any types from a generator function or generator expression,
for this purpose we use the "faux_generator" mark:


.. code-block:: python

    def alpha_strings_generator(items=1, length=10):
        """Generate alpha string value at each iteration."""
        for _ in range(items):
            yield fauxfactory.gen_alpha(length=length)


    @pytest.mark.faux_generator(alpha_strings_generator(items=3, length=12))
    def test_generator_alpha_strings(value):
        """Test function generator with kwargs"""
        assert len(value) == 12

This will generate 3 new tests

::

    tests/test_pytest_fauxfactory.py::test_generator_alpha_strings[WiEgJZexQiTJ] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_alpha_strings[MsgqwMYgtGLA] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_alpha_strings[nOTGNAeWJkOz] PASSED

We can also use a generator expression:

.. code-block:: python

    list_of_integers = [fauxfactory.gen_integer(min_value=0) for _ in range(4)]


    @pytest.mark.faux_generator(int_val for int_val in list_of_integers)
    def test_generator_expression(value):
        """Test generator expression"""
        assert isinstance(value, int)
        assert value >= 0

This will generate 4 tests

::

    tests/test_pytest_fauxfactory.py::test_generator_expression[7567941589364906197] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_expression[5816026928693750395] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_expression[7144149572714817589] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_expression[5753372709616898246] PASSED


of cause the returned values can be of any type:


.. code-block:: python

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


This will generate 2 tests

::

    tests/test_pytest_fauxfactory.py::test_generator_foo_generator[foo] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_foo_generator[value1] PASSED

we can also combine all the above generators:

.. code-block:: python

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

This will generate 9 tests

::

    tests/test_pytest_fauxfactory.py::test_generator_combined[uyzwVdwKxPHH] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[kEieggUropBb] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[HwZtYgdEyoyX] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[7347036629722650799] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[4556800111586158449] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[3273311764181187971] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[8196370314569916631] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[foo] PASSED
    tests/test_pytest_fauxfactory.py::test_generator_combined[value8] PASSED
