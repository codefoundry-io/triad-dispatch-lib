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
- Exclude MCP-based implementation candidates. Investigate `openai-codex`
  authentication through the direct local app-server interface only.

## Current slice

The development package `0.1.0.dev1` implements strict original-JSON parsing,
canonical v2 verdict admission with six invocation bindings and pinned common
prompt rendering for Codex/B. Schema and prompt assets are pinned to spec
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8` with packaged provenance and SHA-256.
Python 3.12 is the development/CI baseline; Rust source implementation is deferred.

Work is on `codex/strict-v2-admission` in
[draft PR #1](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1).
The owner explicitly selected tests in this library repository only. Existing
Codex/Claude hosts are read-only references, with no runtime adoption or host test
execution. Local checks now pass 157 tests; installed-wheel replay passes 10 raw
cases and the expanded Codex adapter passes 54 cases across three review phases.
Four new native sessions verified plan/implementation control and defect packets;
the earlier two pre-merge observations remain separate evidence. Both prior
packaging and missing-wheel CLI minors are resolved. Independent whole-branch
review found no Critical/Important/Minor issues. Native Ubuntu 24.04 x86-64 and
macOS 15 ARM64 CI passed 157 source tests, 157 unpacked-sdist tests, 10 raw replay
cases and 54 installed Codex adapter cases on each platform.
See [current evidence](verification/2026-10-12-lib-only-codex-integration.md),
[earlier prompt evidence](verification/2026-10-12-codex-prompt-smoke.md) and
[first-slice evidence](verification/2026-10-12-v2-admission.md).

- [Design and API](design/2026-10-12-v2-admission.md)
- [Execution plan](superpowers/plans/2026-10-12-v2-admission.md)
- [Original research](research/2026-10-12-shared-library-assessment.md)
- [Prompt smoke design](design/2026-10-12-codex-prompt-smoke.md)
- [Prompt smoke execution plan](superpowers/plans/2026-10-12-codex-prompt-smoke.md)
- [Library-only integration plan](superpowers/plans/2026-10-12-lib-only-codex-integration.md)

## Next slices

The owner corrected the intended scope to four configurable execution choices.
The latest spec already permits this: use named Codex and Claude entries plus
two Google entries pinned separately to Gemini and AGY. Implement common roster
resolution, all required prompt profiles, and unanimous agreement for every
selected entry; do not treat the three remaining routes as optional product scope.
See the [design direction and verification order](design/2026-10-12-configurable-four-leg-library.md).

The [CLI feature assessment](research/2026-10-12-cli-feature-assessment.md)
compares official current documentation/releases with installed versions and
the existing B wrappers. It identifies optional transport experiments and
already-adopted capabilities. This research changes no runtime code, package
dependencies, spec pin or installed CLI. The four-route implementation is still
pending; current package capabilities remain those listed above.
The follow-up authentication check found the installed CLI reports ChatGPT
login. Official documentation supports ChatGPT OAuth and API-key authentication
for the app-server used by the Python SDK; SDK reuse on this machine has not
been executed. The Gemini replacement candidate is withdrawn by owner direction.

Consumer adoption is separate: thin host adapters consume the common core and
retain native execution. Existing host tests/bootstrap are not part of this
library test plan. Classification follows measured typed carriers and the latest
shared contract, without automatic full-CLI retries.

## Boundaries

Neither host imports this package yet. The parent dispatched fresh native Codex
test children; the library and driver do not spawn. No global installation,
package-index publication, final merge or release occurred.
Platform proof covers the recorded native Python 3.12 combinations only.
The review profile is ordinary independent Codex review, not formal TRIAD
multi-family admission. Consumer adoption requires separate scoped work.
