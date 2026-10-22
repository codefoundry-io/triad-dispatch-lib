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


@pytest.mark.parametrize("negative", [False, True])
@pytest.mark.parametrize("as_bytes", [False, True])
def test_agy_metadata_admits_actual_verdict_without_rewriting_raw(negative, as_bytes):
    data = dict(BASE, family="google", route="agy")
    if negative:
        data.update(verdict="DO NOT MERGE", findings=[FINDING])
    raw = '{ "toolAction" : {"name":"read"}, "toolSummary" : [null, true, "한글"], ' + json.dumps(data)[1:]
    envelope = wrap(raw, "agy-stream-json")
    if as_bytes:
        raw, envelope = raw.encode(), envelope.encode()
    observed = output(envelope, "agy-stream-json")
    assert lib.admit_output(observed, expected={k: data[k] for k in BINDINGS}) == data
    assert observed.stdout == envelope
    assert lib.extract_final(observed) == raw
    payload, metadata = lib.separate_agy_metadata(raw)
    assert payload == data
    assert metadata == {"toolAction": {"name": "read"}, "toolSummary": [None, True, "한글"]}


@pytest.mark.parametrize("declared_fields,want_payload,want_metadata", [
    ((), {"answer": 42}, {"toolAction": False, "toolSummary": None}),
    (("toolAction",), {"answer": 42, "toolAction": False}, {"toolSummary": None}),
    (("toolSummary",), {"answer": 42, "toolSummary": None}, {"toolAction": False}),
    (("toolAction", "toolSummary"), {"answer": 42, "toolAction": False, "toolSummary": None}, {}),
])
def test_separate_agy_metadata_preserves_explicit_payload_declarations(declared_fields, want_payload, want_metadata):
    payload, metadata = lib.separate_agy_metadata(
        '{"answer":42,"toolAction":false,"toolSummary":null}', declared_fields=declared_fields)
    assert payload == want_payload
    assert metadata == want_metadata


def test_separate_agy_metadata_returns_fresh_independent_objects_and_retains_other_names():
    raw = b'{"nested":{"toolAction":[1]},"other":[2],"toolAction":{"items":[3]},"toolSummary":0.5}'
    payload, metadata = lib.separate_agy_metadata(raw)
    assert payload == {"nested": {"toolAction": [1]}, "other": [2]}
    assert metadata == {"toolAction": {"items": [3]}, "toolSummary": 0.5}
    payload["nested"]["toolAction"].append(4)
    metadata["toolAction"]["items"].append(5)
    assert lib.separate_agy_metadata(raw) == (
        {"nested": {"toolAction": [1]}, "other": [2]},
        {"toolAction": {"items": [3]}, "toolSummary": 0.5},
    )
    assert payload is not metadata


@pytest.mark.parametrize("raw,code", [
    ('{"toolAction":1,"toolAction":2}', "duplicate_member"),
    ('{"toolSummary":1,"toolSummar\\u0079":2}', "duplicate_member"),
    ('{"toolAction":{"x":1,"\\u0078":2}}', "duplicate_member"),
    ('{"toolAction":NaN}', "nonfinite_number"),
    ('{"toolSummary":Infinity}', "nonfinite_number"),
    ('{"toolSummary":1e999}', "nonfinite_number"),
    ('{"toolSummary":', "invalid_json"),
    (b'\xff', "invalid_utf8"),
    ({}, "invalid_input_type"),
])
def test_separate_agy_metadata_refuses_original_json_before_projection(raw, code):
    with pytest.raises(lib.AdmissionError) as caught:
        lib.separate_agy_metadata(raw)
    assert caught.value.code == code


@pytest.mark.parametrize("raw", ["null", "[]", '"text"', "1", "false"])
def test_separate_agy_metadata_requires_object(raw):
    with pytest.raises(lib.OutputError) as caught:
        lib.separate_agy_metadata(raw)
    assert caught.value.code == "invalid_envelope"


@pytest.mark.parametrize("declared_fields", [None, [], "toolAction", (1,), ("toolSummary", None)])
def test_separate_agy_metadata_requires_tuple_of_field_names(declared_fields):
    with pytest.raises(lib.OutputError) as caught:
        lib.separate_agy_metadata("{}", declared_fields=declared_fields)
    assert caught.value.code == "invalid_output"


