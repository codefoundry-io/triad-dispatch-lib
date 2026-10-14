# Claude handoff: Codex + three Google review legs

> **Historical handoff; agreement and per-leg personas superseded on 2026-10-02.**
> The two-family `OWNER_DECISION_REQUIRED` condition, separate leg emphases and owner-final
> machine-review approval below describe the earlier contract, including its copy-ready prompt.
> Current [R-AGREE](../reference/review-rules.md#R-AGREE),
> [R-ROSTER](../reference/review-rules.md#R-ROSTER) and
> [R-PROMPT](../reference/review-rules.md#R-PROMPT) require explicit approval from every selected leg,
> independent of family count, with one shared purpose and no default per-leg personas.
> Use the [current Claude implementation handoff](claude-review-strategy-handoff.md).
> Historical source evidence remains a record; human integration, merge, installation and release
> authority stays separate from machine agreement.
> Its review-web instruction (input 4 and the paragraph after the inputs: web only on the owner's direct request) is
> superseded on 2026-10-03 by [D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003): current
> [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB) allows web for every selected review leg in every round.

Finish the existing TRIAD skill infrastructure. This is a concrete operating
profile under existing contracts, not a UI project or PRD/spec-to-code research
framework. Claude acknowledgement of this amendment remains pending.

## Read these inputs at the same handed commit

1. [Owner operating agreement](2026-09-21-codex-google-four-leg-agreement.md).
2. [Operating specification and B project-roster example](codex-google-four-leg-operating-spec.md).
3. [Existing Claude-host implementation PRD](claude-host-v2-implementation-prd.md)
   and [v2 implementation specification](rev-2-implementation-spec.md).
4. [Review-web handoff and retained known issues](claude-review-web-handoff.md).

The first two specialize the existing roster/agreement rules. They do not replace
the v2 contracts. The later R-REVIEW-WEB amendment supersedes older unconditional
REVIEW no-web wording: enable web for every participating leg only on the owner's
direct request for that review, with short wording and no technology heuristic.
Publishing or reading this handoff does not itself enable web for a review.

## Current-source distinction: A is not B

The [agreement's B source table](2026-09-21-codex-google-four-leg-agreement.md#source-evidence-and-publication-boundary)
describes released v0.2.556. B supports named v2 entries; the task table uses the
already-bound `leg_name`. It has no first-class automatic lens field. Its clean
two-family result is `OWNER_DECISION_REQUIRED`.

A's published remote `main` was inspected on 2026-09-21 at
`8efeb74d127a3ca90efe6ed22bbe39cb53719204` in `codefoundry-io/triad-dispatch`.
That remote snapshot is not a claim about A's local implementation in progress.
The earlier local snapshot was `db9d97e0f3ef81af65be92ee463bca6fc26babcd` with
uncommitted implementation work. Inspect the actual checkout, fetch current
remote main, and preserve those changes; do not reset to either snapshot.

| Published A seam | Evidence and consequence |
|---|---|
| Native family is Claude; Google CLIs share one family | [SKILL.md:49](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/SKILL.md#L49-L63). B's native Codex call is not an A migration template. |
| Extra same-family X legs are advisory | [review_scratch.py:2618](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/lib/review_scratch.py#L2618-L2623), [parser:2744](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/lib/review_scratch.py#L2744-L2859). Do not count advisory X legs as proven v2 participating entries. |
| Renderer has no named task/lens input | [review_scratch.py:2395](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/lib/review_scratch.py#L2395-L2498). [X-leg rendering:4483](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/lib/review_scratch.py#L4483-L4507) reuses family prompts. Verify the in-progress v2 task/identity seam rather than adding a new lens schema. |
| Validation and consolidation retain legacy structure | [validate_verdict.py:524](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/lib/validate_verdict.py#L524-L620), [triage.md:282](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/references/triage.md#L282-L335). Check named sibling binding, cardinality and two-family disposition in the actual v2 implementation. |
| Owner decision is procedural | [triage.md:38](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/references/triage.md#L38-L62). A verdict alone is not evidence that the owner approved it. |

The exact request uses a native Codex child on B. An A equivalent uses its Codex
CLI route; identify that difference rather than promising the identical native
topology. Preserve A's native Claude route and active AGY hook/load/read-audit.
Do not edit B merely to make the hosts look alike.

## Bounded work and acceptance evidence

- Brief the owner on current implementation versus these contracts, with exact
  code locations. Reuse current v2 work; do not restart the older PRD plan.
- Map C33 and its C12/C14/C19/C20 dependencies to existing tests. Where current
  code fails an already approved contract, follow the repository's diagnosis and
  TDD process; implement only the confirmed in-scope gap. Propose any new contract
  separately before implementation.
- Deliver the host-appropriate roster/task example, four separate bound attempt
  and evidence paths, verified two-family disposition, retry/re-review checks,
  and the owner's round-specific decision record when a live round is approved.
- Keep exact live four-leg execution NOT RUN until actually performed. A single
  owner-confirmed Gemini invocation does not prove concurrency, effective policy,
  runtime model identity or distinct lens coverage.
- Retain KI-AGY-URL-BODY-PREFIX and other unresolved evidence limits from the web
  handoff. Do not call a URL, cached search result, path-only read event or exit 0
  complete source evidence. Keep missing external checks separate from code fixes.

No new `lens`/`focus`/`prompt` roster field, voting policy, scheduler, long common
prompt, UI or generalized framework is approved by this handoff. Merge,
installation, release and shared revision tagging keep their existing boundaries.

## Copy-ready prompt

```text
이 커밋의 합의문, 운영 스펙, Claude 인계 문서를 읽고 기존 TRIAD 스킬
인프라 작업을 이어서 마무리해줘. 현재 checkout과 진행 중인 변경을 보존하고,
문서와 구현의 차이를 코드 위치와 함께 먼저 짧게 브리핑해.

요구사항은 Codex 1개 + 서로 다른 관점의 Google 3개, 총 4개 leg야.
모두 공통 전체 범위를 검토하고 TASK의 leg 이름별 관점 표를 사용해.
최종 승인은 내가 해당 결과를 보고 결정해. 4개 leg는 2개 계열이며,
누락·실패·차단 결과를 합의로 바꾸거나 내 사전 승인으로 취급하지 마.
Codex native는 B의 경로야. A는 기존 native Claude/Codex CLI 구조와
AGY hook/load/read-audit를 보존하고 현재 v2 구현에 맞춰 적용해.

C33과 기존 계약 사례를 검증하고 필요한 기존 계약 미충족 부분만
저장소의 진단·TDD·리뷰 절차로 수정해. 자동 lens 필드나 새 투표 정책,
UI, PRD/spec-to-code 연구는 추가하지 마. 리뷰 웹은 내가 그 리뷰에서
직접 요청할 때만 전 leg에 허용하고 짧은 공통 문구만 사용해.
Known issue와 미실행 검증은 남겨두고, 완료 보고에 변경·검증·남은 제약을
구분해줘. 최종 merge·설치·release는 기존 승인 경계를 유지해.
```
