# Independent host adoption

`triad-dispatch-lib` owns common contracts, prompt clauses, cases and deterministic
behavior. The Claude host (`triad-dispatch`) and Codex host
(`triad-codex-dispatch`) own native spawning, model/effort resolution, native
callback adapters, provider CLI setup, permissions, installation and configuration.
The four configurable routes and native callback interfaces remain supported.
Implement a shared semantic change once here with its specification, code and
cases; implement host mechanisms in their owning repository.

Neither host has completed released adoption of this consolidation. Codex has a
separate source-adoption candidate; release/installation follow the library PR
merge as separately scoped work. Host versions and release dates are independent;
hosts may adopt different compatible library releases. The unpublished library
`0.1.0.dev3`, candidate schema status and historical spec tags are distinct.

## Adoption record

Each host should retain the following with its adapter/release evidence:

- Exact library package version, artifact SHA-256 and source/build commit when known.
- All consumed bundle names and `contract_id` values, plus the verified payload
  digest maps. An ID identifies one bundle, not every normative document.
- Host adapter version/commit and independent host release version.
- Supported routes, platform/Python combination, native controls, explicit host
  exceptions and case/conformance results with unrun checks named.

`spec/import-origin.json` records original import ancestry only. It does not pin
newly edited guidance. Legacy schema `$id` values remain wire identities even
though authoring moved. Runtime manifests have exactly six fields:
`schema_version`, `source_repository`, `source_path`, `status`, `sha256`,
`contract_id`; release provenance belongs outside them. Content integrity does
not prove artifact authenticity. A live main URL never changes adopted behavior.

## Required adapter contracts

The [library conformance map](../spec/reference/library-conformance.md) identifies
implemented portions and tests; it is not full host conformance. Use the
[Python API contract](../spec/reference/library-api.md) for exact signatures,
result fields, emitted errors, input copies and shallow result mutability.

- **AGY recovery (C23 / R-CONTAIN):** `agy-stream-json` intentionally accepts one
  SUCCESS terminal only. Preserve the host's existing same-run ERROR/exit0 recovery
  decision: ordered failed-then-successful finish evidence, read/tool/error checks,
  and the adopted host's exit/auth/timeout/transport rules. Do not feed a recovered
  raw ERROR stream directly to the strict carrier or admit arbitrary ERROR results.
  After establishing recovery, an adapter may pass the original final verdict JSON
  through `native-final` with truthful host-observed terminal metadata and the same
  Google/AGY binding. This does not move execution or custody into the library.
  Exercise positive recovery, missing/reversed success, invalid answer, other
  execution errors and retained binding/terminal refusals before adopting that path.
- **Integrity and host faults (R-AGREE):** `run_review` is a callback coordinator,
  not a complete collector. Its ordinary integrity exceptions, self-cancellation
  and non-bool values become `integrity_ok=False`; it does not expose why.
  The host must separately preserve inability to launch/finish its check and
  abort collection without a collection record for that host fault. Do not infer
  that a check completed from `ReviewRun` alone. Packaged-contract `ContractError`
  separately propagates after callback cleanup. Check deadlines and diagnostics
  remain adapter-owned; `integrity_check` has no library timeout.
- **Failure classification:** typed carrier guards are not the R-AUTH/R-CLASSIFY/
  R-TOKENS classifier. Keep measured vendor-error carriers, authentication STOP
  precedence, token mapping and repair analysis in the host until a separately
  specified extraction. Do not replace these with verdict-text keyword matching.
- **Cancellation custody:** callbacks must retain each published native request
  until terminal acknowledgement, including cancellation-publication errors and
  failed receipt readiness/read operations or malformed/stale acknowledgement
  input. Separate matching terminal metadata
  from response admission: bad response bytes after an established terminal
  acknowledgement still fail admission, but do not undo observed termination.
  An expired review timeout starts cancellation; it is not proof of native cleanup.
  A late affirmative response remains timed out and cannot approve.
- **Dissent records (R-AGREE):** the reducer retains valid negative verdicts and
  emits `negative_verdict`; it does not classify a Minor-only negative as a
  selection deviation. The host collector/leader must preserve that required
  deviation record separately while keeping the negative ballot unchanged.
- **Budgets and results:** preflight and invocation each receive the full entry
  timeout after acquiring their own slot. Queue time, cooperative cleanup and
  integrity checking are not covered by an end-to-end library deadline. Frozen
  result dataclasses contain mutable dictionaries; `agreed` is a computed snapshot.
  Preserve collected evidence and do not mutate it to manufacture a new decision.

The generic `native-final` carrier trusts adapter-supplied execution observations
for any family and validates original JSON, schema and all six bindings. It
neither attests runtime model identity nor makes failed transport successful.
Native spawning, read containment, packet/receipt seals and installer preservation
must remain covered by host tests alongside the mapped library tests.

## Generated content and installers

Edit canonical runtime sources only in `spec/contracts/` and `spec/prompts/`.
Generate `src/triad_dispatch_lib/data/` with `tools/sync_spec_assets.py --write`;
verify with `--check`. Do not copy divergent common orchestration into either
host. Small native adapters consume the same common implementation and clauses.

For the Claude installer, retain a managed-file hash ledger for installed common
assets and separately identify Claude-native instructions/settings. For the Codex
installer, retain the same kind of ledger for common plugin assets and separately
identify Codex-native dispatch/configuration. Each ledger should name the source
library/bundle version, installed relative path and hash last written by that
installer. It is installer metadata, not an extra runtime-manifest field.

Before either installer replaces or removes a managed file, compare its current
hash with the ledger. If the user changed it, preserve it and report the conflict
with the proposed replacement; do not overwrite, reset or delete user content.
Update the ledger only after successful writes, retain unrelated files and
support recovery from interrupted upgrades. These are recommendations for future
host work; this library slice changes no installer or global installation.

## Verification boundaries

Source tests, authoring validation, deterministic generation, unpacked-sdist
tests and isolated wheel drivers establish static/synthetic library behavior.
The installed probe verifies verdict, roster and prompt bundle identities and
all eight payload digests from an isolated interpreter. Four-route synthetic
responses exercise carriers and shared orchestration; they do not establish
provider authentication, permissions, effective model controls or host adoption.

Each host port additionally needs its own installer preservation/upgrade checks,
native route execution and cancellation/cleanup evidence on the claimed platform,
followed by its separate review and release. Earlier native Codex observations
remain evidence for their recorded dev2 build only. This slice does not run real
providers, publish packages, merge PRs, archive the old repository or port hosts.
