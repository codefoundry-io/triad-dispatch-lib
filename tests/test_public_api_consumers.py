"""Selected dev4 consumer contracts; runnable without pytest or a Git checkout."""

import argparse
from dataclasses import FrozenInstanceError
from importlib.metadata import version
import json
from pathlib import Path
import unittest

import triad_dispatch_lib as lib


EXPORTS = """AdmissionError AgreementError AgreementResult CallOutcome ContractError
DispatchError InvestigationRequest OutputError PromptError ProviderOutput ReceiptError
ReviewRequest ReviewRun RosterError admit_output evaluate_agreement extract_final
load_roster_contract merge_roster parse_json render_data render_investigation_prompt
render_review_clauses resolve_roster run_investigations run_review select_entries separate_agy_metadata
validate_binding validate_resolved validate_transport_receipt validate_verdict""".split()
BINDING = dict(review_id="consumer-1", family="codex", content_digest="a" * 64,
               leg_name="c", attempt=1, route=None)
VERDICT = dict(schema_version=2, **BINDING, verdict="SAFE TO MERGE",
               criteria_checked=["correctness"], findings=[],
               affected_surfaces_inspected=["api.py"], open_questions=[])


def entry(name):
    return dict(name=name, vendor="codex", enabled=True, acceptance="required",
                timeout_s=30, codex={"model": "opaque future/model build"})


