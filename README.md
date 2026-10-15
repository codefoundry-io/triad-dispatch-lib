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

The development package (`0.1.0.dev4`) provides strict original-JSON parsing,
canonical v2 verdict admission, named roster resolution, all four route prompt
profiles on hosts A/B, strict output carriers, unanimous agreement and bounded
async host callbacks. Repository drivers verify the installed package with
synthetic four-route responses; earlier fresh Codex observations remain historical.
The dev4 package is not published to a package index. Codex host v0.2.561
independently released with library dev3 from `2d1e62e7`; Claude adoption remains
planned. Neither host is claimed to adopt dev4. See
[independent host adoption](docs/host-adoption.md).

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

The canonical specification now lives in [`spec/`](spec/README.md) alongside
its deterministic implementation and tests. Edit `spec/contracts/` and
`spec/prompts/`, then run `tools/sync_spec_assets.py --write`; never hand-edit
`src/triad_dispatch_lib/data/`. `--check` detects missing, stale and unexpected
generated assets without writing or requiring Git/network access.

[`spec/import-origin.json`](spec/import-origin.json) records the original import
commit and file hashes as ancestry, not current document hashes. The three runtime
manifests each contain exactly `schema_version`, `source_repository`, `source_path`,
`status`, `sha256` and `contract_id`. Each ID identifies one bundle of payload
bytes, not the entire specification or a repository commit. Integrity establishes
consistency, not authenticity. Legacy schema `$id` values remain unchanged.

Specification consolidation merged in PR #1 at `9489543e`. Posting the
old-repository notice remains separate work; no remote retirement is claimed.
See [migration](spec/MIGRATION.md) and
[independent host adoption](docs/host-adoption.md). Each host retains native
spawning, model/effort integration, installation and independent releases.
The [library conformance map](spec/reference/library-conformance.md) links current
rules/cases to APIs and tests, with partial coverage and host responsibilities.

## API

The [current Python API contract](spec/reference/library-api.md) covers all 29
package-root exports: signatures, result fields, mutation boundaries, emitted
error codes and callback lifecycle. It supplements the canonical wire and review
rules; historical implementation plans are not the current API entry point.

`merge_roster(defaults, overrides=None)` returns an independent merge after
validating the complete defaults and strict JSON override inputs.
`validate_resolved(roster)` validates the exact merged document and returns
`None`. The intermediate merge may contain incomplete entries or inherited
incompatible vendor blocks; host checks must safely handle these and final
validation is mandatory before consumption. `resolve_roster` retains its
validated dictionary return. Capability, route and custom diagnostic checks
remain host-owned; later mutations require revalidation.

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

See the API contract for error codes and edge cases. Runtime bundles have candidate
content IDs; historical import commits are separate. The API does not convert v1 data.
Output admission and unanimous agreement are implemented; native adapters
remain host-owned. Rust is deferred until a measured need justifies it.

