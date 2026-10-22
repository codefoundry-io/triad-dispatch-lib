# Independent host adoption

For library acquisition, see [obtain and install the library](installing.md):
exact-source/release selection, artifact verification, isolated installation,
public API smoke and platform dependency requirements.

`triad-dispatch-lib` owns common contracts, prompt clauses, cases and deterministic
behavior. The Claude host (`triad-dispatch`), Codex host
(`triad-codex-dispatch`) and AGY host (`agy-triad-dispatch`) own native spawning,
model/effort resolution, native
callback adapters, provider CLI setup, permissions, installation and configuration.
The four configurable routes and native callback interfaces remain supported.
Implement a shared semantic change once here with its specification, code and
cases; implement host mechanisms in their owning repository.

## Current recorded adoption (2026-10-22)

All three pinned repository manifests record library `0.1.0.dev4`, source
`087af94a7078de0ae9701fb057840b5492f51f66`, wheel SHA-256
`c5bfdf10c4ce81f431ec7f77106e4d77b1556ac9c7b6b01bdb6616f988e8b2cc`,
and the same four runtime bundle IDs:

| Host | Pinned repository evidence | Follow-up proposal |
| --- | --- | --- |
| Codex | [Manifest at `db0fe780`](https://github.com/codefoundry-io/triad-codex-dispatch/blob/db0fe780ff85483a98bafd3a1668dd8b7ab2f90f/contracts/library-adoption.json) | [Draft PR #46](https://github.com/codefoundry-io/triad-codex-dispatch/pull/46) |
| Claude | [Export manifest at `c02cd976`](https://github.com/codefoundry-io/triad-dispatch/blob/c02cd9769880dc14b98f54f4bbe70a669b9b8611/skills/triad-cross-family-review/lib/lib-adoption.json) | [Draft PR #1](https://github.com/codefoundry-io/triad-dispatch/pull/1) |
| AGY | [Manifest at `aa4b8db0`](https://github.com/codefoundry-io/agy-triad-dispatch/blob/aa4b8db07881cf299ec174e2f23c310196975600/contracts/library-adoption.json) | [Draft PR #2](https://github.com/codefoundry-io/agy-triad-dispatch/pull/2) |

These are recorded provenance checks, not fresh verification of each vendored
file, every API integration, installation or live-provider behavior. The proposal
PRs contain documentation only. Claude implementation belongs in its owning
`codefoundry-io/triad` source before export; AGY currently uses default branch
`feat/agy-triad-dispatch`. AGY's adoption does not add a new library host-profile
literal: its proposed work preserves the existing `host="B"` integration.

The existing `.path`, `.missing`, `.document`, `validate_transport_receipt` and
`ReceiptError` APIs are already in published dev4. Issue #9 remains partial/open
for optional diagnostics; none of these manifests implies host-message parity.
See the [triage and release plan](requests/2026-10-22-triage-and-release-plan.md).

## Earlier integration checkpoints

The following records describe their original integration boundaries; current
recorded adoption is listed above.

Library [PR #1](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1)
merged at `9489543ee24f338e9c6d0e3b032a1aa389986429`, preserving the reviewed
`2d1e62e7de6f33fa13a918a39579c6b5e74def00` tree. The independently released
[Codex host v0.2.561](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.561)
bundles library `0.1.0.dev3` from that source for JSON/verdict admission, roster
resolution and prompt rendering. Its scheduler and native adapters remain
host-owned. See its [pinned refresh record](https://github.com/codefoundry-io/triad-codex-dispatch/blob/c81c02984825af7dd1ec69a14af83f0ff18d0551/docs/verification/2026-10-15-library-refresh.md).
At that checkpoint Claude adoption was planned and dev4 was unpublished.
Host releases, local installation and fresh-session exposure remain separate
claims; a library change does not automatically update a consumer.

The 2026-10-16 follow-up adds `RosterError.path/missing/document` and
`validate_transport_receipt`/`ReceiptError`, retaining `0.1.0.dev4`. These are
library contracts whose host adoption was tracked separately. See the
[API](../spec/reference/library-api.md#rosters-and-contract-loading) and
[contribution dispositions](requests/2026-10-16-adoption-followups-disposition.md).
Issue #9 remains partial: unknown-key spelling is declined for this slice,
without a permanent prohibition or host-message parity claim.

Library [PR #2](https://github.com/codefoundry-io/triad-dispatch-lib/pull/2)
merged at `ee8b4b4ab3c1440788733931874047a1821ee08e`, after R5 `AGREED` on
reviewed head `830942e05d3681e7ded04a91d60850d18ea00d10`. Subsequent
[main CI run 38690043657](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/38690043657)
succeeded. That integration establishes neither a package release nor new host adoption.

## Adoption record

Each host should retain the following with its adapter/release evidence:

- Exact library package version, artifact SHA-256 and source/build commit when known.
- All consumed bundle names and `contract_id` values, plus the verified payload
  digest maps. An ID identifies one bundle, not every normative document.
- Host adapter version/commit and independent host release version.
- Supported routes, platform/Python combination, native controls, explicit host
  exceptions and case/conformance results with unrun checks named.

The release-notice tool optionally reads `contracts/library-adoption.json` to
report a consumer's previously recorded library version. When present, it must be
a regular JSON file containing an object with top-level `name` equal to
`"triad-dispatch-lib"` and a nonempty string `version`; additional fields are
allowed. An absent file reports `unrecorded`, not proof of no adoption. An existing
incompatible record fails notice delivery only for that target; other targets
continue independently. This describes existing notice metadata, not a new host
schema or a requirement to port or create a record.

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
- **Transport shape (C9):** pass only the parsed nested `transport` object to
  `validate_transport_receipt`. Shape does not verify invocation identity,
  `wrapper_cmd` equality, route/binary observations, attempt currency, stdin or
  execution truth, envelopes, ownership, seals, reads or collection. Keep those
  checks in the host; a shape-valid receipt cannot approve a review.
- **Roster diagnostics:** `.document` names the evaluated defaults/override/
  resolved document, not merged-property origin. `.path` contains schema
  evaluation metadata, with possible omitted `$ref`/`if` hops; `.missing` is
  selected-required-only and may remain `None` for missing route blocks under
  `anyOf`. Preserve the host's formatting and reduced-diagnostics deviation.
  Exception contexts/tracebacks may retain input references even when the public
  attributes and message are value-free.
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

PR #11's restored lock and tests at A `26e80918` remain attributed observations,
without independently verified source. Host A owns its installer lock. Host B
should check overlapping bootstrap, `scripts/bootstrap.sh --remove` and ordinary
configuration readers against the same target. This is guidance consistent with
R-THREAT's machine-level concurrency, not proof of a B race or a lock-transplant
requirement. See the [scoped disposition](requests/2026-10-16-adoption-followups-disposition.md#pr-11-host-concurrency).

## Claude host adoption assessment (2026-10-15)

The [request record](requests/2026-10-15-claude-host-adoption-requests.md)
retains the host leader's dev3 measurements and links the published scratch
scripts, captured outputs and input identities. The matching host implementation,
assets and measured roster input remain unpublished, so independent reproduction
is still incomplete. The reported 24 prompt comparisons used a scratch bundle
rebuilt from host assets; they do not establish parity with packaged dev3 prompts.
The 47 verdict decisions and latest six-leg merge (two disabled) remain attributed captures. The
reported wheel closure now has a published inventory and hashes, but no wheel binaries
or exact download/install command; it establishes no new native platform proof.

The amended leader-driven Claude first slice plans two functions:
`render_review_clauses` and `validate_binding` (`select_entries` drops disabled
entries the host keeps in its round record; the host reads its own vendored contract
copy, which stays its one bound copy with eight mapped payload-pair byte comparisons
against the vendored bundle at round preparation, as reported by the host). It will vendor with Git-blob-checked file hashes, recursively
extend exporter/toolkit coverage excluding bytecode, record bundle IDs and the
adoption record, and gate import/Registry failures as host faults. This is planned
host work, not released adoption evidence. The host also reports a preparation-time
text-parity gate before using its own manifest; a later slice plans `with_manifest=True`
adoption and removal of that render core. These unpublished implementation reports
have not been independently verified. Verdict admission and roster merging remain
host-owned until independently adopted. The owner settled issue #3/#4 roster and
admission decisions in the
[approved adoption APIs](design/2026-10-15-adoption-apis.md): the library now
implements `merge_roster`, `validate_resolved` and safe `.missing` for the selected
canonical required violation. Duplicate `.member` disclosure is declined; the
host retains its own strict duplicate parser as a documented deviation. The
separate [issue #5 boundary proposals](design/2026-10-15-adoption-boundary-proposals.md)
remain proposals only, not approved owner decisions. The
requester accepted dev4 `.field`/trusted schema `.path` and withdrew `.detail`,
instance pointers and the duplicate pre-pass; see the
[request sync evidence](verification/2026-10-15-provenance-request-sync.md).
At that 2026-10-15 checkpoint, these settled library APIs did not establish host
adaptation, full parse delegation or released adoption, and dev4 remained
unpublished and source-pinned. Combined verification is recorded separately in
the [adoption API record](verification/2026-10-15-adoption-apis.md); current release
and adoption evidence is at the top of this guide.

The host's raw replacement/residual forms, case-folded directory-name checks and
reported 3600-second entry timeout remain host responsibilities. This project's
review timeout remains 2400 seconds. Claude withdrew its separate manifest/toggle
requests; the owner independently approved the additive library manifest API.

Adopted state (2026-10-18, LIB-ADOPT slices 1a / 1b / 2 on `codefoundry-io/triad`, the host
repository's ledger `docs/reviews/2026-10-17-lib-adopt-residuals.md`): the claude host vendors
v0.1.0.dev4 from the verified wheel (`triad_dispatch_lib-0.1.0.dev4-py3-none-any.whl`, sha256
`c5bfdf10c4ce81f431ec7f77106e4d77b1556ac9c7b6b01bdb6616f988e8b2cc`, 47734 bytes) into
`.claude/skills/triad-cross-family-review/lib/triad_dispatch_lib/` beside its adoption record
`lib/lib-adoption.json` (the pin, the file digests, the nine spec↔data pairs, the spec map; no
repository-root record — the record sits with the package) and the MIT notice; the exporter ships
the three byte for byte and the toolkit map refuses a changed package file as host fault 64. Functions
consumed: `render_review_clauses` (`host="A"`, `with_manifest=True`; behind the host's data-side and
spec-side identity checks), `validate_binding`, `validate_verdict`, `merge_roster`, `validate_resolved`,
`validate_transport_receipt`. Recorded deviations: the host's own duplicate-member name scan after the
library's `duplicate_member` (§ 5.22); `invalid_expected` classified as host fault 64 (§ 5.23); the host's
roster checks (required fields, vendor blocks, case-fold duplicates, capabilities, the Google route) on
top of `merge_roster` / `validate_resolved` (§ 5.24). Recorded behaviour changes on the host: a non-finite
number in a reply is exit 2 (was 1); a malformed expected pair beside an unparseable reply is 64 (was
2); a hand-edited override with a duplicated key or a non-finite number is refused; an unknown roster key
is refused by its schema path; a run-log whose transport object is absent or violates
`receipt-fields.json` no longer counts. Platform gate (the exported plugin from a neutral directory,
both admission paths and the planted wrapper receipt through `collect`): GATE OK on macOS arm64 (brew
Python 3.12), Ubuntu 24.04 aarch64 and Ubuntu 24.04 x86_64 (Docker, the `~/.venvs/triad` closures
recorded in the host's `docs/lib-dependency-closures.md`), recorded in the host's
`docs/reviews/inputs/2026-10-17-lib-adopt/platform-gate.md`. Host adapter heads: 1a merged into `main`
at 45a2b1c1, 1b at 6fd777b8, slice 2 agreed at 024b1f9e; exported plugin versions 0.2.1959 (1b) and
0.2.1971 (slice 2). Independent reproduction of the host's runs stays outside this repository.

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
The installed probe verifies verdict, roster, prompt and receipt bundle identities,
all nine payload digests and the new API/diagnostic refusals from an isolated
interpreter. The runtime contains four schemas in four bundles; sixteen other
canonical contracts remain source-only (also retained in the sdist). Four-route synthetic
responses exercise carriers and shared orchestration; they do not establish
provider authentication, permissions, effective model controls or host adoption.

Each host port additionally needs its own installer preservation/upgrade checks,
native route execution and cancellation/cleanup evidence on the claimed platform,
followed by its separate review and release. Earlier native Codex observations
remain evidence for their recorded dev2 build only. This slice does not run real
providers, publish packages, merge PRs, archive the old repository or port hosts.
