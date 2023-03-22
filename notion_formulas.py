from __future__ import annotations

import abc
import json
from typing import Any, TypeVar, Union, cast

try:  # python < 3.8
    from typing import Literal, Protocol
except ImportError:
    from typing_extensions import Literal, Protocol

try:  # python < 3.10
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias


__author__ = "Trevor Olson"
__email__ = "trevor@heytrevor.com"
__version__ = "1.0.0"

Scalar = Union[bool, int, float, str]
Expr = Union[Scalar, "BooleanExpr", "NumberExpr", "StringExpr", "DateExpr"]

Boolean = Union[bool, "BooleanExpr"]
Number = Union[int, float, "NumberExpr"]
String = Union[str, "StringExpr"]
Date: TypeAlias = "DateExpr"

DateUnit = Union[
    Literal[
        "years",
        "quarters",
        "months",
        "weeks",
        "days",
        "hours",
        "minutes",
        "seconds",
        "milliseconds",
    ],
    "StringExpr",
]

# Precedence | Operator
# ==================================
#         11 | function
#         10 | not
#          9 | pow
#          8 | unary plus/minus
#          7 | multiply, divide, mod
#          6 | add, subtract
#          5 | larger, largerEq,
#            | smaller, smallerEq
#          4 | unequal, equal
#          3 | and
#          2 | or
#          1 | if


class ExprImpl(abc.ABC):
    @abc.abstractproperty
    def precedence(self) -> int:
        ...

    @precedence.setter
    @abc.abstractmethod
    def precedence(self, value: int) -> None:
        ...

    @abc.abstractmethod
    def encode(self) -> str:
        ...

    def __str__(self) -> str:
        return self.encode()

    def __add__(self, other: Any) -> Any:
        return add(cast(Any, self), other)

    def __radd__(self, other: Any) -> Any:
        return add(other, cast(Any, self))

    def __sub__(self, other: Any) -> Any:
        return subtract(cast(Any, self), other)

    def __rsub__(self, other: Any) -> Any:
        return subtract(other, cast(Any, self))

    def __mul__(self, other: Any) -> Any:
        return multiply(cast(Any, self), other)

    def __rmul__(self, other: Any) -> Any:
        return multiply(other, cast(Any, self))

    def __truediv__(self, other: Any) -> Any:
        return divide(cast(Any, self), other)

    def __rtruediv__(self, other: Any) -> Any:
        return divide(other, cast(Any, self))

    def __pow__(self, other: Any) -> Any:
        return pow(cast(Any, self), other)

    def __rpow__(self, other: Any) -> Any:
        return pow(other, cast(Any, self))

    def __mod__(self, other: Any) -> Any:
        return mod(cast(Any, self), other)

    def __rmod__(self, other: Any) -> Any:
        return mod(other, cast(Any, self))

    def __neg__(self) -> Any:
        return unary_minus(cast(Any, self))

    def __and__(self, other: Any) -> Any:
        return and_(cast(Any, self), other)

    def __rand__(self, other: Any) -> Any:
        return and_(other, cast(Any, self))

    def __or__(self, other: Any) -> Any:
        return or_(cast(Any, self), other)

    def __ror__(self, other: Any) -> Any:
        return or_(other, cast(Any, self))

    def __invert__(self) -> Any:
        return not_(cast(Any, self))

    def __lt__(self, other: Any) -> Any:
        return smaller(cast(Any, self), other)

    def __le__(self, other: Any) -> Any:
        return smaller_eq(cast(Any, self), other)

    def __eq__(self, other: Any) -> Any:
        return equal(cast(Any, self), other)

    def __ne__(self, other: Any) -> Any:
        return unequal(cast(Any, self), other)

    def __gt__(self, other: Any) -> Any:
        return larger(cast(Any, self), other)

    def __ge__(self, other: Any) -> Any:
        return larger_eq(cast(Any, self), other)


