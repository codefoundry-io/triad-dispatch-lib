# Host B owner-requested review web verification

> **Historical record; its review-web condition is superseded on 2026-10-03.** The direct-owner-request,
> default-false review web it records is replaced by the owner's standing authorization in current
> [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)).

Status: source implementation verified; host A acknowledgement and adoption pending.
This records the implementation of the owner amendment at
`7f527ef1777336b93ca626744aedcd0c7d90aff9`; it does not change its prompt or policy bytes.

## Source and contract

B source: `3c09ad192d5d4aab22620f960367a003d34c5e71`, [PR #37](https://github.com/codefoundry-io/triad-codex-dispatch/pull/37).
Only a direct owner request for the current review enables web for its participating
legs. The shared `review_web_authorized` condition defaults to false and binds the
legacy/v2 basis, rendered prompts, preflight and CLI invocation. The common prompt
adds one short permission clause. There is no technology classifier or automatic
search trigger. Raw Claude forwards the caller prompt unchanged and adds exactly
`--allowedTools WebSearch WebFetch`; existing deny rules remain authoritative.

AGY preserves its non-web restrictions, no-autoapproval formal invocation and
settings restoration. Gemini selects the complete separately pinned web profile;
default profile bytes remain unchanged. Native Codex receives the same conditional
prompt and requires a bound current-host web-availability report. Known AGY
`read_url(*)` owner denies refuse requested review web before inference without
removing the owner's rule. No new public verdict or transport fields were introduced;
no persistent global configuration, installed cache or host A source was edited.

Authorization does not select the provider's search mode. Codex's
[cached and live modes](https://learn.chatgpt.com/docs/config-file/config-basic#web-search-mode)
remain host settings; cached results reduce prompt-injection exposure but remain
untrusted. Claude's native tool permissions are a separate control. This clarification
adds no common-prompt clause or automatic mode switch.

## Source entry points

These B references describe verified behavior; A preserves its own topology.

| Boundary | B implementation |
|---|---|
| Fixed raw/formal Claude web permit | [claude_wrapper.py:418](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/claude_wrapper.py#L418) |
| Strict prompt/flag binding | [_common.py:577](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/_common.py#L577) |
| Native web availability in v2 controls | [review_adapters_v2.py:61](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/review_adapters_v2.py#L61) |
| Legacy prepared/worktree host observation | [review_round.py:2006](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/review_round.py#L2006), [review_round.py:2128](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/review_round.py#L2128) |
| Known AGY deny refusal and active lease check | [_agy_settings.py:95](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/_agy_settings.py#L95), [_agy_settings.py:571](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3c09ad192d5d4aab22620f960367a003d34c5e71/bin/_agy_settings.py#L571) |

## Verification

- Dedicated source-skill RED: 28 failed / 7 passed before implementation.
- Dedicated preflight-correction RED: 12 intended failures before correction.
- Dedicated documentation scenario: mode-specific operator guidance was RED before
  correction and GREEN afterward; existing regression coverage was retained.
- Final dedicated GREEN: 61 focused tests and 1682 full-suite tests passed;
  source fingerprint remained unchanged and owned fixtures were removed.
- Source skill validator and provider-free lifecycle: passed; lifecycle SUCCESS.
- Formal round `triad-b-review-web-r4`: ADMITTED_SAFE with matching final source integrity;
  Claude opus/xhigh, AGY Pro/high, AGY Flash/high and fresh Codex Terra/xhigh.
  This gate used the default no-web condition, as the owner did not request web
  for this review. It does not prove live effective web permissions in every route.
- Shared contract suite: 80 tests passed at the amendment commit.

## Live observation and remaining limits

Retained nonblocking review observations: v2 basis creation and rendering perform
repeated validation reads of the small pinned prompt bundle; the legacy default branch imports v2 to recover
the existing no-web constant. The shared explanatory note quotes the first no-web
sentence, while B preserves its existing second sentence about reporting external
evidence gaps. The normative rule permits the host's normal no-web clause; current
restriction and digest behavior remain correct. These efficiency/documentation
refinements are recorded without changing reviewed bytes or vendored payloads.
Legacy Claude relies on the native CLI refusing an unsupported `--allowedTools`
option at dispatch; v2 probes support before sealing. Current selected CLI support
was observed, but this is not a claim of preflight coverage for every legacy CLI.

Two additional nonblocking limits remain source-confirmed:

- An authorized legacy render encountering a corrupt or unreadable pinned web
  prompt bundle can emit a traceback/exit 1 instead of the usual controlled
  diagnostic/exit 2. It refuses before prompt emission or inference; default
  no-web rendering is unaffected (`review_round.py:98-100,2585-2587`).
- The per-family default v2 render test does not directly assert the no-web
  sentence and removal of its placeholder. Current substitution is correct by
  source inspection and pinned-payload checks; this is a targeted coverage gap.

These are B observations, not established A defects or reasons to broaden policy.

One actual source Claude wrapper probe exited 0 with zero recorded permission
denials and the fixed web argv. Its response described a partial page preview;
complete page verification was not established. This is an evidence-coverage limit,
not a confirmed vendor defect. No retry was used to hide that limit.

Authenticated all-provider authorized-review checks in `contracts/review-web.verify.toml`
remain NOT RUN, as do the previously unrun host policy checks. No revision tag,
installation, fresh-process exposure, distribution archive for this candidate,
final merge or release is claimed. The prior archive verification belongs to its
earlier source commit. The existing AGY body-prefix observation and host A's active
hook/read-audit requirements remain as documented in the implementation PRD and
known-issue handoff. PRD-to-contract/spec-to-code research remains a proposal.
