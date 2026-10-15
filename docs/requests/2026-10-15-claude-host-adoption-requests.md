# Claude host adoption assessment and library requests

Original report: Claude host (A) leader, 2026-10-15, against `0.1.0.dev3`
at `2d1e62e7de6f33fa13a918a39579c6b5e74def00` (merged as `9489543e`).
Maintainer disposition: owner-approved on 2026-10-15 after comparison with
Codex `c81c02984825af7dd1ec69a14af83f0ff18d0551` and published Claude
`e4cadf2f751308d1ab75e4199b08d89849bb93b3`.

Concurrent host amendments through `e763df8` are incorporated below. The earlier
candidate `3afc4d7e` was unavailable in the public remote and three known local
reference repositories. The newly published scratch record identifies reported
host head `f925395f` on `impl/claude-host-2026-10`; that implementation branch
remains unpublished. The named first slice and request records supersede earlier counts.

Some requests extract existing host semantics; others require new library API
contracts. They are not all already inside the public API boundary. This slice
implements bounded L2/L7, documents L10-L12 and records prerequisites for the other
requests. See the [design](../design/2026-10-15-adoption-observability.md) and
[plan](../superpowers/plans/2026-10-15-adoption-observability.md).

## 1. Reported scratch measurements and evidence limits

The original report describes throwaway runs without changing either host.
Its evidence path is `codefoundry-io/triad-dispatch:docs/reviews/2026-10-15-triad-dispatch-lib-pr1-claude-host-review.md`, section 6.
At the 2026-10-15 maintainer review that path returned 404, its path history was
empty, and the only published branch was main at `e4cadf2f`. The harness, host
revision and scratch bundle hashes were not published then. The later amendments
publish scripts, captured outputs and input identities in this PR, linked below.
These counts remain **host-leader reported, not independently reproduced**:
the matching host source/assets and measured roster input are not included.
Published captures alone establish neither conformance nor released adoption.

