from notion_formulas import Number, encode, prop

NUMBER: Number = prop("number")


def test_left_greater() -> None:
    assert encode((NUMBER * 2) + 3) == 'prop("number") * 2 + 3'


def test_left_equal() -> None:
    assert encode((NUMBER * 2) / 3) == 'prop("number") * 2 / 3'


def test_left_less() -> None:
    assert encode((NUMBER + 2) * 3) == '(prop("number") + 2) * 3'


def test_right_greater() -> None:
    assert encode(3 + (NUMBER * 2)) == '3 + prop("number") * 2'


def test_right_equal() -> None:
    assert encode(3 / (NUMBER * 2)) == '3 / (prop("number") * 2)'


def test_right_less() -> None:
    assert encode(3 * (NUMBER + 2)) == '3 * (prop("number") + 2)'
