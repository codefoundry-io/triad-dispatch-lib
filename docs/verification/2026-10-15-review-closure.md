# Quality follow-up verification

The owner authorized continuing verified quality corrections to convergence.
R12 `20261015-lib-spec-r12-9cedd4` reviewed `8ceaa7d10a199339cbac1a1e51fad4b7f593288a`
with digest `b8ca95d1c4318a780bae77f80d63d357f6a4b15f732d68341efc06f59e907f94`.
All three required entries completed SAFE TO MERGE; the collector returned
AGREED with no missing entries or selection deviations. Sol reported one Minor,
Opus two, and Argon none. The separate Astra comparison found no actionable
defect. All producers were terminal before canonical export and cleanup.

## Receipt observation before request publication

Sol identified a neighboring Python 3.14 error boundary in the repository-only
native driver: the receipt-reuse predicates before request publication still
suppressed filesystem errors. Actual Python 3.14.6 syscall injection reproduced
both EIO and EACCES failures: a queued leg's premature receipt did not prevent
request publication. The test drained any wrongly published request before its
assertions, preserving custody even in the failing experiment.

The check now uses `lstat()`, treating only `FileNotFoundError` as absence.
Other errors fail that callback before request publication. The existing queued
receipt regression adds EIO/EACCES variants; all three cases pass on Python
3.12.13 and 3.14.6. The complete native-driver file passes 71 tests on each.
No library API, provider behavior, terminal acknowledgement or cancellation
contract changes. Focused logs and exact commands are retained under the owner
evidence directory `20261015-lib-reference-closure/r12-receipt-prepublication/`.

The final queued-receipt regression waits for an event emitted by the injected
syscall failure, rather than assuming the queued callback ran within a fixed
delay. It still disarms and drains any wrongly published RED request before
asserting the no-publication contract.

## Related file-preservation boundaries

The leader's same-class audit found another native-driver use of suppressing
predicates in `atomic()`. Actual Python 3.14.6 EIO injection replaced an existing
destination; Python 3.12.13 raised before writing. The minimal correction uses
the same non-following `lstat()` absence rule before creating a temporary file.
Six refusal cases cover regular/dangling destinations with no fault, EIO or
EACCES; one case preserves successful publication to an absent destination.
Before correction, Python 3.14 failed four overwrite assertions and passed the
three normal cases. After correction, all seven pass on both interpreters.
The native-driver suite then passes 78 cases on each. This preserves the
existing reuse-refusal contract; it adds no locking or concurrent-writer policy.

A separate bounded generator experiment reproduced suppression of link-status
errors on Python 3.14, allowing an output symlink's target to be overwritten.
The same EIO/EACCES experiment on Python 3.12 refused before writing. The
generator now observes link status with `lstat()` and checks `S_ISLNK`; only
missing components are skipped so initial output creation remains supported.
The source-tree scan uses that same check. Eight regressions cover source/output
links, read/write modes and both errno values: all eight fail on old Python 3.14
behavior, and the corrected 44-case asset suite passes on both interpreters.
Existing outside-sentinel, deterministic-byte and missing-input tests remain.

The output-root status-error control already raised before changing files
through directory creation, so it did not justify a separate implementation
change. Generator observations and commands are under the owner evidence
`20261015-lib-reference-closure/r12-assets-diagnosis/`; all reproduction files
were task-owned temporary fixtures. Canonical payload bytes remain unchanged.

## Coverage-map references

Opus found that the C12/C14 canonical schema wildcards were unqualified. The
map now explicitly names `spec/tests/test_schemas.py::test_c12_*` and
`spec/tests/test_schemas.py::test_c14_*`, matching the existing C32 pattern style.
C68 remains qualified as corrected in the preceding round.

An independent external AST audit resolves **184 references**: 97 file-qualified
and 87 in-cell shorthand references across the case and conformance tables.
There are 181 exact names and three wildcard occurrences, covering 107 unique
references in 17 files. All pass, with no missing or ambiguous target. File
context resets per cell/row. Six prose shorthand references outside tables are
recorded as outside this audit, without guessed file context. This establishes
reference identity, not semantic completeness or runtime coverage. The checker
imports no candidate code; it adds no permanent repository framework.
Commands, per-reference definitions and hashes are retained under
`20261015-lib-reference-closure/r12-map-audit/` in the owner evidence.

## Native CI source identity

Opus correctly distinguished a run's PR-head metadata from its actual checkout.
The previous workflow used the default PR merge ref. The four runs below each
checked out a merge commit whose tracked Git tree equals the reviewed head's
tree. Their test results remain valid for those tracked contents, but previous
"exact-head" wording must not be read as proof of checkout of the head SHA.

