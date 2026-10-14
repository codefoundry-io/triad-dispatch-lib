# Python 3.14 and R8 follow-ups

The owner authorized all three nonblocking R8 follow-ups, regression tests,
Python 3.14 verification and a fresh complete review. R8
`20261014-lib-spec-r8-a49108` completed `AGREED` on `00ed792`; that approval does
not transfer to changed bytes. Its required Opus/Sol/Argon entries and separate
Astra comparison remain the selected profile, each with a 2400-second budget.

CI identity clarification: the R9–R12 PR runs checked out merge commits with
tracked trees verified identical to their reviewed heads. Historical "exact-head"
wording below identifies the head-associated results, not an exact checkout SHA.
See the [checkout identities and subsequent correction](2026-10-15-review-closure.md#native-ci-source-identity).

## Corrections and regression evidence

- The native repository driver now observes receipt readiness with `lstat()`.
  Only `FileNotFoundError` means pending; permission/I/O failures preserve the
  first refusal, request cancellation and retain custody until terminal
  acknowledgement. Ordinary absence and dangling links have explicit tests.
  Six syscall-injected error cases cover normal/cleanup EACCES and EIO,
  deadline EACCES and parent-cancellation EIO. Four redundant predicate-specific
  variants were removed when two predicates became one observation.
- `four_route_smoke.identity()` resolves the import verifier once per call.
  A fresh subprocess loads the actual copied package and real verifier, checks
  all 27 exports plus the package, and rejects external export/package origins.
  Two identity calls prove per-call loading without a global cache. Both Python
  versions reproduced 56 helper loads instead of two before correction.
- The public wheel help already hid internal `--probe`; the new regression
  checks exit zero, visible `wheel`, absent `--probe` and no installation.
  An in-memory former-visible source mutation fails that exact absence
  assertion on both interpreters; current source history was never reverted.

The readiness test injection was corrected to the syscall boundary because
Python 3.14 `Path.lstat()` directly uses `os.lstat`, bypassing the previous
`Path.stat` patch. Initial failed runs remain retained, not counted as successful
verification. Final syscall tests against an isolated copy of the pre-fix driver
reproduce six Python 3.14 failures; the candidate source was not replaced.

## Current external evidence

Accessed 2026-10-14:

- [Python 3.14 pathlib file-status queries](https://docs.python.org/3.14/library/pathlib.html#querying-file-type-and-status)
  document suppression of all `OSError` by predicate methods in 3.14 and advise
  `stat()` for exceptions. This explains delayed refusal with `exists()` and
  `is_symlink()`; the driver uses non-following `lstat()` to retain link checks.
- [uv UV_PYTHON reference](https://docs.astral.sh/uv/reference/environment/#uv_python)
  defines the interpreter selector. CI sets it per matrix entry and asserts
  the actual interpreter for both checkout and unpacked archive, preventing
  `.python-version` from silently selecting 3.12 in the 3.14 job.

Official documentation, installed interpreters and actual verification are
separate evidence. Local interpreters are Python 3.12.13 and 3.14.6. No default
interpreter, dependency, canonical payload, schema or host configuration changes.
The production delta is nine additions and three deletions across two test
drivers; the shared library implementation is unchanged.

## Verification boundary

Focused helper/help tests pass 41 cases and native-driver tests pass 67 cases on
each interpreter. The initial full 3.12 source/archive checks passed 702 tests.
The initial full 3.14 check passed 701 and failed the pre-existing decoder test:
10,000 nested arrays no longer reliably reach the interpreter's recursion limit.
The library promises translation of decoder errors, not a fixed depth limit;
the test was corrected to exercise that contract directly. Initial failed
logs and their completed temporary-directory cleanup remain retained.

The corrected `test_decoder_limits` injects `RecursionError` at the decoder
boundary and checks `nesting_limit`, private-detail omission and suppressed
exception context. Separate cases retain the real integer-conversion limit and
verify safe 32-level nesting. The file passes 28 tests on both interpreters;
an isolated missing-catch mutation fails on both. The conformance-map test name
is preserved; production and specification require no change.

Tagged [CPython 3.14.6 JSON](https://raw.githubusercontent.com/python/cpython/v3.14.6/Modules/_json.c)
and [recursion helper](https://raw.githubusercontent.com/python/cpython/v3.14.6/Include/internal/pycore_ceval.h)
use actual stack bounds, whereas the [3.12.13 helper](https://raw.githubusercontent.com/python/cpython/v3.12.13/Include/internal/pycore_ceval.h)
uses a C-recursion counter. The [official JSON documentation](https://docs.python.org/3.14/library/json.html)
defines no independent fixed nesting maximum. These sources were accessed
2026-10-15; the observed threshold remains interpreter/platform dependent.

Final local verification on macOS 26.6.2 ARM64:

| Interpreter | Source suite | Unpacked-sdist suite | Installed-wheel paths |
| --- | --- | --- | --- |
| Python 3.12.13 | 704 passed | 704 passed | All four passed |
| Python 3.14.6 | 704 passed | 704 passed | All four passed |

Both runs also pass canonical authoring, generated-asset consistency, diff checks
and the interface map (53 test references and 27 exports, none missing).
Wheel checks cover bundle replay, Codex prompt/admission, four-route synthetic
matrix and supervised synthetic callback exchange. Binary dependencies install
successfully on both interpreters. Default `.venv`, Python pin and lockfile remain
unchanged. The test count is 700 - 4 redundant variants + 8 new cases = 704.

Measured artifact SHA-256 values:

| Interpreter | sdist | Rebuilt wheel |
| --- | --- | --- |
| 3.12.13 | `771ed0adf92eeac06351795a2c7206476a23878366d6607d7e65de67ec087d98` | `27f90ee2981d6842c85fafdf6eef61b817b51b0ce397802b38fb669e9f5776f3` |
| 3.14.6 | `1c89a871d195705a5e5530901b3d378cf106b3e7277c6765c2cb0e64bc64138f` | `324244ea26b311b8422aae1f58f951c8c0b1438c9e4b65f086bb94210f7c23fb` |

These identify measured working-tree builds before this documentation-only result
recording. They do not assert reproducible archive bytes or identify the later
commit. Runtime/tests/assets did not change after measurement. Exact owned build
stages were removed after terminal completion; raw logs, commands and hashes are
retained under `_runs/reviews/20261014-lib-python314/final-{3.12,3.14}-r2/`.

Committed-head native CI and the fresh review follow this source record. Their
exact head, run URLs, all four job results, review ID and adjudication are retained
with the owner-managed evidence and [draft PR](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1).
The CI matrix covers Ubuntu 24.04 and macOS 15 with Python 3.12 and 3.14; a
configured job is not a successful platform observation.

Synthetic callback tests do not attest real backend termination, effective
provider settings, consumer adoption or release. Final merge and publication
remain separate boundaries.

## R9 outcome and follow-up boundary

R9 `20261014-lib-spec-r9-053dee` completed AGREED on `6f790f6`, digest
`9cf742bc5da6e473d86bda974ba0c81698ddf8e5f5520ce545a48eec9a89ec51`.
Opus, Sol and Argon all returned SAFE TO MERGE; separate Astra reported no
concrete defect. The three R8 follow-ups were confirmed closed. Opus retained
two Minor maintenance findings: forced-color help test portability and per-entry
native preflight helper loading. All children/producers terminated and the exact
round roots were exported/cleaned before subsequent edits. Original outputs and
adjudication are retained in the owner workspace; no approval transfers.

[Native CI run 38586758282](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38586758282)
passed on the exact `6f790f6cd21a9555bd8d1eeb7a375abe4cf67b5c` head. Each native
job passed 704 source and 704 sdist tests, interpreter assertions, asset/authoring
checks, archive rebuild and all four installed-wheel checks:

| Native platform | Actual source/archive Python |
| --- | --- |
| macOS 15 ARM64 | 3.12.10 and 3.14.7 |
| Ubuntu 24.04 x86_64 | 3.12.15 and 3.14.8 |

The bounded correction isolates the test's color environment and reuses the
native preflight callable per run, while preserving every context revalidation.
Actual Python 3.14.6 with `PYTHON_COLORS=1` reproduced the help failure; the same
file now passes 30 tests on each interpreter and with both caller color variables
forced on 3.14. `FORCE_COLOR` alone did not reproduce in the inherited environment
and is not counted as RED evidence. The existing test locally sets
`PYTHON_COLORS=0`, restores it through monkeypatch, and leaves CLI behavior and
all previous assertions intact.

The [3.14 argparse color documentation](https://docs.python.org/3.14/library/argparse.html#color)
and [CPython v3.14.6 color helper](https://raw.githubusercontent.com/python/cpython/v3.14.6/Lib/_colorize.py)
were checked on 2026-10-15. The pinned source gives `PYTHON_COLORS=0` precedence
over competing color controls when environment handling is enabled.

Native preflight now retains a real `prepare_context` callable per run. Two real
three-request exchanges reproduce helper-load counts `[4, 8]` before correction
and `[2, 4]` afterward. The two loads per run deliberately retain `prepare()`'s
own load plus one callback lookup, avoiding a new return contract or global cache.
Every preflight still calls the real validator: a packet changed after preparation
is refused with `preflight_failed` before any request is published. Production
delta is +2/-1; regressions add two cases. Its final source/archive/native-CI and
fresh review evidence follow this recording boundary.

Final follow-up verification: local macOS 26.6.2 ARM64, Python 3.12.13 and 3.14.6
each pass **706 source + 706 unpacked-sdist tests**, all four installed-wheel
paths, authoring/generator/diff and 53-test-reference/27-export map checks.
Focused native suites each pass 69 cases. These runs follow the two bounded R9
corrections; the earlier 704-test measurements remain historical.

| Interpreter | Follow-up sdist SHA-256 | Follow-up rebuilt wheel SHA-256 |
| --- | --- | --- |
| 3.12.13 | `79a11252d1533caf3349275cc1d61ddd9f5b8f691bb5436e96550c2513ff35a9` | `78410de6fe5eca99a6c2e230a355e697afec94ccad15e0ad0bee8f63c4fc5e23` |
| 3.14.6 | `b12a96e3d8ec413a71dd61fd617ee0a8a2a8eabe5d4e862174e47cf877c7361b` | `d124e19bd8109176900a5b3dc901dc3fe37f95c354ac7bfc29c1d0178769a574` |

Commands, terminal exits, hashes and successful exact-stage cleanup are retained
in `final-{3.12,3.14}-r3/` under the same owner evidence root. This paragraph is
documentation-only recording after measurement. The next committed-head CI and
fresh review outcomes are recorded externally with their exact head and round;
no old approval or platform result is transferred to the new commit.

## R10 outcome and isolated-interpreter follow-up

R10 `20261014-lib-spec-r10-9218dc` completed AGREED on
`3ad33e8180492a624dbbac9fce38f74788efd013`, digest
`f0e00da07b30a85a626122a606bcb8a81aa84494f949b086dfd42988399e8a1e`.
All three required reviewers returned SAFE TO MERGE; Sol and Argon had no
findings, and the separate Astra comparison found no actionable defect. All
results were terminal before canonical export and cleanup. Each review had the
same 2400-second budget and authorization for current official web evidence.

[Native CI run 38591880134](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38591880134)
passed on that exact head: each of the four jobs passed **706 source and 706
unpacked-sdist tests**, actual source/archive interpreter assertions, authoring,
asset checks, wheel rebuilding and all four installed-wheel checks. Actual
Python versions were macOS 3.12.10/3.14.7 and Ubuntu 3.12.15/3.14.8.

Opus found a Minor in the derived case map: its current-measurement link pointed
at the older R1-R4 record, and workflow line anchors no longer identified the
Python selection or all installed-wheel steps. The map now links the current
status entry point and names the matrix and workflow steps. Normative case text,
runtime contracts and generated assets are unchanged. Its optional suggestion
to introduce an inventory test framework is outside this small documentation fix;
existing external `verify.py` directly executes the map checks and saves
`interface-map-check.json`, separate from subprocess rows in `results.json`.

A separate hardening suggestion concerned Python 3.14 `-E`/`-I`: the pinned
[CPython v3.14.6 color helper](https://raw.githubusercontent.com/python/cpython/v3.14.6/Lib/_colorize.py),
checked 2026-10-15, skips PYTHON_COLORS when environment handling is disabled,
then checks NO_COLOR before FORCE_COLOR. Actual Python 3.14.6 execution with
`NO_COLOR` unset and `FORCE_COLOR=1`, through `python -I -m pytest`, reproduced
the existing help test failure: **1 failed, 29 deselected**, with ANSI escapes
around the positional wheel text. This does not affect the product CLI or the
documented ordinary pytest/CI command. The bounded correction adds test-local
`NO_COLOR=1` alongside `PYTHON_COLORS=0`, restoring both via monkeypatch and
retaining every help assertion. No new runtime code or duplicated test is needed.

After correction, the complete help-test file passes **30 cases** on Python
3.12.13 and 3.14.6, including an actual 3.14 `-I` run with FORCE_COLOR=1 and
NO_COLOR unset in the caller. A targeted 3.14 `-E` run also passes. The test adds
one line and no cases; source and archive suites remain **706 tests each**.
Both interpreters pass those full suites, authoring/generator/diff checks,
the 53-test-reference/27-export checks and all four installed-wheel paths.

| Interpreter | R10 follow-up sdist SHA-256 | R10 follow-up rebuilt wheel SHA-256 |
| --- | --- | --- |
| 3.12.13 | `1e54c0bce7ef33fd92924d15433d4d2eb6c022e7e15d1e0881b2352ebc38eb0d` | `6da2f93d198a8a0b0f36b72d5f76f8eacea4492d31d97d30af4a7d2df2e72b88` |
| 3.14.6 | `53e02dd8b830f83d03f86f8c679b0c931281058c118f2f0ad9b3dbd8660b1496` | `7ea335e104c772cdbde43ee4764fd4d9ba369fd4fae0f4594e3f1de08b781e4d` |

Raw observations and cleanup receipts are retained in `final-{3.12,3.14}-r4/`
under the same owner evidence root; focused reproduction is in
`r10-followups/help/`. These hashes identify measured builds before this
documentation-only recording. No runtime/test/asset changed afterward. Native CI
will build the exact resulting commit independently. Its result and the fresh
full review are recorded externally with the frozen head and draft PR.

## R11 outcome and reference closure

R11 `20261014-lib-spec-r11-63f374` completed AGREED on
`c7bf2bc2bcacfa3fa9c2d4b28cc8e58986a7c072`, digest
`0a1809391f7eea7445c0afa918a135de19a7bb2d9155d01c99adf02f4b0f757a`.
All three required reviewers returned SAFE TO MERGE; Sol, Argon and the separate
Astra comparison had no actionable finding. Opus identified one Minor: the C68
case-map reference used a bare `test_spec_records.py` path even though the map
defines bare filenames as `tests/` paths. The actual function belongs to
`spec/tests/test_spec_records.py`; the reference now includes that prefix.

[Native CI run 38595740079](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38595740079)
passed all four jobs on the reviewed head: each passed 706 source and 706
unpacked-sdist tests, interpreter assertions, authoring/assets, wheel rebuilding
and all four installed-wheel checks. Actual Python versions were macOS
3.12.10/3.14.7 and Ubuntu 3.12.15/3.14.8. R11 was exported and its exact owned
roots cleaned after every reviewer and producer reached terminal state.

The owner authorized further verified quality corrections on 2026-10-15. A
separate read-only AST audit checked the other 94 explicit file-qualified test
references across the case and conformance maps: 93 exact function names and
one intentional C32 wildcard matching six definitions. All resolve under the
maps' documented conventions; no additional missing or misassigned reference
was found. This checks reference identity, not semantic coverage, unqualified
shorthand, runtime behavior or every host-owned requirement. The audit imports
no candidate code and is external verification, not a new repository framework.
Commands, source hashes and per-reference definition locations are retained in
the owner evidence under `_runs/reviews/20261015-lib-reference-closure/audit/`.

Only the reference and progress records change in this follow-up. Post-correction
verification passes all 95 references, including corrected C68 (94 exact names
and one wildcard, across 17 files). Local Python 3.12.13 and 3.14.6 each pass
706 source and 706 unpacked-sdist tests, authoring/assets, diff checks and all
four installed-wheel paths. Commands, terminal results, artifact hashes and
successful owned-stage cleanup are retained in `final-{3.12,3.14}-r5/` under
the earlier Python follow-up evidence root; the corrected-reference receipt is
under `20261015-lib-reference-closure/post-fix/`. These builds precede this
documentation-only result recording; runtime/tests/assets are unchanged.
The resulting commit requires its own native CI and full review with the same three required
entries, separate Astra comparison, 2400-second budgets and current official
web authorization. Those outcomes are recorded externally after source freeze;
no earlier approval or platform result transfers to the new snapshot.
