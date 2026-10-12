# Model catalog gates versus evidenced model-remapping defects

Status: RESOLVED by D-GEMINI-FLOOR-20261009. The owner selected one common
Gemini CLI floor of 0.63.0. Historical alternatives below are not the selected
policy. Shared-source changes remain untagged and host adoption is separate.
Date: 2026-10-09. Current shared main inspected: `3afc4d7`.

The selected resolution applies 0.63.0 to raw, legacy and v2 Gemini paths on
both hosts, with no per-model allowlist. The Codex leader has resumed the bounded
unit; the earlier stopped-state record below is historical. Source and boundary
tests are being verified; no host release or runtime conformance is claimed.

## Evidence and conflict

R-MODEL removes vendor catalog probes and packaged model-list gates. R-GOOGLE
also says a Gemini review needs only the 0.34.0 policy floor. In contrast,
R-CLI-VERSION preserves minimum-version restrictions justified by a specific
known defect. Removing B's entire `gemini_model_support` function removes both
the unwanted allowlist and its existing 0.61.0 requirement for the explicit
`gemini-3.8-flash` pin.

Vendor source fetched again on 2026-10-09:

- [Gemini CLI v0.60.0 models.ts](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/config/models.ts#L216-L254):
  when `useGemini3_5Flash` is enabled, `resolveModel` maps values accepted by
  `isFlashModel` to `DEFAULT_GEMINI_FLASH_MODEL`. That predicate includes any
  value ending in `flash`, including `gemini-3.8-flash`.
- [Gemini CLI v0.61.0 models.ts](https://github.com/google-gemini/gemini-cli/blob/v0.61.0/packages/core/src/config/models.ts#L286-L336):
  the promotion predicate uses named aliases/backend IDs; the broad suffix
  match is gone and explicit newer Flash IDs are preserved by this branch.

This is conditional source evidence, not a captured live account invocation.
It establishes a known route behavior; it does not establish all effective
runtime identities or make every 0.61.0 path exact. Other backend mappings and
preview-access fallbacks remain vendor behavior. No paid model probe or login
change was performed to investigate this issue.

B already documents this basis in `docs/installation.md#gemini-cli-38-high`
and tests the model-specific floor in `tests/test_gemini_version_floor.py`.
A's DL-116 gate-removal evidence confirms removal, but does not settle this
specific pin/version behavior. A's native Claude leg is unrelated and excluded.

## Proposed shared clarification (recommended)

Replace the unconditional "only the 0.34.0 policy floor" sentence with:

> A Gemini review requires the 0.34.0 policy floor. Catalog membership and model
> availability are never preflight gates. Separately retain a minimum-version
> restriction justified by vendor-source or captured evidence that an older
> CLI silently substitutes a user's explicit model pin (R-CLI-VERSION). Such
> an exception names the exact pin, defect and evidence; it does not authorize
> a model-list probe, substitute model, or general supported-model allowlist.
> For `gemini-3.8-flash`, retain the existing 0.61.0 floor for the evidenced
> broad Flash remapping behavior in 0.60.0. Version evidence does not attest
> runtime identity; exposed contradictions remain refused.

Add C18 coverage that a previously unlisted model passes unchanged, while the
documented `gemini-3.8-flash` / 0.60.0 defect is refused before inference without
querying a model catalog. Keep the required policy-floor and receipt controls.

Alternative: explicitly remove this defect floor as well, pass every pin on
0.34.0+, and record that a known vendor remapping may remain unobservable. This
weakens what the existing B guard prevents; it needs an explicit owner choice.

## Request to Claude's shared-spec maintainer

After the owner selects the policy, reconcile R-MODEL, R-GOOGLE,
R-CLI-VERSION and C18 together. Check A's Gemini CLI gate-removal path against
the exact `gemini-3.8-flash` / 0.60.0 combination, and report source/test evidence
or an explicit unmeasured limit. Do not infer correctness from B's previous
allowlist or A's completed gate-removal commit. No native-leg changes requested.

## Execution state

The Codex Google unit reached expected RED: seven new classifier-independent
wrapper cases failed on existing catalog gates; the source-skill executor also
selected catalog refusal. Initial removal edits are unreviewed and retained in
Codex's task evidence `model-draft-held/candidate.patch`; source was restored to
the exact pre-unit state, preserving unrelated work. Dependent Gemini
implementation stops here until this conflict is decided; neither the unit nor
whole-task completion is claimed.
