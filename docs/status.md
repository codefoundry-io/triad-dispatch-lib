# Current status

Updated: 2026-10-15

## Owner decisions

- Develop the common library in public `codefoundry-io/triad-dispatch-lib`.
- Write the design and implementation plan, then proceed.
- Preserve host-owned native execution and the shared specification authority.
- Consolidate the shared specification with this library; keep Claude and Codex
  distribution independent and record their adoption separately.
- Support configurable Codex, Claude, Gemini CLI and AGY entries, including all
  four together. The Codex-first tests do not limit the product's supported scope.
- Keep implementation and integration tests in this library repository; existing
  consumer repositories remain read-only references until their separate ports.
- Preserve the existing Gemini workaround. The owner reports that 0.63.0
  non-interactive plan execution did not work adequately and has no available
  verification path; do not replace or retest that path as part of this work.
- Exclude MCP-based implementation candidates. Keep `openai-codex` as a deferred
  TODO after authentication/file-access research; spike the other CLI candidates
  here without adopting new runtime defaults.
- Trial this project's reviews with Argon/high, Sol 6.1/xhigh and Opus 5.5/xhigh
  as three required entries, plus a separate Astra/high comparison without a
  vote. This is a project override, not a host-distribution or workspace default.
  See [review profile](review-profile.md) and its separate setup evidence.

## Current adoption-observability slice (2026-10-15)

Library PR #1 merged at `9489543ee24f338e9c6d0e3b032a1aa389986429`, with the
reviewed `2d1e62e7` tree unchanged. Codex PR #44 merged and independently
released v0.2.561 using vendored library dev3. Claude adoption remains planned;
its PR #2 scratch measurements are attributed and lack published reproducible
evidence. Older candidate/no-adoption statements below describe their dated slices.

The owner approved PR #2 corrections and additive L2/L7 development. The
[design](design/2026-10-15-adoption-observability.md) and
[plan](superpowers/plans/2026-10-15-adoption-observability.md) bound this dev4
slice to safe admission locations, optional clause manifests and adoption docs.
L10 keeps existing dependency floors; L11/L12 clarify selective use. Other
requests remain design work. No consumer or provider defaults change.
The [local verification record](verification/2026-10-15-adoption-observability.md)
records 952 source and 952 archive tests on each of Python 3.12/3.14, all four
installed-wheel drivers and new API probes. Concurrent Claude documentation
amendments are preserved: four-function first slice, expanded L2 issue #3, L13
issue #4 and boundary decisions issue #5. This bounded L2 does not fully satisfy
issue #3. Current exact-head CI/formal outcomes are retained with PR #2 after
freeze; earlier approval does not transfer to changed bytes.

