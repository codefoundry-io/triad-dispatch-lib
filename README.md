# triad-dispatch-lib

Shared deterministic logic for the Claude-hosted
[triad-dispatch](https://github.com/codefoundry-io/triad-dispatch) and the
Codex-hosted [triad-codex-dispatch](https://github.com/codefoundry-io/triad-codex-dispatch).
Implement common rules once while preserving each host's native execution.

The product scope is configurable **Codex, Claude, Gemini CLI and AGY** review
entries, including all four together. Codex is the first test environment, not
the library's support boundary. Gemini and AGY are separate execution routes of
the canonical Google family. See the [four-route design direction](docs/design/2026-10-12-configurable-four-leg-library.md)
and [current CLI feature assessment](docs/research/2026-10-12-cli-feature-assessment.md).

## Status

The development package (`0.1.0.dev2`) provides strict original-JSON parsing,
canonical v2 verdict admission, named roster resolution, all four route prompt
profiles on hosts A/B, strict output carriers, unanimous agreement and bounded
async host callbacks. Repository drivers verify the installed package with
synthetic four-route responses; earlier fresh Codex observations remain historical.
It is not published to a package index and neither host has adopted it yet.

- [Current status and next work](docs/status.md)
- [Research assessment](docs/research/2026-10-12-shared-library-assessment.md)
- [API design and staged Codex testing](docs/design/2026-10-12-v2-admission.md)
- [Implementation plan](docs/superpowers/plans/2026-10-12-v2-admission.md)
- [Verification evidence and limits](docs/verification/2026-10-12-v2-admission.md)
- [Prompt renderer and test-driver design](docs/design/2026-10-12-codex-prompt-smoke.md)
- [Prompt smoke plan](docs/superpowers/plans/2026-10-12-codex-prompt-smoke.md)
- [Installed-package and fresh Codex evidence](docs/verification/2026-10-12-codex-prompt-smoke.md)
- [Library-only Codex integration matrix](docs/verification/2026-10-12-lib-only-codex-integration.md)
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
Output admission and unanimous agreement are implemented; native host adapters
remain separate work. Rust is deferred until a measured need justifies it.

`validate_binding(expected)` checks invocation bindings without a response.
`render_review_clauses(...)` selects byte-preserved canonical clauses in their
specified order for an explicit date, phase and web permission. It accepts
Codex, Claude and Google on hosts A/B; Google requires explicit `agy` or `gemini`.
Google also requires `gated-patch-file` in replacements; active hook clauses
require Google/AGY on host A. Unsupported profiles raise `PromptError`.
`render_data(text)` quotes residual evidence as data. These pure functions do not
launch agents. See the [renderer contract](docs/design/2026-10-12-codex-prompt-smoke.md)
for the exact replacement keys and phase behavior.

## Async host callbacks

`resolve_roster(defaults, overrides=None)` merges canonical named entries from
strict override JSON;
`select_entries(resolved)` returns enabled entries and refuses an empty selection.
Model/effort values are opaque requests; hosts resolve supported native controls
and unpinned Google routes before constructing formal requests. All selected
entries count, including repeated families and informational entries.

```python
import asyncio
from triad_dispatch_lib import ReviewRequest, run_review, run_investigations

async def review(selected, bindings, prompts, adapter):
    requests = [ReviewRequest(entry, bindings[entry["name"]], prompts[entry["name"]])
                for entry in selected]

    async def preflight(request):
        await adapter.check_capabilities(request.entry)
        # Must return None. Any exception or other return aborts before invokes.

    async def invoke(request):
        # Return ProviderOutput with original carrier bytes and observed state.
        # Adapter cooperates with cancellation and awaits native process cleanup.
        return await adapter.invoke(request)

    async def integrity():
        # Fresh packet, prompt, artifact and custody checks owned by the host.
        return await adapter.check_integrity()

    return await run_review(requests, invoke, preflight=preflight,
                            integrity_check=integrity, max_concurrency=2)

# asyncio.run(review(selected, bindings, prompts, adapter))
```

Each request binds exactly review_id, family, content_digest, leg_name, attempt
and route. Formal reviewers receive the complete common scope. The host prepares
and hashes packets/prompts and supplies current integrity evidence. Callbacks
execute once, without retries. Deadlines start after acquiring an invoke slot.
A callback returning is a completed outcome; admission separately checks terminal
metadata and verdicts. Integrity exceptions/non-bools preserve completed outcomes
but block agreement. Invalid arguments or refused preflight raise `DispatchError`;
broken packaged contracts raise `ContractError` after owned child cleanup.
Parent cancellation propagates after awaiting child cleanup, including repeated
cancellation. Callbacks must cooperate; the library cannot forcibly terminate
native processes or guarantee a deadline for a callback that suppresses cancellation.

`ProviderOutput` supports `native-final`, `claude-json`, `gemini-json` and
`agy-stream-json`. Native-final is original JSON after host-owned marker/fence
removal; the library never strips markers. Claude requires an object-valued
`structured_output`, Gemini a string-valued `response`, and AGY exactly one
successful result terminal with object-valued structured output in valid JSONL.
Duplicate members, malformed tails and ambiguous terminals are refused. Completion,
timeout, transport and exit observations precede admission; unsupported envelope
adaptation remains host-owned. `admit_output` preserves embedded JSON evidence.
`evaluate_agreement` re-admits every selected binding and requires unanimous safe
verdicts plus true integrity. Valid dissent is retained and blocks approval.

`InvestigationRequest(entry, prompt, web_authorized=False)` and
`run_investigations(requests, invoke, preflight=..., max_concurrency=...)` use the
same bounded callback model but return ordinary ordered outcomes without ballots.
`render_investigation_prompt` adds the authorized Google web suffix only where
applicable. New formal reviewers require a newly bound round.
See [four-route verification](docs/verification/2026-10-12-four-route-core.md).

## Work locally

```sh
git clone git@github.com:codefoundry-io/triad-dispatch-lib.git
cd triad-dispatch-lib
uv sync --locked
uv run --locked pytest -q
uv build --sdist
uv build dist/triad_dispatch_lib-0.1.0.dev2.tar.gz --wheel
uv run --locked python tools/verify_wheel.py dist/triad_dispatch_lib-0.1.0.dev2-py3-none-any.whl
uv run --locked python tools/codex_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev2-py3-none-any.whl --expected-version 0.1.0.dev2 self-test
uv run --locked python tools/four_route_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev2-py3-none-any.whl --expected-version 0.1.0.dev2
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
uv run --locked python tools/codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev2 render --context context.json --prompt prompt.txt
# Dispatch prompt.txt using the host's native agent mechanism; save its final JSON.
uv run --locked python tools/codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev2 admit --context context.json --prompt prompt.txt --result result.json
```

Each command installs the specified wheel into a fresh temporary environment and
checks the package version and actual validator's site-packages path. Admission
requires unchanged packets and prompt, then passes raw response bytes directly
to `validate_verdict`. A valid negative verdict is admitted successfully; this
does not grant merge permission. The driver does not spawn agents or establish
formal host custody. CI uses synthetic responses; fresh native response evidence
is recorded separately with its capture limitations.

All these experiments belong to this library repository. They do not execute or
modify an existing Codex/Claude host, install a plugin, or change host settings.
`self-test` reports 54 cases: 18 each for formal-plan, implementation-review and
pre-merge. It preserves valid negative verdicts and rejects every mismatched
binding, malformed original JSON, and changed packet/prompt. The non-null Codex
route case is a schema refusal; it cannot be a schema-valid route swap.
The matrix also checks that the rendered phase and purpose match each case.
Missing wheel paths are refused with exit code 2 before installation starts.

## License

[MIT](LICENSE), consistent with the existing TRIAD host repositories.
