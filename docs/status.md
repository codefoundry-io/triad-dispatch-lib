# Current status

Updated: 2026-10-12

## Owner decisions

- Create `codefoundry-io/triad-dispatch-lib` as a public GitHub repository.
- Use this independent repository as the development home for shared library work.
- Preserve the existing hosts and shared specification during initialization.

## Current scope

Repository initialization and a durable handoff of the preceding research.
The repository contains documentation and project guidance only. No package has
been built, no host imports this library, and no release or installation has
been performed. Repository visibility is not evidence of runtime readiness.

## Research direction

The [assessment](research/2026-10-12-shared-library-assessment.md) recommends
Python 3.12+, shared deterministic functions, pinned specification artifacts,
and host-owned integration adapters. It recommends deferring a Rust rewrite.
These recommendations do not settle public APIs or constitute an approved
implementation plan.

## Next work

Develop a concrete first-slice design for strict original-JSON parsing and v2
verdict admission. Define the input/output and error contracts, specification
provenance, shared conformance vectors, and compatibility expectations before
extracting code. Refresh the relevant shared-spec revision when that work starts.

Keep canonical validation separate from vendor-facing schema projections and
legacy v1 interfaces. Model/effort selection, native spawning, provider calls,
installation, and destructive cleanup are outside that initial proposed slice.

The design should resolve package layout, dependency/release pinning, review
profile, and verification commands. Later implementation belongs on a `codex/`
work branch in this repository. Consumer adoption remains separate scoped work.

## Verification boundary

Initialization checks cover repository isolation, document links and whitespace,
public visibility, and equality of the local and remote initial commit. They do
not establish schema conformance, vendor behavior, or macOS/Ubuntu support.