- **S1 dependencies:** reported 165 failed / 101 passed with jsonschema 4.10.3
  and referencing 0.31.0, including unsupported `registry` keyword errors.
  That environment is below the declared jsonschema>=4.26,<5 and
  referencing>=0.37,<1 floors; the keyword's introduction in 4.18 does not lower
  the package requirements. The [Ubuntu package](https://packages.ubuntu.com/noble/python3-jsonschema)
  confirms its older distribution version. The reported six-wheel/620 KB
  manylinux CPython 3.12 closure does not establish macOS or Python 3.14 support.
- **S2 renderer comparison:** amended report: 24 matching host-A profiles with raw
  replacements **after rebuilding the library bundle from host-owned prompts**.
  This is renderer-only comparison with substituted assets, not packaged dev3
  prompt parity. Published host and library common/Claude clauses differ.
  The amendment uses `agy_hook_active=True` for every AGY profile; this
  supersedes the original unsupported 30-profile/hook-off account. Reported suffix parity concerns each route separately;
  AGY and Gemini outputs themselves use different tool names.
- **S3 verdict decisions:** captured 47 matching accept/reject decisions (13
  accepts, 28 non-binding rejections and 6 binding-mismatch rejections),
  with NaN/1e999 refused at different stages. Fixtures and captured outputs are
  now published; the matching host validator source remains unpublished.
- **S4 roster merge:** the published rerun captures six merged legs, including
  two disabled entries, and four enabled/startable entries. It compares sorted-JSON
  leg content and checks override `_comment`, not the complete document. This
  supersedes the earlier five-entry report with a different measured override.
  That uncommitted per-round override is identified only by hash, so publishing
  the host commit alone would not enable replay. Native route resolution and
  capability checks remain host-owned.

Claude's amended first slice (its review round r2, concurrent with this slice) plans
exactly two functions: `render_review_clauses` (the bound prompt bytes, with the
host's clause manifest computed over the same canonical bytes) and
`validate_binding`. `select_entries` is not adopted: it drops disabled entries and
refuses an all-disabled roster, while the host keeps disabled legs in its round
record with a separate startable list. `load_roster_contract` is not adopted: the
host reads its own vendored contract copy. Verdict admission and roster merging stay
wholly host-owned pending the remaining L2 duplicate-member and new L13 requests. The earlier
twelve/eight/four-function counts are superseded by this named pair. Its
leader-driven lifecycle does not need callback coordinators.

The host reports two further implementation facts from that round: its `spec/contracts` and
`spec/prompts` remain its ONE bound copy and the vendored `data/` bundle must be
byte-equal, checked at round preparation by comparing the eight payload pairs byte for
byte through a mapping recorded in the host's adoption record (drift refuses; the host
does not recompute bundle ids, which would depend on the non-exported `bundle_manifest`
module and the `BUNDLES` map of `tools/sync_spec_assets.py`); and the host's `bin/` wrappers load its clause renderer by
file path with `bin/` first on `sys.path`, so the renderer imports the library lazily
with its own directory on the path and keeps the bare investigation clause
import-free (`render_investigation_prompt` has no host call site).

The host reports three further observations from its round r3 (2026-10-15).
Its first slice retains its renderer for the prompt manifest and refuses preparation
unless that text matches the library's `render_review_clauses` result. This is a
reported parity gate, not independently verified host behavior. Its planned second
slice adopts `with_manifest=True` and removes the host render core. The host records
the web-policy manifest entry after every clause carrying the placeholder, while the
library records it once; the host reports equivalence for its current clause set.
The requester accepts implemented `.field` and trusted schema `.path`; `.member`
remains requested, while `.detail` and instance-pointer expectations are withdrawn.
L5 (`check_opaque_pins`) has one reported consumer, the Claude host, so it remains
host-only unless a concrete second consumer and shared contract justify extraction.

The scratch measurements are now published in this PR:
[`docs/verification/2026-10-15-claude-host-spikes/`](../verification/2026-10-15-claude-host-spikes/README.md)
(scripts, captured outputs, input identities, environment). The host's implementation
branch stays unpublished; its file hashes in that record allow a byte-for-byte match
at publication.

The host also reports these planned safeguards: re-vendor its specification at
the library pin; compare vendored file hashes with pinned Git blobs; extend
exporter/toolkit coverage recursively, excluding
bytecode and including the adoption record; map import failures, Registry-probe
failures and library ContractError to host faults. Raw scalar replacements and
its residual brief fence remain host-owned under R-CONTEXT. The reported
3600-second host timeout is separate from this project's 2400-second review
budget. Case-folded name refusal for filesystem directories remains host-owned;
shared roster names remain case-sensitive. None of these reported plans proves
that the unpublished host branch or an installed release implements them.

## 2. Host boundary

Native spawning/presets, capability resolution, permissions, processes/timeouts,
receipt authenticity and current-attempt custody, packet seals, read auditing,
transport/exit observations and installation stay host-owned. A pure helper may
consume observations without attesting that they were actually made. Full
canonical admission remains required after carrier or recovery adaptation.

## 3. Request dispositions

| Request | Evidence and boundary | Disposition |
| --- | --- | --- |
| L1: collection reducer | `evaluate_agreement` already re-admits original outputs. R-AGREE distinguishes failed integrity (refuse, preserve prior record) from inability to run the check (host fault, no collection record). | Design a separate model-neutral reducer with typed observed states, integrity refusal, host faults and selection deviations. Preserve original admission and selected-skipped blocking; checking/publication stay host-owned. |
| L2: refusal locations | Codex already delegates admission to the library (`bin/validate_v2.py`). The library previously exposed only a code; R-BIND/R-DIAG do not define a diagnostic object. | Implement additive `AdmissionError.field` for binding mismatch and `.path` for the trusted schema evaluation path (not necessarily a source-document JSON Pointer), never provider values or arbitrary instance keys. See the public API contract. |
| L3: receipts | C9 `receipt-fields.json` validates the transport object, not a host envelope. Codex compares `wrapper_cmd` with `invocation["argv"][1:]` after CLI identity checks. | The host narrows this request to transport shape validation only. Executed-command comparison and attempt currency remain host-side; transport shape alone is not receipt/custody validation. |
| L4: tokens/classification | R-CLASSIFY data distinguishes CLI, carrier, whole lines and operator-only observations. Text-only classification loses required context. | Consider verified data/token lookup and CLI/carrier-qualified evidence lookup; preserve precedence and unknown-token behavior. Define the API before extraction. |
| L5: placeholders/opaque pins | `resolve_roster` already preserves model/effort values. R-MODEL also covers wrapper/parser boundaries; no generic shared `<...>` grammar is defined. | Host-only with one reported consumer. Shared extraction requires a concrete second consumer and a defined placeholder syntax/timing contract; Codex retains its preflight. Dictionary validation cannot prove CLI transport. |
| L6: producer schema | Codex binds the canonical schema and narrowly projects for Claude. Claude's published projection removes additional keywords; DL-103 records measured differences. | Share canonical loading/copying/binding after design. Keep measured vendor/version projections distinct and complete canonical admission unchanged; equal producer bytes are not required. |
| L7: clause manifest | Claude has `render_with_manifest`; Codex already hashes toolkit sources into its basis. Clause-level output is an additive API. | Claude withdrew its standalone request in the concurrent amendment. The owner separately approved this additive library API: implement optional `with_manifest=True` with ordered source hashes, nested web policy and unchanged default bytes; it is not a Claude first-slice prerequisite. The host now reports planned second-slice adoption of `with_manifest=True`. |
| L8: AGY recovery | Both hosts already implement recovery. Codex `_agy_finish_resubmitted` and `test_agy_finish_resubmission.py` exist; DL-113 records its exit0 boundary. | Consider structured-evidence predicates. Events alone cannot establish admission: preserve route/profile, exit, actual allowed reads, terminal/order checks, no executed forbidden tools, and final schema/six bindings. Never relabel ERROR as SUCCESS. |
| L9: basis digest | R-PREPARE defines freezing/meaning, not common serialization. Hosts hash different members and newline conventions. | Defer until member schema, value domain, ordering, Unicode/nonfinite rules, version/domain marker and invalidation are specified. Equal-input hashing does not imply equal host bases. |
| L10: dependencies | Distribution packages can fall below the supported jsonschema>=4.26,<5 and referencing>=0.37,<1 floors. | Keep current Registry design/floors; document installation and per-platform/Python offline wheel checks. No 4.10.3 backport in this slice. |
| L11: raw clauses | Canonical Claude clauses distinguish A raw/native and B structured CLI admission. The reported `HostControls(raw_admission)` symbol was not found at the published A pin. | Claude withdrew the toggle request. Document the fixed profile; no new toggle without a concrete use case and contract. |
| L12: optional coordinator | Admission/rendering/agreement functions work independently of callback coordinators. | Document selective adoption and model-neutral future collection helpers. |

## Concurrent issues and unmet adoption requirements

- [Issue #3](https://github.com/codefoundry-io/triad-dispatch-lib/issues/3)
  now accepts dev4's implemented `.field` and trusted **schema** `.path`.
  The requester's r3 amendment withdraws decoder-detail and instance-pointer
  expectations; its original broader issue body remains historical. Only `.member`
  remains requested. It would expose a provider-chosen duplicate name and needs a
  separate diagnostic/privacy decision; it is not implemented here. The requester
  offers a host-side duplicate parser as a recorded deviation if that surface stays
  excluded. Keep the issue open; complete Claude verdict delegation is not claimed
  unblocked, and existing library error selection is unchanged.
- [Issue #4](https://github.com/codefoundry-io/triad-dispatch-lib/issues/4)
  adds L13: `merge_roster(defaults, overrides)` would validate input documents,
  return the merged document before final resolved validation, then
  `validate_resolved(roster)` would validate it. The host wants to name inherited
  vendor blocks first. `resolve_roster` would remain the validating composition.
  This new public intermediate-state API needs separate design and regression
  vectors; it is not implemented or approved by this slice. Never treat its
  proposed intermediate result as a runnable/resolved roster.
- [Issue #5](https://github.com/codefoundry-io/triad-dispatch-lib/issues/5)
  tracks the five boundary decisions L1/L4/L6/L8/L9. The amended CLI identity in
  L4 is necessary, but carrier/context constraints still apply. L6 and L9 require
  new shared-byte contracts. L8's old B-none claim remains corrected above.

The amended S1 reports that old jsonschema's default resolver can retrieve remote
references despite `$defs` re-rooting. Retain no-retrieval behavior; a future
lower-floor proposal would need explicit protection and old-version CI. No such
backport is selected here. Published scratch captures do not supply the missing
host inputs for independent reproduction or the reported wheel-closure artifacts.

## 4. Sequence and specification work

Correct evidence, implement L2/L7 with regressions, and document L10-L12. Then
design the remaining L2 `.member` request and L13 alongside L1/L3/L4/L6; L8/L9
follow their own contract decisions. L5 remains host-only. This is not approval of every proposed signature. Update API/conformance references for
implemented portions; retain native ownership in `spec/units.json`.

Bundle IDs already belong in adoption records. Requiring them as separate members
of every host basis would be an additional L9 decision. Scalar path encoding and
residual-data form stay outside this slice; scratch S2 proves neither a universal
encoding nor parity of untested forms.

## 5. Independent adoption

Claude's planned vendoring, adoption record and regressions can proceed
independently. Each later helper adoption needs a compatible library pin and host
evidence. This slice changes no consumer, provider default, callback scheduling
or canonical payload. New additive API contracts are specified and tested here.
