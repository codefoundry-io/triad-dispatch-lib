# Claude host adoption: measured facts and library change requests

Author: the claude host (A) leader, 2026-10-15. Library pin under discussion:
`0.1.0.dev3` at `2d1e62e7de6f33fa13a918a39579c6b5e74def00` (merged as `9489543e`).
This document records what the claude host measured while assessing adoption and
asks for the library changes that let one library carry the rules all three leader
tasks (codex host B, claude host A, the Argon work on the Google routes) implement
separately today. It changes no runtime code. Each request names the rule the
specification already states; none asks for a new rule. The owner decides the
unit in which the requests land.

## 1. Facts measured on the claude host

All runs were throwaway and read-only toward the library; nothing in either host
changed. Commands and numbers are in the claude host's review record
(`docs/reviews/2026-10-15-triad-dispatch-lib-pr1-claude-host-review.md` § 6 in
`codefoundry-io/triad-dispatch`).

- **Dependency floor (S1).** With `jsonschema==4.10.3` and `referencing==0.31.0`
  pinned (the Ubuntu 24.04 apt versions, packages.ubuntu.com read 2026-10-15),
  `parse_json` and `load_roster_contract` work; `validate_binding`,
  `resolve_roster` and `render_review_clauses` raise
  `TypeError: ... unexpected keyword argument 'registry'` (the argument exists since
  jsonschema 4.18.0). Library tests on that environment: 165 failed, 101 passed.
  The manylinux wheel closure for the declared floor is six wheels, 620 KB
  (jsonschema, jsonschema_specifications, referencing, rpds_py cp312, attrs,
  typing_extensions).
- **Prompt rendering parity (S2).** The prompt bundle regenerated from the claude
  host's vendored prompt bytes; 30 host-A profiles (codex / claude / google×agy,gemini
  × formal-plan / implementation-review / pre-merge × web on/off × agy hook on/off)
  rendered by `render_review_clauses(host="A", ...)` and by the host's own renderer
  with RAW (not JSON-encoded) replacement strings: 30/30 byte-identical. The
  investigation web-evidence suffix is identical for agy and gemini.
- **Verdict admission parity (S3).** 47 reply cases (8 valid, 33 invalid, 6 binding
  mismatches) through the host admitter and `validate_verdict`: 47/47 the same
  accept/reject decision. NaN and 1e999 differ only in the refusing stage (host:
  schema; library: parser).
- **Roster parity (S4).** `resolve_roster(host defaults, project override)` and the
  host's merge produce byte-identical legs (5 entries). The host's Google route
  resolution and its capability checks (which refuse `claude.model` and
  `claude.effort`, R-ROSTER host A paragraph) have no library counterpart and stay
  in the host.
- **Execution model.** The claude host has no long-running host process: the
  leader runs the dispatch lines `prepare` prints, the claude leg is an in-session
  agent spawn, and `collect` folds the attempts afterwards. `run_review` and
  `run_investigations` therefore do not apply on host A; the host adopts 12 of the
  14 package-root functions.
- **Distribution.** The claude host will adopt by vendoring the package under its
  skill `lib/` with an adoption record (source commit, version, per-file hashes,
  the three bundle `contract_id`s), as the codex host did in
  `triad-codex-dispatch#44`, and will add the six wheels to its existing Ubuntu
  offline wheel set. Its round toolkit map (sha256 of every file under `lib/`,
  compared at collect and retry) then covers the vendored package; the bundle
  `contract_id`s are added to that map.

## 2. What the claude host keeps

Native claude leg (agent spawn, shipped presets), Google route resolution and
its skip-and-log policy, capability checks, dispatch-line rendering and the
executed-command receipt comparison, the vendor wrappers (spawn, capture,
timeout, classification, repair loop, audit), AGY containment (hook, read-audit
gate, census collection), packet lifecycle and seals, the plugin exporter and
tests. These touch processes, files, permissions or the leader session, or are
recorded host policy (`spec/units.json`).

## 3. Requests: rules both hosts implement separately today

Each item is a pure function over data, with no process, file custody or
provider access, inside the boundary `spec/reference/library-api.md` § Internal
mechanisms and host boundary already draws. "A" cites the claude host's file,
"B" the codex host's, "spec" the normative anchor. Tests and a specification row
are expected with each item; the claude host refreshes its pin afterwards.