| Review / CI run | Reviewed head | Actual checkout | Equal tracked tree |
| --- | --- | --- | --- |
| R9 / 38586758282 | `6f790f6` | `69a901ad410d7d0602a158ab63732311032596b3` | `306dde0fd0431cefb0755bb076ec3a60faa28d1f` |
| R10 / 38591880134 | `3ad33e8` | `4a837fffd9ef5d6b5e50ad55a6a3ecfd8a7ab887` | `fb7c20205e61cd2afc5236357fad772653bee8a3` |
| R11 / 38595740079 | `c7bf2bc` | `20a15dac9835e265c89d99e47c3bd8dcfcf38736` | `75d2ab2a8744c6c89cf3e81b239b6a65a37b4aaf` |
| R12 / 38604433269 | `8ceaa7d` | `939afa9eed46ac2d9bd7bf3a59e62527503380cc` | `4d002b954365cf614f1215e99d83103f59689fe9` |

All four jobs per run have matching checkout observations. GitHub commit objects
confirm tree equality and parents; the common base is
`c6dd9819a22ac5d20575802969ecbd47752615ef`. R9 retains 704 source/archive tests
per job; R10–R12 retain 706 each, with their recorded installed-wheel checks.
No rerun or broader historical equivalence is inferred. Original records remain
unchanged; supplemental logs/API objects are under
`20261015-lib-reference-closure/r12-ci-binding/` in the owner evidence.

The workflow now explicitly selects `github.event.pull_request.head.sha`, with
`github.sha` for push events, and asserts the actual checked-out SHA before
tests. It logs both commit and tree. The four platform/interpreter jobs and
read-only token permission remain unchanged. This makes later exact-head
claims depend on the observed assertion, not run metadata alone.

Official references checked on 2026-10-15:

