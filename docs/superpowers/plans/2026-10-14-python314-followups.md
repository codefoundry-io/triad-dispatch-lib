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
- [ ] Extend CI to both interpreters on Ubuntu/macOS with explicit UV_PYTHON
  selection and recorded runtime versions; commit/push and await exact-head CI.
- [ ] Update status/evidence, then run a fresh full-scope required
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
