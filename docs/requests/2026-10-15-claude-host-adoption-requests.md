# Claude host adoption assessment and library requests

Original report: Claude host (A) leader, 2026-10-15, against `0.1.0.dev3`
at `2d1e62e7de6f33fa13a918a39579c6b5e74def00` (merged as `9489543e`).
Maintainer disposition: owner-approved on 2026-10-15 after comparison with
Codex `c81c02984825af7dd1ec69a14af83f0ff18d0551` and published Claude
`e4cadf2f751308d1ab75e4199b08d89849bb93b3`.

Some requests extract existing host semantics; others require new library API
contracts. They are not all already inside the public API boundary. This slice
implements L2/L7, documents L10-L12 and records prerequisites for the other
requests. See the [design](../design/2026-10-15-adoption-observability.md) and
[plan](../superpowers/plans/2026-10-15-adoption-observability.md).

## 1. Reported scratch measurements and evidence limits

The original report describes throwaway runs without changing either host.
Its evidence path is `codefoundry-io/triad-dispatch:docs/reviews/2026-10-15-triad-dispatch-lib-pr1-claude-host-review.md`, section 6.
At the 2026-10-15 maintainer review that path returned 404, its path history was
empty, and the only published branch was main at `e4cadf2f`. The harness, host
revision and scratch bundle hashes were not published. These counts are
**host-leader reported, not independently reproduced**. An immutable record of
source, commands, fixtures, bundle hashes and outputs is needed before treating
them as conformance or released-adoption evidence.

- **S1 dependencies:** reported 165 failed / 101 passed with jsonschema 4.10.3
  and referencing 0.31.0, including unsupported `registry` keyword errors.
  That environment is below the declared jsonschema>=4.26,<5 and
  referencing>=0.37,<1 floors; the keyword's introduction in 4.18 does not lower
  the package requirements. The [Ubuntu package](https://packages.ubuntu.com/noble/python3-jsonschema)
  confirms its older distribution version. The reported six-wheel/620 KB
  manylinux CPython 3.12 closure does not establish macOS or Python 3.14 support.
- **S2 renderer comparison:** reported 30 matching host-A profiles with raw
  replacements **after rebuilding the library bundle from host-owned prompts**.
  This is renderer-only comparison with substituted assets, not packaged dev3
  prompt parity. Published host and library common/Claude clauses differ.
  Hook-off profiles also require a pinned harness: the published host always adds
  its AGY hook clause. Reported suffix parity concerns each route separately;
  AGY and Gemini outputs themselves use different tool names.
- **S3 verdict decisions:** reported 47 matching decisions (8 valid, 33 invalid,
  6 binding mismatches), with NaN/1e999 refused at different stages. Fixtures and
  outputs remain unpublished.
- **S4 roster merge:** reported five byte-identical merged entries. Native route
  resolution and capability checks remain host-owned.

Claude plans to use twelve of the fourteen package-root functions; its
leader-driven lifecycle does not need the callback coordinators. This is planned
integration. Vendoring, adoption records, offline wheels and toolkit hashing
remain Claude's separate implementation and verification work.

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
| L2: refusal locations | Codex already delegates admission to the library (`bin/validate_v2.py`). The library previously exposed only a code; R-BIND/R-DIAG do not define a diagnostic object. | Implement additive `AdmissionError.field` for binding mismatch and `.path` for trusted schema location, never provider values or arbitrary instance keys. See the public API contract. |
| L3: receipts | C9 `receipt-fields.json` validates the transport object, not a host envelope. Codex compares `wrapper_cmd` with `invocation["argv"][1:]` after CLI identity checks. | Design transport-only validation separately from host-normalized argv comparison. Neither is complete receipt/custody validation. |
| L4: tokens/classification | R-CLASSIFY data distinguishes CLI, carrier, whole lines and operator-only observations. Text-only classification loses required context. | Consider verified data/token lookup and CLI/carrier-qualified evidence lookup; preserve precedence and unknown-token behavior. Define the API before extraction. |
| L5: placeholders/opaque pins | `resolve_roster` already preserves model/effort values. R-MODEL also covers wrapper/parser boundaries; no generic shared `<...>` grammar is defined. | Specify placeholder syntax/timing before preflight extraction. Dictionary validation cannot prove CLI transport. |
| L6: producer schema | Codex binds the canonical schema and narrowly projects for Claude. Claude's published projection removes additional keywords; DL-103 records measured differences. | Share canonical loading/copying/binding after design. Keep measured vendor/version projections distinct and complete canonical admission unchanged; equal producer bytes are not required. |
| L7: clause manifest | Claude has `render_with_manifest`; Codex already hashes toolkit sources into its basis. Clause-level output is an additive API. | Implement optional `with_manifest=True`, ordered source names/hashes including nested web policy, with unchanged default rendered bytes. |
| L8: AGY recovery | Both hosts already implement recovery. Codex `_agy_finish_resubmitted` and `test_agy_finish_resubmission.py` exist; DL-113 records its exit0 boundary. | Consider structured-evidence predicates. Events alone cannot establish admission: preserve route/profile, exit, actual allowed reads, terminal/order checks, no executed forbidden tools, and final schema/six bindings. Never relabel ERROR as SUCCESS. |
| L9: basis digest | R-PREPARE defines freezing/meaning, not common serialization. Hosts hash different members and newline conventions. | Defer until member schema, value domain, ordering, Unicode/nonfinite rules, version/domain marker and invalidation are specified. Equal-input hashing does not imply equal host bases. |
| L10: dependencies | Distribution packages can fall below the supported jsonschema>=4.26,<5 and referencing>=0.37,<1 floors. | Keep current Registry design/floors; document installation and per-platform/Python offline wheel checks. No 4.10.3 backport in this slice. |
| L11: raw clauses | Canonical Claude clauses distinguish A raw/native and B structured CLI admission. The reported `HostControls(raw_admission)` symbol was not found at the published A pin. | Document the fixed profile; no toggle without a concrete second use case and contract. |
| L12: optional coordinator | Admission/rendering/agreement functions work independently of callback coordinators. | Document selective adoption and model-neutral future collection helpers. |

## 4. Sequence and specification work

Correct evidence, implement L2/L7 with regressions, and document L10-L12. Then
design L1/L3/L4/L5/L6; L8/L9 follow their own contract decisions. This is not
approval of every proposed signature. Update API/conformance references for
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