class BooleanExpr(Protocol):
    def encode(self) -> str:
        ...

    def __and__(self, other: Boolean) -> Boolean:
        return and_(self, other)

    def __rand__(self, other: Boolean) -> Boolean:
        return and_(other, self)

    def __or__(self, other: Boolean) -> Boolean:
        return or_(self, other)

    def __ror__(self, other: Boolean) -> Boolean:
        return or_(other, self)

    def __invert__(self) -> Boolean:
        return not_(self)

    def __lt__(self, other: Boolean) -> Boolean:
        return smaller(self, other)

    def __le__(self, other: Boolean) -> Boolean:
        return smaller_eq(self, other)

    def __eq__(self, other: Boolean) -> Boolean:  # type: ignore[override]
        return equal(self, other)

    def __ne__(self, other: Boolean) -> Boolean:  # type: ignore[override]
        return unequal(self, other)

    def __gt__(self, other: Boolean) -> Boolean:
        return larger(self, other)

    def __ge__(self, other: Boolean) -> Boolean:
        return larger_eq(self, other)


class NumberExpr(Protocol):
    def encode(self) -> str:
        ...

    def __add__(self, other: Number) -> Number:
        return add(self, other)

    def __radd__(self, other: Number) -> Number:
        return add(other, self)

    def __sub__(self, other: Number) -> Number:
        return subtract(self, other)

    def __rsub__(self, other: Number) -> Number:
        return subtract(other, self)

    def __mul__(self, other: Number) -> Number:
        return multiply(self, other)

    def __rmul__(self, other: Number) -> Number:
        return multiply(other, self)

    def __truediv__(self, other: Number) -> Number:
        return divide(self, other)

    def __rtruediv__(self, other: Number) -> Number:
        return divide(other, self)

    def __pow__(self, other: Number) -> Number:
        return pow(self, other)

    def __rpow__(self, other: Number) -> Number:
        return pow(other, self)

    def __mod__(self, other: Number) -> Number:
        return mod(self, other)

    def __rmod__(self, other: Number) -> Number:
        return mod(other, self)

    def __neg__(self) -> Number:
        return unary_minus(self)

    def __lt__(self, other: Number) -> Boolean:
        return smaller(self, other)

    def __le__(self, other: Number) -> Boolean:
        return smaller_eq(self, other)

    def __eq__(self, other: Number) -> Boolean:  # type: ignore[override]
        return equal(self, other)

    def __ne__(self, other: Number) -> Boolean:  # type: ignore[override]
        return unequal(self, other)

    def __gt__(self, other: Number) -> Boolean:
        return larger(self, other)

    def __ge__(self, other: Number) -> Boolean:
        return larger_eq(self, other)


class StringExpr(Protocol):
    def encode(self) -> str:
        ...

    def __len__(self) -> Number:
        return length(self)

    def __add__(self, other: String) -> String:
        return add(self, other)

    def __radd__(self, other: String) -> String:
        return add(other, self)

    def __lt__(self, other: String) -> Boolean:
        return smaller(self, other)

    def __le__(self, other: String) -> Boolean:
        return smaller_eq(self, other)

    def __eq__(self, other: String) -> Boolean:  # type: ignore[override]
        return equal(self, other)

    def __ne__(self, other: String) -> Boolean:  # type: ignore[override]
        return unequal(self, other)

    def __gt__(self, other: String) -> Boolean:
        return larger(self, other)

    def __ge__(self, other: String) -> Boolean:
        return larger_eq(self, other)


class DateExpr(Protocol):
    def encode(self) -> str:
        ...

    def __lt__(self, other: Date) -> Boolean:
        return smaller(self, other)

    def __le__(self, other: Date) -> Boolean:
        return smaller_eq(self, other)

    def __eq__(self, other: Date) -> Boolean:  # type: ignore[override]
        return equal(self, other)

    def __ne__(self, other: Date) -> Boolean:  # type: ignore[override]
        return unequal(self, other)

    def __gt__(self, other: Date) -> Boolean:
        return larger(self, other)

    def __ge__(self, other: Date) -> Boolean:
        return larger_eq(self, other)


class Constant(ExprImpl):
    precedence = 12

    def __init__(self, name: str) -> None:
        self.name = name

    def encode(self) -> str:
        return self.name


class Function(ExprImpl):
    precedence = 11

    def __init__(self, name: str, *args: Expr) -> None:
        self.name = name
        self.args = args

    def encode(self) -> str:
        args = ", ".join(encode(arg) for arg in self.args)
        return f"{self.name}({args})"