- [Python 3.14 pathlib status queries](https://docs.python.org/3.14/library/pathlib.html#querying-file-type-and-status)
  document suppression of `OSError` by file predicates.
- [GitHub pull_request events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request)
  document the default merge-ref identity.
- [Official checkout head-commit example](https://github.com/actions/checkout#checkout-pull-request-head-commit-instead-of-merge-commit)
  demonstrates explicit PR-head selection.

## Completion boundary

Local macOS ARM64 verification passes **723 source and 723 unpacked-sdist tests**
on both Python 3.12.13 and 3.14.6. Both pass authoring, canonical-asset, diff and
interface checks plus all four installed-wheel paths. The final table-reference
audit still resolves all 184 references. Raw logs, commands, artifact hashes and
successful owned-stage cleanup are retained under `final-{3.12,3.14}-r6/` in the
owner's earlier Python follow-up evidence root; final reference receipts are in
`20261015-lib-reference-closure/r13-map-audit/`. These builds precede this
documentation-only result recording; runtime, tests and assets are unchanged.

The corrected snapshot still requires native CI on its actual SHA and a fresh
complete review. Those results are
recorded externally after source freeze. The selected Opus/Sol/Argon profile,
separate Astra comparison, current official web authorization and 2400-second
budgets remain unchanged. Synthetic tests do not establish actual native backend
termination, provider settings, consumer adoption, publication or installation.

## R13 directory inventory and regular-file diagnosis

R13 `20261015-lib-spec-r13-dcf36d` reviewed `d9d0055ec67a6465342acb1f09bc2c1dbe0716c5`
with digest `576e4f23d525b0b16dfa7b74057404ce1da50aba8e7c9385ee5f1e23dd0b763c`.
All required entries completed; Sol returned MERGE WITH FIXES, Opus and Argon
SAFE TO MERGE. Collection was BLOCKED with no missing entries or selection
deviations. The separate Astra comparison independently found the same generator
issue as Sol and Opus. Original outputs, terminal observations and canonical
export remain in the owner's R13 evidence; all review roots were cleaned.

[Native CI run 38608784436](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38608784436)
asserted actual checkout of `d9d0055` in all four jobs, with tracked tree
`483d331f3c04b09a201e39e1f4684d7ab7cc1d50`. Each passed 723 source and 723
archive tests plus four installed-wheel paths. macOS 15 ARM64 used Python
3.12.10/3.14.7; Ubuntu 24.04 x86_64 used 3.12.15/3.14.8. Those passing tests
did not cover the newly identified scan-error boundary.

The generator's `rglob()` scan suppresses directory-enumeration failures.
An expected output symlink omitted by that scan reaches following occupancy
checks and `write_bytes()`. External experiments on actual Python 3.12.13 and
3.14.6 reproduced this with EACCES/EIO injection. A nested directory with mode
0300 also reproduced an outside-sentinel overwrite under the ordinary local
account on both interpreters. Only task-owned fixtures were used; permissions
were restored before cleanup. Check mode could refuse later for byte drift,
but that does not establish complete inventory validation.

Opus also proposed hardening `regular()` against a non-following metadata fault.
Independent diagnosis confirmed that Python 3.14 suppresses the injected errno
in both `is_symlink()` and non-strict `resolve()`, after which following file
checks and reading return the target bytes. Python 3.12 refuses at the first
predicate. Ordinary files pass and ordinary links are refused on both versions.
This is a split syscall-fault model, not evidence that an ordinary permission
mode produces different lstat/stat access or that a live provider was affected.

Both corrections restore existing contracts: validate the whole inventory before
writing, and refuse links or failed metadata observation before reading. They
do not introduce concurrent-writer containment, a new public API or a provider
mechanism. Focused and integrated results are recorded below after verification.

Official references checked on 2026-10-15:

- [Python 3.14 pathlib glob behavior](https://docs.python.org/3.14/library/pathlib.html#pathlib.Path.rglob)
  explains directory-scan error suppression.
- [Python 3.12 pathlib traversal](https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.walk)
  distinguishes ignored scan errors from explicit error propagation.

### R13 correction results

The generator now traverses with explicit `os.scandir()` and each child's
non-following `lstat()` mode, rejecting links before descent and propagating
enumeration/status errors. Output classification reuses that observed mode.
Thirty-two injected scan cases cover source/output root/nested directories,
link/extra-file fixtures, check/write modes and EACCES/EIO. Two further tests
exercise mode 0300 directly and restore permissions in `finally`; they skip
only for accounts that can still list the directory. Both ran here. All 34
fail on frozen original code; the corrected asset file passes 78 cases on both
interpreters. Existing initial-generation and byte-preservation tests remain.

The native driver now observes link metadata through `lstat()` before reading.
Its narrow ELOOP normalization preserves the existing canonical-file ValueError;
other OSError values propagate. The three new ordinary-link/EIO/EACCES cases
include a regular-file success control. Python 3.14 RED is two failures and one
pass; focused GREEN is 14 on each interpreter, including existing cyclic-path
and custody cases. The complete native file passes 81 tests on each interpreter.
Detailed commands, original/corrected fixtures and cleanup receipts remain under
`20261015-lib-reference-closure/r13-generator-scan/` and
`20261015-lib-reference-closure/r13-regular-diagnosis/` in the owner evidence.

Integrated local macOS ARM64 runs on Python 3.12.13 and 3.14.6 each pass **760
source and 760 unpacked-sdist tests**, authoring/generator checks, interface
checks and all four isolated installed-wheel paths. The external AST audit
still resolves all 184 scoped table references. Production changes total
+27/-7 (net +20); tests add 101 lines and 37 cases. Shared library code, payloads,
dependencies and default interpreter are unchanged.

Raw integrated logs, commands, artifact hashes and successful cleanup are in
`final-{3.12,3.14}-r7/` under the owner Python follow-up evidence root; current
reference receipts are in `20261015-lib-reference-closure/r14-map-audit/`.
Both local rebuilt wheels have SHA-256
`ec62ab3a2816dc50473ed4ff48dc9c42c555f27d903de76cdda6635b39022955`.
These measurements precede this documentation-only result recording. The new
committed snapshot still needs actual-head native CI and a complete fresh review,
recorded externally after freeze; R13 approval is not inferred.

### Canonical ancestor observation follow-up

Before starting the next review, the leader checked the same metadata boundary
at a symlinked ancestor. On both Python 3.12.13 and 3.14.6, final-leaf `lstat()`
succeeds while injected EIO/EACCES on an ancestor is suppressed by non-strict
resolution. The resulting unchanged alias path incorrectly passes the canonical
path comparison and allows target bytes to be read. Ordinary canonical files
pass and ordinary aliases are refused; fixtures remain unchanged and are removed.

Strict resolution raises the original ancestor error on both interpreters.
The bounded follow-up therefore uses `resolve(strict=True)` in `regular()`;
final-leaf observation already requires an existing file. Existing absolute-path,
link, file-type and ELOOP refusal behavior remains. This is the same injected
fault model, not an observed permission-only layout or live-provider incident.
The earlier 760-test measurements belong to the preceding snapshot. New
regression and integrated results follow below; no R14 review started on it.

The existing metadata-failure test now covers final-link and ancestor-link paths.
In the ancestor variant it explicitly confirms that leaf metadata is available
while the ancestor fault is armed. Both interpreters reproduce two failing
ancestor cases before correction; the six variants plus existing ancestor-loop
case pass afterward. The complete native file passes 84 cases on each version.
The follow-up adds one changed production line (+1/-1) and three test cases
(+12/-4 test lines). Its report and raw evidence are retained in
`r13-regular-diagnosis/ancestor-correction-report.md` beside the original diagnosis.

Final local runs each pass **763 source and 763 unpacked-sdist tests**, authoring,
generator, interface checks and all four installed-wheel paths on Python 3.12.13
and 3.14.6. The final table-reference audit still resolves 184 references.
Logs, commands, hashes and successful cleanup are in `final-{3.12,3.14}-r8/`;
reference receipts are in `20261015-lib-reference-closure/r14-final-map-audit/`.
These measurements again precede only their documentation result recording.

Intermediate [CI run 38612676070](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38612676070)
tested the preceding `f9f03677845550d36cf14a2ae2421f4491577fa6` exactly. All four
jobs passed 760 source/archive tests with no skips and all four wheel paths.
This remains useful evidence for that commit, but does not cover strict ancestor
resolution. Final committed CI and R14 outcomes are recorded externally after
source freeze; no result is transferred from the intermediate candidate.
