from notion_formulas import (
    Boolean,
    Date,
    Number,
    String,
    abs,
    cbrt,
    ceil,
    concat,
    contains,
    date,
    date_add,
    date_between,
    date_subtract,
    day,
    empty,
    encode,
    end,
    exp,
    floor,
    format,
    format_date,
    from_timestamp,
    hour,
    id,
    join,
    length,
    log2,
    log10,
    max,
    min,
    minute,
    month,
    now,
    prop,
    replace,
    replace_all,
    round,
    sign,
    slice,
    sqrt,
    start,
    timestamp,
    to_number,
    year,
)
from notion_formulas import test as notion_test

BOOLEAN: Boolean = prop("boolean")
NUMBER: Number = prop("number")
STRING: String = prop("string")
DATE: Date = prop("date")


def test_concat() -> None:
    assert encode(concat(STRING, STRING)) == 'concat(prop("string"), prop("string"))'
    assert (
        encode(concat(STRING, "test", STRING))
        == 'concat(prop("string"), "test", prop("string"))'
    )


def test_join() -> None:
    assert encode(join(STRING, STRING)) == 'join(prop("string"), prop("string"))'
    assert (
        encode(join(", ", STRING, STRING))
        == 'join(", ", prop("string"), prop("string"))'
    )


def test_slice() -> None:
    assert encode(slice(STRING, 1)) == 'slice(prop("string"), 1)'
    assert encode(slice(STRING, 1, 2)) == 'slice(prop("string"), 1, 2)'


def test_length() -> None:
    assert encode(length(STRING)) == 'length(prop("string"))'


def test_format() -> None:
    assert encode(format(STRING)) == 'format(prop("string"))'
    assert encode(format(NUMBER)) == 'format(prop("number"))'


def test_to_number() -> None:
    assert encode(to_number(STRING)) == 'toNumber(prop("string"))'
    assert encode(to_number(BOOLEAN)) == 'toNumber(prop("boolean"))'


def test_contains() -> None:
    assert (
        encode(contains(STRING, STRING)) == 'contains(prop("string"), prop("string"))'
    )
    assert encode(contains(STRING, "test")) == 'contains(prop("string"), "test")'


def test_replace() -> None:
    assert (
        encode(replace(STRING, STRING, STRING))
        == 'replace(prop("string"), prop("string"), prop("string"))'
    )
    assert (
        encode(replace(STRING, "pattern", "test"))
        == 'replace(prop("string"), "pattern", "test")'
    )
    assert (
        encode(replace(STRING, r"^\d+", "test"))
        == 'replace(prop("string"), "^\\\\d+", "test")'
    )


def test_replace_all() -> None:
    assert (
        encode(replace_all(STRING, STRING, STRING))
        == 'replaceAll(prop("string"), prop("string"), prop("string"))'
    )
    assert (
        encode(replace_all(STRING, "pattern", "test"))
        == 'replaceAll(prop("string"), "pattern", "test")'
    )
    assert (
        encode(replace_all(STRING, r"^\d+", "test"))
        == 'replaceAll(prop("string"), "^\\\\d+", "test")'
    )


def test_test() -> None:
    assert encode(notion_test(STRING, STRING)) == 'test(prop("string"), prop("string"))'
    assert encode(notion_test(STRING, "pattern")) == 'test(prop("string"), "pattern")'
    assert encode(notion_test(STRING, r"^\d+")) == 'test(prop("string"), "^\\\\d+")'


def test_empty() -> None:
    assert encode(empty(STRING)) == 'empty(prop("string"))'


def test_abs() -> None:
    assert encode(abs(NUMBER)) == 'abs(prop("number"))'


def test_cbrt() -> None:
    assert encode(cbrt(NUMBER)) == 'cbrt(prop("number"))'


def test_ceil() -> None:
    assert encode(ceil(NUMBER)) == 'ceil(prop("number"))'


def test_exp() -> None:
    assert encode(exp(NUMBER)) == 'exp(prop("number"))'


def test_floor() -> None:
    assert encode(floor(NUMBER)) == 'floor(prop("number"))'


def test_log10() -> None:
    assert encode(log10(NUMBER)) == 'log10(prop("number"))'


def test_log2() -> None:
    assert encode(log2(NUMBER)) == 'log2(prop("number"))'


def test_max() -> None:
    assert encode(max(NUMBER, NUMBER)) == 'max(prop("number"), prop("number"))'
    assert (
        encode(max(NUMBER, NUMBER, NUMBER))
        == 'max(prop("number"), prop("number"), prop("number"))'
    )


def test_min() -> None:
    assert encode(min(NUMBER, NUMBER)) == 'min(prop("number"), prop("number"))'
    assert (
        encode(min(NUMBER, NUMBER, NUMBER))
        == 'min(prop("number"), prop("number"), prop("number"))'
    )


def test_round() -> None:
    assert encode(round(NUMBER)) == 'round(prop("number"))'


def test_sign() -> None:
    assert encode(sign(NUMBER)) == 'sign(prop("number"))'


def test_sqrt() -> None:
    assert encode(sqrt(NUMBER)) == 'sqrt(prop("number"))'


def test_start() -> None:
    assert encode(start(DATE)) == 'start(prop("date"))'


def test_end() -> None:
    assert encode(end(DATE)) == 'end(prop("date"))'


def test_now() -> None:
    assert encode(now()) == "now()"


def test_timestamp() -> None:
    assert encode(timestamp(DATE)) == 'timestamp(prop("date"))'


def test_from_timestamp() -> None:
    assert encode(from_timestamp(NUMBER)) == 'fromTimestamp(prop("number"))'


def test_date_add() -> None:
    assert (
        encode(date_add(DATE, NUMBER, "day"))
        == 'dateAdd(prop("date"), prop("number"), "day")'
    )


def test_date_subtract() -> None:
    assert (
        encode(date_subtract(DATE, NUMBER, "day"))
        == 'dateSubtract(prop("date"), prop("number"), "day")'
    )


def test_date_between() -> None:
    assert (
        encode(date_between(DATE, DATE, "day"))
        == 'dateBetween(prop("date"), prop("date"), "day")'
    )


def test_format_date() -> None:
    assert (
        encode(format_date(DATE, "MMMM Do YYYY, h:mm:ss a"))
        == 'formatDate(prop("date"), "MMMM Do YYYY, h:mm:ss a")'
    )


def test_minute() -> None:
    assert encode(minute(DATE)) == 'minute(prop("date"))'


def test_hour() -> None:
    assert encode(hour(DATE)) == 'hour(prop("date"))'


def test_day() -> None:
    assert encode(day(DATE)) == 'day(prop("date"))'


def test_date() -> None:
    assert encode(date(DATE)) == 'date(prop("date"))'


def test_month() -> None:
    assert encode(month(DATE)) == 'month(prop("date"))'


def test_year() -> None:
    assert encode(year(DATE)) == 'year(prop("date"))'


def test_id() -> None:
    assert encode(id()) == "id()"
