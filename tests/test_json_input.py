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


def test_decoder_limits(monkeypatch):
    from triad_dispatch_lib import json_input

    def exhausted_decoder(raw, **kwargs):
        raise RecursionError("PRIVATE_DECODER_DETAIL")

    # Interpreter stack thresholds vary; the contract translates decoder errors.
    monkeypatch.setattr(json_input.json, "loads", exhausted_decoder)
    with pytest.raises(lib.AdmissionError) as caught:
        parse("[0]")
    assert caught.value.code == "nesting_limit"
    assert "PRIVATE_DECODER_DETAIL" not in str(caught.value)
    assert caught.value.__suppress_context__ is True


def test_integer_conversion_limit():
    limit = sys.get_int_max_str_digits()
    if not limit:
        pytest.skip("Interpreter integer conversion limit is disabled")
    with pytest.raises(lib.AdmissionError) as caught:
        parse("1" * (limit + 1))
    assert caught.value.code == "invalid_json"


def test_bounded_nested_json_decodes():
    value = parse("[" * 32 + "0" + "]" * 32)
    for _ in range(32):
        assert isinstance(value, list) and len(value) == 1
        value = value[0]
    assert value == 0
