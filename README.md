# pytest-fauxfactory

[![Downloads](https://pypip.in/download/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![Latest version](https://pypip.in/version/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![Supported Python versions](https://pypip.in/py_versions/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![License](https://pypip.in/license/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)
[![Format](https://pypip.in/format/pytest-fauxfactory/badge.svg?style=flat)](https://pypi.python.org/pypi/pytest-fauxfactory/)


Now you pass random data to your tests using this **Pytest** plugin for [FauxFactory](https://github.com/omaciel/fauxfactory).

The easiest way to use it is to decorate your test with the `gen_string` mark and write a test that expects a `value` argument:

```python
@pytest.mark.gen_string()
def test_generate_alpha_strings(value):
    assert value
```

By default a single random string will be generated for your test.

```shell
test_generate_alpha_strings[:<;--{#+,&] PASSED
```

Suppose you want to generate **4** random strings (identified as **value**) for a test:

```python
@pytest.mark.gen_string(4, 'alpha')
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
@pytest.mark.gen_string(4, 'alpha', length=43)
def test_generate_alpha_strings(value):
    assert len(value) == 43
```

You can also get random types of strings by excluding the second argument:

```python
@pytest.mark.gen_string(4)
def test_generate_alpha_strings(value):
    assert len(value) > 0
```

