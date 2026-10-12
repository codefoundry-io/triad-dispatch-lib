# triad-dispatch-lib

Shared deterministic logic for the Claude-hosted
[triad-dispatch](https://github.com/codefoundry-io/triad-dispatch) and the
Codex-hosted [triad-codex-dispatch](https://github.com/codefoundry-io/triad-codex-dispatch).

The goal is to implement common rules once while preserving each host's native
agent execution and integration boundaries.

## Status

This public repository is the development home for the proposed shared library.
It currently contains project guidance and the initial research assessment.
There is no installable package, runtime implementation, or host integration yet.

- [Current status and next work](docs/status.md)
- [Research assessment](docs/research/2026-10-12-shared-library-assessment.md)
- [Contributor and agent guidance](AGENTS.md)

## Relationship to the shared specification

[triad-dispatch-spec](https://github.com/codefoundry-io/triad-dispatch-spec)
remains the authority for common behavior, schemas, prompt clauses, and cases.
This repository is intended to implement those contracts; it must not introduce
a second editable copy of the canonical rules.

The proposed dependency direction is: pinned specification artifacts → shared
library → host adapters. Each host retains its native spawning, model and effort
integration, installation, and platform-specific execution. Hosts retain
independent release schedules and explicitly record the versions they adopt.

## Initial direction

The research recommends Python 3.12+ and an initial scope of strict JSON parsing
and v2 verdict validation with shared conformance vectors. Failure classification
and result aggregation are later candidates. Rust remains an option for a
measured need rather than an initial rewrite.

These are research recommendations. Public APIs, packaging, dependencies, and
the first implementation plan still need to be specified.

## Work locally

```sh
git clone git@github.com:codefoundry-io/triad-dispatch-lib.git
cd triad-dispatch-lib
git status --short
git diff --check
```

Read the current status before starting work. No dependency installation, build,
or runtime test command exists at this documentation-only stage. Those commands
will be documented with the first executable slice.

## License

[MIT](LICENSE), consistent with the existing TRIAD host repositories.
