# Claude host adoption: measured facts and library change requests

Author: the claude host (A) leader, 2026-10-15 (amended the same day after the claude
host's four-leg review round r1; the amendments are marked). Library pin under
discussion: `0.1.0.dev3` at `2d1e62e7de6f33fa13a918a39579c6b5e74def00` (merged as
`9489543e`). This document records what the claude host measured while assessing
adoption and asks for the library changes that let one library carry the rules the
three leader tasks (codex host B, claude host A, the Argon work on the Google routes)
implement separately today. It changes no runtime code. The owner decides the unit
in which the requests land.

## 1. Facts measured on the claude host

All runs were throwaway and read-only toward the library; nothing in either host
changed. Commands and numbers are in the claude host's review record
(`docs/reviews/2026-10-15-triad-dispatch-lib-pr1-claude-host-review.md` § 6 and
§ 6.1 in `codefoundry-io/triad-dispatch`); the host basis is its implementation
branch `impl/claude-host-2026-10`.

- **Dependency floor (S1).** With `jsonschema==4.10.3` and `referencing==0.31.0`
  pinned (the Ubuntu 24.04 apt versions, packages.ubuntu.com read 2026-10-15),
  `parse_json` and `load_roster_contract` work; `validate_binding`,
  `resolve_roster` and `render_review_clauses` raise
  `TypeError: ... unexpected keyword argument 'registry'` (the argument exists since
  jsonschema 4.18.0). Library tests on that environment: 165 failed, 101 passed.
  The manylinux wheel closure for the declared floor is six wheels, 620 KB.
  Amended: jsonschema 4.10.3's default `RefResolver.resolve_remote` retrieves
  remote references (measured); the claude host's `$defs` re-rooting therefore
  does NOT block remote `$ref` the way `registry=Registry()` does.
- **Prompt rendering parity (S2').** The prompt bundle regenerated from the claude
  host's vendored prompt bytes (candidate `3afc4d7e`, one clause line, one
  leg-claude line and one exit-tokens line behind the library's spec); 24 host-A
  profiles (codex / claude / google×agy,gemini × formal-plan / implementation-review
  / pre-merge × web on/off) rendered by `render_review_clauses(host="A", ...)` and
  by the host's own `render(family, ctx)` with RAW replacement strings: 24/24
  byte-identical; agy profiles match with `agy_hook_active=True` (the host always
  renders its hook clause for agy). The investigation web-evidence suffix is
  identical for agy and gemini. Not measured: equality with the unmodified release
  bundle (pending the host's spec re-vendor at the pin).
- **Verdict admission parity (S3').** 47 reply cases (8 valid, 33 invalid, 6 binding
  mismatches) through the host admitter and `validate_verdict`: 47/47 the same
  accept/reject decision. NaN and 1e999 differ only in the refusing stage (host:
  schema; library: parser). Reason text was not compared; the host keeps its
  field-naming binding reasons and schema-location reasons over the library's
  parse and schema validity.
- **Roster parity (S4').** `resolve_roster(host defaults, project override)` and the
  host's merge produce byte-identical legs (5 entries). Kept in the host: Google
  route resolution, capability checks (which refuse `claude.model` and
  `claude.effort`, R-ROSTER host A paragraph), block and effort checks, drift
  warnings, and the refusal of case-folded duplicate names (the library accepts
  `codex` and `Codex` together; macOS volumes collide on the entry directories).
- **Execution model.** The claude host has no long-running host process: the
  leader runs the dispatch lines `prepare` prints, the claude leg is an in-session
  agent spawn, and `collect` folds the attempts afterwards. `run_review` and
  `run_investigations` therefore do not apply on host A. Amended twice: the first
  adoption slice calls `render_review_clauses` (the bound prompt bytes, with the
  host's clause manifest computed over the same canonical bytes), `validate_binding`,
  `load_roster_contract` and `select_entries`. Verdict admission and roster merging
  stay whole in the host until L2 and L13 exist (round r2 of the host's review:
  the host's admitter names the duplicated member, the JSON-syntax detail that gates
  its entity-unescape retry and the deepest schema location — fixed codes cannot carry
  them without duplicating schema validation, which the handoff forbids; the host's
  roster checks run on the merged legs BEFORE final validation to name an inherited
  vendor block, which `resolve_roster` validates away in one call). Not called:
  `parse_json`, `validate_verdict`, `resolve_roster`, `render_investigation_prompt`
  (the host's wrappers load its clause renderer by file path and need the clause
  alone), `extract_final`, `admit_output`, `render_data`, `evaluate_agreement`,
  `run_review`, `run_investigations`.
- **Distribution.** The claude host will adopt by vendoring the package under its
  skill `lib/` with an adoption record (source commit, version, per-file sha256
  checked against the library's git blobs at the pin, the three bundle
  `contract_id`s), as the codex host did in `triad-codex-dispatch#44`, and will add
  the six wheels to its existing Ubuntu offline wheel set. Amended: its exporter
  and its round toolkit map cover only top-level `lib/` files today and are
  extended in that slice; a capability gate wraps the package import itself (an `ImportError`, e.g. a
  missing `referencing` beside apt's jsonschema) and the `registry=` probe, and maps
  a library `TypeError` or `ContractError` to the host-fault exit.
- **Host-native forms (amended).** Raw replacement strings and the host's brief
  fence for the residual are host-native forms under R-CONTEXT ("any framing the
  host adds ... leaves the exact value recoverable"); the library's only
  constraint (single-line, caller-encoded) is met. No library change is asked.

## 2. What the claude host keeps

Native claude leg (agent spawn, shipped presets), Google route resolution and
its skip-and-log policy, capability / block / duplicate-name checks and drift
warnings, dispatch-line rendering and the executed-command receipt comparison,
the vendor wrappers (spawn, capture, timeout, classification, repair loop,
audit), AGY containment (hook, read-audit gate, census collection and the
finish-recovery judgement), packet lifecycle, seals and the toolkit map, the
plugin exporter, the user-side installers and tests. These touch processes,
files, permissions or the leader session, or are recorded host policy
(`spec/units.json`), or are responsibilities `spec/reference/library-api.md`
§ Internal mechanisms and host boundary assigns to hosts.

## 3. Requests

Amended after the review round: the earlier single list claimed every item only
relocated an existing rule. Four of them change the library's documented host
boundary and are therefore design decisions for the owner and the library, not
relocations. The split below keeps that distinction. "A" cites the claude host's
file, "B" the codex host's, "spec" the normative anchor. Tests and a specification
row are expected with each item; the claude host refreshes its pin afterwards.

### 3a. Pure-function moves inside the current boundary

| # | Request | A today | B today | Spec | Proposed shape |
| --- | --- | --- | --- | --- | --- |
| L2 | Structured refusal reasons without payload values: the schema violation's location and the mismatched binding field name | `lib/verdict_v2.py` `_schema_reason`, `_binding_reason` (the leader branches on which binding broke) | own | R-BIND, R-DIAG | `AdmissionError.field` / `.path` (names only, never values). The Argon handoff asks for the same |
| L3 | Receipt SHAPE validation (C9 `contracts/receipt-fields.json`). The executed-command comparison (`wrapper_cmd` equals the recorded argv) is attempt currency and stays in the host | `lib/collect_v2.py` (part) | `record_cli_attempt` (part) | C9 | `validate_receipt(doc)` |
| L5 | Placeholder preflight (an unresolved `<...>` value is refused) and opaque transport of model/effort pins. Note: the codex host's adoption design keeps its placeholder preflight host-side, so this is optional for B | `lib/roster_v2.py` | `bin/review_roster.py` placeholder preflight | R-MODEL, C18, C34 | `check_opaque_pins(roster)` after `resolve_roster` |
| L13 | Roster merge-only seam (added after round r2): a function that merges defaults and a validated override by name WITHOUT the final resolved-roster validation, so a host can run its own checks on the merged legs first (the claude host names an inherited vendor block before the schema reports only the missing one; `t12` axis 24), then calls the final validation itself | `lib/roster_v2.py` `_merge_leg` + `_check_blocks` ordering | — | R-ROSTER, C12 | `merge_roster(defaults, overrides) -> dict` (merged, unvalidated) and `validate_resolved(roster)`; `resolve_roster` stays as their composition |
| L10 | Dependency floor | — | — | R-PLATFORM (Ubuntu 24.04) | Default: record the floor as a platform fact that each host meets with wheels. If the library lowers the floor, it must add an explicit no-retrieval mechanism (refuse any `$ref` not beginning with `#` when a packaged schema is loaded) and a CI leg on jsonschema 4.10.3; re-rooting `$defs` alone does not block retrieval |

### 3b. Boundary changes — design decisions for the owner and the library

`spec/reference/library-api.md` states that hosts retain "AGY recovery and failure
classification, packet/attempt sealing and currency, fresh integrity checks,
collector host-fault handling, deviation evidence". Each request here would move
part of that sentence into the library; it is raised as a decision, not asked as
a relocation.

| # | Request | A today | B today | Boundary sentence touched | Proposed shape if accepted |
| --- | --- | --- | --- | --- | --- |
| L1 | Round collection reducer: per-entry attempt states (valid, invalid, failed-to-run, missing, skipped) plus the integrity result fold into AGREED / BLOCKED / INCOMPLETE; host faults separated from outcomes; a Minor-only negative yields the selection-deviation record | `lib/collect_v2.py` | `bin/review_round_v2.py collect` | collector host-fault handling, deviation evidence | State input instead of only an output map; a distinct exception for a host fault; the deviation record returned. Execution-model neutral (callable by the coordinator and by a leader-driven host) |
| L4 | Exit-token and vendor-failure-line membership (C8, R-CLASSIFY): table lookup, no judgement. Amended: the signature carries the CLI identity, because each sentence applies only to its emitting CLI and the table rows carry `cli` | `3rd-Agent/wrappers/_common.py` tables + membership test `t55` | `bin/_common.py` | failure classification | Ship the two contract JSON files as a verified bundle; `classify_sentence(cli, text)`, `token_exit(token)`; cross-CLI negative vectors |
| L8 | AGY finish resubmission and denied-before-execution judgement from structured stream fields only | `3rd-Agent/wrappers/antigravity_wrapper.py` `_census` (part) | none (B refuses every non-SUCCESS terminal, DL-113) | AGY recovery | `recover_agy_finish(events) -> (admitted, answer_index, reason)` beside the strict carrier. Single-host today; drop if B keeps DL-113 |
| L6 | Producer schema projection: the output schema a host hands the vendor, derived from `leg-verdict.schema.json`. Moved here after round r2: the host's projection is a provider-compatibility transform (six steps, each forced by a live vendor probe), the codex host keeps its own pydantic projection, and "all hosts send the same bytes" is a new requirement | `lib/roster_v2.py` `projected_schema_text()` | pydantic projection in `bin/verdict_v2.py` | provider/version compatibility | `producer_schema()` only with a specification sentence making the bytes common |
| L9 | Canonical serialization of the bound-basis digest members | `_v2_config_digest`, delivery record | `basis-v2.json` + `.sha256` | sealing and currency; R-PREPARE allows re-deriving or hashing, so "the same digest on every host" is a new requirement | `basis_digest(members)` |

### 3c. Single-host or documentation

L7 (rendered-clause manifest; only the claude host binds it) and L11 (the host-A
raw-admission clause toggle) are single-host and are not requested. L12 is a
documentation request: state in `library-api.md` that the coordinator is one
optional execution model and that any collection reducer is model-neutral.

Suggested order: L10 (as a fact), L2, L13, L3, L5; then, after the owner's decision,
L1, L4, L6, L9, L8. L2 and L13 block the claude host's second slice (verdict admission
and roster merging) and are also filed as issues.

## 4. Specification items

- Record the host A adoption facts of § 1 (this PR adds them to
  `docs/host-adoption.md`; a dev-log row points here).
- R-PREPARE: the round toolkit map includes the vendored package files (with
  bytecode excluded) and the three bundle `contract_id`s (with L9 if accepted,
  otherwise as a host fact).
- `spec/units.json`: as each 3a item lands, name the library as the implementing
  location of that surface (R-PARITY `common` name).
- The scalar-replacement encoding form and the residual-data form are host-native
  under R-CONTEXT and are not requested or decided here.

## 5. Out of scope

No coordinator semantics change, no host code, no provider behavior, no new rule.
The claude host's first adoption slice (vendoring with the identity proof, the
exporter and toolkit-map extensions, the spec re-vendor at the pin, the import
capability gate, the eight functions, regression tests) proceeds independently of
these requests; its second slice replaces the duplicated host code once the 3a
items exist and the 3b decisions are made.
