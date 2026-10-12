# Pinned Clauses and Codex Smoke Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Track steps with checkboxes and a task ledger.

**Goal:** Exercise pinned common clauses and fresh Codex JSON through the installed library.

**Architecture:** A pure clause renderer owns common text selection. A repository
test adapter owns packet I/O and isolated wheel execution. Native children remain
outside the library and return only JSON.

**Tech Stack:** Python 3.12, existing jsonschema/referencing/uv/pytest stack.

**Spec:** [Prompt smoke design](../../design/2026-10-12-codex-prompt-smoke.md).

## Global Constraints

- Current branch/PR #1, no consumer/spec/config edits, final merge or release.
- Pin source `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`; preserve canonical bytes.
- First rendering profile: family=codex, host=B; refuse others explicitly.
- Version `0.1.0.dev1`; Python 3.12 baseline; existing dependency ranges remain.
- Native response capture is parent-transcribed-final-text, not machine attestation.
- Workstation Python/tests/builds/Git mutations/GitHub use `/bin/zsh -lic`
  with `sandbox_permissions="require_escalated"` on the first call.

## Review Focus

- Canonical notes or unselected clauses leak into output: strict parsing/order tests (Task 1).
- Caller values override phase/web policy or get substituted twice: hostile replacement tests (Task 1).
- Driver bypasses installed validation or reports a checkout import: call-through/path tests (Task 2).
- Packet/prompt changes or stale bindings receive credit: mutation/raw rejection tests (Task 2).
- Source archive lacks the tests' support files: unpacked-sdist and installed replay checks (Task 3).

### Task 1: Verified canonical clause rendering

**Files:** `src/triad_dispatch_lib/{contracts,verdict,errors,__init__,prompts}.py`,
`src/triad_dispatch_lib/data/prompt-bundle/`, `tests/test_prompts.py`,
`tests/test_verdict.py`, `pyproject.toml`, `uv.lock`.

**Interfaces:** Add public `validate_binding(expected: dict) -> None`,
`render_review_clauses(*, family, host, review_date, review_web_authorized,
replacements, review_kind="pre-merge") -> str`, `render_data(value: str) -> str`,
`PromptError(ValueError)`. Share internal `load_verified_bundle(root, names)`.

- [x] Fetch pinned payload bytes/manifest. Write `test_phase_and_order`,
  `test_web_and_arguments`, `test_replacement_once`, `test_bundle_damage`,
  `test_clause_format`, `test_residual_roundtrip`, `test_validate_binding_api`.
  Assert three phases, exact canonical order, strict booleans/date/profile,
  missing/extra replacements, no notes/A-only leakage, placeholder preservation,
  manifest refusal and JSON-decoded hostile residual equality.
- [x] Run `uv run pytest tests/test_prompts.py tests/test_verdict.py -q`.
  Expected: new API assertions fail; prior admission cases pass.
- [x] Implement minimal pure renderer and shared integrity/binding helpers.
  Package nested data resources; bump dev version and refresh uv lock.
- [x] Run `uv run pytest -q`. Expected: all pass, unchanged admission semantics.
- [x] Commit `feat: render pinned Codex review clauses`; complete with full suite.

### Task 2: Installed-wheel Codex test adapter

**Files:** `tools/codex_smoke.py`, `tools/verify_wheel.py`,
`tests/test_codex_smoke.py`, `tests/fixtures/codex/{brief.md,example.py}`.

**Interfaces:** Reuse `installed_wheel(wheel)` context manager yielding
`(python, prefix, neutral_cwd)`. Driver exposes `prepare_context(context)`,
`render_prompt(context)`, `admit_result(raw, context, prompt)` for focused tests;
CLI `--wheel W --expected-version V render --context C --prompt P`,
`... admit --context C --prompt P --result R`, and `... self-test`.

- [x] Write `test_context_and_prompt`, `test_scope_rejection`,
  `test_packet_and_prompt_changes`, `test_admission_call_through`,
  `test_raw_rejections`, `test_profile_and_identity`.
  Assert decoded scope/residual equality, confined regular files and digest,
  no duplicate packet paths, actual validator spy/sentinel, unchanged raw bytes,
  stale binding/duplicate rejection and explicit version/path checks.
- [x] Run `uv run pytest tests/test_codex_smoke.py -q`.
  Expected: missing-driver assertions fail.
- [x] Implement driver and reuse wheel environment creation. Record hashes and
  installed callable origin. `self-test` builds a temporary synthetic context,
  exercises render plus positive/duplicate/stale admission without any provider.
- [x] Run `uv run pytest -q`. Expected: all pass.
- [x] Commit `test: add isolated Codex prompt admission driver`; complete with full suite.

### Task 3: Distribution, fresh native smoke and recorded evidence

**Files:** `MANIFEST.in`, `.github/workflows/test.yml`, `README.md`,
`docs/status.md`, `docs/verification/2026-10-12-codex-prompt-smoke.md`.

**Interfaces:** Task 2 CLI plus actual collaboration final JSON as original text.

- [x] Test built sdist membership for fixture/tool requirements; observe missing
  support files before adding MANIFEST.in. Include tools, fixture data and local
  test-support files; do not include `_runs` or private prompt/provider records.
- [x] Build sdist and wheel, unpack sdist and run tests there. Run installed-wheel
  replay and `codex_smoke.py --wheel W --expected-version 0.1.0.dev1 self-test`.
  Expected: full tests and synthetic render/admission pass outside source imports.
- [x] Record control/defect expectations, prepare two bounded synthetic packets
  under ignored `_runs/`, and render prompts via the installed wheel.
  Dispatch two fresh Sol/medium read-only native children (`fork_turns=none`).
  Save exact final text and observed receipt metadata, then admit both via the
  installed wheel. Expected: schema/bindings pass, correct control is SAFE,
  defective case identifies the concrete defect despite instruction-like data.
  Do not repair/retry a failing model response invisibly; report the observation.
- [x] Add native CI synthetic driver step; record actual local/live outcomes and
  custody limits. Update package commands and next scope. Commit
  `test: verify packaged prompt driver and fresh native responses`.
- [ ] Complete with `uv run pytest -q`, then fresh whole-branch reviewer, any
  necessary TDD fixes, push/update draft PR and inspect both native CI jobs.

## Completion

Report deterministic tests, installed-package evidence and fresh native response
evidence separately. Preserve full context limits. No existing host adoption,
formal multi-family admission, final merge or package-index release is claimed.
