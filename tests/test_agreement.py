import json

import pytest

import triad_dispatch_lib as lib
from tests.test_verdict import BASE, BINDINGS, FINDING


def evaluate(expected=None, results=None, integrity=True):
    assert hasattr(lib, "evaluate_agreement"), "agreement API missing"
    if expected is None:
        expected = {"codex-leg": {k: BASE[k] for k in BINDINGS}}
    if results is None:
        results = {"codex-leg": lib.ProviderOutput("native-final", json.dumps(BASE), None, True)}
    return lib.evaluate_agreement(expected, results, integrity_ok=integrity)


def test_every_same_family_leg_counts():
    a = dict(BASE, leg_name="a")
    b = dict(BASE, leg_name="b")
    expected = {v["leg_name"]: {k: v[k] for k in BINDINGS} for v in [a, b]}
    results = {v["leg_name"]: lib.ProviderOutput("native-final", json.dumps(v), None, True) for v in [a, b]}
    result = evaluate(expected, results)
    assert result.agreed and result.integrity_ok
    assert result.verdicts == {"a": a, "b": b} and result.reasons == {}
    results.pop("b")
    result = evaluate(expected, results)
    assert not result.agreed and result.reasons == {"b": "missing_output"}


@pytest.mark.parametrize("change,reason", [
    ({"verdict": "MERGE WITH FIXES", "findings": [FINDING]}, "negative_verdict"),
    ({"attempt": 2}, "binding_mismatch"), ({"leg_name": "other"}, "binding_mismatch"),
    ({"review_id": "old"}, "binding_mismatch"),
])
def test_negative_invalid_stale_and_swapped_block(change, reason):
    assert hasattr(lib, "ProviderOutput"), "ProviderOutput API missing"
    result = evaluate(results={"codex-leg": lib.ProviderOutput("native-final", json.dumps(BASE | change), None, True)})
    assert not result.agreed and result.reasons == {"codex-leg": reason}


def test_failure_and_invalid_payload_block():
    assert hasattr(lib, "ProviderOutput"), "ProviderOutput API missing"
    for raw, exit_code, reason in [("bad", None, "invalid_json"), (json.dumps(BASE), 1, "nonzero_exit")]:
        result = evaluate(results={"codex-leg": lib.ProviderOutput("native-final", raw, exit_code, True)})
        assert not result.agreed and result.reasons == {"codex-leg": reason}


def test_host_integrity_blocks_unanimous_safe():
    result = evaluate(integrity=False)
    assert not result.agreed and not result.integrity_ok
    assert result.verdicts == {"codex-leg": BASE}


@pytest.mark.parametrize("expected,results,integrity,code", [
    ({}, {}, True, "empty_selection"), ([], {}, True, "invalid_expected_map"),
    ({"wrong": {k: BASE[k] for k in BINDINGS}}, {}, True, "name_mismatch"),
    ({"a": {k: BASE[k] for k in BINDINGS} | {"leg_name": "a"},
      "b": {k: BASE[k] for k in BINDINGS} | {"leg_name": "b", "content_digest": "b" * 64}}, {}, True, "mixed_basis"),
    ({"codex-leg": {k: BASE[k] for k in BINDINGS}}, {"extra": {}}, True, "extra_output"),
    ({"codex-leg": {k: BASE[k] for k in BINDINGS}}, [], True, "invalid_outputs_map"),
    ({"codex-leg": {k: BASE[k] for k in BINDINGS}}, {"codex-leg": BASE}, True, "invalid_output"),
    ({"codex-leg": {k: BASE[k] for k in BINDINGS}}, {}, 1, "invalid_integrity"),
])
def test_invalid_callers_raise(expected, results, integrity, code):
    assert hasattr(lib, "AgreementError"), "AgreementError API missing"
    with pytest.raises(lib.AgreementError) as caught:
        evaluate(expected, results, integrity)
    assert caught.value.code == code


def test_contract_failure_propagates(monkeypatch):
    import triad_dispatch_lib.verdict as verdict_module
    def broken():
        raise lib.ContractError("Broken package")
    monkeypatch.setattr(verdict_module, "load_contract", broken)
    with pytest.raises(lib.ContractError):
        evaluate()


@pytest.mark.parametrize("field,value", [
    ("family", "claude"), ("content_digest", "b" * 64),
    ("route", "gemini"),
])
def test_all_binding_fields_are_rechecked(field, value):
    data = dict(BASE)
    if field == "route":
        data.update(family="google", route="agy")
    expected = {"codex-leg": {k: data[k] for k in BINDINGS}}
    data[field] = value
    result = evaluate(expected, {"codex-leg": lib.ProviderOutput("native-final", json.dumps(data), None, True)})
    assert not result.agreed and result.reasons == {"codex-leg": "binding_mismatch"}


def test_mixed_review_ids_and_invalid_binding_are_caller_errors():
    expected = {"a": {k: BASE[k] for k in BINDINGS} | {"leg_name": "a"},
                "b": {k: BASE[k] for k in BINDINGS} | {"leg_name": "b", "review_id": "other"}}
    with pytest.raises(lib.AgreementError) as caught:
        evaluate(expected, {})
    assert caught.value.code == "mixed_basis"
    with pytest.raises(lib.AgreementError) as caught:
        evaluate({"codex-leg": {}}, {})
    assert caught.value.code == "invalid_binding"


def test_four_carrier_round_counts_both_google_routes():
    from tests.test_output import wrap
    expected, results = {}, {}
    for name, carrier, family, route in [
        ("c", "native-final", "codex", None), ("a", "claude-json", "claude", None),
        ("g", "gemini-json", "google", "gemini"), ("y", "agy-stream-json", "google", "agy"),
    ]:
        data = dict(BASE, leg_name=name, family=family, route=route)
        expected[name] = {k: data[k] for k in BINDINGS}
        results[name] = lib.ProviderOutput(carrier, wrap(json.dumps(data), carrier), 0, True)
    assert evaluate(expected, results).agreed
    negative = dict(BASE, leg_name="g", family="google", route="gemini",
                    verdict="DO NOT MERGE", findings=[FINDING])
    results["g"] = lib.ProviderOutput("gemini-json", wrap(json.dumps(negative), "gemini-json"), 0, True)
    result = evaluate(expected, results)
    assert not result.agreed and result.reasons == {"g": "negative_verdict"}
