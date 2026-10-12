# Owner decisions — rulings and their effect (public, site-neutral)

Dates in decision headings and IDs are the owner's local date (KST, UTC+9); timestamps given with `Z` are UTC.

<a id="D-U8-WITHDRAWN-20261010"></a>
## D-U8-WITHDRAWN-20261010: withdraw installation coexistence work

Owner, 2026-10-10, direct instruction to the Codex leader (verbatim):

> 설치 공존 — U8 이건 사용자 문제고 레어케이스니 폐기

Recorded effect: installation coexistence is an operator-managed rare case;
withdraw B's entire U8 investigation/implementation unit, including dual-install
launcher resolution, upgrade-path pin probes and the concurrent configuration
publication investigation. Remove its tests/review work and completion
dependencies; do not transfer them to another unit or silently reopen them.
This is WITHDRAWN, not FIXED or verified. A new explicit owner scope decision is
required to reopen the unit.

B's U8 checks under DL-105/108/109 are withdrawn accordingly; historical rows
remain evidence, not active scheduling authority. Other requirements once listed
as U8 references (authentication, binary presence and existing preflight binding)
are not repealed, and no new work is created by preserving them. Existing
installation code/tests stay. U7's runtime AGY shared-settings work is separate.
Share this disposition with A for its own plan reconciliation; it does not
authorize B to edit A's host code or label A's independent work completed.

<a id="D-NO-CLAUDE-AGENT-BACKLOG-20261009"></a>
## D-NO-CLAUDE-AGENT-BACKLOG-20261009: remove unsupported agent work

Owner, direct instruction (verbatim):

> claude에 --agent 가 들어가야할 이유가 있으면 넣어 근데 없으면 깔끔하게 플랜 문서 메모리에서 지워라

Current B evidence supplies no need to introduce a named Claude CLI agent:
the shipped roster has agent null; the adapter and wrapper pass model/effort
directly; prior bounded diagnostics established reading/searching without agent
selection. An existing optional pass-through and its tests are not a use case.
Remove the former U1c task and deferred/resume instructions from active plans,
handoffs and memory guidance. Do not retain it as a dormant research obligation.
This supersedes its deferred status under the preceding backlog decision.

This planning/documentation cleanup does not remove the existing optional CLI
interface or certify its unresolved binding behavior. Conditional C19/DL-49
compatibility requirements remain if that interface is actually selected;
they do not create a resolver project. AGY profiles and host-native agents are
unaffected. A concrete future need is a new scope decision, not automatic resume.

<a id="D-BACKLOG-DISPOSITIONS-20261009"></a>
## D-BACKLOG-DISPOSITIONS-20261009: distinguish non-active work and plan its removal

Owner, direct instruction (verbatim):

> 보류 폐끼 이식 불필ㅇ됴 항목읁 차이점으로 스펙에 업데이트하고 없애는거 플랜에 넣어

Interpretation: record deferred, withdrawn and no-port differences in the shared
specification; remove obsolete active tasks and plan removal of confirmed
remnants. Preserve deferred-feature contracts and historical evidence. The
[item dispositions and removal scope](2026-10-09-backlog-dispositions.md) apply
to both hosts' corresponding plans without changing native-leg ownership.

<a id="D-PROMPT-REVIEW-BOUNDED-20261009"></a>
## D-PROMPT-REVIEW-BOUNDED-20261009: bounded prompt review and U4a residual acceptance

Owner, direct reply to the Codex leader's request to treat the two remaining U4a
README/phrase-pinning-test demands as nonblocking and proceed to U4b (verbatim):

> OK 프롬프트는 나중에 내가 직잡볼테니 2~3번 큰 디펙만 보고 실제 동직만 보는지금 방식이 맞아

For prompt work in this shared spec-to-code effort, use two to three review
passes focused on substantial defects and observed behavior. The owner will
inspect prompt wording later. When wording judgments repeat, use the established
fresh scenario/control probes; correct decisions end wording iteration. Do not
add literal-pinning tests solely to satisfy wording review. A demonstrated wrong
decision or unresolved substantial defect still needs correction or escalation;
the pass count is not an automatic correctness or approval result.

Specific disposition: the owner accepts B U4a's two remaining demands as
nonblocking and authorizes the next U4b stage on the existing tested candidate.
Keep R1/R2/R3 NOT_APPROVED receipts unchanged; record owner acceptance separately.
No fourth unchanged prompt round, native-leg change, installation, merge or release
is authorized or required. This does not rewrite the collector or its unanimous
approval semantics. Both maintainers use the bounded prompt-development guidance;
each host retains its implementation and native mechanisms.

<a id="D-SELECTOR-PROPOSAL-WITHDRAWN-20261009"></a>
## Model/effort environment proposal withdrawn — 2026-10-09

Owner (verbatim):

> 이 스펙은 없애자 어차피 사용자 환경 설정은 건드리는거 아니고 기존에 effort는 잘 동작했으니 스펙에서도 폐기해

Discard the additional selector inspection/warning/verification proposal,
including the preceding preserve-and-warn direction. Preserve user settings
and existing model/effort forwarding. Historical research is not an outstanding
implementation requirement. See the [bounded cancellation and host effects](2026-10-09-selector-proposal-withdrawn.md).


<a id="D-REVIEW-STRATEGY-20261002"></a>
## Review strategy — owner direction, 2026-10-02

Verbatim excerpts from the current Codex conversation (the original Korean is preserved):

> 내 의견을 주자면 leg의 만장일치가 통과 기준이지 leg가 몇개인지 같은 모델 계열인지는 안 중요한 것 같아. 구독 요금이나 한도에 따라서 매번 조절 가능한게 맞는 것 같아.

> 프롬프트에 대한 지침은 니가 테스트할수 없어. 너는 이 직전의  결정과 지침 컨텍스트에 영향을 받고 니가 스킬이나 프롬프트를 재현하려면 ㄹresy eye에서 스킬을 테스트하거나 해야하는데 그건 triad 스킬의 범위를 벗어난 거야.

> 기존 리뷰 프롬프트에서 환경이나 라이브러리버전 이런 부분이 제대로 전달되지 않아서 리뷰어가 잘못판단하지 않을까 하는 우려가 있는데
> 기계적으로 복사하듯이 넣어야 하는 부분과 메인에이전트가 그때그때 판단에 따라 넣어줘야하는 부분들이 이전처럼 잘 나뉘어져 있으면 좋겠어.

> 이제 스펙을  PR을 업데이트하고 구현에 들어갈 검토를 시작하자 제시안 부터 줘 md로 줘 굳이 html로 만들지 말고

> 이후에 큰 이견 없으면 스펙 업데이트하고 업데이트 전에 정리사항 다시 md로 공유해줘

> 그리고 모델의 업데이트가 잦으니 모델명 설정을 쉽게하고 codex, agy, claude 버전을 너무 엄격하게 보지마
> 생성 파일에 대한 클린업을 다른 스펙 참고해서 제대로 관리하도록 우지 할 것

> claude 쪽 코드는 보지마 아직 스펙적용안했어

> Cli 로출하려먄 어쩔수 없이 모델을 정확히 적어야해. 그부분은 냅두고..json에 한군데맘 수정하게 설정으로 뽑으라고 이미되어있을건데

