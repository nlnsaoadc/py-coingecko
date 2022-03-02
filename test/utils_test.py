from coingecko.utils import (
    clean_dict_values,
    clean_params,
    remove_empty_dict_values,
)


def test_remove_empty_dict_values():
    dict_with_empty_values = {"a": None, "b": 123, "c": "foo", "d": None}
    new_dict = remove_empty_dict_values(dict_with_empty_values)
    for value in new_dict.values():
        assert value is not None


def test_clean_dict_values():
    input_dict = {"c": "foo", "e": True, "f": ["foo", "bar"]}
    new_dict = clean_dict_values(input_dict)
    assert isinstance(new_dict["e"], str)
    assert isinstance(new_dict["f"], str)
    assert new_dict["e"] == "true"
    assert new_dict["f"] == "foo,bar"


def test_clean_params():
    new_dict = clean_params({"a": None, "b": ["foo", "bar"], "c": True})
    assert "a" not in new_dict
    assert new_dict["b"] == "foo,bar"
    assert new_dict["c"] == "true"


def test_clean_params_empty():
    new_dict = clean_params(None)
    assert new_dict is None
