# Current status

Updated: 2026-10-12

## Owner decisions

- Develop the common library in public `codefoundry-io/triad-dispatch-lib`.
- Write the design and implementation plan, then proceed.
- Preserve host-owned native execution and the shared specification authority.

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
packaging and missing-wheel CLI minors are resolved. Independent review and
native CI for this latest test-only extension are pending.
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

Design classification and agreement logic against shared contract cases; extend
renderer profiles when their contracts are ready. Consumer adoption is separate:
replace selected duplicate logic through thin host adapters, then verify the
actual consumer call path and fresh installed behavior. The repository test
driver is ready for bounded experiments without copying a full host skill.

## Boundaries

Neither host imports this package yet. The parent dispatched fresh native Codex
test children; the library and driver do not spawn. No global installation,
package-index publication, final merge or release occurred.
Platform proof covers the recorded native Python 3.12 combinations only.
The review profile is ordinary independent Codex review, not formal TRIAD
multi-family admission. Consumer adoption requires separate scoped work.