class UnaryOperation(ExprImpl):
    precedence = 0

    def __init__(self, precedence: int, operator: str, operand: Expr) -> None:
        self.precedence = precedence
        self.operator = operator
        self.operand = operand

    def encode(self) -> str:
        operand = _encode_with_precedence_right(self.precedence, self.operand)
        return f"{self.operator}{operand}"


class BinaryOperation(ExprImpl):
    precedence = 0

    def __init__(self, precedence: int, operator: str, left: Expr, right: Expr) -> None:
        self.precedence = precedence
        self.operator = operator
        self.left = left
        self.right = right

    def encode(self) -> str:
        left = _encode_with_precedence_left(self.precedence, self.left)
        right = _encode_with_precedence_right(self.precedence, self.right)
        return f"{left}{self.operator}{right}"


#
# Constants
#
E: Number = Constant("e")
PI: Number = Constant("pi")


#
# Props
#
def prop(name: str) -> Function:
    return Function("prop", name)


def boolean_prop(name: str) -> Boolean:
    return prop(name)


def number_prop(name: str) -> Number:
    return prop(name)


def string_prop(name: str) -> String:
    return prop(name)


def date_prop(name: str) -> Date:
    return prop(name)


#
# Operators
#
_T = TypeVar("_T", Boolean, Number, String, Date)
_U = TypeVar("_U", Boolean, Number, String, Date)


def if_(test: Boolean, true_value: _T, false_value: _U) -> _T | _U:
    """Switches between two options based on another value."""
    return Function("if", test, true_value, false_value)


_V = TypeVar("_V", Number, String)


def add(value: _V, other: _V) -> _V:
    """Adds two numbers and returns their sum, or concatenates two strings."""
    if isinstance(other, (int, float)) and other < 0:
        return subtract(value, -other)
    if isinstance(value, (int, float)) and value == 0:
        return other
    if isinstance(other, (int, float)) and other == 0:
        return value
    return BinaryOperation(6, " + ", value, other)


def subtract(value: Number, other: Number) -> Number:
    """Subtracts two numbers and returns their difference."""
    if isinstance(other, (int, float)) and other < 0:
        return add(value, -other)
    if (
        isinstance(value, (int, float))
        and value == 0
        and isinstance(other, (int, float, ExprImpl))
    ):
        return -other
    if isinstance(other, (int, float)) and other == 0:
        return value
    return BinaryOperation(6, " - ", value, other)


def multiply(value: Number, other: Number) -> Number:
    """Multiplies two numbers and returns their product."""
    if isinstance(value, (int, float)) and value == 0:
        return 0
    if isinstance(other, (int, float)) and other == 0:
        return 0
    if isinstance(value, (int, float)) and value == 1:
        return other
    if isinstance(other, (int, float)) and other == 1:
        return value
    if isinstance(value, (int, float)) and value == -1:
        return -other
    if isinstance(other, (int, float)) and other == -1:
        return -value
    return BinaryOperation(7, " * ", value, other)


def divide(value: Number, other: Number) -> Number:
    """Multiplies two numbers and returns their product."""
    if isinstance(other, (int, float)) and other == 0:
        raise ZeroDivisionError("division by zero")
    if isinstance(value, (int, float)) and value == 0:
        return 0
    if isinstance(other, (int, float)) and other == 1:
        return value
    if isinstance(other, (int, float)) and other == -1:
        return -value
    return BinaryOperation(7, " / ", value, other)


def pow(base: Number, power: Number) -> Number:
    """Returns base to the exponent power, that is, baseexponent."""
    if isinstance(power, (int, float)) and power == 0:
        return 1
    if isinstance(power, (int, float)) and power == 1:
        return base
    if isinstance(base, (int, float)) and (base == 0 or base == 1):
        return base
    return BinaryOperation(9, " ^ ", base, power)


def mod(value: Number, other: Number) -> Number:
    """Divides two numbers and returns their remainder."""
    if isinstance(other, (int, float)) and other == 0:
        raise ZeroDivisionError("division by zero")
    if isinstance(other, (int, float)) and other == 1:
        return 0
    if isinstance(value, (int, float)) and (value == 0 or value == 1):
        return value
    return BinaryOperation(7, " % ", value, other)


