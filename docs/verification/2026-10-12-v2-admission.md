# First-slice verification

Date: 2026-10-12. This records source/package verification, not host adoption.

## Contract and TDD evidence

Canonical source: shared-spec `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`.
Packaged `leg-verdict.schema.json` SHA-256:
`d755905ac60348542fc1dbbeb37b92bc3fab0a2dc34b7a1b454c935d0be04184`.
The original bytes were fetched from that exact GitHub commit.

| Task | Observed RED | Observed GREEN |
| --- | --- | --- |
| Original JSON parser | 26 missing-API assertion failures | 26 passed |
| Contract and v2 admission | 71 missing-API assertions | 97 total passed |
| Replay verifier | 2 missing-verifier failures; 10 replay cases already passed | 109 total passed |
| macOS venv regression | `test_environment_interpreter_starts` failed with SIGABRT | Regression passed; 110 total passed |

The macOS regression was a copied standalone Python executable failing relative
`libpython3.13.dylib` lookup. The same executable with `symlinks=True` started
successfully. The verifier now uses symlinks on the two selected POSIX platforms.
No host setting or provider behavior changed.

## Local package check

Final local baseline: Python 3.12.13, macOS 26.6.2 ARM64, uv 0.11.8.
`uv sync --locked` followed by `uv run --locked pytest -q`: **110 passed**.
Earlier unit runs used uv-selected Python 3.13.13; `.python-version` now pins
3.12 to match the required CI baseline. Those earlier runs alone are not a claim
of full 3.13 support.

Commands:

```sh
uv build --sdist
uv build dist/*.tar.gz --wheel
uv run --locked python tools/verify_wheel.py dist/*.whl
```

The wheel rebuilt from the sdist installed with `--only-binary=:all:` in a fresh
temporary venv outside the checkout. Python's `-I` isolated subprocess loaded
`triad_dispatch_lib` from that venv's `lib/python3.12/site-packages`, reported
version `0.1.0.dev0`, verified the packaged source/digest and passed all 10 raw
replay cases. Resolved runtime versions included jsonschema 4.26.0, referencing
0.37.0, rpds-py 2026.9.1 and attrs 26.1.0. The tool prints the specific wheel hash
on each run; build timestamps and subsequent metadata edits can change it.

## Execution decisions

- Added `.python-version=3.12` after uv selected an installed 3.13 interpreter.
  This makes development match the planned baseline. The tradeoff is that newer
  Python versions remain outside the required matrix until explicitly added.
- The reviewer prompt remains read-only. A dedicated package replay driver runs
  tests; no runtime Codex prompt was copied or modified.
- Instruction changes in AGENTS.md only replace obsolete documentation-only
  commands and record the review profile; no prompt behavior experiment applies.

## Independent review and CI

Pending fresh independent Codex whole-branch review and native GitHub CI.
The workflow selects Ubuntu 24.04 x86-64 and macOS 15 ARM64, Python 3.12, and
performs the same tests, sdist-derived wheel build and binary-only replay.
See [GitHub's runner definitions](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
Action versions were resolved through the official repositories and pinned to
commit SHAs. Workflow presence is not platform verification.

## Limits

The corpus is synthetic. It proves deterministic rejection/admission and package
loading, not a real provider round. No host adapter, prompt renderer integration,
provider execution, merge permission, installed plugin exposure or release is
established. Consumer adoption and real fresh-session smoke remain later work.
