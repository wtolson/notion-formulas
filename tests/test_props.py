from notion_formulas import (
    boolean_prop,
    date_prop,
    encode,
    number_prop,
    prop,
    string_prop,
)


def test_prop() -> None:
    assert encode(prop("test")) == 'prop("test")'


def test_boolean_prop() -> None:
    assert encode(boolean_prop("test")) == 'prop("test")'


def test_number_prop() -> None:
    assert encode(number_prop("test")) == 'prop("test")'


def test_string_prop() -> None:
    assert encode(string_prop("test")) == 'prop("test")'


def test_date_prop() -> None:
    assert encode(date_prop("test")) == 'prop("test")'
