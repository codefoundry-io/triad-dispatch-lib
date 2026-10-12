# Current status

Updated: 2026-10-12

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

The unpublished development package `0.1.0.dev2` implements strict original-JSON
admission, canonical named roster resolution, all four route prompt profiles on
hosts A/B, supported carrier extraction, unanimous agreement and bounded async
host callbacks with separate investigations. Canonical assets retain spec pin
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8`; Python 3.12 remains the baseline.

Work remains on `codex/strict-v2-admission` in
[draft PR #1](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1).
Current local source/sdist/wheel evidence is recorded in
[four-route verification](verification/2026-10-12-four-route-core.md).
Native Ubuntu 24.04 x86-64/macOS 15 ARM64
[CI passed](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38217590730)
on implementation commit `2f8c813`: 364 source tests and 364 unpacked-sdist tests
per platform, plus all three isolated installed-wheel drivers. Independent final
review and scoped re-review left no open findings.
Earlier 157-test CI and fresh Codex observations describe the historical
[previous slice](verification/2026-10-12-lib-only-codex-integration.md), not this build.
Installed synthetic replay does not establish real provider success or host adoption.

- [Four-route design](design/2026-10-12-configurable-four-leg-library.md)
- [Four-route execution plan](superpowers/plans/2026-10-12-four-route-core.md)
- [Original admission design and API](design/2026-10-12-v2-admission.md)
- [Original admission execution plan](superpowers/plans/2026-10-12-v2-admission.md)
- [Original research](research/2026-10-12-shared-library-assessment.md)
- [Prompt smoke design](design/2026-10-12-codex-prompt-smoke.md)
- [Prompt smoke execution plan](superpowers/plans/2026-10-12-codex-prompt-smoke.md)
- [Library-only integration plan](superpowers/plans/2026-10-12-lib-only-codex-integration.md)

## Next slices

The common four-route core is implemented. Consumer adoption and optional
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
