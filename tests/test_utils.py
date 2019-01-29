from src.utils import get_langs_dict
from src.utils import get_PG_number

import pytest


def test_get_langs_dict():
    """Test that the languages dict is correct."""
    langs_dict = get_langs_dict()
    assert isinstance(langs_dict, dict)
    for k, v in [
        ("cs", "czech"),
        ("da", "danish"),
        ("nl", "dutch"),
        ("en", "english"),
        ("et", "estonian"),
        ("fi", "finnish"),
        ("fr", "french"),
        ("de", "german"),
        ("el", "greek"),
        ("it", "italian"),
        ("no", "norwegian"),
        ("pl", "polish"),
        ("pt", "portuguese"),
        ("sl", "slovene"),
        ("es", "spanish"),
        ("sv", "swedish")
    ]:
        assert langs_dict[k] == v


def test_get_PG_number():
    """Test that we correctly extract PG numbers from strings."""
    expected_PG_number = "12345"

    # case 12345-0.txt
    string = "12345-0.txt"
    assert expected_PG_number == get_PG_number(string)

    # case pg12345.txt.utf8
    string = "pg12345.txt.utf8"
    assert expected_PG_number == get_PG_number(string)


def test_get_PG_number_fail():
    """Test that we raise an exception when the PG number is not recognized"""
    with pytest.raises(RuntimeError):
        _ = get_PG_number("asdf")

    with pytest.raises(RuntimeError):
        _ = get_PG_number("pg12345-0.txt.gz")
