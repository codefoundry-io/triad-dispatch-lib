# Worktree discovery and incident-driven log inspection

Owner decision: D-REVIEW-DISCOVERY-20261009. Rules/cases: R-PROMPT, R-CONTAIN,
R-VERIFY, C70/C71. Latest main fetched 2026-10-09: `3afc4d7`; PR12 `6a2883d`,
PR13 prior head `5c040ff`. This draft is not adoption or release.

## Evidence and current behavior

B source `632f426` plus dirty work: canonical SKILL.md:39-44 permits paths or
categories; bin/review_round.py:2250-2261 permits related unchanged inspection.
However, B's Opus R1 operational render-review.py:50-52 imposed exact-file-only
access. Its close-review.py:67-80 read AGY telemetry on every normal collection
and failed paths absent from that list. The approved adapter's direct capability
JSON dependency was not listed. Two independent fresh Codex Sol/high diagnoses
confirmed the causal chain. B's local diagnosis names exact evidence paths.

A source inspected read-only at `a91b436365385751beac674d21579ab91f4d8157`, clean:
all paths below are under `.claude/skills/triad-cross-family-review/`.

- spec/prompts/leg-claude.md:22 permits Read/Grep/Glob including unchanged code;
  leg-google.md:28,34 allows verification beyond the patch and scoped search.
- lib/prompts_v2.py:258-284 binds packet inputs, without a per-source-file grant
  field; SKILL.md:208-212 permits verification across the pinned tree.
- lib/collect_v2.py:1022-1059 and lib/review_scratch.py:4443-4454 use AGY's
  required-input-read and hook checks. lib/read_audit_gate.sh:180-181 checks
  successful reads of brief.md and diff.prod.patch, not every source path
  against a source allowlist. These are coded route controls, not a leader's
  routine forensic source-path audit.

No equivalent exact-file-only defect was established on A. Both hosts' wording
leaves the distinction between packet inventory and source inspection implicit;
the common clarification prevents B's observed misuse from becoming a contract.
No A runtime test or provider invocation was performed in this investigation.

## Correction and preserved behavior

R-PROMPT now explicitly gives related-file discovery to the reviewer and limits
leader log inspection to concrete incidents or requested audits. C70/C71 define
normal and boundary cases before B implementation. The common code-purpose
clause carries the reviewer-facing clarification without a new prompt engine,
field, file authorization mechanism or per-leg rule. Preserve read-only tools,
explicit exclusions, symlink-target binding, required route evidence, immutable
results and source integrity. Each native leg stays host-owned.

B corrected its project guidance and future round scripts, retaining failed
historical receipts. A fresh canonical-skill baseline already selected the
intended behavior, so B's product skill/renderer needed no change. A fresh
follow-up executor discovered an unlisted helper defect through the diff's
caller and chose incident-driven log inspection. Controlled collector cases
failed on the unwanted audit-log dependency before removal, then all three
passed. Combined collector/review-round/review-condition checks: 191 passed
in 23.74s; skill validator valid, all under-test hashes unchanged. The executor
disclosed generic lifecycle-memory exposure, without this scenario's expected
answer or defect. No operational review, A execution, revision adoption or
authenticated-service conformance is claimed. B's next U1b round remains pending.

Subsequent live U1b R2: three SAFE, Pro NOT-SAFE due to missing native search
tools, with matching integrity. The distinct AGY default-toolset change and
proposed remedy are recorded in [the capability follow-up](2026-10-09-agy-search-tools.md).
This does not reinstate source allowlists or routine read-log audits.

## Request to Claude maintainer

Review this same spec commit's R-PROMPT/code-purpose/C70/C71 clarification.
Confirm the source observations above against your current checkout; adopt the
shared prompt clarification through your normal revision process. Check that
operational leader instructions do not add exhaustive source lists or routine
manual read-log inspection. Preserve existing AGY required-input-read/tool-effect
and hook checks: this request does not remove them or change your native leg.
Report any conflicting requirement with its exact source and observable effect.
