import json

import pytest

import triad_dispatch_lib as lib
from tests.test_verdict import BASE, BINDINGS, FINDING


def output(raw, carrier="native-final", **kwargs):
    assert hasattr(lib, "ProviderOutput"), "ProviderOutput API missing"
    return lib.ProviderOutput(carrier, raw, kwargs.pop("exit_code", 0),
                              kwargs.pop("completed", True), **kwargs)


def wrap(raw, carrier):
    if carrier == "native-final":
        return raw
    if carrier == "claude-json":
        return '{"subtype":"success","structured_output":' + raw + '}'
    if carrier == "gemini-json":
        return json.dumps({"response": raw})
    return '{"event":"result","result":{"status":"SUCCESS","structured_output":' + raw + '}}'


@pytest.mark.parametrize("carrier,family,route", [
    ("native-final", "codex", None), ("native-final", "claude", None),
    ("claude-json", "claude", None), ("gemini-json", "google", "gemini"),
    ("agy-stream-json", "google", "agy"),
])
@pytest.mark.parametrize("negative", [False, True])
def test_admit_all_carriers(carrier, family, route, negative):
    data = dict(BASE, family=family, route=route)
    if negative:
        data.update(verdict="DO NOT MERGE", findings=[FINDING])
    raw = wrap(json.dumps(data), carrier)
    assert lib.admit_output(output(raw, carrier), expected={k: data[k] for k in BINDINGS}) == data


@pytest.mark.parametrize("carrier", ["native-final", "claude-json", "gemini-json", "agy-stream-json"])
@pytest.mark.parametrize("as_bytes", [False, True])
def test_extraction_preserves_original_representation(carrier, as_bytes):
    raw = '{ "attempt" : 1, "text":"한글\\u0061" }'
    envelope = wrap(raw, carrier).replace('"structured_output"', '"structured_\\u006futput"')
    if as_bytes:
        envelope = envelope.encode()
    extracted = lib.extract_final(output(envelope, carrier))
    assert extracted == (raw.encode() if as_bytes and carrier != "gemini-json" else raw)


@pytest.mark.parametrize("carrier", ["native-final", "claude-json", "gemini-json", "agy-stream-json"])
@pytest.mark.parametrize("raw,code", [
    ('{"a":1,"\\u0061":2}', "duplicate_member"),
    ('{"a":NaN}', "nonfinite_number"), ('{"a":1e999}', "nonfinite_number"),
    ('{"a":', "invalid_json"),
])
def test_inner_evidence_reaches_strict_parser(carrier, raw, code):
    expected = {k: BASE[k] for k in BINDINGS}
    if carrier == "claude-json":
        expected.update(family="claude")
    elif carrier != "native-final":
        expected.update(family="google", route="gemini" if carrier == "gemini-json" else "agy")
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output(wrap(raw, carrier), carrier), expected=expected)
    assert caught.value.code == code


@pytest.mark.parametrize("raw,carrier,code", [
    ('{"response":"{}","respon\\u0073e":"{}"}', "gemini-json", "duplicate_member"),
    ('{"structured_output":{},"x":NaN}', "claude-json", "nonfinite_number"),
    (b'\xff', "claude-json", "invalid_utf8"),
])
def test_full_envelope_is_strict(raw, carrier, code):
    with pytest.raises(lib.AdmissionError) as caught:
        lib.extract_final(output(raw, carrier))
    assert caught.value.code == code


@pytest.mark.parametrize("change", [
    {"completed": False}, {"completed": 1}, {"timed_out": True},
    {"timed_out": 1}, {"transport_failed": True}, {"transport_failed": 0},
    {"exit_code": 3}, {"exit_code": True}, {"exit_code": "0"},
])
def test_terminal_guards_precede_payload(change):
    with pytest.raises(lib.OutputError):
        lib.extract_final(output('malformed private payload', **change))


def test_exit_none_only_native():
    assert lib.extract_final(output("{}", exit_code=None)) == "{}"
    with pytest.raises(lib.OutputError):
        lib.extract_final(output('{"response":"{}"}', "gemini-json", exit_code=None))


