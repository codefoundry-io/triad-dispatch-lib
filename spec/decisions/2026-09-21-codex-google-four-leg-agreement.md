# Codex + three Google legs: operating agreement

> **Historical agreement; approval and per-leg personas superseded on 2026-10-02.**
> The fewer-than-three-family approval condition, distinct review emphases and owner-final
> machine-review approval below describe the earlier contract. Current
> [R-AGREE](../reference/review-rules.md#R-AGREE),
> [R-ROSTER](../reference/review-rules.md#R-ROSTER) and
> [R-PROMPT](../reference/review-rules.md#R-PROMPT) require explicit approval from every selected leg,
> independent of family count, with one shared purpose and no default per-leg personas.
> Use the [current Claude implementation handoff](claude-review-strategy-handoff.md).
> The topology and dated evidence remain historical context; human integration, merge, installation
> and release authority stays separate from machine agreement.

Status: owner-requested operating profile under the existing shared rules;
Claude maintainer acknowledgement is pending. This is not a new revision tag,
host adoption, a completed review round, or approval of a future result.

## Owner intent and scope

The owner clarified the intended topology:

> 1개 codex 서브에이전트와 1google leg가 뷸안하니 여러렌즈로 규글을 3개 뛰워서 4leg로 쓸수 있나묻는거야

The owner then clarified the decision boundary:

> 작동에는 문제가 없는거지 리뷰승인은 내가하면되고?

The owner requested publication and a Claude handoff:

> 합의문서랑 spec 리모트에 올려놓고 cluade가작업할 프롬프트줘

These statements establish the requested operating scenario: one Codex reviewer
and three independently invoked Google reviewers, with different review emphases,
followed by the owner's decision. They do not establish a successful four-leg
live run or approve its future findings in advance. The owner decision index is
[D-FOUR-LEG-20260921](owner-register.md#d-four-leg-20260921).

The agreed implementation basis already supports named entries and the owner
decision boundary. No automatic `lens`/`focus` field, new scheduler, majority
vote, reduced validation, or replacement agreement token is requested here.
The concrete operating specification is
[codex-google-four-leg-operating-spec.md](codex-google-four-leg-operating-spec.md).
Automatic per-entry lens configuration is a separate, unapproved extension.

## Existing rules reused

- [R-ROSTER](../reference/review-rules.md#R-ROSTER) already allows additional
  same-family entries with a different perspective; the default remains three
  families. Four entries in this profile still cover only Codex and Google.
- [R-AGREE](../reference/review-rules.md#R-AGREE) already requires a recorded
  owner decision when fewer than three families return results. It does not
  turn absent, invalid or failed results into agreement.
- [R-BIND](../reference/review-rules.md#R-BIND),
  [R-RETRY](../reference/review-rules.md#R-RETRY) and
  [R-REREVIEW](../reference/review-rules.md#R-REREVIEW) preserve separate named
  attempts, failure evidence, unchanged-basis retry and complete re-review when
  the source or review conditions change.
- [R-SMELL](../reference/review-rules.md#R-SMELL) remains a common criterion for
  every reviewer. An emphasis never creates a reviewer exempt from common scope.

No normative rule, schema, shared prompt clause, policy payload or default roster
changes in this agreement. Case C33 specializes the existing rules for this
profile; it does not redefine their expected behavior.

## Source evidence and publication boundary

Shared remote `main` was fetched on 2026-09-21 at
`2eb883fee59e66556ee7c7f87189b38231136622`. The existing authoring branch
`codex/host-b-preimplementation-audit` and local authoring basis both resolved to
`921388bfb3973c64c19677fa8bf5eebb34f1aac1`, with no main-only changes.
At that publication checkpoint, this amendment was on the authoring branch.
PR #1 subsequently merged it into `main` at
`c6406eb1a3a09fefdc1d7e98f26095242bd07c07`; revision tagging and host adoption
remain separate.

Host B is publicly released as
[v0.2.556](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.556)
at `5a12f822b6e19f5ecd162e4cc54888269ec0ffd9`. Its tree equals the reviewed/tested
`2d4d71b1a6df09b26fae44d228229cd9aa43218d` tree. Source inspection confirms:

| Boundary | Released B source |
|---|---|
| Merge overrides by unique entry name | [review_roster.py:70](https://github.com/codefoundry-io/triad-codex-dispatch/blob/5a12f822b6e19f5ecd162e4cc54888269ec0ffd9/bin/review_roster.py#L70) |
| Prepare each enabled entry's own controls and receipts | [review_adapters_v2.py:206](https://github.com/codefoundry-io/triad-codex-dispatch/blob/5a12f822b6e19f5ecd162e4cc54888269ec0ffd9/bin/review_adapters_v2.py#L206) |
| Common task/criteria, with bound leg identity | [review_round_v2.py:189](https://github.com/codefoundry-io/triad-codex-dispatch/blob/5a12f822b6e19f5ecd162e4cc54888269ec0ffd9/bin/review_round_v2.py#L189) |
| Independent attempt/result/read-evidence paths | [review_round_v2.py:283](https://github.com/codefoundry-io/triad-codex-dispatch/blob/5a12f822b6e19f5ecd162e4cc54888269ec0ffd9/bin/review_round_v2.py#L283) |
| Two-family completion requires owner decision | [review_round_v2.py:505](https://github.com/codefoundry-io/triad-codex-dispatch/blob/5a12f822b6e19f5ecd162e4cc54888269ec0ffd9/bin/review_round_v2.py#L505) |

The three-Google simultaneous live scenario remains NOT RUN. The separate
[owner-confirmed Gemini invocation](owner-register.md#gemini-invocation-20260921)
does not establish it. Schema acceptance, source inspection, deterministic tests,
live invocation, owner approval and host adoption remain distinct evidence.

Authoring verification on 2026-09-21: 80 existing shared schema/policy tests
passed; the example validated both as an override and after merging B's released
defaults, with exactly four enabled entries/two families. Local links/anchors and
all 33 case IDs, surfaces and rule references passed. These are offline checks.

Claude's bounded work and current-source seams are in
[the handoff](claude-codex-google-four-leg-handoff.md). Recheck the actual checkout
before work; retain its existing changes and host-native execution topology.
