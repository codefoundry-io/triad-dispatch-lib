import sys

import pytest

import triad_dispatch_lib as lib


def parse(raw):
    assert callable(getattr(lib, "parse_json", None)), "parse_json API is missing"
    return lib.parse_json(raw)


@pytest.mark.parametrize("raw,value", [
    ('{"a": [1, true, null, {"한글": "값"}]}', {"a": [1, True, None, {"한글": "값"}]}),
    (b"1.0", 1.0), ('"text"', "text"), ("false", False), ("null", None),
])
def test_original_json(raw, value):
    result = parse(raw)
    assert result == value
    assert type(result) is type(value)


@pytest.mark.parametrize("raw,code", [
    ('{"a":1,"a":2}', "duplicate_member"),
    ('{"outer":[{"a":1,"a":2}]}', "duplicate_member"),
    (r'{"a":1,"\u0061":2}', "duplicate_member"),
    ("NaN", "nonfinite_number"), ("Infinity", "nonfinite_number"),
    ("-Infinity", "nonfinite_number"), ("1e400", "nonfinite_number"),
    ("[-1e400]", "nonfinite_number"), (b'"\xff"', "invalid_utf8"),
    (b'\xff\xfe{\x00}\x00', "invalid_utf8"),
    ("```json\n{}\n```", "invalid_json"), ("{} {}", "invalid_json"),
    ("{", "invalid_json"), ("\ufeff{}", "invalid_json"),
])
def test_rejected_raw(raw, code):
    assert callable(getattr(lib, "parse_json", None)), "parse_json API is missing"
    with pytest.raises(lib.AdmissionError) as caught:
        parse(raw)
    assert caught.value.code == code


@pytest.mark.parametrize("raw", [{}, [], 1, None, bytearray(b"{}")])
def test_input_type(raw):
    assert callable(getattr(lib, "parse_json", None)), "parse_json API is missing"
    with pytest.raises(lib.AdmissionError) as caught:
        parse(raw)
    assert caught.value.code == "invalid_input_type"


def test_errors_do_not_echo_input():
    assert callable(getattr(lib, "parse_json", None)), "parse_json API is missing"
    with pytest.raises(lib.AdmissionError) as caught:
        parse('{"PRIVATE_TOKEN":1,"PRIVATE_TOKEN":2}')
    assert "PRIVATE_TOKEN" not in str(caught.value)


def test_decoder_limits():
    assert callable(getattr(lib, "parse_json", None)), "parse_json API is missing"
    with pytest.raises(lib.AdmissionError) as caught:
        parse("[" * 10000 + "0" + "]" * 10000)
    assert caught.value.code == "nesting_limit"
    limit = sys.get_int_max_str_digits()
    if limit:
        with pytest.raises(lib.AdmissionError) as caught:
            parse("1" * (limit + 1))
        assert caught.value.code == "invalid_json"