@pytest.mark.parametrize("raw,carrier", [
    ('{"is_error":true,"structured_output":{}}', "claude-json"),
    ('{"subtype":"error_max_turns","structured_output":{}}', "claude-json"),
    ('{"terminal_reason":"api_error","structured_output":{}}', "claude-json"),
    ('{"status":"ERROR","structured_output":{}}', "claude-json"),
    ('{"error":{"code":429},"response":"{}"}', "gemini-json"),
    ('{"response":{}}', "gemini-json"),
    ('{"structured_output":"{}","result":"{}"}', "claude-json"),
    ('[]', "claude-json"), ('{}', "unknown"),
])
def test_failed_or_wrong_envelopes_refused(raw, carrier):
    with pytest.raises(lib.OutputError):
        lib.extract_final(output(raw, carrier))


@pytest.mark.parametrize("suffix", ["\n{", '\n{"event":"result","result":{}}', '\n[]'])
def test_agy_malformed_or_ambiguous_tail_refused(suffix):
    with pytest.raises((lib.OutputError, lib.AdmissionError)):
        lib.extract_final(output(wrap("{}", "agy-stream-json") + suffix, "agy-stream-json"))


@pytest.mark.parametrize("raw", [
    '{"event":"progress"}',
    '{"event":"result","result":{"status":"FAILED","structured_output":{}}}',
    '{"event":"result","result":{"status":"SUCCESS","structured_output":"{}"}}',
])
def test_agy_missing_or_failed_result_refused(raw):
    with pytest.raises(lib.OutputError):
        lib.extract_final(output(raw, "agy-stream-json"))


def test_agy_ignores_well_formed_nonterminal_and_blank_records():
    raw = '\n{"event":"progress","data":{"text":"quota auth"}}\n' + wrap("{}", "agy-stream-json") + '\n'
    assert lib.extract_final(output(raw, "agy-stream-json")) == "{}"


@pytest.mark.parametrize("carrier", ["claude-json", "gemini-json", "agy-stream-json"])
def test_carrier_must_match_binding(carrier):
    with pytest.raises(lib.OutputError) as caught:
        lib.admit_output(output(wrap(json.dumps(BASE), carrier), carrier), expected={k: BASE[k] for k in BINDINGS})
    assert caught.value.code == "carrier_mismatch"


def test_quota_looking_evidence_is_ordinary_data():
    data = dict(BASE, findings=[dict(FINDING, evidence="quota auth token expired")])
    assert lib.admit_output(output(json.dumps(data)), expected={k: BASE[k] for k in BINDINGS}) == data


def test_agy_preserves_literal_unicode_line_separator_in_json_string():
    raw = '{"text":"a\u2028b"}'
    assert lib.extract_final(output(wrap(raw, "agy-stream-json"), "agy-stream-json")) == raw


def test_agy_non_json_record_separator_is_not_a_line_boundary():
    raw = '{"event":"progress"}\x1e' + wrap("{}", "agy-stream-json")
    with pytest.raises(lib.AdmissionError) as caught:
        lib.extract_final(output(raw, "agy-stream-json"))
    assert caught.value.code == "invalid_json"


def test_agy_exit_three_refuses_partial_valid_result_before_parse():
    with pytest.raises(lib.OutputError) as caught:
        lib.extract_final(output(wrap("{}", "agy-stream-json") + '\n{', "agy-stream-json", exit_code=3))
    assert caught.value.code == "nonzero_exit"


@pytest.mark.parametrize("carrier,route", [("gemini-json", "agy"), ("agy-stream-json", "gemini")])
def test_google_sibling_carrier_cannot_swap(carrier, route):
    expected = {k: BASE[k] for k in BINDINGS} | {"family": "google", "route": route}
    with pytest.raises(lib.OutputError) as caught:
        lib.admit_output(output(wrap("{}", carrier), carrier), expected=expected)
    assert caught.value.code == "carrier_mismatch"


def test_native_does_not_strip_host_markers():
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output('```json\n' + json.dumps(BASE) + '\n```'), expected={k: BASE[k] for k in BINDINGS})
    assert caught.value.code == "invalid_json"
