# triad-dispatch-lib

Shared deterministic logic for the Claude-hosted
[triad-dispatch](https://github.com/codefoundry-io/triad-dispatch) and the
Codex-hosted [triad-codex-dispatch](https://github.com/codefoundry-io/triad-codex-dispatch).
Implement common rules once while preserving each host's native execution.

## Status

The first development package (`0.1.0.dev0`) provides strict original-JSON parsing
and canonical v2 verdict admission. It is not published to a package index and
neither host has adopted it yet.

- [Current status and next work](docs/status.md)
- [Research assessment](docs/research/2026-10-12-shared-library-assessment.md)
- [API design and staged Codex testing](docs/design/2026-10-12-v2-admission.md)
- [Implementation plan](docs/superpowers/plans/2026-10-12-v2-admission.md)
- [Verification evidence and limits](docs/verification/2026-10-12-v2-admission.md)
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

## Work locally

```sh
git clone git@github.com:codefoundry-io/triad-dispatch-lib.git
cd triad-dispatch-lib
uv sync --locked
uv run --locked pytest -q
uv build --sdist
uv build dist/*.tar.gz --wheel
uv run --locked python tools/verify_wheel.py dist/*.whl
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

## License

[MIT](LICENSE), consistent with the existing TRIAD host repositories.
