# Skipped enabled entry: review disposition and regression case

Status: reviewed against main `c6406eb1a3a09fefdc1d7e98f26095242bd07c07` on
2026-09-22. The proposed new-rule rationale is refuted; the concrete boundary
example is retained in C33 under the existing rules. Host A's reported defect
and repair remain host-owned; this record does not verify its live run or fix.

## Original report and actual basis

[PR #2](https://github.com/codefoundry-io/triad-dispatch-spec/pull/2) reported
that A's collector omitted an enabled Google entry skipped during route
resolution. Completed same-family siblings could then hide the missing entry.
The maintainer reported gate-1 round r11 as
`BLOCKED entries=4/4 families=2 blocking=19`; that report is not independent
verification of A's source, runtime or repair.

The proposal commit `e435b5364d27bfb4d17cfcee3b1af46b599b6979` has parent
`24376000a11bdb03cf3743fad47c6c3286aee75d`. That parent's tree is identical to
the reviewed main tree. The PR's statement that main lacked C33 described the
pre-PR-1 publication state. It does not establish that the proposal was authored
from an obsolete tree. The verifiable problem is an incomplete reading of the
contracts already present on its own basis.

## Claims checked against the shared specification

| Claim | Disposition and evidence |
|---|---|
| The shared rules permit dropping a skipped enabled entry if a sibling covers its family. | Refuted. [R-GOOGLE](../reference/review-rules.md#R-GOOGLE) says neither the skip nor refusal outcome is agreement. [R-AGREE](../reference/review-rules.md#R-AGREE) excludes missing results from agreement. C27 already repeats the skip/refusal boundary. |
| Family coverage decides whether a missing entry matters. | Refuted. [V2 collection](rev-2-implementation-spec.md#same-basis-retry-and-changed-basis-review) counts all participating entries, including absent results, and reports family coverage separately. The [Claude PRD](claude-host-v2-implementation-prd.md#agreement-correction-and-retry) explicitly counts all enabled entries. |
| B is correct only because preparation refuses early. | Refuted. The [released collector](https://github.com/codefoundry-io/triad-codex-dispatch/blob/5a12f822b6e19f5ecd162e4cc54888269ec0ffd9/bin/review_round_v2.py#L508) independently iterates every enabled entry, retains missing entries and selects INCOMPLETE before family coverage. The [four-leg operating spec](codex-google-four-leg-operating-spec.md#b-dispatch-collection-and-owner-decision) already records that B outcome. |
| A skipped entry plus completed same-family siblings deserves an explicit regression input. | Accepted. C33 now names this input and makes the retained missing entry explicit. This specializes existing expectations; it does not add a shared outcome token or change fallback policy. |

## Retained check and host follow-up

Use four enabled entries: one Codex and three Google. Skip one Google entry
before provider execution; complete the other three. Verify that the skipped
entry remains named and missing in collection even though Google is represented
by the completed siblings. The machine result cannot be agreement. Preserve
that result separately from any later owner decision.

B's existing collector uses INCOMPLETE. A keeps its route-resolution behavior
and must satisfy the shared missing-entry semantics in its own collector. A
host that refuses preparation cannot claim a completed round. Host tests should
map this input to C33 and report actual evidence; this documentation check does
not establish that either host executed the new explicit input.

No normative rule, wire schema, prompt clause, policy payload, default roster,
host implementation or revision tag changes here. The specification already
owns the behavior; C33 preserves the discovered interpretation failure as a
shared test asset.