`validate_binding(expected)` checks invocation bindings without a response.
`render_review_clauses(...)` selects byte-preserved canonical clauses in their
specified order for an explicit date, phase and web permission. It accepts
Codex, Claude and Google on hosts A/B; Google requires explicit `agy` or `gemini`.
Google also requires `gated-patch-file` in replacements; active hook clauses
require Google/AGY on host A. Unsupported profiles raise `PromptError`.
`render_data(text)` quotes residual evidence as data. These pure functions do not
launch agents. See the [renderer contract](spec/reference/library-api.md#prompt-rendering)
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
execute once, without retries. Each preflight gets its full entry timeout after
acquiring a preflight slot; invocation then gets a separate full timeout after
acquiring an invoke slot. Queue time is excluded from both budgets.
A callback returning is a completed outcome; admission separately checks terminal
metadata and verdicts. Integrity exceptions/non-bools preserve completed outcomes
but block agreement. Invalid arguments or refused preflight raise `DispatchError`;
broken packaged contracts raise `ContractError` after owned child cleanup.
Parent cancellation propagates after awaiting child cleanup, including repeated
cancellation. Callbacks must cooperate; the library cannot forcibly terminate
native processes or guarantee a deadline for a callback that suppresses cancellation.
Wait-setup errors also settle the created callback before propagating. The canonical
timeout schema has no operational maximum; an unschedulable value may raise a
runtime scheduling error. `integrity_check` has no built-in timeout. A refused
preflight exposes the aggregate `preflight_failed` code, not per-entry diagnostics.
Full collectors must preserve the [host-fault distinction](docs/host-adoption.md#required-adapter-contracts).

`ProviderOutput` supports `native-final`, `claude-json`, `gemini-json` and
`agy-stream-json`. Native-final is original JSON after host-owned marker/fence
removal; the library never strips markers. Claude requires an object-valued
`structured_output`, Gemini a string-valued `response`, and AGY exactly one
successful result terminal with object-valued structured output in valid JSONL.
Duplicate members, malformed tails and ambiguous terminals are refused. Completion,
timeout, transport and exit observations precede admission; unsupported envelope
adaptation remains host-owned. `admit_output` preserves embedded JSON evidence.
The strict AGY carrier does not perform C23 same-run finish recovery; adopting
hosts must retain that decision and its guards before admitting recovered output.
Generic `native-final` trusts host-observed completion and original final bytes
for any family; it does not attest execution or authorize relabelling failed transport.
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
uv run --locked python spec/tools/check_authoring.py
uv run --locked python tools/sync_spec_assets.py --check
uv build --sdist
uv build dist/triad_dispatch_lib-0.1.0.dev4.tar.gz --wheel
uv run --locked python tools/verify_wheel.py dist/triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl
uv run --locked python tools/codex_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl --expected-version 0.1.0.dev4 self-test
uv run --locked python tools/four_route_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl --expected-version 0.1.0.dev4
uv run --locked python tools/native_codex_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl --expected-version 0.1.0.dev4 --self-test
git diff --check
```

Use Python 3.12 (selected by `.python-version`) and uv 0.11.8 by default. The package
metadata permits Python 3.12+; tested combinations are recorded in verification
evidence. `uv.lock` pins development dependencies. The wheel probe creates a
temporary environment outside the checkout and installs the wheel and allowed
runtime dependencies using binary wheels only, then replays the raw fixtures.
It verifies all three bundle manifests and all eight payloads, reporting their
content IDs/digests, import path, versions, platform and wheel hash. That
probe needs package-index access for installation; the admission API itself is
offline. Transitive `rpds-py` includes native Rust code, so wheel availability is
checked per platform even though this repository needs no Rust source build.

Root pytest discovers both `tests/` and `spec/tests/` with importlib mode.
The sdist includes canonical sources, checkers, tests and TOML policy inputs; the
wheel includes only the runtime package. For archive verification, unpack the
sdist in a neutral temporary directory, unset `VIRTUAL_ENV`, run `uv sync --locked`,
the same pytest/checker/generator commands there, and `uv build --wheel`. Pass
that rebuilt wheel to all four drivers above. CI performs this full sequence.

CI uses [native GitHub runners](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
for Ubuntu 24.04 x86-64 and macOS 15 ARM64 with Python 3.12 and 3.14. Each job sets
`UV_PYTHON` and checks the actual source/archive interpreter, overriding the
repository's 3.12 development default. Platform claims require
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
uv run --locked python tools/codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev4 render --context context.json --prompt prompt.txt
# Dispatch prompt.txt using the host's native agent mechanism; save its final JSON.
uv run --locked python tools/codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev4 admit --context context.json --prompt prompt.txt --result result.json
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

## Supervised native callback experiment

`tools/native_codex_smoke.py` installs the specified wheel in isolation, verifies
all exported runtime import paths, and runs a `-I` child from a neutral directory.
It uses the library's real bounded callbacks and agreement. The driver never
spawns agents: a Codex parent supervises a test-only file exchange.

```sh
uv run --locked python tools/native_codex_smoke.py --wheel dist/triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl --expected-version 0.1.0.dev4 --self-test
uv run --locked python tools/native_codex_smoke.py --wheel path/to/package.whl --expected-version 0.1.0.dev4 --config /absolute/config.json --run-dir /absolute/new-run
```

The self-test is **synthetic**, with three named review entries, concurrency two,
valid dissent and a separate ordinary investigation. It supplies no native proof.
A supervised config has exactly `mode` (`review` or `investigation`), a fresh safe
ASCII `run_id`, positive integer `max_concurrency`, `host`, and nonempty `requests`.
Each request has `entry` and the existing [Codex context](#codex-response-experiment);
investigations also require a nonempty `perspective`. Names/run IDs match
`[A-Za-z0-9][A-Za-z0-9_-]{0,127}`. The driver also rejects entry names that differ
only by letter case before creating artifacts, so its directory exchange works
consistently on case-sensitive and case-insensitive filesystems. Shared library
roster names remain case-sensitive. Entries must be enabled canonical Codex entries,
with explicit `codex.model`/`codex.reasoning` and timeout 1..3600 seconds. Formal
contexts share the complete basis, packet and scope, except `expected.leg_name`.
All inputs are preflighted before any request is published. Use canonical absolute
regular input paths and a new canonical run directory whose parent already exists
as a directory. No run or receipt reuse.

The exact `host` object is:

```json
{"supervisor":"codex-parent","native_tool":"collaboration.spawn_agent","supported_settings":[{"model":"gpt-6.1-sol","reasoning":"high"}],"capture_method":"parent-tool-final-string","cleanup":"interrupt-and-await-terminal","effective_settings":"UNEXPOSED"}
```

This is parent-supplied availability evidence. It does not measure effective
model settings or establish provider-enforced containment. Each requested pair
must appear in `supported_settings`. `manifest.json` binds config, wheel, package,
packets and prompts. Each invoke slot writes its exact `prompt.txt`, then atomically
publishes `request.json` last as readiness. For example (hash placeholders must be
replaced with the actual lowercase SHA-256 values):

```json
{"run_id":"native-correct-1","leg_name":"codex-1","mode":"review","entry":{"name":"codex-1","vendor":"codex","enabled":true,"acceptance":"required","timeout_s":300,"codex":{"model":"gpt-6.1-sol","reasoning":"high"}},"expected":{"review_id":"native-correct-1","family":"codex","content_digest":"<packet digest>","leg_name":"codex-1","attempt":1,"route":null},"requested_settings":{"model":"gpt-6.1-sol","reasoning":"high"},"prompt_path":"/absolute/new-run/codex-1/prompt.txt","prompt_sha256":"<prompt hash>","capture_method":"parent-tool-final-string","effective_settings":"UNEXPOSED"}
```

The parent dispatches that exact prompt with the requested settings. It saves the
original returned final string verbatim as UTF-8 `response.txt`, then atomically
renames a complete temporary receipt to `receipt.json`. Receipt fields are exact;
duplicate JSON members, unknown fields and binding/hash mismatches are refused:

```json
{"run_id":"native-correct-1","leg_name":"codex-1","request_sha256":"<hash of exact request.json bytes>","prompt_sha256":"<prompt hash>","response_sha256":"<hash of original response.txt bytes>","agent_id":"/root/native_correct_1","status":"completed","capture_method":"parent-tool-final-string","requested_settings":{"model":"gpt-6.1-sol","reasoning":"high"},"effective_settings":"UNEXPOSED","parent_spawned_at":1791760000.0,"parent_terminal_at":1791760040.0}
```

`agent_id` is the unique supervisor-visible canonical collaboration task identity;
opaque backend IDs remain unexposed. Times are finite Unix numbers recording
parent observations, with terminal >= spawn; they do not measure backend timing.
Terminal status is `completed`, `failed` or `cancelled`. Only a matching completed
receipt with the original regular response file can create native output, with
exit code `None`. No marker/fence removal, normalization or retries occur.

On cancellation, or a refused receipt before terminal acknowledgement, the
driver attempts to publish `cancel-request.json` once, containing `run_id`,
`leg_name`, `request_sha256` and `prompt_sha256`. The parent interrupts its owned
child when needed, awaits terminal status and posts the same fully bound terminal
receipt as cleanup acknowledgement. A completed receipt after cancellation is
cleanup evidence only. This cooperative wait can continue indefinitely if the
parent fails or posts malformed acknowledgement; the driver has no process or
native cancellation API. The parent must finish or interrupt/await every owned child.

For a cooperative CLI interrupt, the outer process forwards the first SIGINT to
its isolated inner driver and waits for it to exit. Repeated interrupts to the
outer process do not interrupt that cleanup. In `--self-test`, the synthetic
supervisor finishes the current scenario's receipt exchange before cancellation
propagates, so its temporary directory is cleaned along with the installed
environment. The normal supervised path still requires the parent's terminal
acknowledgement. Forced process death is outside this cooperative protocol,
and this behavior does not establish native backend termination.

If synthetic response or receipt publication fails, `--self-test` aborts its
known in-memory callbacks, drains its owned run and reports the original error.
This private synthetic cleanup path is unavailable to configured native runs,
which still require matching terminal acknowledgement.

Malformed or stale receipts retain the slot until a valid replacement establishes
terminal custody. The original refusal remains a failed observation; replacement
does not retry the review or turn it into approval. Terminal acknowledgement and
response admission are separate: after valid unique terminal metadata, unreadable,
invalid UTF-8 or hash-mismatched response bytes fail output admission but do not
require another terminal event. Cleanup records that response error and completes.

Receipt readiness uses `lstat()` so only `FileNotFoundError` means pending work.
Other filesystem errors retain the first refusal and enter the same cancellation
and acknowledgement path on every supported Python version. Present links still
reach the regular-file custody checks and are refused, including dangling links.

`report.json` retains ordered callback start/finish times and active/peak counts,
actual outcomes, observations and original artifact hashes. Bytes in dataclass
outcomes are represented by hash/length. Review reports retain the library's
actual admitted verdicts and agreement; investigations preserve ordinary response
files, report fresh integrity separately and contain no agreement field. Fresh
integrity rechecks config, wheel, packet, prompt, request and consumed artifacts.
A report file or exit zero means the experiment was recorded, not that agreement
passed. Callback overlap, observed native overlap and backend scheduling are
separate claims. Parent-captured final strings are not raw model wire bytes.
