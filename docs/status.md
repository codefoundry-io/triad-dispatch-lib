# Current status

Updated: 2026-10-13

## Owner decisions

- Develop the common library in public `codefoundry-io/triad-dispatch-lib`.
- Write the design and implementation plan, then proceed.
- Preserve host-owned native execution and the shared specification authority.
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

## Current slice

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
for artifact identities, RED/GREEN and limits. Current-branch remote CI and real
providers have not been observed in this slice. Independent task/branch review
and PR integration remain controller work.

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

Neither host imports this package yet. The earlier Codex integration experiment
used parent-dispatched native children; the library and driver do not spawn
native agents or provider processes. No global installation,
package-index publication, final merge or release occurred.
Platform proof covers the recorded native Python 3.12 combinations only.
The review profile is ordinary independent Codex review, not formal TRIAD
multi-family admission. Consumer adoption requires separate scoped work.
