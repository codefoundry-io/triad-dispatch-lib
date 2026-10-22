# Open-item review and release plan — 2026-10-22

## Basis and current release

This review covers the one open PR and four open issues observed before this
documentation update, against main `f043c257ccd748371c34e9d1f23e32064e139354`.
It records dispositions and a proposed release sequence, not implementation
approval for the pending contract choices or permission to merge or publish.

The only published library release is
[v0.1.0.dev4](https://github.com/codefoundry-io/triad-dispatch-lib/releases/tag/v0.1.0.dev4),
a prerelease published on 2026-10-16 from
`087af94a7078de0ae9701fb057840b5492f51f66`.
Current main has an identical `src/` tree. Existing `.path`, `.missing`,
`.document`, `validate_transport_receipt` and `ReceiptError` already ship in
dev4. The API compatibility tooling merged after that release.

## Dispositions

| Item | Verified result | Action |
| --- | --- | --- |
| [PR #20](https://github.com/codefoundry-io/triad-dispatch-lib/pull/20) — leg wording | Head `13bee142` changes six specification/example/history files; no runtime schema or prompt changes. Inline supersession agrees with the later owner decision. | No source correction requested. Record the review and successful CI; final merge remains the owner's. |
| [Issue #9](https://github.com/codefoundry-io/triad-dispatch-lib/issues/9) — roster diagnostics | Invalid inputs are rejected, but the public schema path loses the array index. A later-entry failure is indistinguishable from the same failure at entry zero. | Keep partial/open. A separate additive instance-location proposal is justified by the concrete multi-entry case; it remains optional and nonblocking. |
| [Issue #17](https://github.com/codefoundry-io/triad-dispatch-lib/issues/17) — old schema URLs | Legacy `$id` values are intentional identities; current-source metadata already names this repository and `spec/`. | Explain the identity/source distinction. Keep identifiers unchanged; no URL-only runtime fix is needed. |
| [Issue #21](https://github.com/codefoundry-io/triad-dispatch-lib/issues/21) — acceptance labels | Labels do not affect unanimous agreement, but resolved-schema validation requires them and hosts can seal the entire roster. | Correct the dependency assessment. Retain the current contract pending an owner decision on any coordinated transition. |
| [Issue #5](https://github.com/codefoundry-io/triad-dispatch-lib/issues/5) — shared extraction boundaries | No new approval supersedes the existing L1/L4/L6/L8/L9 hold. | Retain the existing disposition; no speculative extraction or exhaustive vendor-error catalog. |

PR #20 passed [package CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39637801186)
and [API compatibility CI](https://github.com/codefoundry-io/triad-dispatch-lib/actions/runs/39637801137)
at that exact head. This source review and those runs do not substitute for any
required project formal review. PR #20 alone does not require a new runtime
release. Its documents are included in the sdist, so a newly built sdist can
differ even though runtime payloads do not. Preserve the already published dev4
assets; do not regenerate or overwrite them for wording changes.

### Diagnostic and compatibility evidence

`src/triad_dispatch_lib/roster.py` selects the first validator error, sets
`.path` from `absolute_schema_path`, and supplies `.missing` only for the selected
`required` failure. `errors.py` has no instance-location attribute. With four
valid named defaults, a string `timeout_s` in an override at index zero or three
produces the same code, message, schema path and document attribution. A resolved
Google AGY entry carrying only a `gemini` block reports `.missing="agy"` but
does not identify the entry index. These are diagnostic limits, not admission
bypasses. Existing first-error and disclosure constraints remain intact.

For #17, `spec/MIGRATION.md`, `bundle_manifest.py` and `contracts.py` distinguish
source location from canonical identity. Roster validation registers `$id`
locally; it does not fetch the old repository. `tests/test_contracts.py` verifies
that even recomputed matching hashes do not admit a noncanonical roster ID.

For #21, `review-legs.schema.json` requires `acceptance` in resolved entries;
`resolve_roster` validates those entries before dispatch. `select_entries` uses
`enabled`, and agreement counts every selected entry. The Codex host additionally
seals and compares the complete roster in `bin/review_round_v2.py`. Optionality
would preserve old valid inputs in a new validator, but omitted-field inputs
would fail older validators. Removing the property under
`additionalProperties: false` would reject existing labeled rosters. Neither
change is a harmless cleanup or an informational-leg voting exemption.

## Three host proposals

The [pinned manifest records](../host-adoption.md#current-recorded-adoption-2026-10-22)
all name the same dev4 source, wheel and four bundles. They establish recorded
provenance, not a fresh rerun of every consumer integration or provider path.

| Host proposal | Observed state | Next owned work |
| --- | --- | --- |
| [Codex #46](https://github.com/codefoundry-io/triad-codex-dispatch/pull/46), `68cfc052` | Open draft, mergeable; [macOS/Ubuntu distribution CI](https://github.com/codefoundry-io/triad-codex-dispatch/actions/runs/39655458840) succeeded. | Proposed offline diagnostic characterization and host formatting. |
| [Claude export #1](https://github.com/codefoundry-io/triad-dispatch/pull/1), `e888776f` | Open draft, mergeable; no PR workflow runs found at this head. | Work in `codefoundry-io/triad` source, verify there, then export. |
| [AGY #2](https://github.com/codefoundry-io/agy-triad-dispatch/pull/2), `0630d7e5` | Open draft, mergeable; no PR workflow runs found at this head. | Work from `feat/agy-triad-dispatch`; preserve the existing library `host="B"` profile. |

These are documentation proposals, not release notices or implemented host
changes. A missing workflow result is not a passing check. Host release,
installation and fresh-session/provider checks remain separate evidence.

## Proposed release sequence

1. **Finish the current documentation queue.** Review PR #20 and these status
   corrections, post the bounded issue responses, and retain #9/#5/#21 decisions
   as open. Keep dev4 as the published version. Correct stale adoption claims in
   README/status/adoption guidance without rewriting historical verification.
2. **Select one optional implementation slice.** If the owner selects #9, first
   specify a roster-only instance-location attribute alongside the existing
   schema path. Preserve the constructor, codes, fixed messages, first-error
   selection and document attribution. Define the meaning of `None`, root and
   array indices; bound disclosure to approved structural segments. Keep raw
   values, arbitrary unknown-key spelling and verdict diagnostics out of this
   slice. Complete the required design review before implementation. Regressions
   must cover index zero/later entries, defaults/override/resolved attribution,
   Google `anyOf` versus selected `required`, non-schema errors, fallback and
   unchanged caller inputs. This is proposed work, not a shipped API.
3. **Prepare one new candidate only when there is a release delta.** For a
   selected and implemented additive change, propose `0.1.0.dev5` if still
   unused, update version/lock/notes as required, and freeze the exact source
   commit. Do not describe existing dev4 diagnostics as newly added. Keep #17,
   #21 and #5 outside this candidate unless separately selected.
4. **Verify the candidate and obtain its review.** Run `uv sync --locked`, full
   pytest, `tools/sync_spec_assets.py --check`, `spec/tools/check_authoring.py`
   and `tools/check_api_compatibility.py`. Build/normalize the sdist, extract it
   outside the checkout, rerun archive checks, rebuild its wheel, and run
   `verify_wheel.py` plus all three installed synthetic drivers. Require the
   exact-head Ubuntu 24.04/macOS 15 × Python 3.12/3.14 matrix. The separate API
   compatibility workflow must also pass; the release reusable test workflow
   does not run that static gate. Complete the [project review](../review-profile.md)
   with Opus/Sol/Argon and separate Astra comparison on the frozen candidate.
   Changed bytes require fresh applicable evidence; missing votes do not pass.
5. **Present the publication packet.** Include source SHA, version/tag, final
   diff, exact-head CI and review links, artifact provenance, release notes and
   the three-host delivery list. Obtain explicit owner authorization for the
   concrete merge/tag/publication actions. Follow [releasing.md](../releasing.md):
   the tag must match package version and a development release must be marked
   prerelease. The release workflow re-verifies its resolved tag and publishes
   the selected Ubuntu/Python 3.12 sdist and wheel, then the manifest.
6. **Deliver to all three consumers.** Verify the published manifest and assets
   before preparing adoption notices. Existing automation covers only Codex and
   Claude. Use a separately authorized manual AGY notice for the first such
   release, or select a separate automation slice before release: update
   `tools/release_prs.py`, workflow App repository scope and operator docs
   together, with three-target selection/failure/idempotency regressions. Owner
   approval is required for App installation/permission changes; current App
   settings have not been re-audited here. Do not equate today's proposal PRs
   with future version-update notices or mutate them into automatic upgrades.
   Dev4's requested change list has since been delivered manually to all three
   proposals; see the [delivery record](../releasing.md#current-activation-boundary).
   Do not automatically retry its old delivery job, whose branch-based
   deduplication cannot recognize those proposals. Any deliberate retry is a
   separate owner decision. Also, the helper currently reads only
   `contracts/library-adoption.json`; Claude's separate `skills/.../lib/lib-adoption.json`
   location makes its prior version appear as `unrecorded` in automated notices.
   A future automation slice should explicitly address that lookup limitation.
7. **Adopt and deploy independently.** Each host verifies the exact artifact,
   adapts diagnostics, updates its provenance and runs its own compatibility,
   packaging and review checks before its separate release/install approval.
   Keep existing dev4 pins until those checks succeed. Record host-native
   installation and live behavior only where actually observed.

If source publication succeeds but notice delivery fails, preserve the release
and successful notices and use the documented failed-job retry after resolving
the diagnosed cause. Never overwrite a published asset to force a retry. If a
new version fails consumer validation, leave existing consumer pins in place
and prepare a separately reviewed fix; do not move the old tag.

## Changes and limits of this update

This section records the historical PR #22 documentation update against main
`f043c257ccd748371c34e9d1f23e32064e139354` on 2026-10-22. The later combined
[PR #24](https://github.com/codefoundry-io/triad-dispatch-lib/pull/24) separately
adds the approved C80 runtime change and `0.1.0.dev5` candidate; its verification
is recorded in the [AGY metadata candidate record](../verification/2026-10-22-agy-metadata.md).
The test total and documentation-only limits below apply to that earlier update.

Local macOS/Python 3.12.13 verification: `uv sync --locked` succeeded; the full
suite passed **1346 tests**; generated assets, spec authoring and the declared
public API compatibility checks passed; `git diff --check` was clean. A separate
four-case probe confirmed equal public diagnostics at indices zero and three for
both timeout overrides and resolved Google route-block failures. An independent
read-only Codex documentation review found no actionable issue. These checks
do not establish a new native-platform matrix or a formal review result.

This update changes documentation only: current adoption/release facts, the open
item dispositions and the proposed sequence above. It does not change runtime
code, schema IDs, acceptance rules, native adapters, package version, App settings
or release assets. No issue is closed and no merge, publication or installation
is performed. The issue-specific source checks are ordinary read-only review;
they are not a new completed formal TRIAD round.
