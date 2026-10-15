# Independent host adoption

`triad-dispatch-lib` owns common contracts, prompt clauses, cases and deterministic
behavior. The Claude host (`triad-dispatch`) and Codex host
(`triad-codex-dispatch`) own native spawning, model/effort resolution, native
callback adapters, provider CLI setup, permissions, installation and configuration.
The four configurable routes and native callback interfaces remain supported.
Implement a shared semantic change once here with its specification, code and
cases; implement host mechanisms in their owning repository.

Library [PR #1](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1)
merged at `9489543ee24f338e9c6d0e3b032a1aa389986429`, preserving the reviewed
`2d1e62e7de6f33fa13a918a39579c6b5e74def00` tree. The independently released
[Codex host v0.2.561](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.561)
bundles library `0.1.0.dev3` from that source for JSON/verdict admission, roster
resolution and prompt rendering. Its scheduler and native adapters remain
host-owned. See its [pinned refresh record](https://github.com/codefoundry-io/triad-codex-dispatch/blob/c81c02984825af7dd1ec69a14af83f0ff18d0551/docs/verification/2026-10-15-library-refresh.md).
Claude adoption remains planned. Host releases, local installation, fresh-session
exposure and adoption of this unpublished `0.1.0.dev4` revision are separate
claims; a library change does not automatically update a consumer.

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
  A CLI re-exec boundary must also preserve cooperative cancellation and keep
  resources available until the supervised callback process terminates. The
  repository driver forwards one SIGINT to its isolated child and continues
  waiting through repeated outer interrupts; forced process death remains
  outside that cooperative guarantee.
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

## Claude host adoption assessment (2026-10-15)

The [request record](requests/2026-10-15-claude-host-adoption-requests.md)
retains the host leader's dev3 measurements and links the published scratch
scripts, captured outputs and input identities. The matching host implementation,
assets and measured roster input remain unpublished, so independent reproduction
is still incomplete. The reported 24 prompt comparisons used a scratch bundle
rebuilt from host assets; they do not establish parity with packaged dev3 prompts.
The 47 verdict decisions and latest six-leg merge (two disabled) remain attributed captures. The
reported wheel closure lacks published artifacts and establishes no new platform proof.

The amended leader-driven Claude first slice plans two functions:
`render_review_clauses` and `validate_binding` (`select_entries` drops disabled
entries the host keeps in its round record; the host reads its own vendored contract
copy, which stays its one bound copy with a byte-equality check against the vendored
bundle at round preparation). It will vendor with Git-blob-checked file hashes, recursively
extend exporter/toolkit coverage excluding bytecode, record bundle IDs and the
adoption record, and gate import/Registry failures as host faults. This is planned
host work, not released adoption evidence. Verdict admission and roster merging
remain host-owned pending the expanded diagnostic request (#3) and merge-only
roster request (#4); dev4's bounded L2 does not claim to unblock them.

The host's raw replacement/residual forms, case-folded directory-name checks and
reported 3600-second entry timeout remain host responsibilities. This project's
review timeout remains 2400 seconds. Claude withdrew its separate manifest/toggle
requests; the owner independently approved the additive library manifest API.

## Selective adoption and dependencies

`run_review` and `run_investigations` are optional callback coordinators. Hosts
can use parsing, validation, roster and rendering functions independently, and
can call `evaluate_agreement` without either coordinator. A leader-driven host
retains its own collection/custody lifecycle. Native spawning never moves into
this library. Future collection helpers must remain execution-model neutral.

Host-A Claude rendering includes the canonical raw-admission clauses; host B
uses its structured-CLI profile. This fixed selection does not expose a generic
raw-admission toggle. `agy_hook_active` remains a separate Google/AGY/A control.

Install with Python >=3.12, jsonschema>=4.26,<5 and referencing>=0.37,<1.
Ubuntu's stock packages may be older; they are not the supported runtime floor.
Use an isolated environment or host-owned vendoring/wheel installation that
actually satisfies the package metadata. Preserve offline reference refusal;
do not remove Registry merely to support an older distribution package.

For offline distribution, obtain the complete allowed binary-wheel dependency
closure separately for each supported OS, architecture, Python version and ABI.
Record filenames/versions/hashes and verify installation/import plus the host's
adoption tests on that native combination. `rpds-py` has native code: a manylinux
CPython 3.12 wheel set is not macOS or Python 3.14 evidence. Installation and
dependency packaging remain host-owned; runtime admission does not use a network.

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