def unary_minus(value: Number) -> Number:
    """Negates a number."""
    if isinstance(value, (int, float)) and isinstance(value, (int, float)):
        return -value
    return UnaryOperation(8, "-", value)


def unary_plus(value: Expr) -> Number:
    """Converts its argument into a number."""
    if isinstance(value, (int, float)):
        return value
    return UnaryOperation(8, "+", value)


def not_(value: Boolean) -> Boolean:
    """Returns the logical NOT of its argument."""
    if isinstance(value, (bool)):
        return not value
    return UnaryOperation(10, "not ", value)


def and_(value: Boolean, other: Boolean) -> Boolean:
    """Returns the logical AND of its two arguments."""
    return BinaryOperation(3, " and ", value, other)


def or_(value: Boolean, other: Boolean) -> Boolean:
    """Returns the logical OR of its two arguments."""
    return BinaryOperation(2, " or ", value, other)


def equal(value: _T, other: _T) -> Boolean:
    """Returns true if its arguments are equal, and false otherwise."""
    return BinaryOperation(4, " == ", value, other)


def unequal(value: _T, other: _T) -> Boolean:
    """Returns false if its arguments are equal, and true otherwise."""
    return BinaryOperation(4, " != ", value, other)


def larger(value: _T, other: _T) -> Boolean:
    """Returns true if the first argument is larger than the second."""
    return BinaryOperation(5, " > ", value, other)


def larger_eq(value: _T, other: _T) -> Boolean:
    """Returns true if the first argument is larger than or equal to than the
    second."""
    return BinaryOperation(5, " >= ", value, other)


def smaller(value: _T, other: _T) -> Boolean:
    """Returns true if the first argument is smaller than the second."""
    return BinaryOperation(5, " < ", value, other)


def smaller_eq(value: _T, other: _T) -> Boolean:
    """Returns true if the first argument is smaller than or equal to than the
    second."""
    return BinaryOperation(5, " <= ", value, other)


#
# Functions
#
def concat(*items: String) -> String:
    """Concatenates its arguments and returns the result."""
    return Function("concat", *items)


def join(separator: String, *items: String) -> String:
    """Inserts the first argument between the rest and returns their
    concatenation."""
    return Function("join", separator, *items)


def slice(value: String, start: Number, end: Number | None = None) -> String:
    """Extracts a substring from a string from the start index (inclusively) to
    the end index (optional and exclusively)."""
    if end is None:
        return Function("slice", value, start)
    else:
        return Function("slice", value, start, end)


def length(value: String) -> Number:
    """Returns the length of a string."""
    return Function("length", value)


def format(value: Expr) -> String:
    """Formats its argument as a string."""
    return Function("format", value)


def to_number(value: Expr) -> Number:
    """Parses a number from text."""
    return Function("toNumber", value)


def contains(value: String, text: String) -> Boolean:
    """Returns true if the second argument is found in the first."""
    return Function("contains", value, text)


def replace(value: Boolean | Number | String, pattern: String, text: String) -> String:
    """Replaces the first match of a regular expression with a new value."""
    return Function("replace", value, pattern, text)


def replace_all(
    value: Boolean | Number | String, pattern: String, text: String
) -> String:
    """Replaces all matches of a regular expression with a new value."""
    return Function("replaceAll", value, pattern, text)


def test(value: Boolean | Number | String, pattern: String) -> Boolean:
    """Tests if a string matches a regular expression."""
    return Function("test", value, pattern)


def empty(value: Expr) -> Boolean:
    """Tests if a value is empty."""
    return Function("empty", value)


def abs(value: Number) -> Number:
    """Returns the absolute value of a number."""
    return Function("abs", value)


def cbrt(value: Number) -> Number:
    """Returns the cube root of a number."""
    return Function("cbrt", value)


def ceil(value: Number) -> Number:
    """Returns the smallest integer greater than or equal to a number."""
    return Function("ceil", value)


def exp(value: Number) -> Number:
    """Returns E^x, where x is the argument, and E is Euler's constant (2.718…),
    the base of the natural logarithm."""
    return Function("exp", value)


def floor(value: Number) -> Number:
    """Returns the largest integer less than or equal to a number."""
    return Function("floor", value)


