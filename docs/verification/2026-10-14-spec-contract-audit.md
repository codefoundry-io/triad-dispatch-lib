# Bidirectional specification and interface audit

The owner requested independent parallel checks in both directions: canonical
requirements to implementation/tests, and functions/interfaces back to a written
contract. Four fresh Sol/high auditors inspected the current library candidate
(`81748d7` plus working changes) on 2026-10-14. Requested native settings were
accepted; effective runtime model/effort was not exposed. This source audit is
separate from the required Opus/Sol/Argon review and advisory Astra comparison.

## Coverage and authority

- Admission/output/agreement: 18 authored function bodies and six related types.
- Roster/prompts: six scoped public APIs and five internal functions.
- Coordinator and repository drivers: 59 declarations (55 functions and four
  dataclasses), with 50 related test functions inspected.
- Bundles/distribution: all 27 package-root exports, 33 active unique normative
  groups, 20 canonical contract files and the actual 58-case inventory.

These counts overlap at module boundaries and must not be added into a unique
function total. Generated dataclass methods and every dependency implementation
were not audited. The case IDs are non-contiguous; C79 is not a count of 79 cases.
Source inspection of a test is coverage evidence, not a newly executed test.
Historical host cases and snapshots were not treated as current host proof.

The [API contract](../../spec/reference/library-api.md) is the maintained reverse
map for supported package-root interfaces. The [conformance map](../../spec/reference/library-conformance.md)
assigns all normative groups to implemented portions or explicit host/development
owners. The [58-case map](../../spec/reference/library-case-coverage.md) gives each
actual case an explicit disposition. Canonical wire schemas and review rules retain their separate authority;
private helper signatures are not new public wire contracts.

## Accepted findings and dispositions

| Finding | Disposition |
| --- | --- |
| Receipt readiness stat/lstat errors escape the native driver's terminal observation guard after publication | Existing R3 defect, independently confirmed; include readiness and consumption in the same refusal boundary and retain custody until acknowledgement. Ten regressions fail before correction and pass afterward. |
| Cyclic packet/worktree paths raise Python 3.12 `RuntimeError`, bypassing the repository CLI's controlled refusal | Normalize only path-resolution failures to the existing `ValueError` boundary. Eight real cyclic leaf/ancestor cases cover preparation and CLI exit 2 without prompt publication; all fail before correction and pass afterward. This occurs before publication and is not a custody leak. |
| Eight of 27 exports lack direct README presentation; result shapes and non-admission code domains are scattered through plans/source | Add one maintained API reference, including signatures, fields, exact emitted codes and validation/admission distinctions; link the README and canonical source map. No new runtime API or compatibility policy. |
| Frozen dataclasses contain mutable dictionaries; computed agreement can become stale after caller mutation | Document shallow freezing, copied inputs, uncopied callback values and decision snapshot semantics. Do not claim deep immutability. |
| Cancellation versus concurrent packaged-contract failure and independent phase budgets are underspecified | Document observed parent-cancellation precedence and separate preflight/invoke deadlines. Add controlled cancellation/ContractError race coverage. |
| README points to the initial Codex/B-only renderer contract; conformance row assigns substitution to `render_data` | Link the current four-route API; assign residual encoding to `render_data` and one-pass replacement to `render_review_clauses`. |
| Thirteen normative groups lack explicit coverage dispositions | Inventory the remaining host, leader and authoring ownership in the conformance map. Missing runtime code for these responsibilities is intentional. |
| Minor-only dissent requires a selection-deviation record, but reducer ownership is unclear | Allocate the record to the host collector/leader in adoption guidance. Preserve the original negative ballot and existing `negative_verdict` reason. |

No confirmed current admission, roster, prompt, bundle or packaging divergence
was established by these auditors. The full 51-profile prompt matrix exists;
uncertainty-only negative agreement is exercised by the four-route smoke driver.
Neither was counted as a missing feature.

## Remaining limits and non-blocking test gaps

Some roster/output refusal tests assert the exception family rather than every
emitted code and precedence combination. Several schema edge axes (optional
correction, finding line/context types, unique surface/question lists) and the
non-exported original-member-span helper lack dedicated assertions in the
inspected tests. The runtime delegates those constraints to the verified schema;
no incorrect acceptance was demonstrated. The audit does not claim exhaustive
branch or error-code compatibility testing.

The roster loader explicitly checks the legacy schema `$id`; verdict and phase
loaders check verified bundle bytes, dialect and schema validity without that
extra runtime equality check. Current source/assets preserve all three IDs and
generation tests pin them. This asymmetry is a clarification, not evidence of a
current payload mismatch or permission to change identities.

Native execution, model availability, credentials, AGY recovery, vendor failure
classification, packet seals, installer preservation and platform-specific host
behavior remain separate adoption responsibilities. Repository test-driver
receipts are synthetic parent claims; library parsing cannot attest backend
termination. See the [correction verification](2026-10-14-review-corrections.md)
for executed tests, artifact identities, formal outcomes and platform limits.
