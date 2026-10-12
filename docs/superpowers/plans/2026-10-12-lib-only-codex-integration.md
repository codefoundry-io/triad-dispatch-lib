# Library-owned Codex Integration Test Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Track steps with checkboxes and the plan ledger.

**Goal:** Test installed-library Codex behavior entirely from this repository.

**Architecture:** Expand the existing synthetic adapter matrix without adding host
runtime logic. Use separate fresh native observations for plan and implementation
review. Existing hosts remain untouched and are not executed.

**Tech Stack:** Python 3.12, existing uv/pytest/jsonschema dependencies.

**Spec:** [Library-only test design](../../design/2026-10-12-lib-only-codex-integration.md).

## Global Constraints

- All changes/tests in triad-dispatch-lib; no existing host execution or adoption.
- Keep runtime package `0.1.0.dev1` and canonical assets unchanged.
- Preserve exact raw bytes and parent-transcribed native capture limitation.
- Workstation Python/tests/builds/Git/GitHub use `/bin/zsh -lic` with
  `sandbox_permissions="require_escalated"` on the first call.
- Existing branch and draft PR #1; no merge, release or global configuration.

## Review Focus

- Negative verdict accidentally counted as approval: unchanged-value checks.
- Matrix reports success without exercising validation: fault-injected admission.
- One phase omitted or wrong clause selected: phase matrix and existing renderer tests.
- Packet mutation contaminates later cases: per-case restoration and matrix completion.
- Missing wheel triggers installation: reject before environment creation.

### Task 1: Expand installed Codex matrix and input refusal

**Files:** `tools/codex_smoke.py`, `tests/test_codex_smoke.py`.

**Interfaces:** `synthetic_smoke() -> dict` retains existing keys and adds `cases`
with exactly 18 named cases per phase, each reporting review_kind/name/outcome.
The CLI remains unchanged.

- [ ] Add `test_synthetic_matrix` asserting all three phases, 18 distinct cases
  each and the exact intended admission/rejection outcomes; add
  `test_synthetic_matrix_refuses_false_admission` and
  `test_missing_wheel_refused_before_install`.
- [ ] Run `uv run --locked pytest tests/test_codex_smoke.py -q`.
  Expected: new matrix assertion and missing-wheel exit-code failures.
- [ ] Extend self-test using real renderer/admission calls with explicit expected
  results and rejection codes. Reject nonexistent wheel via argparse before
  calling installed_wheel. Do not modify src/ or consumer repositories.
- [ ] Run `uv run --locked pytest -q`. Expected: all pass.
- [ ] Commit `test: expand library-owned Codex integration matrix`.

### Task 2: Installed and fresh native evidence

**Files:** `README.md`, `docs/status.md`,
`docs/verification/2026-10-12-lib-only-codex-integration.md`.

**Interfaces:** Existing render/admit/self-test CLI and Task 1 cases report.

- [ ] Build sdist and its wheel, run original wheel replay and expanded installed
  self-test. Expected: 10 replay cases and 54 phase matrix cases pass.
- [ ] Record expectations before dispatch; prepare isolated formal-plan and
  implementation-review control/defect packets in ignored `_runs/`.
  Render through the explicit installed wheel. Dispatch four fresh Sol/medium
  children, fork_turns=none, read-only, no scripts/providers/web/subagents.
- [ ] Save exact final text and observed receipts, admit with the same wheel,
  packet and prompt, report actual outcomes without repair or invisible retry.
  Expected: SAFE controls and arithmetic findings in negative cases; planned
  future files are not represented as inspected.
- [ ] Update docs, run full suite and commit evidence. Request one fresh
  whole-branch reviewer, handle findings according to executing-plans, update
  draft PR and inspect native Ubuntu/macOS CI.

## Completion

Report deterministic and native evidence separately, all recorded rulings/minors,
and the explicit boundary: library-only test adapter, no existing host adoption.
