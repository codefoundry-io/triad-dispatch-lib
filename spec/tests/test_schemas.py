"""Executable schema examples; no vendor calls or host implementation imports."""
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def validator(name, definition=None):
    path = ROOT / "contracts" / name
    assert path.is_file(), f"missing canonical schema: {name}"
    schema = json.loads(path.read_text())
    Draft202012Validator.check_schema(schema)
    if definition:
        schema = {**schema, "$ref": f"#/$defs/{definition}"}
        schema.pop("required", None)
        schema.pop("properties", None)
        schema.pop("additionalProperties", None)
    return Draft202012Validator(schema)


def verdict():
    return {
        "schema_version": 2, "review_id": "round-1", "leg_name": "google-pro",
        "family": "google", "route": "agy", "attempt": 1,
        "content_digest": "a" * 64, "verdict": "SAFE TO MERGE",
        "criteria_checked": ["correctness"], "findings": [],
        "affected_surfaces_inspected": ["src/main.py"], "open_questions": [],
    }


def finding(severity="Minor", path="src/main.py"):
    return {"severity": severity, "path": path, "line": 1, "summary": "Observed issue",
            "trigger": "Concrete input", "evidence": "src/main.py:1",
            "context_known": True}


@pytest.mark.parametrize("name", [
    "leg-verdict.schema.json", "review-legs.schema.json", "receipt-fields.json",
])
def test_canonical_schema_is_valid_202012(name):
    validator(name)


@pytest.mark.parametrize("label", ["SAFE TO MERGE", "MERGE WITH FIXES", "DO NOT MERGE"])
def test_c13_minor_only_result_is_valid_for_each_label(label):
    data = verdict()
    data.update(verdict=label, findings=[finding()])
    validator("leg-verdict.schema.json").validate(data)


def test_c13_uncertainty_only_negative_needs_no_invented_finding():
    data = verdict()
    data.update(verdict="DO NOT MERGE", open_questions=["Missing deployment fact"])
    validator("leg-verdict.schema.json").validate(data)


@pytest.mark.parametrize("mutation", [
    {"verdict": "SAFE"}, {"schema_version": 1}, {"attempt": 0}, {"attempt": True},
    {"route": None}, {"family": "claude"}, {"extra": "unrecognized"},
    {"open_questions": ["unknown"]}, {"findings": [finding("must-fix")]},
    {"criteria_checked": []}, {"criteria_checked": ["x", "x"]},
    {"criteria_checked": [" "]}, {"affected_surfaces_inspected": []},
    {"content_digest": "A"*64}, {"leg_name": "../google"},
    {"verdict": "DO NOT MERGE"},
])
def test_c13_c14_invalid_verdict_is_rejected(mutation):
    data = verdict()
    data.update(mutation)
    assert not validator("leg-verdict.schema.json").is_valid(data)


@pytest.mark.parametrize("path", ["/tmp/file", "../file", "a/../b", "a//b", "./file",
                                  "a\\b", "a\nb", "src/main.py\n", "", " "])
def test_c14_unsafe_or_ambiguous_path_is_rejected(path):
    data = verdict()
    data["findings"] = [finding(path=path)]
    assert not validator("leg-verdict.schema.json").is_valid(data)


@pytest.mark.parametrize("field", ["review_id", "leg_name", "content_digest",
                                   "affected_surfaces_inspected"])
def test_c14_terminal_newline_cannot_escape_binding_or_coverage(field):
    data = verdict()
    if field == "affected_surfaces_inspected":
        data[field] = ["src/main.py\n"]
    else:
        data[field] += "\n"
    assert not validator("leg-verdict.schema.json").is_valid(data)


@pytest.mark.parametrize("key", ["summary", "trigger", "evidence", "context_known", "path"])
def test_c14_missing_finding_evidence_is_rejected(key):
    data = verdict()
    data["findings"] = [finding()]
    del data["findings"][0][key]
    assert not validator("leg-verdict.schema.json").is_valid(data)


@pytest.mark.parametrize("key", ["leg_name", "attempt", "route",
                                 "affected_surfaces_inspected", "open_questions"])
def test_c14_legacy_missing_data_cannot_be_admitted_as_v2(key):
    data = verdict()
    del data[key]
    assert not validator("leg-verdict.schema.json").is_valid(data)


def test_c12_named_partial_override_is_valid():
    data = {"schema": "triad-review-legs.v2",
            "legs": [{"name": "claude", "claude": {"model": "opus", "effort": "high"}}]}
    validator("review-legs.schema.json").validate(data)


def test_c12_shipped_template_has_valid_structure_but_is_not_a_catalog():
    data = json.loads((ROOT / "contracts/review-legs.example.json").read_text())
    validator("review-legs.schema.json", "resolvedRoster").validate(data)
    claude = next(leg["claude"] for leg in data["legs"] if leg["name"] == "claude")
    # R-ROSTER (owner 2026-10-08, D-OWNER-ANSWERS-20261008 item 17): the measured claude alias, not the exact ID
    assert (claude["model"], claude["effort"]) == ("opus", "xhigh")
    codex = next(leg["codex"] for leg in data["legs"] if leg["name"] == "codex")
    assert (codex["model"], codex["reasoning"]) == ("gpt-6-astra", "high")
    assert any("<" in leg.get("agy", {}).get("model", "") for leg in data["legs"])


