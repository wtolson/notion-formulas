import pytest

from notion_formulas import (
    Boolean,
    Number,
    String,
    add,
    and_,
    divide,
    encode,
    equal,
    if_,
    larger,
    larger_eq,
    mod,
    multiply,
    not_,
    or_,
    pow,
    prop,
    smaller,
    smaller_eq,
    subtract,
    unary_minus,
    unary_plus,
    unequal,
)

BOOLEAN: Boolean = prop("boolean")
NUMBER: Number = prop("number")
STRING: String = prop("string")


def test_if() -> None:
    assert (
        encode(if_(NUMBER > 0, NUMBER, NUMBER * -1))
        == 'if(prop("number") > 0, prop("number"), -prop("number"))'
    )


def test_add_numbers() -> None:
    assert encode(NUMBER + 1) == 'prop("number") + 1'
    assert encode(1 + NUMBER) == '1 + prop("number")'

    assert encode(add(NUMBER, 1)) == 'prop("number") + 1'
    assert encode(add(1, NUMBER)) == '1 + prop("number")'

    assert encode(NUMBER + 0) == 'prop("number")'
    assert encode(0 + NUMBER) == 'prop("number")'

    assert encode(add(NUMBER, -1)) == 'prop("number") - 1'
    assert encode(add(-1, NUMBER)) == '-1 + prop("number")'


def test_add_strings() -> None:
    assert encode(STRING + "test") == 'prop("string") + "test"'
    assert encode("test" + STRING) == '"test" + prop("string")'

    assert encode(add(STRING, "test")) == 'prop("string") + "test"'
    assert encode(add("test", STRING)) == '"test" + prop("string")'


def test_subtract_numbers() -> None:
    assert encode(subtract(NUMBER, 1)) == 'prop("number") - 1'
    assert encode(subtract(1, NUMBER)) == '1 - prop("number")'

    assert encode(NUMBER - 1) == 'prop("number") - 1'
    assert encode(1 - NUMBER) == '1 - prop("number")'

    assert encode(NUMBER - 0) == 'prop("number")'
    assert encode(0 - NUMBER) == '-prop("number")'

    assert encode(NUMBER - -1) == 'prop("number") + 1'
    assert encode(-1 - NUMBER) == '-1 - prop("number")'


def test_multiply_numbers() -> None:
    assert encode(multiply(NUMBER, 2)) == 'prop("number") * 2'
    assert encode(multiply(2, NUMBER)) == '2 * prop("number")'

    assert encode(NUMBER * 2) == 'prop("number") * 2'
    assert encode(2 * NUMBER) == '2 * prop("number")'

    assert encode(NUMBER * 1) == 'prop("number")'
    assert encode(1 * NUMBER) == 'prop("number")'

    assert encode(NUMBER * 0) == "0"
    assert encode(0 * NUMBER) == "0"

    assert encode(NUMBER * -1) == '-prop("number")'
    assert encode(-1 * NUMBER) == '-prop("number")'


def test_divide_numbers() -> None:
    assert encode(divide(NUMBER, 2)) == 'prop("number") / 2'
    assert encode(divide(2, NUMBER)) == '2 / prop("number")'

    assert encode(NUMBER / 2) == 'prop("number") / 2'
    assert encode(2 / NUMBER) == '2 / prop("number")'

    assert encode(NUMBER / 1) == 'prop("number")'
    assert encode(1 / NUMBER) == '1 / prop("number")'

    assert encode(NUMBER / -1) == '-prop("number")'
    assert encode(-1 / NUMBER) == '-1 / prop("number")'

    with pytest.raises(ZeroDivisionError):
        divide(NUMBER, 0)

    assert encode(divide(0, NUMBER)) == "0"


def test_pow() -> None:
    assert encode(pow(NUMBER, 2)) == 'prop("number") ^ 2'
    assert encode(pow(2, NUMBER)) == '2 ^ prop("number")'

    assert encode(NUMBER**2) == 'prop("number") ^ 2'
    assert encode(2**NUMBER) == '2 ^ prop("number")'

    assert encode(NUMBER**1) == 'prop("number")'
    assert encode(1**NUMBER) == "1"

    assert encode(NUMBER**0) == "1"
    assert encode(0**NUMBER) == "0"


