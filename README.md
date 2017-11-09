# pytest-fauxfactory

[![Downloads](https://pypip.in/download/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![Latest version](https://pypip.in/version/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![Supported Python versions](https://pypip.in/py_versions/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![License](https://pypip.in/license/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![Format](https://pypip.in/format/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)


Now you pass random data to your tests using this **Pytest** plugin for [FauxFactory](https://github.com/omaciel/fauxfactory).

The easiest way to use it is to decorate your test with the `faux_string` mark and write a test that expects a `value` argument:

```python
@pytest.mark.faux_string()
def test_generate_alpha_strings(value):
    assert value
```

By default a single random string will be generated for your test.

```shell
test_generate_alpha_strings[:<;--{#+,&] PASSED
```

Suppose you want to generate **4** random strings (identified as **value**) for a test:

```python
@pytest.mark.faux_string(4, 'alpha')
def test_generate_alpha_strings(value):
    assert value.isalpha()
```

You will then have 4 tests, each with different values:

```shell
test_generate_alpha_strings[EiOKPHSXNYfv] PASSED
test_generate_alpha_strings[BBATlPxwmHaP] PASSED
test_generate_alpha_strings[kXIGIIXOyZyv] PASSED
test_generate_alpha_strings[eqHxEFneSKNC] PASSED
```

Now, suppose you also want to make sure that all strings have exactly 43 characters:

```python
@pytest.mark.faux_string(4, 'alpha', length=43)
def test_generate_alpha_strings(value):
    assert len(value) == 43
```

You can also get random types of strings by excluding the second argument:

```python
@pytest.mark.faux_string(4)
def test_generate_alpha_strings(value):
    assert len(value) > 0
```

faux_callable:
--------------

Now imagine that you have a custom function that generate value of any type instead of the default types used in faux_string:
To be able to realize that we have to use the "faux_callable" mark
```python
import fauxfactory
import pytest

@pytest.mark.faux_callable(4, fauxfactory.gen_integer)
def test_callable_generate_integers(value):
    """Test function that return generated integer"""
    assert isinstance(value, int)
```
result: 4 tests generated
```shell
tests/test_pytest_fauxfactory.py::test_generate_integers[-40777152258153876] PASSED
tests/test_pytest_fauxfactory.py::test_generate_integers[9141141773039816881] PASSED
tests/test_pytest_fauxfactory.py::test_generate_integers[-2876033762618571864] PASSED
tests/test_pytest_fauxfactory.py::test_generate_integers[2679201549842738042] PASSED
```

faux_callable can also transfer arguments to the callable function:
```python
import fauxfactory
import pytest

@pytest.mark.faux_callable(4, fauxfactory.gen_integer, min_value=0,
                           max_value=100)
def test_callable_generate_integers(value):
    """Test function that return generated integer with kwargs"""
    assert isinstance(value, int)
    assert 0 <= value <= 100
```
result: 4 tests generated
```bash
tests/test_pytest_fauxfactory.py::test_generate_integers[99] PASSED
tests/test_pytest_fauxfactory.py::test_generate_integers[78] PASSED
tests/test_pytest_fauxfactory.py::test_generate_integers[86] PASSED
tests/test_pytest_fauxfactory.py::test_generate_integers[68] PASSED

```

of course the generated value can be of any type, let's generate value as a tuple of alpha strings:  
```python
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
```
result: 5 tests generated

```bash
tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value0] PASSED
tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value1] PASSED
tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value2] PASSED
tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value3] PASSED
tests/test_pytest_fauxfactory.py::test_generate_from_custom_function[value4] PASSED
```

let's now generate from a custom function that return a dict:

```python
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
```
result: 3 tests generated
```bash
tests/test_pytest_fauxfactory.py::test_generate_person[value0] PASSED
tests/test_pytest_fauxfactory.py::test_generate_person[value1] PASSED
tests/test_pytest_fauxfactory.py::test_generate_person[value2] PASSED
```
