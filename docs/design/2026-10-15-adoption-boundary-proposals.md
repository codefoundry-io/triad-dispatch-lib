# Issue #5: proposed boundary decisions

Status: design proposals, not implementation or owner decisions. Basis: library
main `ee8b4b4`, issue #5 and the request record incorporated in PR #2. Common
deterministic semantics should be authored once, while observations and execution
remain host-owned. No native adapter, provider permission, default or release changes.

| Request | Recommended shared contract | Retained host responsibility | Prerequisite |
| --- | --- | --- | --- |
| L1 collection | A separate pure reducer over typed observed outcomes, preserving all selected members, incomplete precedence, negative/Minor-only deviations, and original admission | Fresh integrity execution, inability-to-run classification evidence, custody and publication | Agree on inputs and outputs for failed integrity versus unavailable check; map both hosts' existing status/exit differences before implementation |
| L4 classification | Verified token/rule lookup keyed by CLI, carrier and structured observation kind; unknown inputs remain unknown | Capturing exit/stream observations, auth, remediation and retry | Shared precedence and carrier examples; `classify_sentence(cli, text)` alone is insufficient because ordinary quoted text is not a terminal failure signal |
| L6 producer schemas | Canonical schema loading/copying and canonical admission may remain shared | Provider/version-specific projection and evidence that a projection is accepted | Compare the two hosts' measured transforms; do not assume identical producer bytes or remove canonical post-validation |
| L8 AGY recovery | Consider a pure predicate only after defining every observed input | Route/profile, exit, terminal and event ordering, allowed reads, actual tool execution, retry/custody and final six-binding admission | Cross-host vectors including false-positive finish messages; events alone cannot certify successful execution |
| L9 basis digests | A versioned serializer only after a common data-domain contract exists | Choosing basis members, sealing and currency | Define member schema, order, Unicode/numeric handling, domain/version marker and invalidation; equal hash functions do not make different host bases equivalent |

L5 opaque-placeholder checking is currently a single-consumer request and stays
host-owned absent a concrete shared contract and second consumer. L3 receipt
shape validation is outside issue #5 and does not prove executed-command or
current-attempt custody.

Recommended order: design L1 and L4 independently after adoption seams are
available; defer shared L6/L8/L9 behavior until their observation/byte contracts
are agreed. No broad relocation is approved by this proposal. Before any runtime
unit, add language-neutral expected vectors, API/conformance entries and bounded
tests, then run the project's complete review profile on the implemented bytes.

Evidence: `docs/requests/2026-10-15-claude-host-adoption-requests.md` request
dispositions; `spec/reference/library-api.md` host boundary;
`spec/reference/library-conformance.md` partial groups; `agreement.py` original
admission and selected-member reducer; `output.py` typed terminal guards.