class PublicAPIConsumers(unittest.TestCase):
    def test_exports_and_six_frozen_constructors(self):
        self.assertTrue(set(EXPORTS).issubset(lib.__all__))
        for name in EXPORTS:
            self.assertTrue(callable(getattr(lib, name)), name)
        agreement = lib.AgreementResult(False, {}, {}, True)
        cases = [
            (lib.ProviderOutput("native-final", "{}", None, True), "carrier", "native-final"),
            (lib.ReviewRequest({}, {}, "scope"), "prompt", "scope"),
            (lib.InvestigationRequest({}, "scope"), "web_authorized", False),
            (lib.CallOutcome("c", "completed", None, None), "name", "c"),
            (lib.ReviewRun((), agreement), "agreement", agreement),
            (agreement, "integrity_ok", True),
        ]
        for value, field, expected in cases:
            self.assertEqual(getattr(value, field), expected)
            with self.assertRaises(FrozenInstanceError):
                setattr(value, field, None)

    def test_error_bases_codes_and_diagnostics(self):
        for name, code in [("AdmissionError", "invalid_json"), ("RosterError", "invalid_json"),
                           ("ReceiptError", "schema_violation"), ("OutputError", "timed_out"),
                           ("AgreementError", "empty_selection"), ("DispatchError", "invalid_requests")]:
            error = getattr(lib, name)(code)
            self.assertIsInstance(error, ValueError)
            self.assertEqual(error.code, code)
            self.assertTrue(error.args)
        self.assertIsInstance(lib.ContractError("contract"), RuntimeError)
        self.assertIsInstance(lib.PromptError("prompt"), ValueError)
        error = lib.AdmissionError("invalid_json")
        self.assertEqual((error.field, error.path, error.missing), (None, None, None))
        with self.assertRaises(lib.RosterError) as caught:
            lib.validate_resolved({})
        self.assertEqual((caught.exception.code, caught.exception.document,
                          caught.exception.path, caught.exception.missing),
                         ("schema_violation", "resolved", ("required",), "schema"))

    def test_strict_json_and_all_six_bindings(self):
        self.assertEqual(lib.parse_json(b'{"ok":[1,true,null]}'), {"ok": [1, True, None]})
        for raw, code in [(b"\xff", "invalid_utf8"), ('{"x":1,"x":2}', "duplicate_member"),
                          ("1e999", "nonfinite_number"), ("{", "invalid_json")]:
            with self.assertRaises(lib.AdmissionError) as caught:
                lib.parse_json(raw)
            self.assertEqual(caught.exception.code, code)
        self.assertIsNone(lib.validate_binding(BINDING))
        self.assertEqual(lib.validate_verdict(json.dumps(VERDICT), expected=BINDING), VERDICT)
        for field, changed in dict(review_id="other", family="claude", content_digest="b" * 64,
                                   leg_name="other", attempt=2, route="gemini").items():
            document, expected = dict(VERDICT), dict(BINDING)
            if field == "route":
                document.update(family="google", route="agy")
                expected.update(family="google", route="agy")
            expected[field] = changed
            with self.assertRaises(lib.AdmissionError) as caught:
                lib.validate_verdict(json.dumps(document), expected=expected)
            self.assertEqual((caught.exception.code, caught.exception.field), ("binding_mismatch", field))

    def test_roster_order_copy_and_opaque_models(self):
        original = dict(schema="triad-review-legs.v2", legs=[entry("c"), entry("second")])
        override = dict(schema="triad-review-legs.v2", legs=[dict(name="c", enabled=False), entry("third")])
        merged = lib.merge_roster(original, json.dumps(override))
        self.assertEqual([leg["name"] for leg in merged["legs"]], ["c", "second", "third"])
        self.assertIsNone(lib.validate_resolved(merged))
        self.assertEqual(lib.resolve_roster(original, json.dumps(override)), merged)
        selected = lib.select_entries(merged)
        self.assertEqual([leg["name"] for leg in selected], ["second", "third"])
        selected[0]["codex"]["model"] = "changed"
        self.assertEqual(merged["legs"][1]["codex"]["model"], "opaque future/model build")
        merged["legs"][0]["codex"]["model"] = "changed"
        self.assertEqual(original["legs"][0]["codex"]["model"], "opaque future/model build")
        contract = lib.load_roster_contract()
        contract.clear()
        self.assertTrue(lib.load_roster_contract())

    def test_transport_and_prompt_return_contracts(self):
        receipt = dict(schema_version=2, stdin_delivery="complete", route="codex",
                       binary="codex", cli_version="opaque future CLI build", attempt=1)
        self.assertIsNone(lib.validate_transport_receipt(receipt))
        with self.assertRaises(lib.ReceiptError) as caught:
            lib.validate_transport_receipt({})
        self.assertEqual(caught.exception.code, "schema_violation")
        values = {"worktree": '"/tmp/review"', "brief-file": '"/tmp/brief"',
                  "packet-files": '["/tmp/brief"]', "review-id": "consumer-1",
                  "content-digest": "a" * 64, "leg-name": "c", "attempt": "1"}
        kwargs = dict(family="codex", host="B", review_date="2026-10-16",
                      review_web_authorized=False, replacements=values)
        text = lib.render_review_clauses(**kwargs)
        self.assertIsInstance(text, str)
        self.assertEqual(text, lib.render_review_clauses(**kwargs, review_kind="pre-merge"))
        rendered, manifest = lib.render_review_clauses(**kwargs, with_manifest=True)
        self.assertEqual(rendered, text)
        self.assertTrue(manifest)
        for row in manifest:
            self.assertEqual(set(row), {"name", "sha256"})
            self.assertRegex(row["sha256"], r"^[0-9a-f]{64}$")
        self.assertIsInstance(lib.render_investigation_prompt("scope", family="codex"), str)
        self.assertIn('\n"scope"\n', lib.render_data("scope"))

    def test_carrier_negative_timeout_and_agreement_safety(self):
        raw = json.dumps(VERDICT)
        output = lib.ProviderOutput("native-final", raw, None, True)
        self.assertEqual(lib.extract_final(output), raw)
        self.assertEqual(lib.admit_output(output, expected=BINDING), VERDICT)
        self.assertTrue(lib.evaluate_agreement({"c": BINDING}, {"c": output}, integrity_ok=True).agreed)
        self.assertFalse(lib.evaluate_agreement({"c": BINDING}, {"c": output}, integrity_ok=False).agreed)
        self.assertEqual(lib.evaluate_agreement({"c": BINDING}, {}, integrity_ok=True).reasons,
                         {"c": "missing_output"})
        negative = VERDICT | dict(verdict="DO NOT MERGE", open_questions=["missing context"])
        output = lib.ProviderOutput("native-final", json.dumps(negative), None, True)
        self.assertEqual(lib.admit_output(output, expected=BINDING), negative)
        self.assertEqual(lib.evaluate_agreement({"c": BINDING}, {"c": output}, integrity_ok=True).reasons,
                         {"c": "negative_verdict"})
        for carrier, timed_out, code in [("unknown", False, "invalid_carrier"), ("native-final", True, "timed_out")]:
            with self.assertRaises(lib.OutputError) as caught:
                lib.extract_final(lib.ProviderOutput(carrier, raw, 0, True, timed_out))
            self.assertEqual(caught.exception.code, code)

    def test_agy_metadata_separation_and_negative_admission(self):
        binding = BINDING | dict(family="google", route="agy")
        verdict = VERDICT | binding | dict(verdict="DO NOT MERGE", open_questions=["missing context"])
        raw = json.dumps(verdict | dict(toolAction={"read": True}, toolSummary=[None, "done"])).encode()
        payload, metadata = lib.separate_agy_metadata(raw)
        self.assertEqual(payload, verdict)
        self.assertEqual(metadata, {"toolAction": {"read": True}, "toolSummary": [None, "done"]})
        declared, metadata = lib.separate_agy_metadata(raw, declared_fields=("toolSummary",))
        self.assertEqual(declared, verdict | dict(toolSummary=[None, "done"]))
        self.assertEqual(metadata, {"toolAction": {"read": True}})
        envelope = b'{"event":"result","result":{"status":"SUCCESS","structured_output":' + raw + b'}}'
        observed = lib.ProviderOutput("agy-stream-json", envelope, 0, True)
        self.assertEqual(lib.extract_final(observed), raw)
        self.assertEqual(lib.admit_output(observed, expected=binding), verdict)
        self.assertEqual(observed.stdout, envelope)
        self.assertEqual(lib.evaluate_agreement({"c": binding}, {"c": observed}, integrity_ok=True).reasons,
                         {"c": "negative_verdict"})
        with self.assertRaises(lib.AdmissionError) as caught:
            lib.validate_verdict(raw, expected=binding)
        self.assertEqual(caught.exception.code, "schema_violation")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-prefix", type=Path, required=True)
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()
    origin = Path(lib.__file__).resolve()
    relative = origin.relative_to(args.installed_prefix.resolve())
    assert "site-packages" in relative.parts, origin
    assert version("triad-dispatch-lib") == args.expected_version
    unittest.main(argv=[__file__])