@pytest.mark.parametrize("entry", [
    {"name": "x", "unknown": True}, {"name": "../bad"}, {"name": "x\n"},
    {"name": "x", "timeout_s": 0}, {"name": "x", "enabled": "true"},
    {"name": "x", "vendor": "other"}, {"name": "x", "google": {"route": "auto"}},
    {"name": "x", "claude": {"surprise": "value"}},
])
def test_c12_roster_rejects_unknown_fields_and_wrong_types(entry):
    data = {"schema": "triad-review-legs.v2", "legs": [entry]}
    assert not validator("review-legs.schema.json").is_valid(data)


def test_c12_resolved_roster_requires_complete_entries():
    v = validator("review-legs.schema.json", "resolvedRoster")
    data = {"schema": "triad-review-legs.v2", "legs": [{"name": "claude"}]}
    assert not v.is_valid(data)
    data["legs"][0].update(vendor="claude", enabled=True, acceptance="required",
                          timeout_s=1200, claude={"model": "opus", "effort": "xhigh"})
    v.validate(data)
    data["legs"][0]["codex"] = {"model": "terra", "reasoning": "high"}
    assert not v.is_valid(data)


def test_c12_google_route_pin_and_two_cli_blocks_are_valid():
    data = {"schema": "triad-review-legs.v2", "legs": [{
        "name": "google", "vendor": "google", "enabled": True,
        "acceptance": "participating", "timeout_s": 600,
        "google": {"route": "agy"}, "agy": {"model": "pro", "effort": "high"},
        "gemini": {"model": "route-valid-pro", "effort": None},
    }]}
    validator("review-legs.schema.json", "resolvedRoster").validate(data)


@pytest.mark.parametrize("pin,other", [("agy", "gemini"), ("gemini", "agy")])
def test_c12_resolved_google_pin_requires_its_own_block(pin, other):
    entry = {"name": "google", "vendor": "google", "enabled": True,
             "acceptance": "required", "timeout_s": 600,
             "google": {"route": pin}, other: {"model": "other-route-model"}}
    data = {"schema": "triad-review-legs.v2", "legs": [entry]}
    v = validator("review-legs.schema.json", "resolvedRoster")
    assert not v.is_valid(data)
    entry[pin] = {"model": "selected-route-model"}
    v.validate(data)


@pytest.mark.parametrize("pin", [None, "agy", "gemini"])
def test_c12_single_route_configuration_remains_valid(pin):
    selected = pin or "agy"
    entry = {"name": "google", "vendor": "google", "enabled": True,
             "acceptance": "required", "timeout_s": 600,
             selected: {"model": "route-model"}}
    if pin is not None:
        entry["google"] = {"route": pin}
    validator("review-legs.schema.json", "resolvedRoster").validate(
        {"schema": "triad-review-legs.v2", "legs": [entry]})


def receipt():
    return {"schema_version": 2, "stdin_delivery": "complete",
            "route": "claude", "binary": "/usr/local/bin/claude",
            "cli_version": "observed-version", "attempt": 1}


@pytest.mark.parametrize("state", ["not-used", "not-started", "complete", "failed", "unexposed"])
def test_c9_c10_transport_delivery_states(state):
    data = receipt()
    data["stdin_delivery"] = state
    validator("receipt-fields.json").validate(data)


def test_c9_native_receipt_does_not_invent_cli_identity():
    data = receipt()
    data.update(route="native", binary=None, cli_version=None, stdin_delivery="not-used")
    validator("receipt-fields.json").validate(data)
    data["binary"] = "/fake/inferred/path"
    assert not validator("receipt-fields.json").is_valid(data)


@pytest.mark.parametrize("mutation", [
    {"attempt": 0}, {"attempt": True}, {"route": "google"}, {"binary": ""},
    {"cli_version": ""}, {"stdin_delivery": "ok"}, {"secret": "not part of receipt"},
])
def test_c9_c10_receipt_rejects_ambiguous_or_unknown_fields(mutation):
    data = receipt()
    data.update(mutation)
    assert not validator("receipt-fields.json").is_valid(data)


def cleanup_roots_example():
    return json.loads((ROOT / "contracts" / "cleanup-roots.example.json").read_text())


def test_c69_cleanup_roots_example_is_valid():
    validator("cleanup-roots.schema.json").validate(cleanup_roots_example())


@pytest.mark.parametrize("field", ["role", "root", "proof", "min_age_s"])
def test_c69_cleanup_root_entry_requires_each_field(field):
    data = cleanup_roots_example()
    del data["roots"][0][field]
    assert not validator("cleanup-roots.schema.json").is_valid(data)


def test_c69_cleanup_root_proof_is_never_a_bare_name_shape():
    data = cleanup_roots_example()
    data["roots"][0]["proof"] = "name-shape"
    assert not validator("cleanup-roots.schema.json").is_valid(data)


def test_c69_cleanup_role_is_named():
    data = cleanup_roots_example()
    data["roots"][0]["role"] = ""
    assert not validator("cleanup-roots.schema.json").is_valid(data)