def test_mod() -> None:
    assert encode(mod(NUMBER, 2)) == 'prop("number") % 2'
    assert encode(mod(2, NUMBER)) == '2 % prop("number")'

    assert encode(NUMBER % 2) == 'prop("number") % 2'
    assert encode(2 % NUMBER) == '2 % prop("number")'

    assert encode(NUMBER % 1) == "0"
    assert encode(1 % NUMBER) == "1"

    with pytest.raises(ZeroDivisionError):
        NUMBER % 0

    assert encode(0 % NUMBER) == "0"


def test_minus() -> None:
    assert encode(unary_minus(NUMBER)) == '-prop("number")'
    assert encode(-NUMBER) == '-prop("number")'
    assert encode(unary_minus(-1)) == "1"


def test_plus() -> None:
    assert encode(unary_plus(NUMBER)) == '+prop("number")'
    assert encode(unary_plus(STRING)) == '+prop("string")'
    assert encode(unary_plus(1)) == "1"


def test_not() -> None:
    assert encode(not_(BOOLEAN)) == 'not prop("boolean")'
    assert encode(not_(True)) == "false"
    assert encode(not_(False)) == "true"
    assert encode(~BOOLEAN) == 'not prop("boolean")'


def test_and() -> None:
    assert encode(and_(BOOLEAN, True)) == 'prop("boolean") and true'
    assert encode(and_(True, BOOLEAN)) == 'true and prop("boolean")'
    assert encode(BOOLEAN & True) == 'prop("boolean") and true'
    assert encode(True & BOOLEAN) == 'true and prop("boolean")'


def test_or() -> None:
    assert encode(or_(BOOLEAN, False)) == 'prop("boolean") or false'
    assert encode(or_(False, BOOLEAN)) == 'false or prop("boolean")'
    assert encode(BOOLEAN | False) == 'prop("boolean") or false'
    assert encode(False | BOOLEAN) == 'false or prop("boolean")'


def test_equal() -> None:
    assert encode(equal(NUMBER, 1)) == 'prop("number") == 1'
    assert encode(equal(1, NUMBER)) == '1 == prop("number")'
    assert encode(NUMBER == 1) == 'prop("number") == 1'
    assert encode(1 == NUMBER) == 'prop("number") == 1'


def test_unequal() -> None:
    assert encode(unequal(NUMBER, 1)) == 'prop("number") != 1'
    assert encode(unequal(1, NUMBER)) == '1 != prop("number")'
    assert encode(NUMBER != 1) == 'prop("number") != 1'
    assert encode(1 != NUMBER) == 'prop("number") != 1'


def test_larger() -> None:
    assert encode(larger(NUMBER, 1)) == 'prop("number") > 1'
    assert encode(larger(1, NUMBER)) == '1 > prop("number")'
    assert encode(NUMBER > 1) == 'prop("number") > 1'
    assert encode(1 > NUMBER) == 'prop("number") < 1'


def test_larger_eq() -> None:
    assert encode(larger_eq(NUMBER, 1)) == 'prop("number") >= 1'
    assert encode(larger_eq(1, NUMBER)) == '1 >= prop("number")'
    assert encode(NUMBER >= 1) == 'prop("number") >= 1'
    assert encode(1 >= NUMBER) == 'prop("number") <= 1'


def test_smaller() -> None:
    assert encode(smaller(NUMBER, 1)) == 'prop("number") < 1'
    assert encode(smaller(1, NUMBER)) == '1 < prop("number")'
    assert encode(NUMBER < 1) == 'prop("number") < 1'
    assert encode(1 < NUMBER) == 'prop("number") > 1'


def test_smaller_eq() -> None:
    assert encode(smaller_eq(NUMBER, 1)) == 'prop("number") <= 1'
    assert encode(smaller_eq(1, NUMBER)) == '1 <= prop("number")'
    assert encode(NUMBER <= 1) == 'prop("number") <= 1'
    assert encode(1 <= NUMBER) == 'prop("number") >= 1'
