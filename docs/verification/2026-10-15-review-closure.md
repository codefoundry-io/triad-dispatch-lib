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

## R14 output-root and canonical-input boundaries

R14 `20261015-lib-spec-r14-aa4570` reviewed `0e7375c0feda9e397af9ecf5f5254b562bad7aaf`.
All three required results were COMPLETE: Sol requested fixes, while Opus and
Argon returned SAFE. Collection was BLOCKED, with no missing entries or
selection deviations. Separate Astra had no vote. Original results, parent
custody, runtime observations and adjudication were exported before owned
temporary roots were removed. Opus took approximately 795 seconds and Argon
479 seconds; both stayed within their 2400-second budgets. Native effective
model identity and usage remain unexposed.

Exact-head [CI run 38613737116](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38613737116)
passed all four jobs, each asserting head and tree identity and passing 763
source/763 archive tests without skips, authoring/generation checks and four
installed-wheel paths. This verifies the R14 candidate; it does not cover later
corrections or replace review findings.

The remaining generator gate uses a following `data.exists()` predicate before
inventory. Python 3.14 can suppress its status error, skipping the entire scan.
A persistent root-status error can still make later directory creation refuse,
as the earlier control measured. A one-shot error can recover before that call;
check mode can also accept unexpected inventory when all expected bytes match.
These distinct triggers require focused reproduction before assigning impact.
Sol, Opus and Astra independently identified this boundary.

Context preparation and native run-parent validation also retain non-strict
resolution. Astra, Opus and a separate read-only audit identify the same
ancestor-observation fault model already measured for `regular()`. The required
ordering is canonical validation before packet reads or run creation. Later
strict prompt validation does not undo earlier file creation. No final request
publication or false agreement is inferred from this path.

The five-tool audit distinguished these existing-contract gaps from allowed
wheel aliases, lexical import checks and predicates whose failure already
refuses the operation. No new general path grammar or concurrency guarantee
is introduced. The conformance map also gains missing links to generator
scan/status and native regular-file regressions, plus the new boundary tests.

