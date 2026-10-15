# Adoption Observability Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct PR #2's evidence boundaries and provide value-free refusal locations and optional clause manifests.

**Architecture:** Extend existing admission and rendering functions additively.
Keep verified assets and host-owned execution intact; document all deferred API boundaries.

**Tech Stack:** Python 3.12+, jsonschema, referencing, pytest, uv.

**Spec:** [Adoption observability design](../../design/2026-10-15-adoption-observability.md)

## Global Constraints

- Python remains >=3.12; dependencies remain jsonschema>=4.26,<5 and referencing>=0.37,<1.
- Preserve original-output admission, canonical payload bytes, schema identities and all existing error codes.
- False returns exactly the existing string. True returns `(text, manifest)`.
- No provider execution, consumer edits, default changes or final merge belongs to implementation.
- Run Python/tests/builds/Git mutations through `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` on the first call; host cwd `/Users/chaniri/codex_workspace`, then enter this repository.

## Size and review boundary

One bounded additive observability slice: expected production +70/-10/net60,
novel core <=70 lines across errors.py, verdict.py and prompts.py. Tests about
150-220 lines; documentation tracked separately. One independent task review
and one complete project formal review with separate Astra comparison before
another implementation plan. Existing selected checkout is reused in place.

## Review Focus

- Untrusted additional property names must not leak through `.field`, `.path`,
  or the fixed message/`.args`. Existing exception internals and tracebacks are
  outside this diagnostic guarantee; their behavior remains unchanged.
- Simultaneous schema/expected/binding failures preserve the existing refusal order.
- Nested web-policy source clauses are represented without changing rendered bytes.
- Phase/host/route/hook selection has the same clause coverage in both modes.
- Mutable returned manifests and replacement-looking values cannot affect later calls.

### Task 1: Implement and document additive diagnostics

**Files:** `src/triad_dispatch_lib/{errors,verdict,prompts}.py`,
`tests/test_admission_diagnostics.py`, `tests/test_prompt_manifest.py`,
`spec/reference/library-api.md`.

**Interfaces:** Preserve `AdmissionError(code)`; add field/path attributes as the
design specifies. Extend only the renderer's `with_manifest` keyword and return
type. No new exports, dependencies, payload changes or host behavior.

- [x] Write RED tests for all six binding fields, schema keyword locations,
  arbitrary-property privacy, unchanged messages/args and precedence.
- [x] Run `uv run --locked pytest -q tests/test_admission_diagnostics.py` and
  retain the missing-diagnostics failures before implementation.
- [x] Add the minimal error attributes and trusted schema-path propagation.
- [x] Write RED manifest tests for the profile matrix, precise independent
  clause hashes, nested web clause, hook/host omission, invalid flag, tampered
  bundle refusal, fresh return values and nonrecursive caller replacements.
- [x] Run `uv run --locked pytest -q tests/test_prompt_manifest.py` and retain
  the unsupported-keyword failures before implementation.
- [x] Add the optional manifest on the existing rendering path; update the
  public API reference with exact privacy, hashing and return contracts.
- [x] Run both new suites plus existing verdict/prompt/output/agreement tests;
  report RED/GREEN counts and commit only owned files.
- [x] Obtain an independent task review for spec compliance and code quality.

### Task 2: Integrate evidence and verify the package

**Files:** request/adoption/status docs, design/plan, conformance/dev-log and
stale R-CONTAIN fact, README, pyproject.toml and uv.lock.

**Interfaces:** Consume Task 1 unchanged; record dev4 without consumer adoption.

- [x] Correct all PR #2 factual/provenance/scope findings and record each request's disposition.
- [x] Document declared dependency floors, per-platform offline wheels, fixed raw
  clauses and optional coordinators; update conformance links and package version.
- [x] Run source and unpacked-sdist suites with Python 3.12 and 3.14, asset and
  authoring checks, sdist/wheel builds and the four installed-wheel probes.
- [ ] Commit/push the reviewed changes, update PR title/body to the final scope,
  and observe native macOS/Ubuntu 3.12/3.14 CI for the actual committed head.
- [ ] Complete Opus/xhigh, Sol/xhigh, Argon/high formal review plus Astra/high
  comparison with 2400-second budgets and current official-source research allowed.
- [ ] Record outcomes and remaining limits, preserve the open PR merge boundary.
