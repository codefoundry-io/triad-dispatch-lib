# Current status

Updated: 2026-10-14

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

Neither host has completed released adoption; Codex source-adoption work is a
separate candidate. The earlier Codex integration experiment
used parent-dispatched native children; the library and driver do not spawn
native agents or provider processes. No global installation,
package-index publication, final merge or release occurred.
Platform proof covers the recorded native Python 3.12 combinations only.
The historical library slices above used ordinary independent Codex review;
they do not become formal TRIAD admission under the newly selected project
profile. Consumer adoption requires separate scoped work.
