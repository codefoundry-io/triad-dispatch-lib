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

Native [CI run 38201147972](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38201147972)
passed at source commit `08601298b728eeb7def2de8319b9459b63ce418d` on 2026-10-12.
Both jobs completed 110 tests, built the wheel from an sdist, installed with
binary-only dependencies in an isolated venv, and passed all 10 replay cases.

| Native runner | Observed Python / machine | Result |
| --- | --- | --- |
| Ubuntu 24.04 | 3.12.15 / x86_64 (glibc 2.39) | 110 tests + 10 installed-wheel cases |
| macOS 15.7.9 | 3.12.10 / arm64 | 110 tests + 10 installed-wheel cases |

Observed wheel SHA-256 (builds are not asserted byte-reproducible):

- Ubuntu: `44ecef79d223d842fa470a67bc938153eb5966ac4d6f831f7969bf35e4cdb535`.
- macOS CI: `479b6ea08c78ab703f7735eab65038e538afbb6ac960fb05969957cbc23f64bb`.
- Local reviewed wheel: `d152464ca397bcadac9afe41239813bebba8696868f7ff4d55d71f4dd8a2c507`.

All three loaded the package from their fresh venv's `site-packages` and verified
the same pinned source/schema digest. These are the tested combinations, not a
claim about all Python versions or architectures.
See [GitHub's runner definitions](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
Action versions were resolved through the official repositories and pinned to
commit SHAs. Only successful native runs support these platform claims.

## Limits

The corpus is synthetic. It proves deterministic rejection/admission and package
loading, not a real provider round. No host adapter, prompt renderer integration,
provider execution, merge permission, installed plugin exposure or release is
established. Consumer adoption and real fresh-session smoke remain later work.

### Whole-branch review result

Fresh reviewer: requested `gpt-6-astra`, `high`, fresh context; hidden runtime
settings were UNEXPOSED. The review was prompt-controlled read-only. Reviewed
range `c6dd981..0860129`; tracked file fingerprints and HEAD remained unchanged.
Result: no Critical or Important findings, one Minor. Reviewer independently
ran 109 tests with the venv-creation test excluded under its no-install brief,
and checked the existing full 110-test and installed-wheel evidence.

Deferred minor: setuptools includes test modules in the sdist but not the raw
fixture corpus or `tools/verify_wheel.py`. Wheel installation and runtime work;
running the entire test suite from an unpacked sdist requires those support files
from the repository. Include them before source-distribution test support or a
release is promised. The current README development instructions use a Git clone.

Review scope rulings retained: package hashes establish consistency, not
malicious whole-package replacement authentication; input size limits are owned
by callers, so callers must prevent resource exhaustion; host/provider behavior
needs later integration evidence; native platform claims require successful CI,
not the workflow file alone. These preserve the written design's scope.
