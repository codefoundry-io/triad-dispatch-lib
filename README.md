# triad-dispatch-lib

Shared deterministic logic for the Claude-hosted
[triad-dispatch](https://github.com/codefoundry-io/triad-dispatch) and the
Codex-hosted [triad-codex-dispatch](https://github.com/codefoundry-io/triad-codex-dispatch).
Implement common rules once while preserving each host's native execution.

## Status

The development package (`0.1.0.dev1`) provides strict original-JSON parsing,
canonical v2 verdict admission and pinned common-clause rendering for Codex/B.
A repository test driver exercises fresh Codex responses through the installed
package. It is not published to a package index and neither host has adopted it yet.

- [Current status and next work](docs/status.md)
- [Research assessment](docs/research/2026-10-12-shared-library-assessment.md)
- [API design and staged Codex testing](docs/design/2026-10-12-v2-admission.md)
- [Implementation plan](docs/superpowers/plans/2026-10-12-v2-admission.md)
- [Verification evidence and limits](docs/verification/2026-10-12-v2-admission.md)
- [Prompt renderer and test-driver design](docs/design/2026-10-12-codex-prompt-smoke.md)
- [Prompt smoke plan](docs/superpowers/plans/2026-10-12-codex-prompt-smoke.md)
- [Installed-package and fresh Codex evidence](docs/verification/2026-10-12-codex-prompt-smoke.md)
- [Contributor and agent guidance](AGENTS.md)

## Relationship to the shared specification

[triad-dispatch-spec](https://github.com/codefoundry-io/triad-dispatch-spec)
remains the authority for common behavior, schemas, prompt clauses, and cases.
This repository implements those contracts, with byte-preserved pinned schema
data and an adjacent provenance manifest.

The dependency direction is: pinned specification artifacts → shared library →
host adapters. Each host retains native spawning, model and effort integration,
installation, and platform-specific execution. Hosts retain independent release
schedules and explicitly record the versions they adopt.

## API

```python
from triad_dispatch_lib import AdmissionError, ContractError, validate_verdict

try:
    verdict = validate_verdict(raw_json_bytes, expected={
        "review_id": "review-1",
        "family": "codex",
        "content_digest": "a" * 64,  # Actual digest supplied by the host.
        "leg_name": "codex-leg",
        "attempt": 1,
        "route": None,
    })
except AdmissionError as error:
    print(error.code)  # Fixed code, no payload values in the message.
except ContractError:
    raise  # Broken package/contract, not a reviewer verdict.
```

`parse_json(str | bytes)` exposes the same strict parsing boundary separately.
Pass original JSON, not a parsed dictionary or Markdown block. Expected bindings
must contain exactly the six shown fields. Google uses `agy` or `gemini` routes;
other families use null. Admission returns the unmodified parsed object, including
valid negative verdicts; it makes no merge decision. Callers own input size limits.

See the design for error codes and edge cases. The package pins candidate spec
commit `fcd96a15d18f3131c1f0111bdb10c3faceae34f8`; it does not convert v1 data.
Failure classification, result aggregation and native host adapters are later
slices. Rust is deferred until a measured need justifies it.

`validate_binding(expected)` checks invocation bindings without a response.
`render_review_clauses(...)` selects byte-preserved canonical clauses in their
specified order for an explicit date, phase and web permission. It currently
accepts only `family="codex", host="B"`; unsupported profiles raise `PromptError`.
`render_data(text)` quotes residual evidence as data. These pure functions do not
launch agents. See the [renderer contract](docs/design/2026-10-12-codex-prompt-smoke.md)
for the exact replacement keys and phase behavior.

## Work locally

```sh
git clone git@github.com:codefoundry-io/triad-dispatch-lib.git
cd triad-dispatch-lib
uv sync --locked
uv run --locked pytest -q
uv build --sdist
uv build dist/triad_dispatch_lib-0.1.0.dev1.tar.gz --wheel
uv run --locked python tools/verify_wheel.py dist/triad_dispatch_lib-0.1.0.dev1-py3-none-any.whl
uv run --locked python tools/codex_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev1-py3-none-any.whl --expected-version 0.1.0.dev1 self-test
git diff --check
```

Use Python 3.12 (selected by `.python-version`) and uv 0.11.8 as in CI. The package
metadata permits Python 3.12+; tested combinations are recorded in verification
evidence. `uv.lock` pins development dependencies. The wheel probe creates a
temporary environment outside the checkout and installs the wheel and allowed
runtime dependencies using binary wheels only, then replays the raw fixtures.
It reports import path, versions, platform, schema hash and wheel hash. That
probe needs package-index access for installation; the admission API itself is
offline. Transitive `rpds-py` includes native Rust code, so wheel availability is
checked per platform even though this repository needs no Rust source build.

CI uses [native GitHub runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
for Ubuntu 24.04 x86-64 and macOS 15 ARM64 with Python 3.12. Platform claims require
successful runs, not merely the presence of the workflow. For multiple local
build versions, pass specific sdist and wheel paths instead of wildcards.

## Codex response experiment

The repository driver takes a context JSON described in the
[design](docs/design/2026-10-12-codex-prompt-smoke.md); its complete synthetic
example is `synthetic_smoke()` in [tools/codex_smoke.py](tools/codex_smoke.py).
Provide a canonical absolute worktree, bound regular packet files, the six
expected fields, and explicit review scope. The fixture digest convention is
SHA-256 of the sorted compact JSON list of relative paths and file hashes.

```sh
uv run --locked python tools/codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev1 render --context context.json --prompt prompt.txt
# Dispatch prompt.txt using the host's native agent mechanism; save its final JSON.
uv run --locked python tools/codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev1 admit --context context.json --prompt prompt.txt --result result.json
```

Each command installs the specified wheel into a fresh temporary environment and
checks the package version and actual validator's site-packages path. Admission
requires unchanged packets and prompt, then passes raw response bytes directly
to `validate_verdict`. A valid negative verdict is admitted successfully; this
does not grant merge permission. The driver does not spawn agents or establish
formal host custody. CI uses synthetic responses; fresh native response evidence
is recorded separately with its capture limitations.

## License

[MIT](LICENSE), consistent with the existing TRIAD host repositories.