R1 (`20261015-lib-observability-r1-fcb113`) completed `BLOCKED` on `2eff9d0`
after all four native CI jobs passed 952 source/archive tests and four wheel
drivers. Five verified documentation findings now receive bounded corrections:
README/migration adoption status, exact schema diagnostic-path semantics,
exception-internal privacy limits, and historical/released B wording. No runtime,
schema, prompt or dependency changes result. See the
[R1 record](verification/2026-10-15-adoption-observability.md#r1-documentation-corrections).
The exported round's votes do not transfer; new exact-head CI and complete
Opus/Sol/Argon review with separate Astra comparison follow the corrected bytes.

## Project review setup

Shared specification and implementation authoring already lives in this
repository. The Codex host has a separate source-adoption candidate; the earlier
statements below about no host adoption describe release/installation boundaries,
not the absence of that candidate. Claude's port remains separately owned.
This project profile uses existing Codex host v2 configuration and does not move
provider execution or model defaults into the shared library implementation.
The project roster is installed locally. Source/installed host resolution and
provider-free adapter preparation pass; 64 focused tests and fresh Sol/Astra
instruction probes pass. See [setup evidence](verification/2026-10-14-review-profile.md)
for identities and limits. Those setup probes are not formal review evidence.

## Review corrections (2026-10-14)

The first complete project review, `20261014-lib-spec-r1-5754af`, admitted all
three required results and ended BLOCKED: Sol requested fixes; Opus and Argon
approved. Separate Astra comparison independently found the cancellation defect.
The owner approved both reproduced corrections and the adoption/documentation work.

The native test driver now waits for terminal acknowledgement even if publishing
cancellation fails. The shared coordinator reaps a created callback when wait setup
raises, including an overflowing timeout. Regression cases cover these
paths; canonical schemas, dependencies and provider defaults are unchanged.
The [conformance map](../spec/reference/library-conformance.md) and
[adoption contracts](host-adoption.md#required-adapter-contracts) identify AGY
recovery, host-fault and unextracted classifier responsibilities.

All project review entries now allow 2400 seconds, with the same parent-observed
Astra budget. Current verification and re-review evidence belongs to this
correction snapshot; the 633-test consolidation results below remain historical.
See [correction verification](verification/2026-10-14-review-corrections.md)
for the measured results, review dispositions and platform limits.

The complete R2 review, `20261014-lib-spec-r2-917b20`, remained BLOCKED: Sol
found a neighboring malformed-receipt custody path; the separate Astra review
found timestamp overflow escaping cleanup. Both original corrections were
confirmed. The follow-up preserves a published request until valid terminal
acknowledgement, retains first-refusal evidence, and separates terminal custody
from response admission. These changes remain in repository test support.
The pre-R3 correction source and unpacked-sdist suites each passed 654 tests on
macOS/Python 3.12.13; authoring/generation and four installed-wheel verification
paths pass. Corrected-byte Ubuntu execution remains unrun. The linked correction
record identifies the measured artifacts and the documentation-only recording
boundary.

R3 also completed all three entries and remained BLOCKED for receipt readiness
stat/lstat errors escaping custody. That complete observation boundary is now
corrected with ten RED/GREEN regressions. The subsequent four-way
[specification/interface audit](verification/2026-10-14-spec-contract-audit.md)
found a separate pre-publication cyclic-path refusal gap, corrected with eight
RED/GREEN cases. Eight controlled callback races also verify documented
cancellation/ContractError precedence without production changes.
The [current API contract](../spec/reference/library-api.md) inventories all 27
exports; the conformance map assigns all 33 active normative groups and the case
map gives all 58 actual cases an explicit disposition. Final source and unpacked
sdist suites each passed **680 tests**, with all four installed-wheel checks,
authoring/generation, links and interface-map checks passing. See the correction
record for measured hashes and the documentation-only recording boundary.
R4 (`20261014-lib-spec-r4-bf8144`) completed with all three required reviewers
returning `SAFE TO MERGE`; collection was `AGREED`. The separate Astra comparison
found no concrete blocker. Two remaining Minor CLI-input issues were retained:
oversized native-driver timeout integers and cyclic paths at CLI argument
resolution. The owner authorized both corrections, regressions, native Ubuntu
source/package verification and another complete review. These results do not
certify host-only case axes. See the [Minor correction record](verification/2026-10-14-cli-input-corrections.md)
for the new verification boundary and current evidence.

The original two Minor corrections passed 686 source/sdist tests locally and
on native Ubuntu/macOS CI at `174bf13`. R6 then completed `AGREED`, with three
nonblocking neighboring CLI findings. Their bounded corrections now pass 700
source/sdist tests locally and all four installed-wheel checks; focused Python
3.13 checks also pass without changing the 3.12 project baseline. The linked
Minor correction record identifies exact measurements. R6 approval does not
transfer to these changed bytes; current native CI and fresh review outcomes
are recorded with the owner-managed round evidence and PR.

R8 (`20261014-lib-spec-r8-a49108`) completed `AGREED` on `00ed792`, with native
Ubuntu/macOS Python 3.12 CI passing 700 source and 700 archive tests per runner.
The owner then authorized its three nonblocking follow-ups: automated public-help
coverage, exception-preserving receipt readiness on Python 3.14, and per-call
import-verifier loading. The [Python 3.14 follow-up record](verification/2026-10-14-python314-followups.md)
tracks these changes, regression evidence and the expanded native CI matrix.
Local Python 3.12.13 and 3.14.6 each pass 704 source and 704 sdist tests, all four
installed-wheel paths, authoring/assets and interface-map checks. A pre-existing
decoder test's interpreter-dependent depth assumption was corrected without
changing the library contract. Exact-head CI and review outcomes are retained
with the owner-managed evidence and draft PR after this source record.
The default development interpreter remains Python 3.12; a new complete review
must assess the corrected bytes.

R9 completed AGREED on `6f790f6`; native Ubuntu/macOS Python 3.12/3.14 CI passed
704 source and 704 archive tests in all four jobs. The same follow-up record
documents two neighboring Minor corrections from that round: test-local color
isolation and per-run native preflight helper reuse with unchanged freshness
checks. R9 was exported/cleaned before edits; changed bytes require fresh evidence.
The follow-up source and sdist each pass 706 tests on local Python 3.12.13 and
3.14.6, with all four installed-wheel checks. Exact-head CI and the next complete
review are recorded externally after this documentation-only result update.

R10 (`20261014-lib-spec-r10-9218dc`) completed AGREED on `3ad33e8`, with all
three required reviewers approving and no Astra comparison finding. Native CI
run 38591880134 passed 706 source and 706 archive tests plus four installed-wheel
checks in all four Python/platform jobs. Opus retained a stale case-map evidence
link/line-anchor Minor and an isolated-interpreter color hardening suggestion.
The case map now uses the current-status entry point and named workflow steps;
actual `-I` forced-color reproduction drives the bounded test correction in the
same [follow-up record](verification/2026-10-14-python314-followups.md).
The completed round was exported and cleaned before edits. Changed bytes need
new exact-head CI and a fresh complete review, recorded with the draft PR.

R11 (`20261014-lib-spec-r11-63f374`) completed AGREED on `c7bf2bc` after
[native CI run 38595740079](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38595740079)
passed 706 source and 706 archive tests plus four installed-wheel checks in all
four Python/platform jobs. Opus retained one C68 test-path Minor; Sol, Argon
and the separate Astra comparison found no actionable defect. The completed
round was exported and cleaned. The C68 reference now includes `spec/tests/`;
an independent static audit found no additional invalid file-qualified test
references in either coverage map. This documentation-only correction changes
no runtime, test or normative case. New exact-head verification and full review
follow, with outcomes retained beside the draft PR.

R12 (`20261015-lib-spec-r12-9cedd4`) completed AGREED on `8ceaa7d`; Astra
again reported no actionable defect. Three Minor findings led to bounded
follow-ups: error-preserving receipt checks before request publication, explicit
C12/C14 schema-test references and CI checkout identity. The expanded static
table audit resolves all 184 explicit/shorthand references. Earlier R9–R12 CI
used merge commits with tracked trees verified identical to the reviewed heads;
the workflow now selects and asserts the actual head SHA. The
[R12 verification record](verification/2026-10-15-review-closure.md) preserves
the correction, historical identity qualification and verification boundaries.
The same-class audit also reproduced and corrected suppressed status errors in
native artifact reuse and generator symlink checks, with preservation regressions
on both Python versions. Shared-library interfaces and payload bytes are unchanged.

R13 (`20261015-lib-spec-r13-dcf36d`) completed BLOCKED on `d9d0055`, despite
all four native CI jobs passing 723 source/archive tests on the asserted head.
Sol, Opus and the separate Astra comparison identified suppressed directory
enumeration in the generator. External tests reproduced outside-sentinel writes
with scan errors and an actual non-listable directory on both Python versions.
Opus's separate `regular()` suggestion also reproduced under Python 3.14
non-following syscall-error injection. Bounded corrections and regressions
continue under the owner's quality-convergence authorization; the
[quality verification record](verification/2026-10-15-review-closure.md#r13-directory-inventory-and-regular-file-diagnosis)
separates these observations from real-provider guarantees. Changed bytes
require new source/package verification, native CI and a complete fresh review.
The bounded corrections add 37 regressions. Local Python 3.12.13 and 3.14.6
each now pass 760 source and 760 archive tests plus all four installed-wheel
checks; all 184 scoped table references resolve. Native CI and fresh review
outcomes for the committed snapshot are recorded externally after source freeze.
Before review, the same check at symlinked ancestors also exposed non-strict
resolution hiding injected errors on both interpreters. Strict resolution and
three added cases close that canonical-path boundary. Final local suites pass
763 source/archive tests each, all four wheel paths and 184 reference checks.
The preceding `f9f0367` CI passed 760 tests per source/archive job without skips;
it is retained only as intermediate evidence. Final CI/review follow the new SHA.

R14 (`20261015-lib-spec-r14-aa4570`) completed BLOCKED on `0e7375c`; Sol
required a remaining generator output-root observation correction. Opus and
separate Astra independently found the same gap and non-strict resolution at
context/run-parent boundaries. Opus also identified missing links to the newest
regressions in the conformance map. All four native CI jobs at this exact head
passed 763 source/archive tests without skips and all four wheel paths
([run 38613737116](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38613737116)).
The round is exported and cleaned. Focused reproduction, bounded corrections
and traceability updates continue under the owner's existing authorization;
the [R14 closure record](verification/2026-10-15-review-closure.md#r14-output-root-and-canonical-input-boundaries)
distinguishes injected faults, side effects and verification limits. A fresh
complete review is required after the changes.
The corrections add 28 regression cases. Local Python 3.12.13 and 3.14.6 now
each pass 791 source and 791 unpacked-sdist tests plus all four installed-wheel
paths; all 193 scoped references resolve, including the newly linked tests.
Committed-head CI and fresh review outcomes remain external post-freeze evidence.

R15 (`20261015-lib-spec-r15-d50127`) completed AGREED on `10f1795`, with all
three required reviewers SAFE. Its [native CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38617685314)
passed 791 source/archive tests without skips in each of four jobs and all four
wheel paths. Remaining nonblocking findings concern authoring reference link
observation and native run-parent errno diagnostics; separate Astra also found
the authoring gap. Both receive bounded reproduction and regression coverage
under the owner's quality-continuation instruction. See the
[R15 correction record](verification/2026-10-15-review-closure.md#r15-authoring-reference-and-run-parent-diagnostics).
The corrections also preserve the same status errors at canonical file/context
and authoring type checks. They add 22 regression cases; local Python 3.12.13
and 3.14.6 each pass 813 source/archive tests plus all four installed-wheel paths.
All 198 scoped test references resolve. Committed-head native CI and fresh review
outcomes remain recorded externally after source freeze.

R16 (`20261015-lib-spec-r16-b81fbc`) completed AGREED on `89504be`; all
three required entries were SAFE. Sol, Argon and the separate Astra comparison
reported no new findings. Its [native CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38621985362)
asserted the actual head/tree and passed 813 source/archive tests without skips
in all four jobs, plus all installed-wheel paths. Opus retained a CLI interrupt
custody Minor and generator-diagnostic/case-insensitive-name suggestions.
The round was exported and cleaned. Bounded reproduction and corrections
continue under the existing quality-convergence instruction; see the
[R16 closure record](verification/2026-10-15-review-closure.md#r16-cli-interruption-and-portable-preflight).
The corrections add 34 regressions. Local Python 3.12.13 and 3.14.6 each pass
847 source/archive tests and all four installed-wheel paths; 203 scoped
test references resolve. Native CLI interruption now retains the inner process
until acknowledgement, and portable name preflight precedes artifact creation.
Generator following-status errors retain their errno at every original query.
Actual committed-head native CI and fresh review outcomes are recorded externally.

R17 (`20261015-lib-spec-r17-855a0c`) completed AGREED on `ef748ee`; all
three required entries were SAFE. Sol, Argon and separate Astra found no new
issues. [Native CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38627294936)
asserted the actual head/tree and passed 847 source/archive tests without skips
in all four jobs. Opus identified a synthetic self-test interruption Minor.
The round was exported and cleaned. The bounded correction keeps the synthetic
receipt supervisor alive until the current scenario finishes, then propagates
cancellation and cleans its temporary directory. Shared runtime and supervised
native contracts are unchanged. See the
[R17 closure record](verification/2026-10-15-review-closure.md#r17-synthetic-self-test-interruption).
Five new regression cases pass; local Python 3.12.13 and 3.14.6 each pass 852
source/archive tests plus all four installed-wheel paths. The conformance audit
resolves 204 scoped references. Actual committed-head CI and the next complete
review remain separately recorded post-freeze evidence.

R18 (`20261015-lib-spec-r18-aa827a`) completed AGREED on `809b056`; all
required entries returned SAFE. Opus, Argon and separate Astra had no new
findings. [Native CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38631461513)
asserted that exact head/tree and passed 852 source/archive tests without skips
in all four jobs. Sol identified a distinct synthetic publication-failure
Minor, subsequently reproduced with source unchanged. The round was exported
and cleaned. The follow-up gives the self-test explicit task ownership and
fake-only abort/drain on producer error, preserving the original error and
the configured native acknowledgement requirement. See the
[R18 closure record](verification/2026-10-15-review-closure.md#r18-synthetic-publication-failure).
Twelve additional cases pass. Local Python 3.12.13 and 3.14.6 each pass 864
source/archive tests and all four installed-wheel paths; 206 scoped references
resolve. Exact committed-head CI and the next complete review remain external
post-freeze evidence.


## Consolidation slice (historical verification)

The unpublished development package is `0.1.0.dev3`. The shared specification
is consolidated under canonical `spec/`; runtime schemas/prompts generate the
same eight payload bytes with three content-addressed, six-field manifests.
Import commit/hashes remain ancestry in `spec/import-origin.json`, separate from
current content IDs. Python 3.12, current dependencies, all four routes and native
callback interfaces are preserved. Root pytest discovers both test suites.

Local macOS 26.6.2 ARM64 / Python 3.12.13 verification passes 633 combined tests,
the authoring checker and generator check. The dev3 sdist includes canonical
sources, tests/checkers and TOML inputs; unpacked-sdist verification and its
rebuilt wheel pass the same tests and four isolated synthetic drivers. See
[consolidation evidence](verification/2026-10-13-spec-library-consolidation.md)
for artifact identities, RED/GREEN and limits. Both task reviews and the final
whole-branch review approved `3bcb0da` with no open findings.
[Committed-head CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38287530518)
passed on Ubuntu 24.04 x86-64 and macOS 15 ARM64: each runner passed 633 source
and 633 unpacked-sdist tests, authoring/generator checks and all four isolated
installed-wheel drivers. The [draft PR](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1)
is updated. No new real-provider observation is claimed for this migration.

Repository cutover awaits PR merge and the [old-spec notice](../spec/MIGRATION.md).
Neither host has adopted this package; [host adoption and independent releases](host-adoption.md)
are separate scoped work. No merge, publication, global install, host port or
remote retirement is claimed.

## Previous dev2 slice (historical evidence)

The unpublished development package `0.1.0.dev2` implements strict original-JSON
admission, canonical named roster resolution, all four route prompt profiles on
hosts A/B, supported carrier extraction, unanimous agreement and bounded async
host callbacks with separate investigations. Canonical assets retain spec pin
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8`; Python 3.12 remains the baseline.

Work remains on `codex/strict-v2-admission` in
[draft PR #1](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1).
The current repository-only supervised callback driver is implemented at
`9d6f8a0`. Local source/sdist suites each pass 399 tests. Six fresh native Codex
responses passed through installed dev2 callbacks: three unanimous safe reviews,
one admitted negative review that blocks agreement, and two ordinary perspective
investigations without ballots. Formal and investigation callbacks both observed
peak concurrency two; native tool snapshots separately observed overlapping
children. Details and capture limits are in
[native callback verification](verification/2026-10-12-native-codex-callbacks.md).
Task and final whole-branch reviews have no open findings. Reviewed head `99e8e7f`
passed [native CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38222619438)
on Ubuntu 24.04 x86-64 and macOS 15 ARM64: source/sdist each 399 tests per runner
plus all four isolated installed-wheel drivers. CI uses synthetic responses;
actual native Codex observations above were performed on local macOS.
The [actual native lifecycle follow-up](verification/2026-10-12-native-codex-lifecycle.md)
adds three Codex child runs through the same installed wheel: timeout interruption,
repeated parent cancellation with awaited cleanup and no queued dispatch, and a
valid late affirmative response that remains timed out and cannot approve.
Two children reached observed `interrupted` state and one completed. This closes
the earlier actual-Codex lifecycle test gap on macOS; backend process termination,
Ubuntu native-agent behavior and existing consumer adoption remain unmeasured.
The [previous four-route verification](verification/2026-10-12-four-route-core.md)
records the earlier 364-test native CI baseline.
Earlier 157-test CI and fresh Codex observations describe the historical
[previous slice](verification/2026-10-12-lib-only-codex-integration.md), not this build.
Installed synthetic replay does not establish real provider success or host adoption.

- [Four-route design](design/2026-10-12-configurable-four-leg-library.md)
- [Four-route execution plan](superpowers/plans/2026-10-12-four-route-core.md)
- [Native callback verification plan](superpowers/plans/2026-10-12-native-codex-callbacks.md)
- [Original admission design and API](design/2026-10-12-v2-admission.md)
- [Original admission execution plan](superpowers/plans/2026-10-12-v2-admission.md)
- [Original research](research/2026-10-12-shared-library-assessment.md)
- [Prompt smoke design](design/2026-10-12-codex-prompt-smoke.md)
- [Prompt smoke execution plan](superpowers/plans/2026-10-12-codex-prompt-smoke.md)
- [Library-only integration plan](superpowers/plans/2026-10-12-lib-only-codex-integration.md)

## Next slices

The common four-route core and repository-only native callback harness are
implemented. Consumer adoption and optional
transport experiments require separate scoped work. See the
[design direction](design/2026-10-12-configurable-four-leg-library.md).

The [CLI feature assessment](research/2026-10-12-cli-feature-assessment.md)
compares official current documentation/releases with installed versions and
the existing B wrappers. It identifies optional transport experiments and
already-adopted capabilities. This research changes no runtime code, package
dependencies, spec pin or installed CLI. Current implemented common capabilities
are listed above.
The follow-up authentication check found the installed CLI reports ChatGPT
login. Official documentation supports ChatGPT OAuth and API-key authentication
for the app-server used by the Python SDK; SDK reuse on this machine has not
been executed. The Gemini replacement candidate is withdrawn by owner direction.

The [follow-up CLI spikes](research/2026-10-12-cli-feature-spikes.md) record
Codex offline configuration behavior, one quota-blocked Claude request, three
AGY startup validations and 13 passing synthetic Gemini envelope cases.
Claude's failure combined a success subtype with explicit error fields and exit
1; terminal checks must precede admission. AGY rejected the bare primitive name
`string` as invalid JSON and an array-root schema as requiring an object.
Neither result supports changing permission defaults or deleting process
cleanup. `openai-codex` remains a TODO, not the next experiment or a prerequisite
for four-route core work. No Ubuntu provider run or successful live schema-output
run is claimed by these spikes.

Consumer adoption is separate: thin host adapters consume the common core and
retain native execution. Existing host tests/bootstrap are not part of this
library test plan. Classification follows measured typed carriers and the latest
shared contract, without automatic full-CLI retries.

## Boundaries

Codex v0.2.561 independently adopted dev3 after library PR #1 merged.
Claude adoption and adoption of the current dev4 slice remain separate work.
The earlier Codex integration experiment used parent-dispatched native children;
the library and driver do not spawn native agents or provider processes. This
slice performs no consumer update, global installation, package-index publication
or final merge.
Platform proof covers only the combinations measured in the linked verification
records and exact-head CI evidence; a configured matrix alone is not proof.
The historical library slices above used ordinary independent Codex review;
they do not become formal TRIAD admission under the newly selected project
profile. Consumer adoption requires separate scoped work.
