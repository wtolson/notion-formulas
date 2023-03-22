from notion_formulas import (
    BinaryOperation,
    Constant,
    Function,
    UnaryOperation,
    encode,
    prop,
)


def test_encode_scalars() -> None:
    assert encode(1) == "1"
    assert encode(1.0) == "1.0"
    assert encode("test") == '"test"'
    assert encode(True) == "true"
    assert encode(False) == "false"


def test_encode_constant() -> None:
    assert encode(Constant("test")) == "test"


def test_encode_function() -> None:
    assert encode(Function("test")) == "test()"
    assert encode(Function("test", 123)) == "test(123)"
    assert encode(Function("test", 123, 456)) == "test(123, 456)"
    assert encode(Function("test", prop("foo"))) == 'test(prop("foo"))'


def test_encode_unary_operator() -> None:
    assert encode(UnaryOperation(0, "+", 1)) == "+1"
    assert encode(UnaryOperation(0, "-", 1)) == "-1"

    assert encode(UnaryOperation(0, "+", prop("test"))) == '+prop("test")'
    assert encode(UnaryOperation(0, "-", prop("test"))) == '-prop("test")'


def test_binary_operator() -> None:
    assert encode(BinaryOperation(0, " + ", 1, prop("test"))) == '1 + prop("test")'
    assert encode(BinaryOperation(0, " - ", 1, prop("test"))) == '1 - prop("test")'


def test_str() -> None:
    assert str(prop("test")) == 'prop("test")'
