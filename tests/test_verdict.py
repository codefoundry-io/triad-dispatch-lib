import copy
import json

import pytest

import triad_dispatch_lib as lib

BINDINGS = ("review_id", "family", "content_digest", "leg_name", "attempt", "route")
BASE = {
    "schema_version": 2, "review_id": "review-1", "family": "codex",
    "content_digest": "a" * 64, "leg_name": "codex-leg", "attempt": 1,
    "route": None, "verdict": "SAFE TO MERGE", "criteria_checked": ["correctness"],
    "findings": [], "affected_surfaces_inspected": ["src/main.py"], "open_questions": [],
}
FINDING = {
    "path": "src/main.py", "line": 1, "severity": "Minor", "summary": "Summary",
    "trigger": "Input", "evidence": "Observed", "context_known": True,
}


def admit(data, expected=None):
    assert callable(getattr(lib, "validate_verdict", None)), "validate_verdict API is missing"
    if expected is None:
        expected = {key: data[key] for key in BINDINGS}
    return lib.validate_verdict(json.dumps(data), expected=expected)


@pytest.mark.parametrize("family,route", [("codex", None), ("claude", None), ("google", "agy"), ("google", "gemini")])
@pytest.mark.parametrize("verdict", ["SAFE TO MERGE", "MERGE WITH FIXES", "DO NOT MERGE"])
def test_admit_canonical(family, route, verdict):
    data = dict(BASE, family=family, route=route, verdict=verdict)
    if verdict != "SAFE TO MERGE":
        data["findings"] = [FINDING]
    assert admit(data) == data
    expected = {key: data[key] for key in BINDINGS}
    data["attempt"] = 1.0
    result = admit(data, expected)
    assert type(result["attempt"]) is float


@pytest.mark.parametrize("field", list(BASE))
def test_missing_required(field):
    data = dict(BASE)
    del data[field]
    with pytest.raises(lib.AdmissionError) as caught:
        admit(data, {key: BASE[key] for key in BINDINGS})
    assert caught.value.code == "schema_violation"


@pytest.mark.parametrize("change", [
    {"extra": True}, {"schema_version": 1}, {"attempt": True}, {"attempt": 0},
    {"family": "google"}, {"route": "agy"}, {"criteria_checked": []},
    {"open_questions": ["why?"]}, {"verdict": "DO NOT MERGE"},
    {"findings": [dict(FINDING, severity="must-fix")]},
    {"findings": [dict(FINDING, severity="Critical")]},
    {"affected_surfaces_inspected": ["../secret"]},
    {"affected_surfaces_inspected": ["/absolute"]},
    {"criteria_checked": ["same", "same"]},
    {"findings": [dict(FINDING, unknown="x")]},
])
def test_schema_rejections(change):
    with pytest.raises(lib.AdmissionError) as caught:
        admit(dict(BASE, **change))
    assert caught.value.code == "schema_violation"


@pytest.mark.parametrize("field,value", [
    ("review_id", "other"), ("family", "claude"), ("content_digest", "b" * 64),
    ("leg_name", "other"), ("attempt", 2), ("route", "gemini"),
])
def test_each_binding(field, value):
    data = dict(BASE)
    if field == "route":
        data.update(family="google", route="agy")
    expected = {key: data[key] for key in BINDINGS}
    expected[field] = value
    with pytest.raises(lib.AdmissionError) as caught:
        admit(data, expected)
    assert caught.value.code == "binding_mismatch"


@pytest.mark.parametrize("change", [
    {"attempt": True}, {"attempt": 0}, {"extra": 1}, {"family": "invalid"},
    {"route": "agy"}, {"family": "google"}, {"content_digest": "short"},
])
def test_expected_binding(change):
    expected = {key: BASE[key] for key in BINDINGS} | change
    with pytest.raises(lib.AdmissionError) as caught:
        admit(BASE, expected)
    assert caught.value.code == "invalid_expected"


@pytest.mark.parametrize("expected", [{}, [], None, "binding"])
def test_expected_shape(expected):
    assert callable(getattr(lib, "validate_verdict", None)), "validate_verdict API is missing"
    with pytest.raises(lib.AdmissionError) as caught:
        lib.validate_verdict(json.dumps(BASE), expected=expected)
    assert caught.value.code == "invalid_expected"


def test_admission_errors_do_not_echo_input():
    with pytest.raises(lib.AdmissionError) as caught:
        admit(dict(BASE, PRIVATE_TOKEN="PRIVATE_VALUE"))
    assert "PRIVATE" not in str(caught.value)


def test_original_members_reach_parser():
    assert callable(getattr(lib, "validate_verdict", None)), "validate_verdict API is missing"
    raw = json.dumps(BASE).replace('"attempt": 1', '"attempt": 1, "attempt": 1')
    with pytest.raises(lib.AdmissionError) as caught:
        lib.validate_verdict(raw, expected={key: BASE[key] for key in BINDINGS})
    assert caught.value.code == "duplicate_member"


def test_no_shared_mutation():
    original = copy.deepcopy(BASE)
    expected = {key: BASE[key] for key in BINDINGS}
    result = admit(BASE, expected)
    result["criteria_checked"].clear()
    assert BASE == original
    assert expected == {key: BASE[key] for key in BINDINGS}
    assert admit(BASE) == original
