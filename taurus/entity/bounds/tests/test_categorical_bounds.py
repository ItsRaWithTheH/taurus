"""Test of CategoricalBounds."""
import pytest

from taurus.client.json_encoder import dumps, loads
from taurus.entity.bounds.categorical_bounds import CategoricalBounds
from taurus.entity.bounds.real_bounds import RealBounds
from taurus.entity.value.nominal_categorical import NominalCategorical
from taurus.entity.value.nominal_real import NominalReal
from taurus.entity.util import array_like


def test_categories():
    """Test categories setter."""
    assert CategoricalBounds().categories == set()
    assert CategoricalBounds(categories={"foo", "bar"}).categories == {"foo", "bar"}
    assert CategoricalBounds(categories=["foo", "bar"]).categories == {"foo", "bar"}


def test_invalid_constructor():
    """Test types for constructor."""
    with pytest.raises(ValueError):
        CategoricalBounds(categories="foo")

    with pytest.raises(ValueError):
        CategoricalBounds(categories={1, 2})


def test_validate():
    """Test basic validation logic."""
    bounds = CategoricalBounds(categories={"spam", "eggs"})
    assert bounds.validate(NominalCategorical("spam"))
    assert not bounds.validate(NominalCategorical("foo"))
    assert not bounds.validate(NominalReal(2.0, ''))
    with pytest.raises(TypeError):
        bounds.validate("spam")


def test_contains():
    """Test basic contains logic."""
    bounds = CategoricalBounds(categories={"spam", "eggs"})
    assert bounds.contains(CategoricalBounds(categories={"spam"}))
    assert not bounds.contains(CategoricalBounds(categories={"spam", "foo"}))
    assert not bounds.contains(RealBounds(0.0, 2.0, ''))
    with pytest.raises(TypeError):
        bounds.contains({"spam", "eggs"})


def test_json():
    """Test that serialization works (categories is encoded as a list)."""
    bounds = CategoricalBounds(categories={"spam", "eggs"})
    copy = loads(dumps(bounds))
    assert copy == bounds


def test_numpy():
    """Test that ndarrays, Series work as well."""
    assert len(array_like()) < 5  # In case we extend at some point

    if len(array_like()) > 2:  # Test numpy
        import numpy as np
        np_bounds = CategoricalBounds(np.array(["spam", "eggs"], dtype=object))
        np_copy = loads(dumps(np_bounds))
        assert np_copy == np_bounds

    if len(array_like()) > 3:  # Test numpy
        import pandas as pd
        pd_bounds = CategoricalBounds(pd.Series(["spam", "eggs"]))
        pd_copy = loads(dumps(pd_bounds))
        assert pd_copy == pd_bounds