| # | Request | A today | B today | Spec | Proposed shape |
| --- | --- | --- | --- | --- | --- |
| L1 | Round collection reducer: per-entry attempt states (valid, invalid, failed-to-run, missing, skipped) plus the integrity result fold into AGREED / BLOCKED / INCOMPLETE; host faults are separated from outcomes; a Minor-only negative yields the selection-deviation record | `lib/collect_v2.py` (folding part) | `bin/review_round_v2.py collect` | R-AGREE, R-ROSTER | Extend `evaluate_agreement` (or add `collect_round`) to accept per-entry states instead of only an output map; raise a distinct exception for a host fault; return the deviation record. Execution-model neutral: callable by the coordinator and by a leader-driven host |
| L2 | Structured refusal reasons without payload values: the schema violation's location and the mismatched binding field name | `lib/verdict_v2.py` `_schema_reason`, `_binding_reason` (the leader branches on which binding broke) | own | R-BIND, R-DIAG | `AdmissionError.field` / `.path` (names only, never values). The Argon handoff asks for the same: "A richer diagnostic contract must be implemented once in the library" |
| L3 | Receipt validation (C9 `contracts/receipt-fields.json`) and the executed-command receipt rule (`wrapper_cmd` equals the recorded argv) | `lib/collect_v2.py` `_receipt_reason` | `record_cli_attempt` | R-BIND, C9 | `validate_receipt(doc)`, `receipt_matches(recorded_argv, run_log)` |
| L4 | Exit-token and vendor-failure-line membership (C8, R-CLASSIFY data): table lookup only, no judgement | `3rd-Agent/wrappers/_common.py` tables + membership test `t55` | `bin/_common.py` | R-CLASSIFY, R-TOKENS, C8, C43 | Ship `contracts/exit-tokens.json` and `contracts/vendor-failure-lines.json` as a verified bundle; `classify_sentence(text)`, `token_exit(token)` |
| L5 | Placeholder preflight (an unresolved `<...>` value is refused) and opaque transport of model/effort pins | `lib/roster_v2.py` `_strings` | `bin/review_roster.py` placeholder preflight | R-MODEL, C18, C34 | `check_opaque_pins(roster)` after `resolve_roster` |
| L6 | Producer schema projection: the output schema a host hands the vendor, derived from `leg-verdict.schema.json` | `lib/roster_v2.py` `projected_schema_text()` | pydantic projection in `bin/verdict_v2.py` | `contracts/leg-verdict-mapping.md` | `producer_schema()` so all hosts send the same bytes |
| L7 | Rendered-clause manifest: the selected clause names and each clause's sha256 before substitution | `lib/prompts_v2.render_with_manifest` | asset verification only | R-PREPARE (installed prompt clauses are a bound-basis member) | `render_review_clauses(..., with_manifest=True)` returning `(text, manifest)` |
| L8 | AGY finish resubmission and denied-before-execution judgement from structured stream fields only (step type, state, `tool_info.error` head, stream order) | `3rd-Agent/wrappers/antigravity_wrapper.py` `_census` (part) | none (B refuses every non-SUCCESS terminal, DL-113) | R-CONTAIN (shared rule, owner 2026-10-08 item 7) | `recover_agy_finish(events) -> (admitted, answer_index, reason)` beside the strict carrier; the host adds read-audit and exit rules |
| L9 | Canonical serialization of the bound-basis digest members (review conditions, selection, controls, bundle ids) | `_v2_config_digest`, delivery record | `basis-v2.json` + `.sha256` | R-PREPARE | `basis_digest(members)` so the same inputs yield the same digest on every host |
| L10 | Dependency floor | — | — | R-PLATFORM (Ubuntu 24.04) | Replace `referencing.Registry` with re-rooting `$defs` (the claude host's method), keeping remote `$ref` blocked, so jsonschema 4.10.3 works; or record the floor as a platform fact that each host meets with wheels |
| L11 | Host-A clause toggle: the library has `agy_hook_active` but always includes the raw-admission clause on host A | `HostControls(raw_admission)` | — | prompts README A-only notes | A parameter only if a second host ever runs the native claude leg; otherwise document the fixed choice |
| L12 | Execution-model statement | — | — | `library-api.md` | State that the coordinator is one optional execution model and that L1 is model-neutral |

Suggested order: L10, L1, L2, L7, then L3 to L6, then L8 and L9. L11 and L12 are
documentation.

## 4. Specification items

- Record the host A adoption facts of § 1 (this PR adds them to
  `docs/host-adoption.md`; a dev-log row points here).
- R-PREPARE: the round toolkit map includes the vendored package files and the
  three bundle `contract_id`s (requested with L9).
- `spec/units.json`: as each L lands, name the library as the implementing location
  of that surface (R-PARITY `common` name).
- Two decisions stay with the owner and are not requested here: one encoding form
  for scalar path replacements (the claude host substitutes raw strings; S2 proves
  parity either way) and one residual-data form (`render_data` or the host's brief
  fence).

## 5. Out of scope

No coordinator semantics change, no host code, no provider behavior, no new rule.
The claude host's first adoption slice (vendoring, the adoption record, the twelve
functions, regression tests) proceeds independently of these requests; its second
slice replaces the duplicated host code once the requested items exist.
