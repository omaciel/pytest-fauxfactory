# -*- coding: utf-8 -*-
"""Test the usage of custom argument names."""
import fauxfactory
import pytest


def generate_rgb(number=1):
    """Generate random RGB values."""
    return tuple(fauxfactory.gen_integer(0, 255) for _ in range(number))


@pytest.mark.faux_callable(
    4, generate_rgb, number=3, argnames='red, blue, green')
def test_multiple_argument_names_as_string(red, blue, green):
    """Test that multiple argument names can be passed as a string."""
    assert 0 <= red <= 255
    assert 0 <= blue <= 255
    assert 0 <= green <= 255


@pytest.mark.faux_callable(
    1, generate_rgb, number=3, argnames=['red', 'blue', 'green'])
def test_multiple_argument_names_as_list(red, blue, green):
    """Test that multiple argument names can be passed as a list."""
    assert 0 <= red <= 255
    assert 0 <= blue <= 255
    assert 0 <= green <= 255


@pytest.mark.faux_string(argnames='label')
def test_custom_argument_name(label):
    """Test that custom argument name is passed."""
    print(label)
    assert label
