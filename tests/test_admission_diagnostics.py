import json

import pytest

from triad_dispatch_lib import AdmissionError, validate_verdict
from tests.test_verdict import BASE, BINDINGS, FINDING


def refusal(data, expected=None):
    if expected is None:
        expected = {name: BASE[name] for name in BINDINGS}
    with pytest.raises(AdmissionError) as caught:
        validate_verdict(json.dumps(data), expected=expected)
    return caught.value


@pytest.mark.parametrize("field,value", [
    ("review_id", "other"), ("family", "claude"), ("content_digest", "b" * 64),
    ("leg_name", "other"), ("attempt", 2), ("route", "gemini"),
])
def test_binding_field_is_canonical(field, value):
    data = BASE | ({"family": "google", "route": "agy"} if field == "route" else {})
    expected = {name: data[name] for name in BINDINGS} | {field: value}
    error = refusal(data, expected)
    assert error.code == "binding_mismatch"
    assert error.field == field
    assert error.path is None
    assert error.args == ("Verdict does not match the expected invocation.",)


def test_first_binding_mismatch_follows_canonical_order():
    expected = {name: BASE[name] for name in reversed(BINDINGS)}
    expected.update(review_id="other", family="claude", leg_name="other", attempt=2)
    assert refusal(BASE, expected).field == "review_id"


@pytest.mark.parametrize("change,path", [
    ({"attempt": 0}, ("properties", "attempt", "minimum")),
    ({"PRIVATE_PROPERTY": "PRIVATE_VALUE"}, ("additionalProperties",)),
    ({"verdict": "MERGE WITH FIXES", "findings": [FINDING | {"PRIVATE_PROPERTY": "PRIVATE_VALUE"}]},
     ("properties", "findings", "items", "additionalProperties")),
    ({"family": "google"}, ("allOf", 0, "then", "properties", "route", "enum")),
])
def test_schema_path_contains_only_trusted_schema_location(change, path):
    error = refusal(BASE | change)
    assert error.code == "schema_violation"
    assert error.field is None
    assert error.path == path
    assert error.args == ("Verdict violates the canonical schema.",)
    assert "PRIVATE" not in repr(vars(error)) + str(error) + repr(error.args)
    assert error.__cause__ is None
    assert error.__suppress_context__


@pytest.mark.parametrize("code", [
    "invalid_json", "invalid_utf8", "duplicate_member", "nonfinite_number",
    "invalid_input_type", "nesting_limit", "schema_violation", "invalid_expected",
    "binding_mismatch",
])
def test_constructor_retains_message_args_and_empty_diagnostics(code):
    error = AdmissionError(code)
    assert error.field is None and error.path is None
    assert error.args == (str(error),)
    assert error.code == code


@pytest.mark.parametrize("raw,expected,code", [
    ('{"attempt":0,"attempt":1}', {}, "duplicate_member"),
    (json.dumps(BASE | {"attempt": 0}), {}, "schema_violation"),
    (json.dumps(BASE), {"review_id": "other"}, "invalid_expected"),
])
def test_parse_schema_expected_binding_precedence(raw, expected, code):
    with pytest.raises(AdmissionError) as caught:
        validate_verdict(raw, expected=expected)
    error = caught.value
    assert error.code == code
    assert error.field is None
    assert (error.path is not None) == (code == "schema_violation")
