# Python 3.14 and R8 follow-ups

The owner authorized all three nonblocking R8 follow-ups, regression tests,
Python 3.14 verification and a fresh complete review. R8
`20261014-lib-spec-r8-a49108` completed `AGREED` on `00ed792`; that approval does
not transfer to changed bytes. Its required Opus/Sol/Argon entries and separate
Astra comparison remain the selected profile, each with a 2400-second budget.

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
