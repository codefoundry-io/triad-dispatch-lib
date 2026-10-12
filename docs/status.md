# Current status

Updated: 2026-10-12

## Owner decisions

- Develop the common library in public `codefoundry-io/triad-dispatch-lib`.
- Write the design and implementation plan, then proceed.
- Preserve host-owned native execution and the shared specification authority.

## Current slice

The first development package implements strict original-JSON parsing and
canonical v2 verdict admission with six invocation bindings. Its candidate
schema is pinned to spec `fcd96a15d18f3131c1f0111bdb10c3faceae34f8` with a packaged
provenance manifest and SHA-256. Python 3.12 is the development/CI baseline;
Rust source implementation is deferred.

Work is on `codex/strict-v2-admission`. Local tests and the isolated installed-wheel
replay pass. Independent whole-branch review and native GitHub CI are pending.
See [verification evidence](verification/2026-10-12-v2-admission.md).

- [Design and API](design/2026-10-12-v2-admission.md)
- [Execution plan](superpowers/plans/2026-10-12-v2-admission.md)
- [Original research](research/2026-10-12-shared-library-assessment.md)

## Next slices

Design classification and agreement logic against shared contract cases. Then
build a thin Codex integration driver proving the installed library identity and
actual host call path. Use pinned canonical prompt clauses for render tests and
separate fresh-session smoke tests for real model behavior. See the design's
Codex testing section; copying the full Codex skill is not the test strategy.

## Boundaries

Neither host imports this package yet. No native spawning, provider calls, global
installation, package-index publication, final merge or release occurred. Local
macOS proof does not establish Ubuntu support; successful native CI is required.
The review profile is ordinary independent Codex review, not formal TRIAD
multi-family admission. Consumer adoption requires separate scoped work.
