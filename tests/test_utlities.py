from syrupy.assertion import SnapshotAssertion

from notion_formulas import (
    Number,
    String,
    encode,
    format_number,
    format_percent,
    list_length,
    lowercase,
    progressbar,
    prop,
    select,
    uppercase,
)

NUMBER: Number = prop("number")
STRING: String = prop("string")


def test_sum() -> None:
    assert encode(sum([NUMBER])) == 'prop("number")'
    assert encode(sum([NUMBER, NUMBER])) == 'prop("number") + prop("number")'
    assert (
        encode(sum([NUMBER, NUMBER, NUMBER]))
        == 'prop("number") + prop("number") + prop("number")'
    )

    assert encode(sum([NUMBER, 42, NUMBER])) == 'prop("number") + 42 + prop("number")'

    assert (
        encode(sum([NUMBER, 40, 2, NUMBER]))
        == 'prop("number") + 40 + 2 + prop("number")'
    )


def test_select() -> None:
    assert encode(
        select(
            (NUMBER == 1, "one"),
            (NUMBER == 2, "two"),
            (NUMBER == 3, "three"),
            default="other",
        )
    ) == (
        'if(prop("number") == 1, "one", '
        'if(prop("number") == 2, "two", '
        'if(prop("number") == 3, "three", '
        '"other")))'
    )


def test_list_length(snapshot: SnapshotAssertion) -> None:
    assert snapshot == encode(list_length(STRING))


def test_lowercase(snapshot: SnapshotAssertion) -> None:
    assert snapshot == encode(lowercase(STRING))


def test_uppercase(snapshot: SnapshotAssertion) -> None:
    assert snapshot == encode(uppercase(STRING))


def test_format_number(snapshot: SnapshotAssertion) -> None:
    assert snapshot == encode(format_number(NUMBER))


def test_format_percent(snapshot: SnapshotAssertion) -> None:
    assert snapshot == encode(format_percent(NUMBER))


def test_progressbar(snapshot: SnapshotAssertion) -> None:
    assert snapshot == encode(progressbar(NUMBER))
    assert snapshot == encode(progressbar(NUMBER, size=3))
    assert snapshot == encode(progressbar(NUMBER, full="X", empty="x"))
