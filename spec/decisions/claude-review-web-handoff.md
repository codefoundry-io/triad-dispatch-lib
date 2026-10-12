# Claude implementation handoff

> **Historical handoff; its review-web instructions are superseded on 2026-10-03.**
> The direct-request-only review web below, including the copy-ready prompt, describes the earlier rule. Current
> [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB) allows web for every selected review leg in every round by
> the owner's standing authorization ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)).

Complete the existing TRIAD skill infrastructure first. PRD/contract-anchor
spec-to-code methodology remains a research proposal; no UI or general framework
is part of this implementation.

Later operating-profile request: use
[the Codex + three Google handoff](claude-codex-google-four-leg-handoff.md) for
the four-entry/two-family scenario and current published A/B source distinctions.

## Primary implementation inputs

1. [Claude implementation PRD, including source-line migration guidance](https://github.com/codefoundry-io/triad-dispatch-spec/blob/140dda4ce66dfb5b34ba86d7e4c1356dafd026a0/decisions/claude-host-v2-implementation-prd.md).
2. [V2 implementation specification](https://github.com/codefoundry-io/triad-dispatch-spec/blob/140dda4ce66dfb5b34ba86d7e4c1356dafd026a0/decisions/rev-2-implementation-spec.md).

Apply the later [owner-requested review-web amendment](https://github.com/codefoundry-io/triad-dispatch-spec/blob/7f527ef1777336b93ca626744aedcd0c7d90aff9/reference/review-rules.md#R-REVIEW-WEB)
where the older inputs say REVIEW is always no-web. The amendment permits web only
on a direct owner request for the current review, across every participating leg,
with one short common permission clause and no technology-detection heuristic.

[Current B verification and remaining limits](host-b-review-web-verification.md).
[Current A source differences and adoption handoff](2026-09-21-owner-requested-claude-web.md).
A acknowledgement and adoption are pending. Recheck A's actual checkout; pinned
line references describe the recorded source, not a guarantee about later edits.
At the latest read-only check, A was already at `db9d97e0f3ef81af65be92ee463bca6fc26babcd`
with implementation changes in progress. Preserve those changes and continue the
current stage; do not restart from the older PRD's source snapshot.

## Known issues to retain

- [KI-AGY-URL-BODY-PREFIX](https://github.com/codefoundry-io/triad-dispatch-spec/blob/140dda4ce66dfb5b34ba86d7e4c1356dafd026a0/decisions/2026-09-20-owner-follow-up.md#ki-agy-url-body-prefix-non-fatal-known-issue): incomplete delivered page bodies are an observed external limitation, not a confirmed wrapper defect. Preserve terminal success and mark affected evidence incomplete/UNSURE; no automatic retry or invented error token.
- Missing effective-policy/runtime identity evidence remains unverified. Keep unrun authenticated checks marked NOT RUN; a selected model, tool name, URL, path-only read event or successful exit is not complete execution/read proof.
- Preserve A's active AGY hook/load/read-audit and native Claude admission path. B's dormant hook and CLI Claude topology are not migration templates for A.
- The shared web flag authorizes use; it does not equate Claude tool permissions with Codex cached/live search or change host search modes. Cached web content remains untrusted.
- The linked B verification record retains its nonblocking legacy bundle-error diagnostic and default-v2 text-assertion gaps. Verify A's own source before treating either as an A defect.

## Prompt to give Claude

```text
위 구현 PRD와 v2 스펙, 후속 웹 권한 amendment 및 known issues를 기준으로
Claude 호스트 TRIAD 스킬 인프라를 완성해줘. 진행 중인 변경을 보존하고
현재 단계부터 이어가. 실제 checkout과 문서의 차이를 코드 위치로 짧게
브리핑하고, 기존 기능을 보존하는 최소 변경으로 진행해.
PRD/spec-to-code 방법론, UI, 일반화 프레임워크는 이번 구현 범위가 아니야.

리뷰 웹은 내가 해당 리뷰에서 직접 요청할 때만 모든 참여 leg에 허용하고,
신기술 판단이나 자동 검색 트리거, 긴 공통 프롬프트를 추가하지 마.
웹 허가와 벤더별 검색 모드는 별개로 다뤄. 기존 owner deny는 보존하고,
지원하지 못하는 허가는 사전검사에서 거절해. A의 native Claude 경로와
AGY hook/load/read-audit를 B 구조로 대체하지 마.

현재 소스에서 발견 사항을 확인하고 계약 사례 → 실패 테스트 → 최소 구현 →
회귀 검증 → 정해진 리뷰 순서로 마무리해. 미검증 외부 동작과 known issue는
해결됐다고 쓰지 말고 별도로 기록해. 최종 merge·설치·release는 별도 결정이야.
```
