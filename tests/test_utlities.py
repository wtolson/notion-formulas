from notion_formulas import Number, String, encode, list_length, prop, select

NUMBER: Number = prop("number")
STRING: String = prop("string")


def test_sum() -> Number:
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


def test_list_length() -> None:
    assert encode(list_length(STRING)) == (
        'if(empty(prop("string")), 0, '
        'length(replaceAll(prop("string"), "[^,]", "")) + 1)'
    )