def test_separate_agy_metadata_parses_original_before_invalid_declarations():
    with pytest.raises(lib.AdmissionError) as caught:
        lib.separate_agy_metadata('{"toolAction":NaN}', declared_fields=[])
    assert caught.value.code == "nonfinite_number"


@pytest.mark.parametrize("change", [
    {"other": "extra"},
    {"findings": [dict(FINDING, toolSummary="nested extra")]},
])
def test_agy_metadata_does_not_remove_other_or_nested_verdict_extras(change):
    data = dict(BASE, family="google", route="agy", toolAction="read", **change)
    expected = {k: data[k] for k in BINDINGS}
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output(wrap(json.dumps(data), "agy-stream-json"), "agy-stream-json"), expected=expected)
    assert caught.value.code == "schema_violation"


@pytest.mark.parametrize("raw,code", [
    ('{"toolAction":1,"toolAction":2}', "duplicate_member"),
    ('{"toolSummary":1,"toolSummar\\u0079":2}', "duplicate_member"),
    ('{"toolAction":NaN}', "nonfinite_number"),
    ('{"toolSummary":1e999}', "nonfinite_number"),
])
def test_agy_admission_never_discards_malformed_metadata(raw, code):
    expected = {k: BASE[k] for k in BINDINGS} | {"family": "google", "route": "agy"}
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output(wrap(raw, "agy-stream-json"), "agy-stream-json"), expected=expected)
    assert caught.value.code == code


@pytest.mark.parametrize("field,value", [
    ("review_id", "other"), ("family", "claude"), ("content_digest", "b" * 64),
    ("leg_name", "other"), ("attempt", 2), ("route", "gemini"),
])
def test_agy_metadata_does_not_bypass_invocation_binding(field, value):
    data = dict(BASE, family="google", route="agy", toolSummary="read")
    expected = {k: data[k] for k in BINDINGS}
    data[field] = value
    if field == "family":
        data["route"] = None
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output(wrap(json.dumps(data), "agy-stream-json"), "agy-stream-json"), expected=expected)
    assert (caught.value.code, caught.value.field) == ("binding_mismatch", field)


def test_agy_metadata_alone_does_not_supply_missing_verdict():
    expected = {k: BASE[k] for k in BINDINGS} | {"family": "google", "route": "agy"}
    raw = '{"toolAction":"read","toolSummary":"complete"}'
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output(wrap(raw, "agy-stream-json"), "agy-stream-json"), expected=expected)
    assert caught.value.code == "schema_violation"


@pytest.mark.parametrize("carrier,family,route", [
    ("native-final", "codex", None), ("claude-json", "claude", None),
    ("gemini-json", "google", "gemini"),
])
def test_non_agy_carriers_keep_metadata_names_strict(carrier, family, route):
    data = dict(BASE, family=family, route=route, toolAction="read", toolSummary="complete")
    with pytest.raises(lib.AdmissionError) as caught:
        lib.admit_output(output(wrap(json.dumps(data), carrier), carrier), expected={k: data[k] for k in BINDINGS})
    assert caught.value.code == "schema_violation"


def test_generic_verdict_validation_keeps_agy_metadata_names_strict():
    data = dict(BASE, family="google", route="agy", toolAction="read", toolSummary="complete")
    with pytest.raises(lib.AdmissionError) as caught:
        lib.validate_verdict(json.dumps(data), expected={k: data[k] for k in BINDINGS})
    assert caught.value.code == "schema_violation"


@pytest.mark.parametrize("change,code", [
    ({"completed": False}, "not_completed"), ({"timed_out": True}, "timed_out"),
    ({"transport_failed": True}, "transport_failed"), ({"exit_code": 3}, "nonzero_exit"),
])
def test_agy_metadata_admission_preserves_terminal_precedence(change, code):
    expected = {k: BASE[k] for k in BINDINGS} | {"family": "google", "route": "agy"}
    with pytest.raises(lib.OutputError) as caught:
        lib.admit_output(output('malformed private metadata', "agy-stream-json", **change), expected=expected)
    assert caught.value.code == code