def log10(value: Number) -> Number:
    """Returns the base 10 logarithm of a number."""
    return Function("log10", value)


def log2(value: Number) -> Number:
    """Returns the base 2 logarithm of a number."""
    return Function("log2", value)


def max(value: Number, *values: Number) -> Number:
    """Returns the largest of one or more numbers."""
    return Function("max", value, *values)


def min(value: Number, *values: Number) -> Number:
    """Returns the smallest of one or more numbers."""
    return Function("min", value, *values)


def round(value: Number) -> Number:
    """Returns the value of a number rounded to the nearest integer."""
    return Function("round", value)


def sign(value: Number) -> Number:
    """Returns the sign of the x, indicating whether x is positive, negative or zero."""
    return Function("sign", value)


def sqrt(value: Number) -> Number:
    """Returns the positive square root of a number."""
    return Function("sqrt", value)


def start(value: Date) -> Date:
    """Returns the start of a date range."""
    return Function("start", value)


def end(value: Date) -> Date:
    """Returns the end of a date range."""
    return Function("end", value)


def now() -> Date:
    """Returns the current date and time."""
    return Function("now")


def timestamp(value: Date) -> Number:
    """Returns an integer number from a Unix millisecond timestamp,
    corresponding to the number of milliseconds since January 1, 1970."""
    return Function("timestamp", value)


def from_timestamp(value: Number) -> Date:
    """Returns a date constructed from a Unix millisecond timestamp,
    corresponding to the number of milliseconds since January 1, 1970."""
    return Function("fromTimestamp", value)


def date_add(value: Date, amount: Number, unit: DateUnit) -> Date:
    """Add to a date."""
    return Function("dateAdd", value, amount, unit)


def date_subtract(value: Date, amount: Number, unit: DateUnit) -> Date:
    """Subtract from a date."""
    return Function("dateSubtract", value, amount, unit)


def date_between(start: Date, end: Date, unit: DateUnit) -> Number:
    """Returns the time between two dates."""
    return Function("dateBetween", start, end, unit)


def format_date(value: Date, format: String) -> String:
    """Format a date using the Moment standard time format string."""
    return Function("formatDate", value, format)


def minute(value: Date) -> Number:
    """Returns an integer number, between 0 and 59, corresponding to minutes in
    the given date."""
    return Function("minute", value)


def hour(value: Date) -> Number:
    """Returns an integer number, between 0 and 23, corresponding to hour for
    the given date."""
    return Function("hour", value)


def day(value: Date) -> Number:
    """Returns an integer number corresponding to the day of the week for the
    given date: 0 for Sunday, 1 for Monday, 2 for Tuesday, and so on."""
    return Function("day", value)


def date(value: Date) -> Number:
    """Returns an integer number, between 1 and 31, corresponding to day of the
    month for the given."""
    return Function("date", value)


def month(value: Date) -> Number:
    """Returns an integer number, between 0 and 11, corresponding to month in
    the given date according to local time. 0 corresponds to January, 1 to
    February, and so on."""
    return Function("month", value)


def year(value: Date) -> Number:
    """Returns a number corresponding to the year of the given date."""
    return Function("year", value)


def id() -> String:
    """Returns a unique string id for each entry."""
    return Function("id")


#
# Utilities
#
def select(*tests: tuple[Boolean, _T], default: _T) -> _T:
    """Select a value by the first matching test."""
    for test, value in reversed(tests):
        default = if_(test, value, default)
    return default


def list_length(value: String) -> Number:
    """Returns the number of items in a multi-select list."""
    return if_(empty(value), 0, length(replace_all(value, "[^,]", "")) + 1)


#
# Serialization
#
def encode(value: Expr) -> str:
    if isinstance(value, (bool, int, float, str)):
        return json.dumps(value)
    return value.encode()


def _encode_with_precedence_left(precedence: int, other: Expr) -> str:
    if not isinstance(other, ExprImpl):
        return encode(other)

    if other.precedence >= precedence:
        return encode(other)

    return f"({encode(other)})"


def _encode_with_precedence_right(precedence: int, other: Expr) -> str:
    if not isinstance(other, ExprImpl):
        return encode(other)

    if other.precedence > precedence:
        return encode(other)

    return f"({encode(other)})"