Current [Python 3.14 pathlib documentation](https://docs.python.org/3.14/library/pathlib.html)
was checked on 2026-10-15. It documents predicate error suppression and strict
resolution. Split syscall faults below remain injected diagnostic evidence,
not an observed permission-only layout or real-provider incident.
Measured correction results are recorded below after execution.

### R14 correction results

Original generator experiments on Python 3.14.6 reproduced sentinel overwrite
with one-shot EIO/EACCES and false check-mode success with both one-shot and
persistent faults. Persistent write faults instead produced a later
FileExistsError, preserving bytes but losing the original errno. Python 3.12.13
propagated the original error in all cases. The correction uses root `lstat()`
mode and only FileNotFoundError for absence, retaining the existing walker.
Twelve regressions cover those faults and missing/occupied root controls:
original 3.14 has 8 failures/82 passes, corrected asset suites pass 90 on each
version, and the focused 12 pass on each. Original 3.12 already passed all 90.
The corrected external following-stat probe no longer reaches that observation;
separate regression injection proves error propagation at the new lstat gate.

Context and native-parent regressions reproduce reading packet bytes or creating
run artifacts through aliases when non-following metadata faults are suppressed.
Original focused results were 6 failures/8 passes on Python 3.12 and 8 failures/6
passes on 3.14; ordinary aliases were already refused. The correction uses strict
resolution for existing worktree, packet and run-parent paths. Context handling
normalizes only ENOENT, ENOTDIR, ELOOP and the older cyclic-path RuntimeError to
its existing ValueError diagnostics; EIO/EACCES propagate. Existing controls
cover normal inputs and cyclic paths. Sixteen added cases cover three context
alias positions, missing/nondirectory context paths and native run-parent
refusal before creation. These are repository helper tests, not provider runs.
The complete two affected driver files pass 133 tests on each interpreter;
focused GREEN passes 26 on each before the two nondirectory controls were added.

Production changes total +18/-5 (net +13) across three tools; tests add 183 lines
and 28 cases. Canonical runtime payloads, shared APIs and dependencies are
unchanged. The conformance map now points to all preceding and new scoped
regressions. Its fresh external AST audit resolves 193 occurrences (116 unique
test references across 17 files); six existing prose shorthands remain explicitly
introduced by their owning filename and outside that automated audit.

Exact original/corrected logs, commands and cleanup receipts are retained under
`20261015-lib-reference-closure/r14-output-root/` and `r14-context-parent/`;
the reference receipt is `r15-map-audit/`. Integrated measurements follow below.

Integrated local macOS ARM64 runs on Python 3.12.13 and 3.14.6 each pass **791
source and 791 unpacked-sdist tests**, authoring/generator/interface checks and
all four isolated installed-wheel paths. Commands, logs, hashes and successful
owned-stage cleanup are in `final-{3.12,3.14}-r9/` under the Python follow-up
evidence root. These measurements precede this documentation-only result
recording. Actual committed-head native CI and the fresh review are recorded
externally after freeze; no earlier approval transfers.

## R15 authoring reference and run-parent diagnostics

R15 `20261015-lib-spec-r15-d50127` completed AGREED on
`10f179504b31b2da4c5e088399139fed094ea723`. All three required entries were
COMPLETE and SAFE, without missing entries or selection deviations. Sol
reported one Minor; Opus one Minor and one hardening suggestion; Argon none.
Separate Astra reported the same authoring gap as a P2 without a vote.
Original verdicts, runtime observations and parent custody were exported before
owned roots were removed. Opus took approximately 758 seconds and Argon 399;
both remained within 2400 seconds. Native effective identity stays unexposed.

[CI run 38617685314](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38617685314)
asserted the exact head and tree in all four native jobs. Each passed 791 source
and 791 unpacked-sdist tests without skips, authoring/generation checks, rebuild
and all four installed-wheel paths. Actual Python versions were macOS 3.12.10
and 3.14.7, Ubuntu 3.12.15 and 3.14.8. These results belong to the R15 candidate.

The offline authoring checker still uses a suppressing link predicate before
reading local references. Its documented contract forbids reference traversal
through symlinks. The proposed lstat correction must retain missing-reference
error lists while refusing genuine observation errors before a target read.
This applies to document/anchor and catalog consumers of the same helper; no
runtime library agreement or generator bypass is inferred. A separate audit
of all 12 remaining production modules found this one no-link contract gap.
Flat empty map discovery already fails, and runtime resource abstractions
promise content validation rather than general filesystem link containment.

The native run-parent check already refuses following status errors before
creation, but Python 3.14 converts EIO/EACCES into a misleading canonical-path
ValueError where Python 3.12 retains the original error. This is diagnostic
parity, distinct from the earlier validation bypass. Reordering strict
resolution alone does not cover an error confined to the subsequent following
status query; the type observation must also preserve genuine errors while
retaining existing missing/nondirectory/cyclic-path diagnostics.

Current official [Python 3.14 pathlib documentation](https://docs.python.org/3.14/library/pathlib.html#querying-file-type-and-status)
and [CPython v3.14.8 source](https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/pathlib/__init__.py)
were fetched during the review on 2026-10-15. The authoring split-fault scenario
still requires focused reproduction; it is not an observed ordinary permission
layout or provider incident. Correction measurements follow below.

### R15 correction results

Actual Python 3.14.6 authoring tests reproduced target reads and no validation
errors for all four leaf/ancestor EIO/EACCES cases. Python 3.12.13 preserved
the original errors and read nothing. Component lstat/mode checks now refuse
before reading, with FileNotFoundError/NotADirectoryError preserving existing
missing-reference diagnostics. A subsequent following-only type query also
reproduced misleading missing-file errors on 3.14; explicit stat/mode preserves
the original errno. Neither version read target content in that diagnostic-only
variant. The final authoring file passes 36 cases and the actual checker reports
one valid map on both versions. Ten new cases include canonical/missing controls.

Native parent status injection first reproduced two lost-errno failures on
Python 3.14, while all three new cases passed on 3.12. The same bounded check
then reproduced six diagnostic failures across final regular-file, context-root
and context-packet type observations on 3.14; their three ordinary controls pass,
and 3.12 already passes all nine. These paths already refused access and created
no run artifacts; the correction preserves the reason for refusal. Existing
following queries now use stat/mode classification, with no extra queries or
new path grammar. The parent retains narrow missing/nondirectory/cyclic error
normalization. Final focused GREEN passes 37 cases on each interpreter, including
existing alias and cyclic-path controls.
The two affected driver files pass 145 tests on each interpreter. The updated
AST reference audit resolves 198 occurrences (121 unique test references in
18 files), retaining the six documented prose exclusions.

Production changes total +17/-6 (net +11) across the authoring and two smoke
tools; tests add 148 lines and 22 cases. Shared runtime APIs, generated payloads,
dependencies and host ownership are unchanged. Raw original/corrected evidence,
commands and owned cleanup receipts are retained in
`20261015-lib-reference-closure/r15-authoring-ref/` and
`r15-run-parent-diagnostic/`. Conformance links include the new regressions.

Integrated local macOS ARM64 runs on Python 3.12.13 and 3.14.6 each pass **813
source and 813 unpacked-sdist tests**, authoring/generator/interface checks and
all four installed-wheel paths. External `final-{3.12,3.14}-r10/` records exact
commands, logs, artifact hashes and successful owned-stage cleanup; the current
reference receipt is `r16-map-audit/`. Both rebuilt wheels have SHA-256
`b3123bfce42e03e3bb0de945b37e5ab40265e4b36583da7ba563ec5827db79df`.
These measurements precede only this documentation result recording. Actual
committed-head CI and the next full review remain external post-freeze evidence.

## R16 CLI interruption and portable preflight

R16 `20261015-lib-spec-r16-b81fbc` completed AGREED on
`89504bef340b45c4852b530e8f3aebbfe0fa4c19`. All three required entries were
COMPLETE and SAFE, with no missing entry or selection deviation. Sol and Argon
reported no findings; separate Astra reported no actionable defect. Opus retained
one Minor and two hardening suggestions. Originals, host receipts and runtime
observations were exported before all owned review roots were removed.

[CI run 38621985362](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38621985362)
asserted that head and tree `6a9fd0bf7b2578a57d8593ba50d646e91e5a5f0a` in all
four Ubuntu/macOS Python 3.12/3.14 jobs. Each passed 813 source and archive tests,
without skips, and all four installed-wheel paths. Those results belong to the
R16 candidate and do not approve later corrections.

The native CLI's outer installed-wheel process uses `subprocess.run`; on an
operator interrupt this may terminate the inner driver while it awaits a
synthetic parent's terminal acknowledgement. Existing in-process cancellation
tests do not establish the outer CLI guarantee. The root checked current
[CPython subprocess source](https://raw.githubusercontent.com/python/cpython/3.14/Lib/subprocess.py)
and [asyncio interrupt handling](https://docs.python.org/3.14/library/asyncio-runner.html#handling-keyboard-interruption)
on 2026-10-14 UTC. Actual subprocess reproduction and correction measurements
follow; these sources alone do not demonstrate a real provider incident.

Generator following-type/presence checks also retain Python-version-dependent
error suppression after the prior non-following inventory fixes. External
split-syscall tests on Python 3.14.6 reproduce 14 misleading refusal diagnostics
and eight suppressed one-shot errors at sibling presence checks. Four of the
latter return success in check mode; four write the authorized changed canonical
bytes. Python 3.12.13 preserves the original errno in all 22 scenarios. These
are static canonical layouts and injected errors, not a symlink escape or
concurrent-writer experiment. The correction must preserve fresh observations,
their short-circuit order and existing missing-path diagnostics.

The driver also maps exact-case entry names directly to directories; case-only
names can collide on case-insensitive filesystems. A portable driver-only
preflight refusal is proposed, without changing shared roster identity. Exact
RED/GREEN results, commands and cleanup receipts are retained under
`20261015-lib-reference-closure/r16-native-cli/` and
`r16-generator-diagnostics/`. New code requires fresh integrated verification
and a complete independent review.

### R16 generator correction results

A small uncached following-mode helper preserves every original observation and
short-circuit, including separate presence and type checks. Only missing or
nondirectory path errors become the prior false result; other errors propagate.
The production change is +11/-4 (net +7), and 52 test lines add 26 cases.
Original Python 3.14 has 22 failures/94 passes; Python 3.12 passes all 116.
Corrected full asset suites pass 116 on both versions, actual generator checks
exit zero, and all 22 external fault scenarios per interpreter preserve the
original errno and output bytes. Existing absence, occupied-path, drift and
initial-generation controls remain covered. All eight owned test environments
were removed and every command reached a consumed terminal result.

### R16 native CLI correction results

Actual outer CLI runs on Python 3.12.13 and 3.14.6 reproduce premature process
and environment cleanup before a synthetic acknowledgement delayed by 0.8 seconds.
PID-only SIGINT produces no cancellation notice; process-group SIGINT produces
the notice but still loses custody before acknowledgement. Normal wheel-install,
identity and exchange controls exit zero. An actual case-insensitive APFS fixture
also reproduces the case-only name collision after the first prompt is created
but before any request is published.

The driver now isolates the inner process, installs a temporary non-raising
SIGINT handler before child creation, and forwards the first pending interrupt
once. Reentrant interrupts cannot abort forwarding. It restores the prior handler
after terminal wait and retains the installed environment throughout. Cooperative
outer interruption exits 130; normal exit codes remain propagated. Case-only
names are refused during driver preparation; a regression separately confirms
the shared roster still accepts distinct exact-case identities.

Four real outer/inner interrupt regression variants and the name case failed
before correction, while normal/error controls passed. A separate deterministic
test reproduces interruption during child publication and exercises reentry at
the forwarding boundary. Final focused GREEN passes eight cases on each Python
version. These subprocess tests substitute only the installation bootstrap with
a copied installed runtime. Separate actual-wheel CLI replay on both versions
confirms cancellation publication, live child/environment before acknowledgement,
terminal cleanup afterward, no cancelled report and exit 130. Those replays use
a retained unpublished dev3 wheel; they verify the changed repository driver,
not a newly built package or a real backend. Exact rebuilt-package measurements
follow in integrated verification. Forced process death remains outside the
cooperative guarantee.

The complete native file passes 101 tests on each interpreter. Its production
change is +29/-2, with 221 test lines and eight cases; the generator adds
26 cases, for 34 total new regressions. Test failure cleanup also resolves
the exact recorded isolated child before fixture teardown. All six actual
outer/inner replay processes and their environments are gone; this task did
not signal any provider or unrelated process.

Integrated local macOS ARM64 measurements pass **847 source and 847 unpacked-sdist
tests** on each of Python 3.12.13 and 3.14.6. Authoring, generator, diff and API-map
checks plus all four isolated installed-wheel paths pass. Both rebuilt wheels
have SHA-256 `1ec8bb18b2925e372d29ffa23ef778c12e59631c9b67c742cca884b283dd24ae`.
Exact commands, logs, sdist hashes and successful owned cleanup are in
`final-{3.12,3.14}-r11/`. The fresh `r17-map-audit/` resolves 203 occurrences
(126 unique references in 18 files), retaining the six documented prose
exclusions. These measurements precede only this documentation result update;
actual committed-head native CI and the fresh full review are external evidence
recorded after freeze. No previous approval transfers to the changed bytes.
