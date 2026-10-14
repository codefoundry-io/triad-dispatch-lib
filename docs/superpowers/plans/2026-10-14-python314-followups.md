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
- [x] Commit the bounded snapshot, await exact-head native CI and run the same
  complete review profile with 40-minute budgets and current official sources.

No runtime or normative case change is intended. Do not add a new inventory
framework or duplicate tests for the documentation edits. Record current outcomes
externally after the frozen commit, preserving the historical evidence boundary.

## R11 reference closure

R11 completed AGREED on `c7bf2bc`; native CI run 38595740079 passed all four
Python/platform jobs. Opus identified one C68 file-qualified test reference
missing its `spec/tests/` prefix. On 2026-10-15 the owner authorized continuing
verified quality corrections to convergence.

- [x] Correct the C68 path and independently audit the other explicit
  file-qualified references in the case and conformance maps. The read-only
  audit checked 94 references with no additional unresolved path or function.
- [x] Verify all 95 references after correction and run the required source and
  package checks on Python 3.12 and 3.14.
- [x] Await native CI and a fresh complete review; record outcomes
  externally after source freeze, alongside the draft PR.

Production/test delta: zero; one reference correction plus evidence records.
No new inventory framework or duplicate regression test is needed. Review
budgets, current official-source authorization and host boundaries are unchanged.

## R12 bounded follow-ups

R12 completed AGREED on `8ceaa7d`, with three Minor findings and no Astra
comparison defect. The round was exported and cleaned before these changes.

- [x] Reproduce Python 3.14 suppression of pre-publication receipt-status errors
  using real predicates and syscall EIO/EACCES injection. Replace that check
  with `lstat`, treating only FileNotFoundError as absence; extend the queued
  receipt regression and verify both Python versions.
- [x] Qualify C12/C14 canonical schema wildcard references explicitly.
- [x] Audit explicit and in-cell shorthand test references with a bounded
  external static checker; retain the distinction from semantic coverage.
- [x] Select the pull-request head SHA explicitly in CI, with a logged actual
  SHA assertion before tests; preserve the push-to-main path via github.sha.
- [x] Record actual earlier merge/tree identities and verify source/archive/wheel
  behavior on both Python versions: 723 source and 723 archive tests each.
- [x] Run fresh native CI and the complete review profile; retain outcomes
  externally after source freeze alongside the draft PR.

Expected production delta: +4/-1 in the repository-only native driver, no new
shared-library logic; one existing test gains syscall error variants. Workflow
adds nine lines for revision selection/assertion. Documentation and external
evidence are separate. Current R12 CI ran a merge commit whose tracked tree is
verified identical to `8ceaa7d`; it did not check out that head SHA itself.

The same-class audit reproduced two further existing-contract failures on actual
Python 3.14: `atomic()` could replace an existing destination after a status
error, and the asset generator could follow an output symlink after suppressing
its link-status error. Both are bounded preservation fixes under the owner's
quality-continuation instruction, with RED before correction. The output-root
error control already stopped before writes, so it needs no separate change.

- [x] Preserve existing atomic destinations/links on EIO/EACCES; retain missing
  destination publication. Verify seven focused cases on both interpreters.
- [x] Use exception-preserving non-following status for generator symlink checks;
  retain absent-output generation. Verify source/output errors in both modes,
  eight new regressions and the complete 44-case asset suite on both versions.
- [x] Remove the queued-receipt regression's fixed-delay assumption by waiting
  for the injected syscall error before disarming it; drain any RED request.

Revised measured production delta: +17/-5 (net +12) across the two tools, no new
shared-library code or interface. Tests: +135/-4 (net +131), adding 17 cases.
Workflow: +9/-0. Docs and external evidence remain separate. Integrated
source/archive/wheel, native CI and fresh review follow the final snapshot.

## R13 inventory and regular-file observation follow-ups

R13 completed all three entries on `d9d0055` and remained BLOCKED: Sol required
the generator enumeration correction independently identified by Opus and the
separate Astra comparison. Native CI run 38608784436 asserted this actual head
SHA in all four jobs, each passing 723 source/archive tests and four wheel paths.
The round was exported and cleaned before implementation continued.

- [x] Reproduce output scan EACCES/EIO with task-owned fixtures and an outside
  sentinel. Refuse incomplete source/output inventory before any write, using
  error-propagating traversal and non-following status checks. Cover root/nested
  scans, both modes, inventory omissions and initial output creation.
- [x] Preserve `regular()` link refusal when non-following metadata fails.
  Actual Python 3.14 syscall injection showed both `is_symlink()` and non-strict
  `resolve()` suppress the fault, allowing target bytes to be read. Keep absolute,
  canonical-path and regular-file checks; distinguish injected split faults from
  an observed OS permission arrangement.
- [x] Run focused RED/GREEN regressions on Python 3.12 and 3.14, then integrated
  source/archive/wheel verification: 760 source and 760 archive tests per version,
  all four wheel paths and all 184 scoped table references pass.
- [ ] Run native CI and a fresh full review with the
  same three required entries, Astra comparison and 40-minute budgets.

Estimated production delta: approximately +15/-4 across the two repository
tools, no shared-core/API or dependency changes. Tests and records are separate.
These restore existing inventory, link-refusal and file-preservation contracts;
concurrent-writer containment and new host guarantees remain outside scope.

Measured production delta: +27/-7 (net +20) across the two tools; tests +101/-0,
adding 37 cases. Explicit `scandir` and non-following observed modes avoid hidden
enumeration/classification suppression; a narrow ELOOP branch preserves the
native driver's existing canonical-path refusal. This explains the bounded
increase from the estimate. Documentation-only result recording follows local
builds; exact committed native CI and fresh review outcomes are external.

The leader's pre-review ancestor-path countercheck also reproduced non-strict
resolution suppressing ancestor-only metadata errors on both Python versions.
This is the same canonical-file contract; `lstat()` of the final leaf alone
cannot observe its ancestors. Add a one-line strict-resolution correction and
three ancestor variants to the existing new regression, then repeat integrated
verification before the next review. Preserve the preceding 760-test CI as
intermediate evidence for its actual commit, not the final candidate.

This follow-up is complete: RED reproduces both injected ancestor errors on
both interpreters; the native file passes 84 tests each. Final integrated runs
pass 763 source/archive tests per interpreter, all four wheel paths and 184
reference checks. Production follow-up +1/-1, tests +12/-4, three additional
cases. Final native CI and a fresh complete review remain externally recorded
steps after the documentation-only result update.
