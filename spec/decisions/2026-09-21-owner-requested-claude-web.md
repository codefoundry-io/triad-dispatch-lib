# Owner-requested all-leg review web — verification and host handoff

> **Historical record; its review-web condition is superseded on 2026-10-03.** The direct-owner-request,
> default-false review web it records is replaced by the owner's standing authorization in current
> [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)).

Status: owner-authorized amendment; B source implementation verified in
[the current verification record](host-b-review-web-verification.md). Host A acknowledgement
and adoption remain pending; no revision tag or release is claimed.
The owner request and its exact clarification are in the owner register; the normative rule is
[R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB). Research methodology work remains a proposal.

## Evidence and change

Shared pre-change basis: `140dda4ce66dfb5b34ba86d7e4c1356dafd026a0`.
Remote main fetched before authoring: `2eb883fee59e66556ee7c7f87189b38231136622`; no main-only changes.
B pre-change source: `add5805d8dec70f5e133164c49bc0fe3bff75095`.

At the B pre-change baseline, `bin/claude_wrapper.py:391` built fixed native argv
without web preapproval; `:226` exposed no `--web`.
An authorized research call returned exit zero but four native permission denials and no fetched pages.
The prompt's authorization could not grant native tool permission. A task-scoped native probe using
`--allowedTools WebSearch WebFetch` succeeded with no denials; the shared wrapper was still unchanged.
Official references: [Claude permissions](https://code.claude.com/docs/en/permissions),
[CLI reference](https://code.claude.com/docs/en/cli-reference); local CLI help confirmed the native flag.
This is an adapter authorization omission, not a confirmed vendor defect or a reason to loosen global policy.

The owner extended the correction to every leg, then requested minimal prompt wording and no leader judgment
about new technology. B adds fixed Claude `--web`, legacy `--web-authorized`, and transient v2
`review_web_authorized`. Google preflight and wrappers bind the same option; native Codex receives the same
short common permission clause. Gemini selects the complete web-enabled B profile while default bytes stay.
Raw Claude forwards the caller prompt unchanged. Existing raw Google evidence procedure remains unchanged.
Cases C31/C32 bind this behavior. Completed B source checks and their exact limits are
recorded in [the verification record](host-b-review-web-verification.md).

## Host A review request for this commit

Claude maintainer: review amendment `7f527ef1777336b93ca626744aedcd0c7d90aff9`,
including the all-leg rule, shared clause and C31/C32, before adopting.
Acknowledgement is PENDING; no previous agreement is carried forward. Under the owner-designated B-first sequence,
B proceeds on the owner's settled scope and records its result for your later implementation. Do not infer adoption
from this shared branch publication or copy B CLI controls into A's native agent route.

Read-only observation on 2026-09-21: A HEAD
`db9d97e0f3ef81af65be92ee463bca6fc26babcd`, with uncommitted skill/reference and wrapper
guidance work after its gate-1 fix-wave-8 commit. Its round-9 ledger is in progress. No A changes were made by B. Preserve
that work and continue its current stage. Line locations below describe the observed
working tree; recheck dirty files before editing. This is no A implementation or
effective-permission attestation.

- Native Claude v2 identity comes from the resolved roster:
  `.claude/skills/triad-cross-family-review/spec/review-legs.default.json:10-14`
  names `cross-family-review-reviewer`; `lib/roster_v2.py:884-895` emits the native
  subagent_type from the selected entry. Inspect that actual selected native path.
  `.claude/agents/cross-family-review-reviewer.md:4` currently lists Read/Grep/Glob,
  and its body excludes network tools. Preserve its native raw-admission boundary
  while supporting the explicit current-review web condition at A adoption.
  The separate `triad-reviewer` preset is not the cross-family review leg.
- `lib/prompts_v2.py` and `lib/review_scratch.py` remain the prompt/basis seams.
  No `review_web_authorized` occurrence was found in the inspected current files.
  `review_scratch.py:3525` still describes the legacy Codex review route as never
  passing --search. Add no unbound default search behavior.
- `3rd-Agent/wrappers/codex_wrapper.py:103-115,448-453` already distinguishes live
  `codex --search exec` from the explicit no-search `web_search="disabled"` setting.
  Merely omitting --search would leave Codex's cached default available; preserve
  the existing explicit no-web behavior. The common permission bit does not choose
  a uniform cached/live mode for all vendors.

This refresh supersedes older source-location guidance only. Shared contract
adoption, A review acknowledgement, and A service verification remain pending.

## Verification boundary

The [B verification record](host-b-review-web-verification.md) identifies dedicated
RED/GREEN, regressions, source-skill validation, provider-free lifecycle and the
complete formal review. Shared schema tests and anchor/case/unit checks verify
document structure only. Unrun host/service checks remain NOT RUN; search
summaries, prose URLs, successful exit and prefix-only fetched bodies are not
complete evidence. Source checks do not establish host A adoption or installed
behavior.

Known AGY delivered-body limitation remains independently documented as KI-AGY-URL-BODY-PREFIX; no new failure token,
automatic retry, provider-fix claim or permanent raw web-content store is introduced.
