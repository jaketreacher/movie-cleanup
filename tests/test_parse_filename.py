import pytest
from main import parse_filename


def test_parse_filename_happy_case():
    filename = "My Movie (2015)"

    actual = parse_filename(filename)

    expected = ("My Movie", 2015)
    assert expected == actual


def test_parse_filename_bad_name():
    filename = "My Movie - 2015"

    with pytest.raises(Exception):
        actual = parse_filename(filename)
