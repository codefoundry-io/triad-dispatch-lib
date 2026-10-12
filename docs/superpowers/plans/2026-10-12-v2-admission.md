# Strict JSON and v2 Admission Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Deliver an independently installable deterministic v2 admission core.

**Architecture:** Preserve the pinned canonical schema as package data. Separate
original-JSON parsing, package integrity, and binding admission. Both hosts remain
unchanged; raw replay vectors are the future adapter contract.

**Tech Stack:** Python 3.12+, jsonschema, referencing, setuptools, uv, pytest.

**Spec:** [First-slice design](../../design/2026-10-12-v2-admission.md).

## Global Constraints

- Python 3.12+; package `triad-dispatch-lib`, import `triad_dispatch_lib`, version `0.1.0.dev0`.
- Dependencies `jsonschema>=4.26,<5`, `referencing>=0.37,<1`; commit `uv.lock`.
- Canonical schema bytes from spec `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`.
- Six bindings, offline validation, no v1 conversion, no host/global configuration edits.
- Synthetic fixtures must remain raw; no provider calls, publication, or final merge.
- Native Ubuntu 24.04 x86-64 and macOS ARM64 CI, Python 3.12.
- Work in the selected repository on `codex/strict-v2-admission`.
- On the owner workstation, Python/build/test/Git mutations/GitHub commands use
  `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` first.

## Review Focus

- Escaped duplicate names and nonfinite overflow: reject before schema conversion (Task 1).
- Sensitive malformed payloads and keys: errors must not include their contents (Tasks 1/2).
- Boolean versus integer bindings and Google route mismatch: reject without coercion (Task 2).
- Changed package data or unresolved external refs: fail closed without network access (Task 2).
- Installed sdist-derived wheel loading source/host modules accidentally: prove isolated imports (Task 3).

## Files and responsibilities

`src/triad_dispatch_lib/json_input.py` handles original JSON;
`errors.py` defines failure types; `contracts.py` loads verified offline data;
`verdict.py` performs canonical admission; `__init__.py` exports the API.
`tests/` contains unit tests and language-neutral raw fixtures. `tools/verify_wheel.py`
performs isolated installed-package replay. `.github/workflows/test.yml` supplies
native CI. No production CLI is needed for this slice.

### Task 1: Original JSON boundary and installable skeleton

**Files:** Create `pyproject.toml`, `uv.lock`, `src/triad_dispatch_lib/__init__.py`,
`errors.py`, `json_input.py`, and `tests/test_json_input.py`.

**Interfaces:** Produces `parse_json(raw: str | bytes) -> object`,
`AdmissionError(ValueError).code`, `ContractError(RuntimeError)`.

- [ ] Write `test_original_json`, `test_rejected_raw`, `test_input_type`,
  `test_errors_do_not_echo_input`, `test_decoder_limits`: assert valid scalars and
  nested objects preserved; duplicate/escaped duplicate keys, NaN/Infinity/1e400,
  bad UTF-8/fences/trailing content/types/limits produce the specified codes.
- [ ] Add packaging/test configuration and an empty package; run
  `uv run pytest tests/test_json_input.py -q`. Expected: failing assertions for
  missing API behavior (test imports occur inside test bodies).
- [ ] Implement the interface with `json.loads`, duplicate-member hook,
  finite-float and constant hooks; fixed-message errors with no raw payloads.
- [ ] Run `uv run pytest tests/test_json_input.py -q`. Expected: all pass.
- [ ] Commit `feat: add strict original JSON parsing`; complete task with the same command.

### Task 2: Canonical contract integrity and bound admission

**Files:** Create `src/triad_dispatch_lib/contracts.py`, `verdict.py`,
`data/leg-verdict.schema.json`, `data/source-manifest.json`,
`tests/test_verdict.py`, `tests/test_contracts.py`; modify `__init__.py`.

**Interfaces:** Consumes Task 1 API. Produces
`validate_verdict(raw: str | bytes, *, expected: dict) -> dict` and internal
`load_contract() -> dict` (a fresh schema per call, no mutable shared cache).

- [ ] Fetch the exact canonical schema and record its source/digest manifest.
- [ ] Write `test_admit_canonical`, `test_schema_rejections`, `test_each_binding`,
  `test_expected_binding`, `test_admission_errors_do_not_echo_input`,
  `test_original_members_reach_parser`, and `test_no_shared_mutation`.
  Assert all families/routes, valid negatives, integral floats, rejected bools,
  missing/extra fields, SAFE blockers/questions and all six mismatch codes.
- [ ] Write `test_manifest_and_digest`, `test_broken_contract`,
  `test_external_ref_is_offline`: fault manifest/digest/schema and verify refusal;
  unresolved HTTP/file references must raise ContractError without retrieval.
- [ ] Run `uv run pytest tests/test_verdict.py tests/test_contracts.py -q`.
  Expected: failures for absent admission/contract API.
- [ ] Implement verified resource loading, Draft202012Validator with Registry(),
  schema-derived expected binding validation and exact six-field comparison.
  Package resources in wheel/sdist via setuptools package-data.
- [ ] Run `uv run pytest -q`. Expected: all pass.
- [ ] Commit `feat: validate v2 verdicts against pinned offline contracts`;
  complete task with `uv run pytest -q`.

### Task 3: Raw replay, installed-wheel proof and native CI

**Files:** Create `tests/fixtures/replay/{cases.json,*.json,invalid-utf8.bin,README.md}`,
`tests/test_replay.py`, `tools/verify_wheel.py`, `.github/workflows/test.yml`;
update `README.md`, `AGENTS.md`, `docs/status.md`;
add `docs/verification/2026-10-12-v2-admission.md`.

**Interfaces:** Consumes public APIs and packaged data. Produces
`python tools/verify_wheel.py DIST_WHEEL` (binary-only isolated install, subprocess
outside checkout, fixed fixture corpus, import provenance and wheel hash report).

- [ ] Write `test_replay_vectors` against raw fixtures (positive, nested duplicate,
  invalid UTF-8, nonfinite, stale binding, invalid v1, malformed negative).
  Add `test_installed_probe_requires_site_packages` and
  `test_installed_probe_replays_vectors` for the verifier's child probe.
- [ ] Run `uv run pytest tests/test_replay.py -q`. Expected: probe behavior fails
  until implemented; new replay vectors must pass existing admission.
- [ ] Implement isolated verifier and CI with read-only repository permissions,
  fixed action SHAs, native OS matrix and Python 3.12. Build sdist, rebuild wheel
  from sdist, install outside checkout, and replay raw fixtures.
- [ ] Run `uv run pytest -q`, `uv build --sdist`, `uv build dist/*.tar.gz --wheel`,
  `uv run python tools/verify_wheel.py dist/*.whl`, `git diff --check`.
  Expected: green tests, isolated package proof, no whitespace issues.
- [ ] Document exact local results and current remote CI status; update instructions
  only for setup/test commands. Commit `test: verify isolated wheels on macOS and Ubuntu`;
  complete task with `uv run pytest -q`.

## Completion

Self-review the plan against the design before execution. Execute inline with a
durable task ledger and one fresh independent whole-branch reviewer. Resolve
material findings with failing regression tests and a green suite. Push the
feature branch and open a draft PR; inspect native CI before claiming platform
coverage. Update verification evidence. No final merge or package release.

## Later plans

Design classification/aggregation separately, then a thin Codex test adapter and
pinned prompt cases. Run a fresh real Codex smoke only once that driver can prove
which library artifact it imports. Adopt in each host via its own scoped PR.
