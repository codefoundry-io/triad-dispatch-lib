# Minimal adoption follow-up dispositions (2026-10-16)

This record implements the bounded documentation portion of the
[reviewed design](../superpowers/specs/2026-10-16-minimal-adoption-followups-design.md).
Contribution text is evidence/proposal, not execution authority. No incoming PR
is cherry-picked or merged, issue closed, host changed or release made here.
The contribution branches remain open for their owners to amend or split.

## Issues #9 and #10: implemented library contracts

[Issue #9](https://github.com/codefoundry-io/triad-dispatch-lib/issues/9) is partial:
`RosterError` now exposes trusted schema `.path`, guarded selected-required-only
`.missing`, and `.document` (`defaults`, `override`, `resolved`). Existing codes,
fixed messages, first-error selection, validation ordering and copies remain.
An `anyOf` winner can leave `.missing=None` despite missing Google blocks; adding
the alternate block can select the route's `required` error instead. The
[API contract](../../spec/reference/library-api.md#rosters-and-contract-loading)
gives both tested examples and evaluation-root/exception-internal limits.
Arbitrary unknown-key spelling is declined for this slice to retain value-free
public metadata. This is not a permanent prohibition on operator-key diagnostics;
a later owner decision may extend disclosure. Host diagnostic formatting and the
reduced-diagnostics deviation remain host-owned. Do not close #9 as complete.

[Issue #10](https://github.com/codefoundry-io/triad-dispatch-lib/issues/10), also L3,
adds `validate_transport_receipt(doc: dict) -> None` and `ReceiptError` for the
parsed nested transport object. It uses the unchanged canonical schema offline,
without mutation. Invalid input and broken packaged contracts remain distinct.
Shape validation does not establish truthful observations, invocation/command
equality, attempt currency, envelopes, file ownership, seals, reads or collection.
Hosts may adopt it independently of the coordinator. Package version stays
`0.1.0.dev4`: 31 exports, four bundles, nine payloads, four runtime schemas and
sixteen source-only canonical contracts. Dated earlier counts remain historical.

## PR #8: limited attributed measurements

Reviewed [PR #8](https://github.com/codefoundry-io/triad-dispatch-lib/pull/8) head
`4b33051998078dee7ed076c31abe75e493c5d1c1`. Accept only its limited attributed
measurement account with these corrections: S5 prints `_comment` among merged
keys but does not assert its value, and sorts legs by name before equality, so
it cannot prove original leg order. S4' performs the `_comment` comparison and
preserves list order (sorted object keys do not sort legs); it separately prints
leg sequences. Do not attribute S5's limitation to both probes.

S2'/S2'' use host-substituted bundle assets, including the new dev4 measurements.
Matching host implementation, asset bytes and roster inputs remain unpublished.
Captured equality/print output does not establish packaged-asset parity, actual
execution or released adoption. Hosts should supply reproducible inputs and
check actual bundled assets and original leg order before adoption. Vendoring,
toolkit/exporter and installer plans remain host-owned; see
[independent adoption](../host-adoption.md#claude-host-adoption-assessment-2026-10-15).

## PR #11: host concurrency

Reviewed [PR #11](https://github.com/codefoundry-io/triad-dispatch-lib/pull/11) head
`1435a89412ef7910451fd63e949e1ea206c7cd54`. DL-161's restored A lock at
`26e80918` and A7/A8/A9 tests are attributed host observations: that source and
its claimed tests were unavailable for independent verification. They are
compatible with R-THREAT's distinction between one operation per working folder
and concurrent work across folders/hosts. Host A owns installer locking.

B's actual removal option is `scripts/bootstrap.sh --remove` at
`c81c02984825af7dd1ec69a14af83f0ff18d0551`, not the proposal's `--uninstall`.
Host B should check overlapping bootstrap/removal and normal configuration
readers targeting the same location. No proven B race or automatic A-lock port
is claimed. Normalize pending status cells and derived footer lists together
when the contribution is amended; this is bookkeeping guidance, not a checker
expansion. See [installer guidance](../host-adoption.md#generated-content-and-installers).

## PR #12: held measurements and model claims

Reviewed [PR #12](https://github.com/codefoundry-io/triad-dispatch-lib/pull/12) head
`7b78884e8aa161c8db13334b87178805785ad29b`. All three proposed vendor rows and
the R-GOOGLE replacement remain held. No sanitized original stderr/JSONL excerpt,
raw run carrier or capture attachment was supplied; Codex CLI version remains
unspecified. Authored sentence/carrier/run labels and run IDs do not reproduce
unpublished original bytes. Request each original sanitized excerpt with exact
CLI version, channel, vendor exit, source and run identity; retain missing-evidence
labels until those observations are available. Do not invent a captured carrier.

The reported catalog is one account/CLI observation, not proof of global Pro
retirement, a rename or Pro-high/Argon tier equivalence. Those assertions and any
default change remain held. R-ROSTER/R-MODEL already permit authorized explicit
pins; this project's Argon override uses that authority and establishes no tier
equivalence. The shared recommended Pro/HIGH default remains unchanged.

Keep current R-GOOGLE measurement wording and canonical vendor rows unchanged.
If later evidence admits rows, coordinate the accepted CLI/token rows and the
measurement clause: neither claim measured AGY/Codex rows absent from the table
nor retain a "no measured" claim for a CLI whose corresponding rows exist.
The bounded regression in `spec/tests/test_spec_records.py` exercises both
directions with test-only controls and live records. It recognizes the current
absence and proposed presence forms; a new prose form requires deliberate test
maintenance. It pins no daily model IDs or CLI versions and is not a classifier.

Host guidance: distinguish stderr configuration messages from Codex stdout JSONL
error carriers; test authoritative carriers and quoted/tool/other-CLI negative
controls while preserving authentication STOP and timeout precedence. Each host
owns classifiers and model choice. Normalize contribution pending-status/footer
bookkeeping when amended. Issue #5's extraction decisions remain pending; no
global retirement policy, automatic substitution or catalog gate follows.