Effects: [R-AGREE](../reference/review-rules.md#R-AGREE), R-ROSTER, R-PROMPT, R-CONTEXT, R-REREVIEW,
R-VERIFY, R-SMELL, R-STOP, R-CLI-VERSION and R-CLEANUP. Historical Q-S/Q1 Minor-only negative release and
D-4/Q-L minimum-family/count release requirements are superseded; Q-B/Q-H/Q-Q's no-blocker test remains necessary
but is not sufficient without each selected leg's explicit approval. D-FOUR-LEG-20260921's per-leg review
emphases/personas, family-count veto and owner-final approval as a machine-agreement condition are also superseded.
Current [R-PROMPT](../reference/review-rules.md#R-PROMPT) supplies one shared purpose;
[R-ROSTER](../reference/review-rules.md#R-ROSTER) and R-AGREE require every selected leg's explicit approval
independent of family coverage. Human integration, merge, installation and release authority remains separate; an owner
exception cannot turn a non-agreed round into machine agreement. Historical outcomes are not rewritten.
The 2026-09-20 per-change A-source inspection directive is suspended for this amendment: use shared specs and
research documents, do not inspect A implementation code, and do not claim current A conformance.
Same-commit shared-spec review remains possible and is separate from A code inspection.

Leader implementation choices, not verbatim owner rulings: reuse existing prose TASK/brief and `prior_residual`, reuse
legacy stage names, materialize needed prior evidence in existing current packet slots, retain wire tokens, and prepare
a separate review-strategy draft PR with explicit overlap against model-policy PR #6. No new model settings framework,
model default change or model-catalogue policy is authorized by this amendment. Exact IDs remain JSON data consumed by
CLI/native dispatch. The MD change summary was shared before spec mutation after Astra/xhigh and Opus 5.5/xhigh
scoped direction review closed two material objections. See [the evidence and adoption record](2026-10-02-review-strategy.md).
This task authorizes the requested spec/PR work, not host implementation, merge, tags, installation or global settings.

## Historical owner decisions

> **Historical record.** The 2026-09-21 direct-request condition below is superseded for review web by
> [D-REVIEW-LEGS-20261003](#D-REVIEW-LEGS-20261003) (standing authorization; R-REVIEW-WEB now binds true for every round).

2026-09-21 follow-up: owner requested “Claude 웹 수정하고 원격 spec에도 기입해” and clarified
“리뷰시도 웹감증 허용했는데 직접적으료 요청할때만”. The owner then clarified “다른 leg 마찬가지야. 리뷰시 신규기슐은 web검색없으면 없는 Api기능이라고 리뷰한다” and
“그렇게까지 프롬프트를 늘리지마 내가 직접 요청할께 신기술 판단은 리더도못해”. Apply the direct-request condition
to all legs with short permission wording, without technology-detection rules. This conditionally supersedes D-9's absolute
REVIEW prohibition: direct owner request for the current round only. The normative rule is
[R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB); implementation and host boundaries are in
[the amendment and handoff](2026-09-21-owner-requested-claude-web.md). This authorizes the requested
branch amendment, not a revision tag, final merge, global permission change or host A implementation.

This repository is public. Each row records WHAT the owner decided and WHERE it lands here; the owner's exact words
(Korean, verbatim) are kept in the claude host's working record (`triad` plan `2026-09-19-triad-host-parity-plan.md § 8b`)
and in codex's consolidated document for the directions given in codex's session. Where the owner selected an option the
leader had written, the row says "selected option"; the choice is the owner's, the label the leader's. Nothing here is a
new rule; every row points at the normative location.

| ID | Decision | Effect here |
|---|---|---|
| Directive (2026-09-19, current-source and cross-host coordination) | Both leaders read latest remote main; share every common design/contract/prompt/behavior change before implementation; diagnose any omitted existing functionality with three families, however small. Codex drafts the shared protocol; Claude reviews the same commit. Each leader owns only its host | `reference/spec-authoring.md#R-AUTHORING-SYNC`; this new authoring draft awaits Claude review, without carrying forward the old basis acknowledgement |
| Directive (2026-09-20, Codex first) | "니가 먼저 진행하고 같은 문제가 있는지 항상 claude host 쪽 코드를 보고 지적 업데이트해 라인으로 지적하고 codex업데이트가 끝날때 까지 claude 쪽은 업데이트 안할거야" | Lead-host sequencing in `reference/spec-authoring.md#R-AUTHORING-SYNC`; B leads implementation and verification, inspects A at each change, and accumulates commit/file/line evidence and final A instructions. No A edits by Codex |
| D-3 | Verdict wire contract: adjudicate via ONE three-family round, each host keeps its own schema until then | `contracts/leg-verdict.schema.json` (written; host A admits v2 verdicts against its vendored copy, `lib/verdict_v2.py` @ triad `ee011968`); `R-AGREE` last sentence |
| D-4 / Q-L | Three-family review is the default; substitutes are contingency; the model behind each slot is replaceable; at least three legs run | `R-ROSTER` |
| D-9 | Network tools in the gemini review policy: same three-family round, date-anchored web evidence only **Superseded for REVIEW web on 2026-10-03 by [D-REVIEW-LEGS-20261003](#D-REVIEW-LEGS-20261003)** (standing authorization; the no-web posture applies only to a false condition). | `contracts/README.md` (policy row) |
| D-10 | Reviewer framing: CLOSED by owner Q3 (codex session) — evidence-centred, a no-defect conclusion allowed | `prompts/common-clauses.md § adversarial-framing` |
| D-13 | Host A `fixture.sh` contract: header wins (leak prune + 14-day retention), A-side only | none here |
| D-14 / Q4 | RULED 2026-09-19: "링크 자체는 검토하되, 대상을 자동으로 따라가지 않는 방식" — the link itself is reviewed (text fingerprinted, visible); the target is never followed automatically; mechanism per host | `R-PREPARE`, C26 |
| Q-A | The host where gemini is in service can download from GitHub but not upload | `README.md § How a host uses a revision` (owner pushes; results come back by briefing) |
| Q-B / Q-H / Q-Q | Agreement = no unresolved BLOCKING finding from any leg; tiers are data | `R-AGREE`, `R-ROSTER` |
| Q-C | A leg that failed to RUN with nothing changed is retried alone | `R-RETRY` |
| Q-D | A selected investigation returns a free-form report, never a review verdict | `R-ROSTER` last sentences |
| Q-E / Q-M | No "degraded" label ceremony; no per-leg special rules; a leg has a recommended default model, changeable anytime; the count is variable | `R-ROSTER` |
| Q-F / Q-K | No development before the design spec is agreed; approved defect fixes on host A continue | `README.md` (rev-0 is a draft, not implementation authorization) |
| Q-G / Q-J / Q-N | agy and gemini are distinct CLIs of one family with opposite availability at the two sites; keep each host's SHIPPED fallback logic; the owner tests gemini where it is in service and briefs the leader **The two-site framing is superseded as current state on 2026-10-03 by [D-ONE-ENVIRONMENT-20261003](#D-ONE-ENVIRONMENT-20261003)** (host A describes one environment, agy its default Google route and gemini its compatibility route; each host's fallback logic and the owner's gemini testing stand). | `R-GOOGLE` |
| Q-O | `acceptance` is a data field only; every rule derived from it is cut | `R-ROSTER`, `contracts/review-legs.example.json` |
| Q-P | The shared package lives in this SEPARATE repository; enforcement mode is the leaders' call (recommendation: informational drift report first) | `README.md § How a host uses a revision` step 3 |
| Q-S | selected option: a MERGE WITH FIXES with only Minor findings counts as agreement, no extra round | `R-AGREE` |
| Q-T | selected option: leaders hand files, the owner pushes | `README.md` step 1 and 4, `AGENTS.md`/`CLAUDE.md` |
| Q-U | selected option: prompts live here as the one editable copy; hosts vendor at the adopted revision | `prompts/`, `README.md` step 2 |
| Q-V | Concept only, no UI, no LikeC4; this repository is a lightweight experiment lab | `README.md` purpose, `reference/spec-authoring.md § 7` |
| Q1 (codex session) | selected option: "코드를 수정하면 전원 재검토. Minor만 남은 원본은 승인 가능" — Minor-only findings do not block the unchanged reviewed bytes; any change to reviewed content = full participating-roster re-review | `R-AGREE`, `R-REREVIEW` |
| Q2 (codex session) | selected option: "두 CLI 모두 Pro 계열 + 확인 가능한 high로 맞춤; 인증 경계 유지" — Pro family + verifiable HIGH on both Google CLIs; B's Auto-only path and A's unpinned gemini call = migration items | `R-NOCOST`, roster example, C18 |
| Q3 (codex session) | selected option: "증거 중심으로 통일하고 무결함 결론도 허용" — shared review prompt is evidence-centred and allows a no-defect conclusion; D-10 closed | `prompts/common-clauses.md § adversarial-framing` |
| Q-W | Google review leg default model = the 3.1 Pro-high tier; Flash retired as a reviewer; the model option stays only so a future model can be evaluated (corrects the leader's "provider default / auto" reading) | `R-NOCOST`, `contracts/review-legs.example.json`, C18 |

| D-3 (round r2) | Three families converged on a superset v2 wire (`contracts/leg-verdict-mapping.md`); residual choices are leader-level | `R-AGREE` open-question axis, `R-BIND` v2 additions |
| D-9 (round r2) | CONFLICTED: codex and google recommend ALLOW web tools in review legs with a date + version anchor; claude recommends DENY by explicit rows (and found A's policy INHERITS a search allow today). Owner decision requested **Superseded for REVIEW web on 2026-10-03 by [D-REVIEW-LEGS-20261003](#D-REVIEW-LEGS-20261003)** (standing authorization; the no-web posture applies only to a false condition). | `contracts/gemini-readonly.toml` header, `contracts/README.md` |
| Q4 (round r2) | Split 2:1 (materialize in the round copy vs fingerprint + no-follow clause) → owner ruled the PRINCIPLE (review the link itself, never follow the target automatically); the mechanism is each host's migration item | `R-PREPARE`, C26 |

| Directive (2026-09-19) | The recurring relative `--prompt-file` dispatch failure must be solved mechanically, not by instructions: resolve against the caller's cwd or align the path with cwd; record the problem in the plan and specify the fix | `R-CONTAIN` (all wrappers), C28; host plan P4-22 |
| Directive (2026-09-19, web evidence) | The agy web search that had been working degraded in round r2: fix it and test it; deliver the spike record — lines and cause — to the other leader too, so both hosts fix the same seam | `R-INVEST` web-evidence sentence; `prompts/investigation.md` (`web-evidence`); C29; `spikes/2026-09-19-google-web-evidence.md`; host plan P4-23 |
| D-9 RULED (2026-09-19) | Review legs have no web tools: DENY `google_web_search` / `web_fetch` by explicit rows in the shared gemini read-only policy; investigations (R-INVEST) keep web with the `web-evidence` clause. The rule is per OPERATION, not per CLI: codex `web_search` disabled, agy review agents without web tools (B's read-only builder drops `read_url` for review dispatch only), gemini deny rows, every review prompt renderer stops permitting web (codex F2). Applied first; the runtime effect is verified where gemini is in service (owner: apply now, leave the untested part as a separate config-like record) **Superseded for REVIEW web on 2026-10-03 by [D-REVIEW-LEGS-20261003](#D-REVIEW-LEGS-20261003)** (standing authorization; the no-web posture applies only to a false condition). | `contracts/gemini-readonly.toml` (rows at 200), `contracts/gemini-readonly.verify.toml` (V1-V5, NOT RUN), C15, `R-GOOGLE` convention sentence, `R-CONTAIN` gemini bullet; host A applied (t50); B: codex removes the two tools from its 999 allow list |
| Codex rev-1 addendum review (2026-09-19) | Findings F1–F8 accepted and applied by the claude leader — status accuracy (C28 NOT applied on either host), D-9 as an operation-level rule, executable V3/V5 with an isolated control and an evidence rule, C28 wording, Google shape pin in the v2 migration list, byte-identical vendoring of the policy (one definition), C4 original-vs-owned-copy split; leader-level wire choices aligned (`path`, three canonical verdicts, optional `correction`, uncertainty-only negative = DO NOT MERGE + `open_questions`, `SAFE`/`Major` import aliases only) | `R-CONTAIN`, `contracts/gemini-readonly{,.verify}.toml`, C4/C15/C28/C29, `contracts/leg-verdict-mapping.md`, `prompts/leg-google.md`, `units.json`, `spikes/2026-09-19-google-web-evidence.md` |
| Directive (2026-09-19, one place) | A large host restructuring is coming: rulings and conventions are written ONCE, in this shared repository; host documents carry pointers, never a second narration ("do not make the work happen three times") | `reference/spec-authoring.md § 3/§ 4`, `R-GOOGLE` convention; host plans quote verbatim only |
| Directive (2026-09-25, codex baseline and comparison; shared development log) | Codex review BASELINE = `gpt-5.6-terra` / `xhigh` as shipped roster DATA on both hosts (a shipped `null` had left host A's baseline to the operator's personal CLI configuration). Host A additionally runs a COMPARISON entry `codex-astra` = `gpt-6-astra` / `high` in its next round; both entries count, and the terra/astra difference is a ledger observation, never a vote or a policy. The Claude review leg is `claude-opus-5-5` / `xhigh` (the 2026-09-25 default-model handoff). PRD and spec move together; what the other host must fix is written into a shared development log, not a session note **Codex baseline superseded on 2026-10-03 by [D-REVIEW-LEGS-20261003](#D-REVIEW-LEGS-20261003)** (`gpt-6-astra` / `high`); one codex leg with no comparison entry is the leader's reading of "Leg terra 없애고 astra high  로 교체 …" (`authoring/shared-dev-log.md` DL-39). | `R-ROSTER` codex paragraph, C35, `contracts/review-legs.example.json`; `authoring/shared-dev-log.md` (`R-DEV-LOG`) |
| Codex verification amendment (2026-09-19; technical disposition) | Earlier F3/F4 verification changes required further corrections A1–A4; the owner authorized Codex to publish the bounded shared-spec amendment. Runtime checks remain NOT RUN and shipped policy bytes were unchanged; Claude (host A) runs the amended contract byte-for-byte: `3rd-Agent/wrappers/policies/gemini-readonly.toml` equals `contracts/gemini-readonly.toml` @ triad `ee011968` (DL-68) | `decisions/rev-1-codex-verification-amendment.md`; procedure only in `contracts/gemini-readonly.verify.toml`, C15, `R-GOOGLE` |

Withdrawn at the owner's word: a usage-measurement item (2026-09-19) is not recorded anywhere.

<a id="d-four-leg-20260921"></a>
## D-FOUR-LEG-20260921: one Codex and three Google reviewers

> **Historical record.** Its conflicting agreement and per-leg emphasis elements are superseded by
> [D-REVIEW-STRATEGY-20261002](#D-REVIEW-STRATEGY-20261002); use the
> [current Claude implementation handoff](claude-review-strategy-handoff.md) for current work.

The owner requested one Codex subagent and three independently invoked Google
legs with different review emphases, with final review approval decided by the
owner. This specializes existing R-ROSTER/R-AGREE; it does not add an automatic
lens field, a majority vote or a new approval token. Four legs cover two families.
The precise request, source evidence and publication boundary are in
[the operating agreement](2026-09-21-codex-google-four-leg-agreement.md), with
[setup and verification](codex-google-four-leg-operating-spec.md) and case C33.
Publication is owner-requested; host A (Claude) records the four-leg roster as fixture coverage in case C35's
host-A cell (t12 axis 36); exact live-profile verification is NOT RUN. A's native topology remains distinct from B's.

<a id="gemini-invocation-20260921"></a>
## Gemini invocation briefing: 2026-09-21

The owner reported that Gemini CLI invocation succeeded in the reported
environment. This is the R-GOOGLE service briefing, also reflected in the
[B v0.2.556 release](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.556).
The report did not supply an exact installed revision, CLI version, authentication
class or transcript. It confirms the reported invocation only; it does not mark
B1-B3, WEB-B-1, three concurrent Google calls, lens coverage or host A adoption
as passed. Preserve those separate verification statuses.

<a id="review-web-a1-20261003"></a>
## Review-web live check WEB-A-1 (C32): 2026-10-03

The result record, named by the `result_channel` of the service manifest `contracts/review-web.verify.toml`, for check
WEB-A-1 (the true condition on every participating route, live): RUN 2026-10-03 on host A
(`codefoundry-io/triad` `goal/spec-main-conformance` @ `b53409b`). One v2 round, `live-web-c32-r1`, ran every route
with web: codex `--search`; agy `triad-readonly-research` with audit `review_web: true` and the hook in `--web` mode;
claude `-web` and `-high-web` twins, each of which, per the host A record, fetched
https://code.claude.com/docs/en/sub-agents. Result `ROUND_INTEGRITY_OK`, AGREED 4/4 over three
families (host A record: triad `e192938`, `docs/reviews/2026-10-03-live-web-c32-residuals.md`). Not covered live, unit-tested
only: the false condition and a mismatched launch switch (check WEB-A-3, NOT RUN live; host A tests t23, t62) and the
gemini route. WEB-A-3, WEB-B-1 and WEB-A-2 remain NOT RUN (WEB-A-2: gemini is host A's compatibility route and has not
been run on host A; [D-ONE-ENVIRONMENT-20261003](#D-ONE-ENVIRONMENT-20261003)).

<a id="d-auth-browser-login-20260926"></a>
## D-AUTH-BROWSER-LOGIN-20260926: CLI authentication is the user's own browser login only

Owner, 2026-09-26, ruling on the host A round r18 incident (a codex CLI that
presented an API-key-shaped bearer, `401 Incorrect API key`, on a subscription
login): "api key 형태의 어떤 것도 시도하지 말아야하는데 스펙이나 이런 사양이 있으면
금지시키도록 명시해 사용자 직접 웹을 통한 로그인만 허용 비용 발생 위험" — nothing
API-key-shaped is ever tried; the spec states the ban; only the user's own direct
browser (web) login of a CLI is allowed; the reason is billing risk. Recorded as
rule R-AUTH (`reference/review-rules.md#R-AUTH`), case C37 and dev-log row
DL-16. It sharpens R-NOCOST (CLI only, the user's own login); it adds no
credential handling of any kind to either host — an observed API-key-shaped
authentication is a STOP whose only remedy is the owner's browser re-login.

<a id="d-rulings-20260927"></a>
## D-RULINGS-20260927: operations equivalence, native legs, retention, identity

Owner rulings of 2026-09-27 on the leader's issue list, recorded once here and
carried by the dev-log rows named: item 8 → DL-17 (A's refuse-before-write plus
the committed ledger equals the start-failure record, preparation custody and
export); item 9 → DL-18 ("네이티브 서브에이전트 스폰 … 자체 진단 기능이 있어서 별도
디버그용 감사가 필요 없음 이전 리뷰 히스토리 정도만 필요" — a native same-family
sub-agent leg keeps only its review history); item 16 → DL-19 (the 2026-09-17
retention ruling upheld; item 6 of 2026-09-26 adds "모든 로그와 워크트리 생성이
기간이 지나면 clean up 되어서 용량이 무제한 늘어나는 일이 없어야함"); item 14 →
"일단 지금 체제로": the leader keeps pushing as the owner account for now, every
push and merge under the owner's explicit approval; item 18 → the deploy push of
the directives-only distribution approved.

<a id="d-rulings-20260927b"></a>
## D-RULINGS-20260927B: quota-cap default, R-MODEL, web for every leg

Owner answers of 2026-09-27 to the leader's proposals: Q7-1 "a 그리고 leg를 추가할지
다른 관점의 같은 모델을 추가할지는 사용자가 직접 요청할테니 기능만 가능하면 이걸로 종결"
— after a quota cap the round ends with the answering families and the owner's
decision; adding a leg or a same-model different-perspective entry is the user's
explicit request (DL-20). Q7-2: nothing is substituted by default, so no re-run
follows. Q10-1 "올림" — R-MODEL is a shared rule (`reference/review-rules.md#R-MODEL`,
DL-21). Q10-2 "거부 유지" — an exposed runtime identity that contradicts the request
is refused. Q11-2 "모든 다리 일괄임" — owner-authorized web verification applies to
every participating leg of the round, never to a subset (R-REVIEW-WEB as written).

<a id="d-rulings-20260927c"></a>
## D-RULINGS-20260927C: cleanup records, empty directories, distribution

Owner, 2026-09-27, on host A's retention slice and distribution: (1) "악의적 공격을
당할 이유가 없는 환경인 A 안으로" — a program-owned root + the name shape + the
program-written record are the allocation proof; no content-bound record is
built (DL-22 reading 1). (2) "권고안으로 진행할거고" — an EMPTY name-shaped
candidate past the age floor may be removed with `rmdir` alone
(`reference/review-rules.md#R-CLEANUP`, amended; DL-22 reading 2). (3) "현재
배포판 동작으로 하되 설치되는 파일을 고지하고 언인스톨만 깨끗하게 하면 돼 복잡하게
하지말자" — the distributed plugin keeps applying a repair proposal
automatically; every file it writes is disclosed and one clean uninstall is
provided (host A slice; no shared rule).

Current form: items (1) and (2) are superseded by
[D-DELETION-BY-CODE-20261004](#D-DELETION-BY-CODE-20261004) — only host code deletes, and only inside a
root declared with its proof; an EMPTY folder inside a marker role's root past the floor is removed with `rmdir`
(`reference/review-rules.md#R-CLEANUP`).

<a id="d-rulings-20260928b"></a>
## D-RULINGS-20260928B: a fact is written in its present form

Owner, 2026-09-28, on how a vendor failure sentence enters this specification:
"스펙에 이력이 즁요할까? 지금 형태만 나타내면 딻은 인터페이스와 prd규약에 에러로
들어가야할 것같은데" — is history important in the spec; stated as it is now, it
belongs in a short interface and as an error in the rules. On publishing it:
"… 스펙에도 올려 목적자체가 같은코드와 같은 프롬프트를 가지려는거니까" — publish it
to the spec; the purpose is that the hosts have the same code and the same
prompts. Recorded as rule R-CLASSIFY (`reference/review-rules.md#R-CLASSIFY`),
contract `contracts/vendor-failure-lines.json` and case C43, with no
development-log row. The owner also confirmed the narrow codex match phrase
`selected model is at capacity` in place of the wide `is at capacity`. This
decides this item only; whether other parts of the specification are rewritten
the same way is a later decision of the owner.


<a id="D-REVIEW-STRATEGY-IMPLEMENTATION-20261002"></a>
## D-REVIEW-STRATEGY-IMPLEMENTATION-20261002: Codex first, then shared main

The owner's later implementation instruction supersedes the earlier planning-only
boundary for this work: "승인된 구현 계획과 R3 리뷰 보고서를 읽고, 구현 메모 3건을 포함해
구현·테스트·코드 리뷰를 진행해." After verification: "공유 스펙을 main에 반영해 Claude
host가 구현할 수 있는 가이드로 정리해." The selected review roster is Opus 5.5/xhigh,
Google Pro/high, Flash/high and Astra/high; AI-related review may use web evidence.
Verified in-scope corrections and demonstrated spec errors may be addressed.
Claude-host implementation inspection remains excluded. Existing dirty work, exact
model IDs and existing JSON configuration are preserved. The owner requires macOS
and Ubuntu support and their terminal environment outside the development sandbox.
Shared-spec main landing is authorized after its required review and CI; product
merge, installation and release remain separate. See the
[implementation handoff](claude-review-strategy-handoff.md) for evidence and A's
remaining work. Historical decisions above remain historical evidence.

<a id="D-REVIEW-LEGS-20261003"></a>
## D-REVIEW-LEGS-20261003: codex review default Astra/high; web search for every AI leg

Owner, 2026-10-03, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-02/03 (UTC)):

> Leg terra 없애고 astra high  로 교체 웹검색 허용

To the question "Where should 'allow web search' apply?" (the leader's options), the owner selected:

> All review legs, always

Typed separately by the owner (2026-10-02 19:41:51Z UTC, before the selection above was made at 19:42:32Z), not part of
the selected option:

> 모든leg Ai기능 관련은 웹건색 허용해

("웹건색" [sic], as typed: 웹검색, web search.)

Reading recorded with the decision (the leader's, not the owner's words): (a) the codex review leg's
recommended default becomes `gpt-6-astra` with reasoning `high` on both hosts, replacing `gpt-5.6-terra` /
`xhigh`; (b) web search is allowed for every leg's AI-feature-related work ("Ai기능 관련은"), always — read as every AI-run
leg, not as a limit by topic: every selected review leg in every review round, by the owner's standing authorization (no
longer a per-round request; settled by "All review legs, always"), and every investigation/dispatch leg, with no
technology heuristic (R-INVEST, R-REVIEW-WEB). This reading of "Ai기능 관련은" is the leader's, for the owner to confirm
at publication. Both hosts' legacy entry points (on A the small review path and the v1 path; on B the workspace
four-leg gate and the fixed legacy formal route) do not bind the standing authorization — recorded non-conformance facts
(R-REVIEW-WEB On A and On B), not exceptions; whether to keep or retire them was an open owner item
(`authoring/shared-dev-log.md` DL-59), answered below for host A.

Owner answers, 2026-10-03, typed (verbatim; source: host A's leader session record (unpublished)):

To the leader's reading (b) of "Ai기능 관련은":

> AI는 모델 조사 프롬프트 엔지니어링 기법 검토에 필요

Recorded effect: every AI leg may use web search; the purposes the owner names are model research and the review of
prompt-engineering techniques. Reading (b) is confirmed in that sense (R-INVEST).

To keeping or retiring the legacy entry points:

> 레거시 경로 차후 폐기

Recorded effect: host A's legacy entry points (the small review path and the v1 path) are retired — the v1 path @
triad `12b1dd6f`, its verdict schema @ `cc5f2f3f`, the small path @ `32124be5` (`authoring/shared-dev-log.md` DL-128) —
so their non-conformance no longer exists on A. Host B's legacy renderers remain host B's own decision; this answer
makes no ruling on B.

Effect: [R-ROSTER](../reference/review-rules.md#R-ROSTER) (codex default),
[R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB) (standing authorization; `review_web_authorized`
true for every round unless the owner revokes it), [R-CONTAIN](../reference/review-rules.md#R-CONTAIN) (the
no-web posture applies to a false condition only), [R-INVEST](../reference/review-rules.md#R-INVEST) (web
allowed for every investigation/dispatch leg), `contracts/review-legs.example.json` (codex entry), the prompt clauses
`review-web-permission` (`prompts/common-clauses.md`) and `google-a-hook-audit` (`prompts/leg-google.md`), cases C15,
C29, C32 and C35, dev-log row DL-39. It supersedes the codex baseline of the 2026-09-25 directive, D-9's REVIEW
prohibition and the 2026-09-21 direct-request condition, including the review-web instructions of
[the review-web handoff](claude-review-web-handoff.md) and
[the Codex + three Google handoff](claude-codex-google-four-leg-handoff.md), the web condition of
[the 2026-09-21 amendment and handoff](2026-09-21-owner-requested-claude-web.md) and
[B's review-web verification record](host-b-review-web-verification.md), and the review-web and codex-default
preservation sentences of [the 2026-10-02 review strategy](2026-10-02-review-strategy.md); read-only containment, R-AUTH, R-NOCOST, the
web-evidence rule (C29), exact IDs as roster data and the requested-versus-runtime identity rules are unchanged.
Host adoption, publication and revision tags remain separate.

Follow-up rulings, owner, 2026-10-03, typed or answered (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-02/03 (UTC)):

The leader's question (verbatim), to which the owner typed the answer below:

> With web always on for review legs, what should happen when a leg's route cannot use web (e.g. host A's in-company gemini has no web-enabled policy profile yet)?

(The question's "in-company" framing is history; the current state is one environment,
[D-ONE-ENVIRONMENT-20261003](#D-ONE-ENVIRONMENT-20261003).)

The owner's answer:

> 웹 지원 가능하도록 하는거 쉬ㅣㅂ잖아 먼저 구현휴 진행

Reading: a route that cannot use web under the standing authorization is not exempted — R-REVIEW-WEB keeps "a missing
capability is a preflight refusal", and every route of every host gets web support. The spec therefore defines host
A's complete web-enabled Gemini profile (`contracts/gemini-readonly-web.toml`, check WEB-A-2) as it defines B's.

> 1. A아만 적용되는 사항은 a에는 이렇다고 넣어야함

Reading: a behaviour that holds on one host only is written as "On A: …" or "On B: …", never left implicit
([spec-authoring § 3](../reference/spec-authoring.md)).

> 목적 자체가 원본이 분실되도 스펙으로부타 구현이 가능해야해

Reading: each host must be rebuildable from this specification alone; R-REVIEW-WEB states, per host, how each route
receives web ([spec-authoring § 3](../reference/spec-authoring.md)).

<a id="D-SPEC-GAPS-20261003"></a>
## D-SPEC-GAPS-20261003: close every spec gap a host implementation exposed

Owner, 2026-10-03, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-02/03 (UTC)):

> 여태 찾은 수펙 미상세해서 codex코드 보고 구현한 부분 있어? 스펙도 업데이트 해야한다 이건 지금 goal에 넣어
> 스펙이 자세하지 못해사 cpdex참조해야했으면 스펙이 미진한사항이니 스펙 업데이트 코덱스쪽 코드고 보고 코덱스쪽에도 버그가 있으면 스펙 업데이트 해야햠

> 스펙은  코덱스와 claude가 공유하는 공통 사양이야 반드시 둘다 공유해야함

> 지금 gemini는 옛모델이라 지금 모델로 구현하면 매번 태클걸껄 없는 모델이라고

The rulings "1. A아만 적용되는 사항은 a에는 이렇다고 넣어야함" and "목적 자체가 원본이 분실되도 스펙으로부타 구현이 가능해야해"
of the same day are recorded under [D-REVIEW-LEGS-20261003](#D-REVIEW-LEGS-20261003).

Reading recorded with the decision (the leader's, not the owner's words): (a) where a host had to read the other host's
code because the specification did not settle a behaviour, the specification is incomplete and is amended, and a defect
found on either host is recorded; (b) every amendment is common to both hosts, with host-only mechanisms written
"On A: …" / "On B: …"; (c) every review leg receives the round's date and the instruction that names newer than its
training data exist and are verified on the web or taken from the bound inputs.

Effect: [R-PREPARE](../reference/review-rules.md#R-PREPARE) (one bound-basis definition, pointed to by R-RETRY,
R-REREVIEW, R-PROMPT and R-REVIEW-WEB), [R-PROMPT](../reference/review-rules.md#R-PROMPT) (the stage carrier),
[R-ROSTER](../reference/review-rules.md#R-ROSTER) (empty-roster refusal; host-native controls),
[R-CONTEXT](../reference/review-rules.md#R-CONTEXT) (edges, empty residual, framing collisions),
[R-BIND](../reference/review-rules.md#R-BIND) (sealed attempt), [R-REREVIEW](../reference/review-rules.md#R-REREVIEW)
(the leader's range), [R-AGREE](../reference/review-rules.md#R-AGREE) (where integrity is checked, a fact); prompt clauses
`current-date` and `review-no-web` and `prompts/README.md` § Clause-file format; README § How a host uses a revision;
`units.json`; cases C13, C19, C20, C32, C33, C60, C61, C64 amended, C66 and C67 added; every host statement in the rules,
`units.json` and the cases (tests cells and case texts) checked against both hosts' code, host status moved out of case
texts into tests cells; dev-log rows DL-40–DL-54. Host
adoption, publication and revision tags remain separate.

<a id="D-C66-LIMITS-20261003"></a>
## D-C66-LIMITS-20261003: host A's C66 seal closes with recorded limits

Owner, 2026-10-03, answer to the controller's question about host A's C66 seal (an English option of the question
widget; source: host A's unpublished leader session record, the transcript of 2026-10-03, at the question tool call of
the T4 close). The chosen option, label and description verbatim:

> Close; record limits (Recommended)
>
> Mark T4 done with codex's tampering chains recorded as known limits (one operator, no defence against deliberate
> tampering) in the spec as facts, plus the A-vs-B difference on retrying an invalid answer as a dev-log fact. The plan's
> 'all three PASS' rule gets this owner exception.

Reading recorded with the decision (the leader's, not the owner's words): host A's sealed-attempt implementation
(`4af44cf`) closes C66; its known limits (1)-(3) — codex's tampering chains, which the chosen option covers — are recorded
as FACTS under [R-THREAT](../reference/review-rules.md#R-THREAT), not as rules or open work (limits (4) and (5) in R-BIND
are the leader's ruling under R-THREAT, not this decision); the A-vs-B difference on retrying an answer that could not be admitted is a dev-log fact.

Effect: [R-BIND](../reference/review-rules.md#R-BIND) (On A sentence, limits (1)-(3); the retry difference),
case C66 tests.A, dev-log rows DL-44 and DL-55; the `units.json` review-lifecycle exception for the retry difference
(R-PARITY).

<a id="D-THREAT-MODEL-20261003"></a>
## D-THREAT-MODEL-20261003: the deployment both hosts serve — no malicious actor, no concurrent operation

Owner, 2026-10-03, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-02/03 (UTC)):

> 이건 스펙에 나와있는 부분이야 없었어? 악위적인 공격 변조에 대응하먄 끝이없어

Earlier owner rulings with the same content, recorded until now only in host A's records (verbatim, dates as given):

> 2026-09-27: 너무 과한 설정을 걷어내 누가 진행중에 업데이트를 시도하겠어 …

> 2026-09-28: ...발생하지 않을 악의적 공격에 대한 과장된 방어 이런거 ?

Supporting precedent from another project of the same owner (the Argus static analyzer, 2026-08-15, verbatim and
whole); it is not itself a ruling about the dispatch hosts, for which the 2026-10-03 words above are the ruling:

> 코드를 읽어서 정적분석하는데 왜 이게 버그인지 너무 과도한 방어코드 아니야? 악의적인 공격은 없고 안정된 환경이라고 가정하고 진행해.

Reading recorded with the decision (the leader's, not the owner's words): both hosts serve one operator on a stable
machine with no concurrent operation and no malicious actor; guards defend against ordinary failures; a finding that
needs deliberate tampering, a concurrent operation, a deliberately unusual layout or an exact-instant crash is recorded
as a fact, never code or a blocker. The last two exclusions (a deliberately unusual layout, an exact-instant crash) are
not in the owner's words above; they were the leader's reading of the owner's lens — superseded by the owner's answer
below.

<a id="D-THREAT-MODEL-20261003-answer"></a>
Owner answer, 2026-10-03, typed (verbatim; source: host A's leader session record (unpublished)):

> 이건 리더가 잘못만들수 있는거 아냐? 그리고 토큰이 한도에 달하거나 비정상 종료는 이론상 생기는 일이고 이상하게 만드는 파일 배치는 기계적 생성이 아니라 리더가 임시로 생성하는 파일에는 생길수 있을 것 같은데

Recorded effect: the two leader-added exclusions are rejected. A stop at any point (a crash, or a session that hits its
token or usage limit) and an odd layout of files the leader creates by hand (a leader's mistake) are ORDINARY failures,
in scope at full severity. Out of scope stay only deliberate tampering with the host's own files and a concurrent
operation. Effect: [R-THREAT](../reference/review-rules.md#R-THREAT) and the shared `deployment-context` clause (a
payload change both hosts re-vendor); facts recorded under the earlier wording are to be re-triaged by the hosts
(`authoring/shared-dev-log.md` DL-59).

Effect: [R-THREAT](../reference/review-rules.md#R-THREAT) (new), R-VERIFY's dispositions and the C66 limits under
R-BIND point to it; the shared prompt clause `deployment-context` (`prompts/common-clauses.md`, in every leg order);
case C68; dev-log row DL-56. Host adoption (re-vendor), publication and revision tags remain separate.

<a id="D-PRE-RECORD-REPLY-20261003"></a>
## D-PRE-RECORD-REPLY-20261003: a reply replaced before the host's first record is a known limit, both hosts

Owner, 2026-10-03, typed answer (verbatim; source: host A's leader session record (unpublished), the transcript of
2026-10-03, 11:00Z) to the leader's question (verbatim):

> 호스트가 답을 기록하기 전에 저장된 답 파일이 바뀌는 경우(오류 + 실수 세 가지가 겹침)를 어떻게 처리할까요?

Option 1 of that question, the leader's label and description (verbatim):

> 알려진 한계로 기록 (추천)

> 코드 변경 없음. 스펙의 '알려진 한계' 이유를 새 위협 모델 기준으로 고침: 기록 전 바뀐 파일은 원리상 알 수 없고, 실수 세 가지가 겹쳐야 생김. 두 호스트 공통.

The owner's answer:

> 기간으로 지우잖아 1

The owner's follow-up, typed the same minute:

> 기간으로 지우는 로직없어? 아님 내가 이해를 잘못했어?

Reading recorded with the decision (the leader's, not the owner's words): option 1 — a known limit for both hosts, no
code. The recorded reasons are the option's two: before any host write about a saved reply has landed, no record of its
first bytes exists, so a replacement is undetectable by construction; and the chain needs a host fault or a stop plus
three leader mistakes (ignore the fault, skip the printed guard, save over the existing file). The owner's remark that the
files are deleted after a period is quoted, not used as the reason: retention deletion comes after the round and does not
change an outcome during it. The limit covers every case in which no host write landed — a stop before the host's first
write or that first write itself failing (on A the admission's seal create on a full disk; on B the exclusive create of
`record_attempt`). A write that started and did not complete is not this limit: host A then fails closed.

Effect: [R-BIND](../reference/review-rules.md#R-BIND) (known limits, both hosts), case C66 tests.A,
`authoring/shared-dev-log.md` DL-64.

<a id="D-ENV-DROPPED-LINE-20261003"></a>
## D-ENV-DROPPED-LINE-20261003: a wrapper line with every review marker removed is a known limit, both hosts

Owner, 2026-10-03, selected option (source: host A's leader session record (unpublished), the transcript of 2026-10-03,
14:02Z). The leader's question, and the selected option's label and description (verbatim; the label and description
are the leader's, the choice the owner's):

> 리뷰 표시 두 개를 모두 지운 실행 명령(실행 전에 못 막고, 결과 수집에서 무효 처리됨)을 어떻게 처리할까요?

> 알려진 한계로 기록 (추천)

> 코드 변경 없음. 스펙 C32에 두 호스트 공통 예외로 기록: 표시가 모두 지워진 줄은 실행 후 결과 수집에서 무효 처리(합의 불가).

Recorded effect: a printed wrapper line with every review marker removed (on A both review env values,
`TRIAD_REVIEW_LOG_DIR` and `TRIAD_REVIEW_ARGV_SHA256`) runs as an ordinary call on both hosts — no construction can refuse
before inference a command that carries no review marker — and is caught at collection (INVALID, never agreement). It is
the one exception to C32's "a launch switch that disagrees with the bound condition refuses before inference".

Effect: [R-BIND](../reference/review-rules.md#R-BIND) (the executed-command receipt and its known limit),
[R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB) On A, case C32 tests.A, `authoring/shared-dev-log.md` DL-63.

<a id="D-ONE-ENVIRONMENT-20261003"></a>
## D-ONE-ENVIRONMENT-20261003: one environment — no off-site / in-company split as current state

Owner, 2026-10-03, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-03,
11:37Z):

> 이제 사내 구분안해 없애

The leader's scope question, and the selected option's label and description (verbatim; 11:42Z):

> '사내 구분'을 어디까지 없앨까요?

> 두 환경 서술만 없앰 (추천)

> 지침·문서에서 사외/사내 두 환경 구분을 지우고 한 환경으로 서술. Mac·Ubuntu 호환 의무는 '두 OS 지원'으로 유지, 플러그인 재배포 규칙도 유지. 구글 리뷰어는 agy 기본, gemini는 호환 경로.

Recorded effect: the option was scoped to host A's instructions and documents ("지침·문서"). Host A describes its current
state as one environment, with no off-site / in-company (leaders' site / company site) split; it keeps support of macOS
and Ubuntu 24.04 ([R-PLATFORM](../reference/review-rules.md#R-PLATFORM)) and its plugin re-deploy rule; its Google review
route is agy by default and gemini the compatibility route. In this specification, the shared wording that carried the
two-site framing as current state is reworded or annotated (the Q-G / Q-J / Q-N row, the WEB-A-1 record, WEB-A-2's
reason); each host's shipped Google fallback logic and the owner's gemini testing where gemini is in service (Q-N) stand.
Host B is not changed by this decision: it takes its Google route from the roster pin, else agy when installed, else
gemini; the declared authentication class only refuses gemini for a personal Google login
(`bin/review_adapters_v2.py:142-148` @ `7f75863`). History records are kept as written.

Effect: the Q-G / Q-J / Q-N row, the WEB-A-1 record and the question of D-REVIEW-LEGS-20261003 (annotated),
`contracts/review-web.verify.toml` WEB-A-2 `not_run_reason`, `authoring/shared-dev-log.md` DL-68.

<a id="D-LATE-ANSWER-20261004"></a>
## D-LATE-ANSWER-20261004: a late answer after collection's last custody check is a known limit, both hosts

Owner, 2026-10-04, typed answer (verbatim; source: host A's leader session record (unpublished), the transcript of
2026-10-03, 18:30Z) to the leader's question (verbatim):

> 실행 중인 리뷰어를 재시도한 뒤, 마지막 검사와 합의 기록 사이 아주 짧은 순간에 늦은 답이 들어오는 경우(다음 수집에서 잡힘)를 어떻게 처리할까요?

The question's recommended option, the leader's label and description (verbatim):

> 알려진 한계 + 운영 규칙 (추천)

> 코드 변경 없음. 두 호스트 공통 한계로 스펙에 기록하고, '재시도한 리뷰어가 아직 실행 중일 수 있으면 합의를 쓰기 전에 한 번 더 수집한다'는 규칙을 안내에 추가.

The owner's answer:

> 스펙에 적어.

Reading recorded with the decision (the leader's, not the owner's words): the recommended option, written into the spec —
a leg still running in an attempt a retry replaced can write its answer after collection's last custody check and before
the AGREED record; no construction closes the window on either host; the next collection reports the change. Operator
rule, carried by each host's guidance: when a retried leg may still be running, collect once more before using an AGREED.

Effect: [R-AGREE](../reference/review-rules.md#R-AGREE) (known limit and operator rule), `authoring/shared-dev-log.md`
DL-61.

<a id="D-DECISION-ORDER-20261004"></a>
## D-DECISION-ORDER-20261004: the order of deciding a gap, and what the other host must learn goes into the spec

Owner, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-03 (UTC)). On
2026-10-03, as answers to the leader's question about a hand-edited reviewer command line (10:12Z, 10:15Z):

> 스펙이랑 코덱스쪽 코드 확인했니? 아님 그와 별개의 문제야?

> 왜 지침을 안따라 스펙 확인 스펙에 없으면 코덱스 확인 그래도 듈다 문제면 나에게 요청 이후 스펙추가

On 2026-10-04 (18:31Z and 18:51Z on 2026-10-03 UTC), after the leader asked about two known limits that needed no decision:

> 왜 이걸 못해 수펙에 없으먄 코드 확인 커드에 없으면 수펫에 적는거잖으

> 니가 커덱스 쪽에 알려할게 있으먄 꼭 스펙에넣어 스펙이 부족해서 니가 코덱스쪽글 봐야했ㅇ.ㄹ때도 둘다 문제일때도 플랜이나 스펙이 완전하다고 가정하지말고 좀 지침이나 어디 적어놔라

Reading recorded with the decision (the leader's, not the owner's words): a gap found while implementing is decided in
this order — what the specification already decides; else the other host's code (when it settles the behaviour, the
specification gains the rule); else a fact or limit both hosts lack is recorded in the specification without an owner
question; the owner is asked only for a design choice with a trade-off that neither settles. Whatever the other host must
learn — a gap that made a leader read the other host's code, a defect both hosts share, a defect of the other host — goes
into this specification in the same turn it is found, never only into a host's private record. Neither the plan nor the
specification is assumed complete. The 2026-10-03 order ("나에게 요청 이후 스펙추가") is refined by the 2026-10-04 words for a
fact or limit both hosts lack. Same direction as [D-SPEC-GAPS-20261003](#D-SPEC-GAPS-20261003).

Effect: [R-DECISION-ORDER](../reference/spec-authoring.md#R-DECISION-ORDER) (new), `authoring/shared-dev-log.md`
DL-69.

<a id="D-REVIEW-TIMEOUTS-20261004"></a>
## D-REVIEW-TIMEOUTS-20261004: generous review-leg timeouts — up to 30 minutes by reasoning

Owner, 2026-10-04, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-03,
19:01Z):

> 시간 초과 넉넉히.잡아 claude 도 astra도 리즈닝에따라 30분 가능

Reading recorded with the decision (the leader's, not the owner's words): a review leg's run may take up to about 30
minutes by its reasoning, for the Claude leg and the codex `gpt-6-astra` leg alike, so the timeout is set generously
above that. Host A sets every review roster entry's `timeout_s` to 3600 s in its roster data (shipped default, the
four-leg example and its project file) — the leader's choice of value. A timeout is roster DATA: changing it is a new
basis for rounds prepared after it (R-REREVIEW), and no rule text changes. Host B's maintainer may compare its own routes'
requirements before touching its defaults (R-ROSTER notes B's legacy formal gemini route requires 600 s).

Effect: `authoring/shared-dev-log.md` DL-5 (host A's data change landed: 3600 s on every review entry, triad merge `7a687b6`).

<a id="D-AUTH-ABSOLUTE-20261004"></a>
## D-AUTH-ABSOLUTE-20261004: browser (OAuth) login only — an absolute law

Owner, 2026-10-04, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-03,
20:58Z):

> API로그인은 하지마 직법 cli에서 사용자들이 oauth로그인 하는게 정책이다 api키는 의도하지 않은 금액이 발생해서 금지사항이야 스펙에 없으면 절대법칙으로 넣어

Recorded effect: every vendor CLI is used only through the user's own OAuth (browser) login in that CLI; an API key bills
unintended charges and is forbidden; this specification carries the rule as an ABSOLUTE law that outranks every other
rule, with no host or case exception and no owner question that relaxes it. It restates and hardens
[D-AUTH-BROWSER-LOGIN-20260926](#d-auth-browser-login-20260926), the ruling behind R-AUTH. Reading recorded with the
decision (the leader's, not the owner's words): the law requires a stop before every vendor call whose authentication
mode is not the subscription login, judged from the CLI's own report or its own enforcement setting and never from a key
value or the credential store, on every CLI and route. **That reading is withdrawn by the owner's correction of the same
day, [D-AUTH-JUDGE-STOP-20261004](#D-AUTH-JUDGE-STOP-20261004): there is no pre-call check.**

Effect: [R-AUTH](../reference/review-rules.md#R-AUTH) (absolute law; enforcement (i)-(iii)),
[R-DECISION-ORDER](../reference/spec-authoring.md#R-DECISION-ORDER), R-CLASSIFY (DL-75), cases C16 and C37,
`units.json`, `authoring/shared-dev-log.md` DL-16, DL-62, DL-75, DL-76.

<a id="D-AUTH-JUDGE-STOP-20261004"></a>
## D-AUTH-JUDGE-STOP-20261004: no pre-call login check — judge the outcome, stop, try nothing else

Owner, 2026-10-04, typed (verbatim; source: host A's leader session record (unpublished), the transcript of 2026-10-03,
21:07Z), correcting the leader's reading of [D-AUTH-ABSOLUTE-20261004](#D-AUTH-ABSOLUTE-20261004):

> 매번 확인하지마 로그인은 사용자에게 맡기고 로그인 됐는지 안됐는지만 판단하고 먼추고 다른 시도 안하면 되잖아

Recorded effect: there is NO pre-call authentication-mode check. Login is the user's own act through the CLI. The host
only judges, from the CLI's own outcome, whether a call failed because the login is missing or expired or a credential is
API-key-shaped; it then stops that attempt and tries nothing else — no retry, no other method, no fallback. The silent use
of a valid key stored in a CLI's own configuration is the user's responsibility under this decision. The law stays
absolute (D-AUTH-ABSOLUTE-20261004); the gemini review preflight (C16) is an earlier rule and is unchanged.

Effect: [R-AUTH](../reference/review-rules.md#R-AUTH) (enforcement (i) and (iii) only), cases C37 and C16 (cells
restored), `units.json`, `authoring/shared-dev-log.md` DL-16 (withdrawn), DL-75, DL-76.

<a id="D-DELETION-BY-CODE-20261004"></a>
## D-DELETION-BY-CODE-20261004: only host code deletes; an AI at most names the folder

Owner, 2026-10-04, typed (verbatim, line breaks kept; source: host A's leader session record (unpublished), the
transcript of 2026-10-03, 22:22Z):

> 지우는건 코드화된 결정적코드로 하는거 아니야?
> 프롬프트로 지우는 작업은 폴더를 정하는 정도만해. 
> Json같은 설정 파일에 지워야할 폴더릉 지정하는정도 이거 결정되면 스펙에도 추가해

The leader's design question (verbatim, 22:34Z) and the selected option (the label is the leader's, the choice the
owner's):

> 삭제는 코드만 하고 AI는 폴더만 고르게 하는 설계로 진행할까요? (설정 파일 하나에 지워도 되는 폴더를 적고, 삭제 명령 하나로만 지우며, 손으로 지우라는 문구 약 40곳을 고칩니다)

> 이 설계로 진행 (추천)

Recorded effect: only host code deletes. Every folder a host's code may delete is declared in one JSON configuration
file (role, root, ownership proof, age floor); the declaration adds to the ownership proof and never replaces it. An AI —
the leader, a sub-agent, skill, agent or prompt text, a printed remedy — at most chooses a declared role and a folder and
runs the host's deletion command; no such text carries its own removal command. A call that removes what it created
itself needs no declaration.

Owner answer, 2026-10-04 (source as above, 22:37Z). The leader's question (verbatim) and the selected option (the label
is the leader's, the choice the owner's):

> 삭제 대상 설정 파일이 없거나 형식이 깨졌을 때 어떻게 할까요?

> 지우지 않고 멈춤 (추천)

Recorded effect: when the configuration file is missing or invalid, nothing is deleted — the host's deletion command
refuses (a host fault) and the automatic prunes skip with a one-line note; a host ships a default configuration file so a
fresh install still prunes.

Owner answer, 2026-10-04 (source as above, 22:38Z). The leader's question (verbatim) and the selected option (the label
is the leader's, the choice the owner's):

> 리뷰어 오류 분석이 끝난 실행 로그는 어떻게 지울까요?

> 자동 정리에 맡김 (추천)

Recorded effect: a wrapper run-log is never removed by an AI after a repair analysis; the host's coded sweep (its age
floor and caps) collects it; no prompt carries a run-log removal step. Both open choices of the design are decided.

Effect: [R-CLEANUP](../reference/review-rules.md#R-CLEANUP) and its pointers (R-AGREE, R-BIND, R-CONTAIN),
`contracts/cleanup-roots.schema.json` and `.example.json`, case C69, PRD-RETENTION, `rev-2-implementation-spec.md`,
`units.json` cleanup, the four policy `.verify.toml` `on_fail` texts, `authoring/shared-dev-log.md` DL-77.

<a id="D-MEASURED-SHAPES-20261005"></a>
## D-MEASURED-SHAPES-20261005: code only MEASURED vendor shapes; a constructed shape is a recorded limit

Owner, 2026-10-05, typed (verbatim; source: host A's leader session record (unpublished), the transcript of
2026-10-05), on host A's slice of wrapper classification hardened over eight verification rounds:

> 이게 왜이렇게 복잡해졌어? 과설계된 아니야? 에러메시지는 우리가 관리하는게 아니고 매번 버잔업때마다 새로운 유형이 생길건데 브리핑해봐

The leader's question asked the direction; the selected option (the label is the leader's, the choice the owner's):

> 지금 단순화

Recorded effect: vendor error text belongs to the vendor and changes with each release. A host codes only a MEASURED
vendor shape — a capture, a row of `contracts/vendor-failure-lines.json`, the vendor's own source — and ordinary operator
actions; a shape a reviewer constructs and no run has shown is recorded as a limit, never coded, and a new vendor message
ends `unknown` and reaches the repair analysis. Three guarantees stay whatever the input: a STOP on a measured
authentication signal, a usable answer never discarded because of text inside it, and classification that never raises
and always writes the terminal record. R-THREAT's "a bad vendor answer" is read as one a run has shown.

Effect: [R-CLASSIFY](../reference/review-rules.md#R-CLASSIFY) "Recorded limits" and the plain-fragment rule on every
raw-text list, [R-THREAT](../reference/review-rules.md#R-THREAT), `authoring/shared-dev-log.md` DL-86, DL-90, DL-92,
DL-93.

Owner, 2026-10-05, later the same day (verbatim): "괴설계하지말고 스펙 규칙 지키도 네이티브는 굳이 다룬 cli처럼 감사할 필요없어 cli도 결괴만 중요하지" — no over-design; keep to the spec rules; the native family (the host's own leader family) is not audited the way the wrapped CLIs are; for a wrapped CLI only the result the caller acts on (the answer, the token and exit code) matters, not the perfection of its audit records beyond what the spec requires (DL-98).

<a id="D-TASK-MODE-REMOVED-20261005"></a>
## D-TASK-MODE-REMOVED-20261005: the codex wrapper's `--task` mode is removed; each host runs its own family natively

Owner, 2026-10-05, typed (verbatim; source as above), on a fix-round brief line about guarding host A's codex `--task`
fan-out path:

> 아래 부분이 이상하다고

The leader's question asked whether to keep the mode; the selected option (the label is the leader's, the choice the
owner's):

> 지금 제거

Then, typed (verbatim):

> 스펙에 업데이트 했으면 스펙에서도 제거해

> codec hoost는 cluade --task가 있는거지? 네이티브는 그렇게 할 필요 없는데?

Recorded effect: the codex wrapper's `--task` mode (the fan-out worker layer and `--task code`; no real run since
2026-07-05 on host A) leaves host A and the contract: exits 68 / 69 and the tokens `fanout-spawn-error` and
`fanout-partial`. `task-blocked` (65), the claude wrappers' permission-denial class on both hosts, stays. Each host runs
its leader's own family natively and wraps only the other families; host B has no codex wrapper and removes only the
engine's leftover `--task` pieces.

Effect: [R-TOKENS](../reference/review-rules.md#R-TOKENS), `contracts/exit-tokens.json`, case C8,
`authoring/shared-dev-log.md` DL-72 (superseded in part), DL-91.

<a id="D-OWNER-ANSWERS-20261008B"></a>
## D-OWNER-ANSWERS-20261008B: the owner's second answers (auth signals, C40, packet layout, prompt clauses)

Owner, 2026-10-08, typed (verbatim): "5 지금 로그아웃 되어있으니 직접 리턴값이랑 실측해봐 agy -p \"hi\" / 7이해가 안가는데 모델이 왜 스스로 다시한번  답을 내 자세히 설명 / 8 codex 방식으로 / 10번 둘다 삭제 / 14 다 지워 / 19 번 이 md 파일 용도가 뭐여? 어디서써? 그리고 claude host, codex host 그리고 또 같은 hos라도 다른 폴더에서 작업을 할수도 있어"; then, to two questions: "수정안대로 (권장)" (the prompt clauses) and "유지 + spec 기록 (권장)" (C40).

Recorded effect: (5) the authentication STOP stays as it is — the vendor's codes first (gemini exit 41, claude `api_error_status` 401), then the authentication vocabulary inside the vendor's own error carrier only; the signed-out agy run was measured the same day (`contracts/vendor-failure-lines.json`: exit 1, no authentication code, the stderr banner and the stream-json `result.error`). (7) An agy run whose only errored step is a `finish` submission followed by a successful `finish` in the same run is admitted on both hosts (R-CONTAIN). (8) Host A moves to the codex host's review layout: a fresh review root per round, no re-pinned worktree. (19) The shared prompt clauses `deployment-context` and `severity-instruction` take the owner-approved wording (per-folder versus machine-level concurrency, [D-CONCURRENCY-FACT-20261008](#D-CONCURRENCY-FACT-20261008); a vendor shape no run has shown is a recorded limit labelled HARDENING-SUGGESTION; no schema change). Host-only: (10) host A's two gemini leader skills and (14) its post-edit reminder hook are deleted.

<a id="D-AGY-SETTINGS-UNTOUCHED-20261008"></a>
## D-AGY-SETTINGS-UNTOUCHED-20261008: host A never writes or locks the machine-wide agy settings file

Owner, 2026-10-08, typed (verbatim), after asking why the agy settings transaction exists ("agy 이 설정 병렬 버그 때문에 넣은거 맞지? 개선안됐고 계속 이 방법으로 써야해?") and hearing that agy 1.3.1 still offers no per-call permission option while host A's reviews already run an allowlisted agent: "이 스펙 적고 구현을 시작할건데 지금다 삭제해 그럼 명령어가 어떻게 되는거야 agt -p --agent? agent는 우리가 정의해놨어?".

Recorded effect: host A removes all of its agy settings handling — the guard around its permissive call and that guard's lock, the heal of a stale `.agybak` at `--setup-agents`, the shared-lease / holder / crash-recovery module and its lock-timeout setting. Host A writes none of `~/.gemini/antigravity-cli/settings.json`, `.agybak`, `.agy_settings.lock`, `.agy_settings.shared.json` or `.agy_settings.holders/`, takes no lock, and reads only `settings.json`, at the one point the owner's answer below keeps; the install-time `read_url(*)` allow stays the operator's own setting (R-REVIEW-WEB). Host A's read-only agy leg is `agy -p <prompt> --output-format stream-json --agent triad-readonly-review --add-dir <worktree>` (`triad-readonly-research` when the round has web), the two agents being host A's own definitions that `antigravity_wrapper.py --setup-agents` writes to `~/.gemini/config/agents/`. It supersedes the 2026-10-07 host-A fact that A heals B's stale sentinel (R-REVIEW-WEB) and the owner's 2026-10-08 answer 15 ("잠금만 빼"). A stale `.agybak` the codex host leaves is the codex host's to heal; DL-107 asks it to move to an allowlisted agent so no host changes that file per call.

Owner answer, 2026-10-08 (verbatim): "읽기 확인만 남김 (권장)" — to the leader's question whether host A keeps a check of the `read_url(*)` prerequisite; the selected option: host A only reads the agy settings file, and when the `read_url(*)` allow is missing it stops that round before it starts and says why; writing, locking and healing are removed as already decided; a read does not collide with concurrent runs.

Recorded effect: host A writes none of the agy settings files and takes no lock. It reads `~/.gemini/antigravity-cli/settings.json` at one point only: before a round whose review web is authorized and that has an agy leg (at prepare, and at the retry of such a leg), it checks that `read_url(*)` is allowed and not denied, and refuses before inference when it is not (R-REVIEW-WEB). It does not read `.agybak`, the lock, the shared file or the holders. This keeps host A's per-round preflight (DL-58) and narrows DL-112: the check computes the settings path itself once the `_agy_settings` module goes.

<a id="D-CONCURRENCY-FACT-20261008"></a>
## D-CONCURRENCY-FACT-20261008: different working folders and the two hosts run at the same time; one folder does not

Owner, 2026-10-08, typed fact to host A's leader (verbatim): "같은 폴더에서 작업을하지는 않는데 다른 폴더에서 작업을 하지 claude, codex 호스트도 동시에 돌릴 경우 많은데" (no work happens concurrently inside one folder, but work in different folders does, and the claude and codex hosts are often run at the same time).

Recorded effect: this corrects the "no concurrent operation" part of [D-THREAT-MODEL-20261003](#D-THREAT-MODEL-20261003) and R-THREAT. Inside one working folder there is still no second operation while one runs, so a guard against concurrency inside a folder (its packet directories, worktrees, round records) stays out of scope. Operations started from different folders, and operations of the claude-host and codex-host toolkits on one machine, DO run at the same time and meet at machine-level shared state (for example the agy settings file with its `.agybak`, lock and lease files, the agy agents directory, a classifier extension file, the logs inside one installed toolkit used by several projects, the CLIs' own configuration), so a guard on such state is in scope. R-THREAT and the shared prompt's deployment-context clause are rewritten to this fact in the same specification pass; every earlier judgement that rested on "no concurrent operation" for machine-level state is re-checked.

<a id="D-OWNER-ANSWERS-20261008"></a>
## D-OWNER-ANSWERS-20261008: the owner's answers to host A's decision list after the over-design audit

Owner, 2026-10-08, typed answers to host A's leader, item by item (verbatim; the numbers are the leader's list "owner-decisions-2026-10-08"): "1. 삭제 / 2. 삭제 / 3. 끌것 / 4. 뺄것 / … / 6. \"빼 / … / 9. 제거 gemini 는 계속 업데이트 중이니 상관없음 / … / 11. 삭제 / 12. 유지 / 13. 유지 / … / 15. 잠금만 빼 / 16. 다 결정된 후 병합 지금도 수정중이잖아 / 17. 모델명이 계속 변경되고 있어 대표 모델명을 버전없이 적어도 적용되면 정확한 모델 ID대신 별칭을 사용할 것 / 18. 나중에 / … / 20. 시험은 폐기한다 일단 스펙 부터 완성해야 시험을하지 지금은 스펙도 구현도 마무리 안된 상태 / 21. 삭제 / 22. 삭제 / 23. 마무리 하고 다음 작업" (items 5, 7, 8, 10, 14 and 19 were questions back to the leader; item 24 was a capture, now a `contracts/vendor-failure-lines.json` row).

Recorded effect, host A: (1) the shipped migration starter `CLAUDE.recommended.md` is removed from the distribution; (2) host A's claude CLI wrapper bundle is removed — the claude family runs natively on host A, so C31 / R-INVEST / units.json name no claude CLI route for A; (3) the claude-host installer no longer requires pinned vendor binaries, no longer pins a resolved versioned path and no longer gates an operator's `--pydantic` import (DL-105); (4) host A's codex-host product assembler and its tests are removed (install layers are per host, R-PARITY); (6) host A's pre-spawn review-argv digest refusal is removed — an edited dispatch line is caught at collection by the executed-command receipt, as on B; (9) the agy and gemini daily drift checks are removed; (11) host A's 2026-07 codex-host handoff documents are deleted; (12) the non-review agy read-audit file and (13) the effective child cwd record stay; (15) the agy settings heal stays and its lock goes (no concurrent operation, R-THREAT). Standing: (16) the open spec PRs merge only after every decision is settled; (17) where a versionless representative model name (an alias) works on a CLI, rosters and presets name the alias instead of the exact model ID (it extends D-PRESET-ALIASES-20261006 beyond the claude presets; each CLI's accepted aliases are a measured fact); (20) no test campaign runs until the specification and its implementation are complete; (23) host A's conformance goal closes on its 47 cases.

<a id="D-REPAIR-WEB-20261009"></a>
## D-REPAIR-WEB-20261009: failure-driven repair web research on both hosts

Owner, 2026-10-09, to B's leader (verbatim):

> 에러가 나면 웹검색 허용이비? 신규에러는 새스펙일테니

After the leader identified B's blanket network prohibition, the owner requested
the common specification (verbatim):

> 이건 스펙으로 정리해 코덱스 클라루드 공통적용으로 클호드 코드는 웹 검색 미허용이야?

The normative rule is R-CLASSIFY's repair-research paragraph and C76. This extends
the retained repair loop's research capability on both hosts, not its write or
vendor-execution authority. Current A and B prohibitions and implementation
handoff are recorded in [the evidence note](2026-10-09-repair-web-research.md).
Host implementation, runtime verification and revision adoption are pending.

<a id="D-REPAIR-LOOP-KEEP-20261008"></a>
## D-REPAIR-LOOP-KEEP-20261008: the self-improving classifier repair loop stays; its extras go

Owner, 2026-10-08, typed question to host A's leader after the leader's over-design list put the loop under "discard" (verbatim): "이건 왜 폐기 대상이야? 자기개선 기능을 없앨거야?"; after the leader withdrew the discard recommendation with evidence, the owner's answer to one question (verbatim): "유지 + 군살 정리 (권장)".

Recorded effect: the repair loop stays on both hosts — a failed run that ends `unknown` or `extraction-error` goes to a read-only analyzer that proposes one phrase or exit-code entry from that run's own record (a measured shape, R-CLASSIFY), and deterministic code applies it to the user classifier extension. Its extras go: a wrapper `timeout` is not routed to the analyzer (no proposal can change a timeout classification); the applier keeps its lock and drops the caps written against a malicious analyzer (R-THREAT); a proposal is verified by classifying the stored run record again, not by calling the vendor again; a phrase learned this way is promoted to `contracts/vendor-failure-lines.json` (R-CLASSIFY). Basis: frozen C43's "no user classifier extension present" is that case's input precondition, not a prohibition; the real vendor sentences now in the contract were largely found by this loop (agy `unavailable (code 503)` and `network issue connecting to the server`, codex `selected model is at capacity`, gemini capacity / quota sentences). DL-104.

<a id="D-PRESET-ALIASES-20261006"></a>
## D-PRESET-ALIASES-20261006: host A's shipped claude presets name the model by alias; the older-model preset is removed

Owner, 2026-10-06, typed answers to host A's leader (verbatim). On the model-tier lines: "추르셋은 opus sonnet 같이 적는데 범용성에 좋고 동작도해" (the presets should be written with aliases such as opus / sonnet — better for generality, and it works). Then, shown that an alias always resolves to the latest model (only a full model name pins a version) and that frozen C12 / C34 name `claude-opus-5-5` and require an explicit older model to be selectable: "전부 별칭, 이전 모델 프리셋 제거" (all aliases; remove the older-model preset).

Recorded effect: every claude preset host A ships names `model: opus`; the `-older` / `-older-web` pair is removed; on host A the default is the latest Opus and no older Claude model is selectable. Proposed spec change (the owner's PR): C12's expected result ("including Claude claude-opus-5-5 with xhigh" and "an explicit supported older Claude model"), C34 (explicit Opus 5.5 selection) and R-ROSTER's "older supported models remain selectable" — `authoring/shared-dev-log.md` DL-100 (DL-94 superseded).

This supersedes, for host A's native route, the owner's 2026-09-25 default sentence in R-ROSTER ("Ship the explicit model ID rather than the moving `opus` alias") and the handoff's "exact model/effort pins in preset frontmatter" (the model pin becomes the alias; the effort pin stays exact).

<a id="D-SHIPPED-PRESETS-20261005"></a>
## D-SHIPPED-PRESETS-20261005: host A's claude leg names only shipped presets; skill users get a guide

Owner, 2026-10-05, typed (verbatim; source as above), on host A's code that emulated Claude Code's agent-file reading:

> 아래문제 claude host가 스폰하는 서브에이전트는 자체로깅이 잘되어있어 굳이 관리할 필요있어? 사전에 effort 산택용 모델 에포트 설정된 md만 몇개 만들면 되잖아

> C12는 스킬받는 사람들에게 가이드라도 줘야해 EFFORT를 선택못하는 이슈 설명과 유리같은 프리셋을 주던가

Recorded effect: On A the claude review leg names one of a closed list of SHIPPED reviewer presets (model × effort, each
with a web twin, plus one older-model preset for C12); the shipped file's digest is the bound control (C19); there is no
operator-authored preset lookup and no emulation of Claude Code's agent-file reader — Claude Code records its own
subagent transcripts. Because Claude Code fixes a subagent's model and effort in its agent file, with no per-call effort
override, host A gives skill users a guide that explains this and lists the shipped presets.

Effect: [R-ROSTER](../reference/review-rules.md#R-ROSTER) (On A), R-REVIEW-WEB (On A), cases C12 and C19,
`authoring/shared-dev-log.md` DL-49 — their host-A text is rewritten (host A @ triad `3894879`; DL-94).


<a id="D-GEMINI-FLOOR-20261009"></a>
## D-GEMINI-FLOOR-20261009: Gemini CLI support begins at 0.63.0

Owner, 2026-10-09, direct instruction to the Codex leader (verbatim):

> Gemini믄 63부터 지원하는걸로해

The owner selected a common Gemini CLI minimum of 0.63.0 after checking the
latest stable GitHub release. This replaces the earlier 0.34.0 formal and
0.60.0/0.61.0 model-specific support boundaries with one route floor. It applies
to raw investigation and legacy/v2 review on both hosts; it does not change
model defaults, authorize model-list probes, or alter either host's native leg.
0.63.0 prereleases are below the floor; later versions still need the existing
interface, authentication, containment and receipt controls. No effective
runtime identity is inferred from passing a version gate.

Effects: R-GOOGLE / R-NOCOST, R-CLI-VERSION; C16, C18 and C65. Both host
maintainers update their Gemini checks and tests; the Codex leader changes B
only and requests A's equivalent implementation through the shared handoff.
The earlier alternatives in `2026-10-09-model-pin-version-conflict.md` are
superseded by this explicit owner choice. No release/adoption is implied.


<a id="D-REVIEW-DISCOVERY-20261009"></a>
## D-REVIEW-DISCOVERY-20261009: independent source discovery; incident-driven log inspection

Owner, 2026-10-09, direct instructions to the Codex leader (verbatim):

> 너는 판단을 하지마 무슨 파일이 연관이 되어 있는지 일일히 읽어서 넣을수도 없고
> 또 지금처럼 허용파일만 읽었는지 사후 읽기 감사흫 해서 토큰을 낭비하게 할거야? 읽기 감사는 문제가 있을때만 로그를 읽는거지 왜 매번 읽어서 비용을 낭비 시켜?

> 이것부터 수정하고 claude쪽에도 같은 문제가 있으면 스펙에 추가해

Interpretation: the leader supplies a worktree/diff and objective; reviewers discover
related code. No leader-built exhaustive source allowlist or routine leader read-log
audit. Explicit exclusions and existing coded route containment/custody checks remain.
This is not an instruction to disable A's AGY required-input-read or tool-effect gate.
Source findings and the request to A are in
[the shared diagnosis](2026-10-09-review-read-boundary.md).
Effect: R-PROMPT, common code-purpose clause, C70/C71. No native-leg change, revision
adoption, installation or release is authorized by this record.
