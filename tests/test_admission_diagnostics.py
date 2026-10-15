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
    assert error.missing is None
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
    assert error.missing is None
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
    assert error.missing is None
    assert not hasattr(error, "member")
    assert error.args == (str(error),)
    assert error.code == code


@pytest.mark.parametrize("raw,expected,code,field,missing,path", [
    ('{"attempt":0,"attempt":1}', {}, "duplicate_member", None, None, None),
    (json.dumps(BASE | {"attempt": 0}), {}, "schema_violation", None, None,
     ("properties", "attempt", "minimum")),
    (json.dumps(BASE), {"review_id": "other"}, "invalid_expected", None, None, None),
    ("NaN", {}, "nonfinite_number", None, None, None),
    (json.dumps({k: v for k, v in BASE.items() if k != "review_id"}), {},
     "schema_violation", None, "review_id", ("required",)),
    (json.dumps(BASE), {name: BASE[name] for name in BINDINGS} | {"review_id": "other"},
     "binding_mismatch", "review_id", None, None),
])
def test_parse_schema_expected_binding_precedence(raw, expected, code, field, missing, path):
    with pytest.raises(AdmissionError) as caught:
        validate_verdict(raw, expected=expected)
    error = caught.value
    assert error.code == code
    assert error.field == field
    assert error.missing == missing
    assert error.path == path


@pytest.mark.parametrize("missing_parameter", (
    "path", "line", "severity", "summary", "trigger", "evidence", "context_known",
))
def test_missing_nested_required_is_canonical(missing_parameter):
    finding = {k: v for k, v in FINDING.items() if k != missing_parameter}
    error = refusal(BASE | {"verdict": "MERGE WITH FIXES", "findings": [finding]})
    assert error.code == "schema_violation"
    assert error.missing == missing_parameter
    assert error.field is None
    assert error.path == ("properties", "findings", "items", "required")
    assert error.args == ("Verdict violates the canonical schema.",)


def test_missing_uses_selected_finding_object():
    finding = {k: v for k, v in FINDING.items() if k != "severity"}
    error = refusal(BASE | {"verdict": "MERGE WITH FIXES", "findings": [dict(FINDING), finding]})
    assert error.missing == "severity"
    assert error.path == ("properties", "findings", "items", "required")


@pytest.mark.parametrize("nested", [False, True])
def test_multiple_missing_follow_selected_required_order(nested):
    data = dict(BASE)
    if nested:
        finding = dict(FINDING)
        for name in ("summary", "severity"):
            del finding[name]
        data.update(verdict="MERGE WITH FIXES", findings=[finding])
        missing, path = "severity", ("properties", "findings", "items", "required")
    else:
        for name in ("family", "review_id"):
            del data[name]
        missing, path = "review_id", ("required",)
    error = refusal(data)
    assert error.code == "schema_violation"
    assert error.missing == missing
    assert error.path == path
    assert error.args == ("Verdict violates the canonical schema.",)


def test_competing_schema_error_keeps_existing_winner():
    data = {k: v for k, v in BASE.items() if k != "review_id"}
    error = refusal(data | {"PRIVATE_PROPERTY": "PRIVATE_VALUE"})
    assert error.code == "schema_violation"
    assert error.path == ("additionalProperties",)
    assert error.missing is None
    assert error.field is None
    assert error.args == ("Verdict violates the canonical schema.",)


def test_missing_guaranteed_surface_does_not_echo_provider_data():
    data = {k: v for k, v in BASE.items() if k != "review_id"}
    data.update(verdict="MERGE WITH FIXES", findings=[
        FINDING | {"summary": "PRIVATE_VALUE", "PRIVATE_PROPERTY": "PRIVATE_NESTED_VALUE"},
    ])
    error = refusal(data)
    assert error.code == "schema_violation"
    assert error.missing == "review_id"
    assert error.field is None
    assert error.path == ("required",)
    assert error.args == ("Verdict violates the canonical schema.",)
    assert "PRIVATE" not in repr((error.code, str(error), error.args, error.field, error.path, error.missing))
    assert not hasattr(error, "member")


def test_duplicate_name_stays_out_of_guaranteed_surface():
    with pytest.raises(AdmissionError) as caught:
        validate_verdict('{"PRIVATE_KEY":1,"PRIVATE_KEY":2}', expected={})
    error = caught.value
    assert error.code == "duplicate_member"
    assert error.missing is None
    assert error.field is None
    assert error.path is None
    assert error.args == ("Duplicate JSON object member.",)
    assert not hasattr(error, "member")
    assert "PRIVATE" not in repr((error.code, str(error), error.args, error.field, error.path, error.missing))
