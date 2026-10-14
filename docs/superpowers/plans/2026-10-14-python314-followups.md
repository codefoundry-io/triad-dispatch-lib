# Python 3.14 and review follow-ups

> **For agentic workers:** Use the existing TDD and parallel-agent procedures for
> these owner-authorized bounded corrections. Root owns integration and review.

**Goal:** Close all three R8 follow-ups, preserve native-driver custody on
Python 3.14, and verify source/archive/installed-wheel behavior on macOS/Ubuntu.

**Architecture:** Keep repository-only driver logic separate from the shared
library. Observe receipt presence using an exception-preserving lstat call;
only FileNotFoundError means not ready. Preserve consume/admission, cancellation
and terminal-acknowledgement semantics. Cache the import verifier per identity
check, without a process-global cache or new API.

**Tech stack:** Existing Python >=3.12 library, pytest, uv; default Python 3.12
remains unchanged. Add Python 3.14 to the existing native CI matrix.

**Contracts:** README native-driver contract, spec/reference/library-api.md and
docs/host-adoption.md. R8 findings and owner authorization define this follow-up.

Expected production delta: about 12 additions / 3 deletions (net 9), at most
15 novel lines in tools/native_codex_smoke.py and tools/four_route_smoke.py.
Tests, workflow and evidence documentation are counted separately: roughly
100 test lines and 10 workflow lines. No schema, dependency or host-default change.

- [x] Reproduce readiness failure on actual Python 3.14 before source edits.
- [x] Replace readiness observation; retain missing/present/dangling/cyclic
  behavior, EACCES/EIO first refusal, cancellation and slot custody until ack.
  Update/add regressions covering normal, cleanup, deadline and parent-cancel paths.
- [x] Add an observable public --help regression (wheel remains visible,
  --probe hidden, exit 0 and no installation). Countercheck against the former
  visible-help mutation without replacing current source history.
- [x] Load verify_import once per identity invocation. Test one helper load,
  all real export/package path checks and rejection of invalid origins.
- [x] Correct the existing decoder-limit test's fixed 10,000-level assumption
  exposed by full Python 3.14 verification. Test decoder-error translation
  directly, preserving real integer-limit coverage and the host-owned size bound.
  This is test portability work; add no product depth limit or runtime changes.
- [x] Run focused RED/GREEN checks, then source and rebuilt-sdist suites on
  Python 3.12 and 3.14; check authoring/assets and four installed-wheel drivers.
- [x] Extend CI to both interpreters on Ubuntu/macOS with explicit UV_PYTHON
  selection and recorded runtime versions; commit/push and await exact-head CI.
- [x] Update status/evidence, then run a fresh full-scope required
  Opus5.5/xhigh, Sol6.1/xhigh, Argon/high review plus separate Astra/high,
  each with 2400 seconds and current official web evidence. Preserve all
  results, adjudicate findings and clean exact owned review roots.

Self-review: all three requested follow-ups have implementation/verification
ownership. Missing receipt remains ordinary pending work; inaccessible receipt
is not absence. No optional redesign, consumer port or merge is included.

Measured delta: production +9/-3 (net +6) in the two test drivers; tests +160/-17
(net +143), with eight new cases and four redundant predicate variants removed.
The decoder test portability correction belongs to the authorized Python 3.14
verification and adds no production code. Workflow +12/-1; documentation is
recorded separately. Local source and sdist each pass 704 tests on both versions.
CI/review completion evidence is recorded externally after the committed source
is frozen, so this plan does not predeclare their outcomes.

## R9 bounded follow-up

R9 completed AGREED on 6f790f6 after four native CI jobs passed. Opus retained
two Minor findings within this outcome: forced Python 3.14 color causes a false
failure in the new help assertion, and native preflight reloads the same helper
per request. The completed round was exported/cleaned before further edits.

- [x] Pin PYTHON_COLORS=0 inside the help test after reproducing its failure with
  PYTHON_COLORS=1. Retain public-help behavior and the internal-probe assertion;
  verify both interpreters and Python 3.14 forced-color environments.
- [x] Load the native prepare_context callable once per run before callbacks;
  retain actual per-request context revalidation. Test real loader counts across
  two runs and refusal of context changes before invocation. Keep prepare's
  return contract and avoid a global cache. Estimate +2/-1 production lines.
- [x] Repeat source/archive/wheel checks on both interpreters, exact-head four-job
  CI and a fresh full-scope review with the same profile and 40-minute budgets.

These corrections add no dependency, native protocol, schema or product limit.
Measured follow-up delta: production +2/-1 (net +1), tests +48/-0 and two new
cases. Both local source/archive suites pass 706 tests, with four installed-wheel
checks each. Committed-head CI and the next review still follow this recording.

## R10 documentation and isolated-interpreter follow-up

R10 completed AGREED on `3ad33e8`; all four exact-head native CI jobs passed
706 source and 706 archive tests plus installed-wheel checks. The round was
exported and cleaned before these bounded follow-ups. Opus found a stale current
verification link and workflow line anchors in the derived case map. A separate
hardening suggestion identified the help test's color control under `-E`/`-I`.

- [x] Replace the case map's old measurement link with the current-status entry
  point and unstable workflow line numbers with named steps and the matrix.
- [x] Reproduce the actual Python 3.14 isolated-interpreter color failure;
  additionally set test-local NO_COLOR=1 if confirmed, preserving product help.
- [x] Verify the existing help regression on both interpreters and with actual
  isolated-interpreter forced-color execution.
- [x] Repeat integrated source/archive/wheel checks on both interpreters.
- [ ] Commit the bounded snapshot, await exact-head native CI and run the same
  complete review profile with 40-minute budgets and current official sources.

No runtime or normative case change is intended. Do not add a new inventory
framework or duplicate tests for the documentation edits. Record current outcomes
externally after the frozen commit, preserving the historical evidence boundary.
