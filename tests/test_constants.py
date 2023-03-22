from notion_formulas import PI, E, encode, sqrt


def test_e() -> None:
    assert encode(E) == "e"


def test_pi() -> None:
    assert encode(PI) == "pi"


def test_constant_in_function() -> None:
    assert encode(sqrt(E)) == "sqrt(e)"


def test_constant_math() -> None:
    assert encode(PI * 2) == "pi * 2"
    assert encode(2 * PI) == "2 * pi"
