# Review strategy amendment — 2026-10-02

Status: shared amendment landed on main `19f0cf1f6772ad1c480d828c53129d50910495db`; B `v0.2.558` is published and locally installed under subsequent explicit owner authority. A implementation and adoption remain separate. The original strategy/spec amendment's exact-head shared review/CI evidence is recorded on PR #8; this subsequent release-handoff-only amendment's review/CI is recorded on its owning pull request and is not pre-certified here.
Authoring basis: fetched `main` at `6f57ea499a28725da0dbc83bb673378e620c8bfa`.
Owner authority and verbatim decisions: [D-REVIEW-STRATEGY-20261002](owner-register.md#D-REVIEW-STRATEGY-20261002).
The owner received a Markdown change summary before this amendment was applied.

## Evidence and direction review

The owner compared several prompt variants on previously reviewed plans and commits, then asked for research and
independent direction assessment. The local observations are exploratory: single runs, model variation and different
plan/code tasks do not establish a universal ranking of prompt length or prove that detailed instructions suppress
defect discovery. The strategy is an operational choice to preserve broad discovery, adequate context and clear approval.

Research considered includes [VulContextBench](https://arxiv.org/html/2609.32601v1),
[ZeroPath's Opus 4.6 experiment](https://www.eu.zeropath.com/blog/benchmarking-opus-4-6-vuln-detection),
[SWR-Bench](https://arxiv.org/html/2509.01494v2) and
[PerspectiveGap](https://arxiv.org/html/2606.08878v2). Their tasks and models differ from this workflow. In particular,
viewing a ground-truth code block versus citing it in a final report is not a measure of recognizing a defect versus
deliberately withholding it. These sources do not establish an optimal roster, universal role-prompt harm or mandatory
repeat count. No claimed measured quality improvement is a release criterion for this amendment.

Direction reviewers were requested as Astra/xhigh and Opus 5.5/xhigh (`claude-opus-5-5`), with web authorized.
Requested settings are not certification of hidden runtime settings. R1 was independent; R2 was a scoped correction
check with prior findings disclosed, not a new blind experiment. These were selected investigations, not formal reviews.

| Direction review | Astra | Opus 5.5 |
|---|---|---|
| R1 | READY_WITH_NONBLOCKING_NOTES | MATERIAL_OBJECTION: two input/evidence contract gaps |
| R2 | READY | READY_WITH_NONBLOCKING_NOTES; both material objections closed |

The two corrections are concrete:

1. Environment and residual content remain leader-authored prose. Existing checks establish structural input validity,
   binding and faithful transport, not semantic completeness, state transitions or automatic issue deduplication.
   A typed environment/residual subsystem was explicitly rejected as unnecessary scope.
2. Required earlier excerpts, counterevidence and verification results are included in current bound packet surfaces.
   Historical paths alone cannot supply authority or survive temporary-root cleanup. No new packet slot or retention
   extension is needed.

Remaining R2 notes clarified nonempty field checks, existing transport slots, prose versus enum terminology and the
stage mapping. They introduced no new design choice. The direction reviewers did not inspect this later shared-spec
diff or certify host conformance. Same-commit shared-spec review and required host gates remain later steps.

## Current behavior and changed target

The authoritative rules are [review-rules.md](../reference/review-rules.md); this table identifies changes and seams.

| Current or historical surface | Candidate change | Owning unit / case |
|---|---|---|
| R-AGREE admits Minor-only negative; family coverage can require an owner release | Every selected enabled entry explicitly approves; no family minimum; exception remains non-agreement | review-lifecycle, verdict-wire, roster / C13, C33 |
| v2 prompt says pre-merge; legacy has stage vocabulary | One shared plan or code purpose, selected using the existing vocabulary and omission default | prompts, review-lifecycle / C60 |
| Claude intro also requests `ultrathink` | Remove the extra in-context intensity instruction with the persona/isolation wording; one shared purpose and existing configured effort remain | prompts / C60 |
| Existing TASK/brief and residual strings | Leader writes environment and current issues; host transports without new semantic machinery | prompts / C61, C62 |
| Prior findings can point to earlier records | Materialize evidence needed now in existing currently bound surfaces | cleanup, review-lifecycle / C20, C63 |
| Conflicts/repetition go to the owner | Continue verifiable progress; stop exhausted wording loops without approval | review-lifecycle / C64 |
| B model IDs/efforts use existing roster data; A's native preset pin seam is historical, current A uninspected | Preserve R-ROSTER's single-edit-location target and exact IDs; verify/reconcile A's JSON selection and native pins at implementation start, without a new design here | roster / existing C12, C22, C34; DL-4 |
| Observed CLI versions and capability controls | Observed patch is evidence, not an equality pin; retain justified capability/version guards | engine-transport / C65 |

B proposal baseline was `8bc6b07684058eccc0ed6e7f632077ef4a207b8c`. The owner's later
[implementation authority](owner-register.md#D-REVIEW-STRATEGY-IMPLEMENTATION-20261002) authorized B to implement first.
B historical implementation source `f6651121bf775a40f8743c10cd6c3f3590fef88c` selects/binds phase and requires all-selected approval,
reusing roster, binding, retry and cleanup paths. [Verification and A handoff](claude-review-strategy-handoff.md)
record actual evidence; this shared-spec PR itself contains no product code. The owner excluded A implementation
inspection. A entries in `units.json` remain historical pointers; current A behavior is not asserted.
Historical [DL-4](../authoring/shared-dev-log.md) and [C34](../cases/cases.json) record A's
JSON `claude.agent` selection of a native preset, refusal of roster `claude.model`, and
model/effort pins in preset frontmatter. A must verify its actual configuration boundary
at implementation start and reconcile the single-edit-location intent through its native
seam; native constraints requiring a new design go to the owner under
[R-STOP](../reference/review-rules.md#R-STOP). This remains an A implementation
planning item; shared publication establishes neither present conformance nor its completion.

The `ultrathink` removal is a prompt change, not a claim of equivalent model behavior.
[Official Claude Code documentation](https://code.claude.com/docs/en/model-config)
(checked 2026-10-02) describes it as an extra in-context reasoning instruction.
This amendment avoids a second prompt-level intensity request; the configured model
and effort remain unchanged. No quality effect is inferred.

## Preservation, overlap and adoption

- Keep canonical verdict tokens and fields, duplicate rejection, identity/digest/attempt binding, full-scope re-review
  on changed conditions, failed-to-run-only same-basis retry, containment and directly requested web authorization.
  (Superseded on 2026-10-03 for review web: R-REVIEW-WEB's standing authorization, D-REVIEW-LEGS-20261003.)
- Keep native host topology, exact model IDs, JSON override precedence, explicit null semantics and existing defaults.
  (Superseded on 2026-10-03 for the codex default: R-ROSTER's `gpt-6-astra` / `high`, D-REVIEW-LEGS-20261003.)
  Do not introduce new model configuration, fallback, catalogue probes or wholesale catalogue-policy changes.
- Preserve host-specific [retention and export](claude-host-v2-implementation-prd.md#PRD-RETENTION): generated brief,
  residual and evidence files follow their existing ownership/lifecycle. No common replacement age limit, scheduled
  cleaner, automatic deletion of durable exports/investigations or cleanup of provider-owned resources is introduced.
- Skill/prompt behavior experiments are outside TRIAD. Static schema, text transport and contradiction checks remain
  valid; a leader reenactment does not certify behavioral improvement.
- Open [PR #6](https://github.com/codefoundry-io/triad-dispatch-spec/pull/6), inspected at
  `29777171c1b7e5d0d0fe0daad969291b0cfed7bf`, changes R-ROSTER/model catalogue policy and quota wording. This draft is
  separate. Reconcile overlapping paragraphs explicitly when integrating; a quota/partial-result owner decision must
  not become all-leg agreement. Its proposed cleanup exception is not adopted here.
- Host adoption must align renderer, phase input and collection in one coherent release. Keep explicitly selected legacy
  entry points distinct; do not reinterpret historical results or claim installed behavior changed with this spec PR.
  The shared-spec commit may be reviewed before adoption without inspecting A implementation code.

## Verification and remaining limits

Historical B source `f6651121bf775a40f8743c10cd6c3f3590fef88c`: macOS 26.6.2 arm64 / Python 3.12.13 / pytest 9.0.3: 1818 passed; Ubuntu 24.04.4 arm64 / Python 3.12.3 / pytest 9.0.3 as uid 1000 in Docker: 1816 passed, 2 filesystem-specific skips. This Ubuntu result is a historical container observation, not native Ubuntu proof. Structural source checks, validator and provider-free lifecycle passed on that earlier basis.
Its code review `triad-strategy-impl-20261002-r1` obtained all four selected explicit approvals on the same
bound basis with final integrity. This is historical implementation review, not carried
direction/plan approval, fixed-profile admission, host adoption, installation or release.
The [handoff](claude-review-strategy-handoff.md) maps cases and commands. Source-skill
checks are bounded structural workflow checks, not prompt efficacy or defect-recall proof.

The owner later explicitly authorized B merge, release and local skill/plugin update.
[PR #39](https://github.com/codefoundry-io/triad-codex-dispatch/pull/39) merged at
`7f75863d9d4c8fe82464d90ddfd9eace9d4740bb`, with baseline `0dbd6c2` and reviewed
candidate `632f42633d3a92d6cb27168cd15c4d4debd8558c` as parents; candidate and merge
share tree `6161ed5b`. [Release v0.2.558](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.558)
is published. Final R4 approval/integrity and candidate-archive verification are
[recorded publicly](https://github.com/codefoundry-io/triad-codex-dispatch/pull/39#issuecomment-5954919488):
all four selected legs approved; macOS 1828 passed, 2 skipped; 49 distribution hashes verified.
The [handoff](claude-review-strategy-handoff.md#codex-host-evidence-and-publication-boundary)
records the archive digest, installed-file equality and settings semantic preservation
(global configuration bytes changed). Installed provider-free lifecycle passed all 14
commands with zero failures and exact owned temporary paths cleaned. A fresh ephemeral
Codex session exposed/read the namespaced `0.2.558` skill and returned
`TRIAD_02558_NAMESPACED_AVAILABLE`; [public completion receipt](https://github.com/codefoundry-io/triad-codex-dispatch/pull/39#issuecomment-5955231957).
This does not establish existing Desktop-session live reload. Native Ubuntu checks of the final release
were not run by the macOS host and remain with the Ubuntu owner/native CI; no new
shared release gate is introduced. This subsequent authority does not authorize A deployment.

For the original strategy/spec amendment, shared authoring/schema checks and exact
shared-spec commit review/CI preceded main landing; their actual terminal evidence is recorded on
[PR #8](https://github.com/codefoundry-io/triad-dispatch-spec/pull/8), without changing a
reviewed commit merely to embed its own hash. The phase schema is scalar; the host,
not its default annotation, applies omission defaulting. Shared validation never dispatches a provider.
The subsequent release-handoff-only amendment records its own review/CI on its owning
pull request; the original PR #8 evidence does not pre-certify it.

| Claim | Current evidence boundary |
|---|---|
| B phase/collection/current-context/evidence/compatibility fixtures | Historical results above; final candidate archive: macOS 1828 passed, 2 skipped; cases C13/C20/C33/C60–C65 carry source/test mapping |
| B source-skill workflow, validator and fixed provider-free lifecycle | Historical source checks PASS separately; installed lifecycle 14 commands/zero failures and fresh namespaced skill exposure PASS; no model-quality measurement or existing Desktop live-reload claim |
| Native Ubuntu checks of final B release | NOT RUN by the macOS host; handoff to Ubuntu owner/native CI; historical Docker results are not native proof |
| A revised-strategy implementation and service checks | NOT RUN; A implementation code was not inspected (superseded in place on 2026-10-03: host A's provider-free fixture evidence at triad `faeb86b` is recorded in `contracts/review-strategy.verify.toml` `[host.A]` and the cases' tests.A cells) |
| New authenticated v2 CLI compatibility/effective policy | NOT RUN; fixture success and development review dispatch are not runtime conformance |
| Same-commit shared-spec review and CI | Original strategy/spec amendment: exact-head evidence on PR #8; subsequent release-handoff-only amendment: its own owning pull request, not pre-certified here |
| B product merge/install/release | PR #39 merged; v0.2.558 published and locally installed; evidence and remaining checks in the handoff |
| Shared revision/payload adoption and A implementation/deployment | Separate authority and checks; B vendored payload remains 04245c7, not authoring main 19f0cf1 |

`contracts/review-strategy.verify.toml` records per-host evidence and the existing
check briefs. B implementation did not require a normative rule or payload change.
The later shared-spec review found stale C21 release-path language and older A
handoffs still presented as current. Their corrections align derived acceptance
text and navigation with the already chosen R-AGREE/R-PROMPT rules; canonical
payload bytes and model configuration remain unchanged.
