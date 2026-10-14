# R12 quality follow-up verification

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
