# Codex-host B: current status and Claude handoff

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

## Current implementation status — 2026-09-20

This section supersedes the completion labels in the preserved release audit
below. It changes no normative rule, schema, prompt, policy payload or runtime
behavior. A remains read-only until the owner-designated B handoff point.

| Basis | State |
|---|---|
| Published B baseline | `3d62b7cc370d2c72fc439a431d5f78ab76875b98`, branch `codex/agy-web-evidence`, open PR 37; P1/P2/P4 and their documentation are published |
| Published B P3 source | [add5805d8dec70f5e133164c49bc0fe3bff75095](https://github.com/codefoundry-io/triad-codex-dispatch/commit/add5805d8dec70f5e133164c49bc0fe3bff75095); operational opt-in v2, corrected route/default/version and input-refusal boundaries; formal admission and clean distribution recorded in the current verification record |
| B remote main | `56f0f6657084f81516217ee51698f9b18cfc71dc`; feature publication is not merge or installation |
| A source basis | `92c8afd500499d8736afcc28b39a87a4f87fed50`; no A implementation changes are part of this work |
| Shared remote main | `2eb883fee59e66556ee7c7f87189b38231136622` |
| Authoring baseline | `aef3adee863fd90fdfab60ae2253717cf1b4d303`, candidate branch `codex/host-b-preimplementation-audit`, open PR 1 |
| Payload provenance | Schema bundle `055204c`; review prompts `6bef14c`; P4 policy/investigation amendment `6f0f274`; descriptive mapping refreshes do not repin payload bytes |
| Adoption/release | No new shared adoption, merge, install or release is claimed. The prior 0.2.555 release does not establish installation of this feature branch. |

### Current case register

The complete named test mapping is in [cases.json](../cases/cases.json). The
following table describes implementation and its boundaries; test results and
external checks have separate evidence.

| Cases | Current implementation | Boundary |
|---|---|---|
| C1, C2, C6 | Reader/stdin/owned-group supervision, partial setup, catchable parent signals and guard-release custody | No SIGKILL, host-crash or universal provider guarantee |
| C3–C5, C7 | Fresh-IPC age floor, owned allocation, verified export, inventory, resumable cleanup and idempotence | Only proven B-owned disposable resources |
| C8 | Canonical token map, alias/direct-exit and phase-specific exceptions | Map-only rows do not introduce emitted repair states |
| C9, C10 | Actual CLI/native host observations in immutable invocation custody | Claude stdin must be complete; Google argv delivery is not-used; native may be unexposed. Gemini preflight version is not promoted to a runtime observation. |
| C11, C17 | Common injection scrub and route-specific Google environment/authentication guards | No live principal or account-entitlement proof |
| C12 | Packaged defaults, project `.agents/triad-review-legs.json`, merge by name and capability-checked preparation/dispatch | Omitted fields use exposed/permitted defaults or controlled refusal with preparation-failure custody |
| C13, C14, C30 | Pinned v2 schema/prompts, producer projections, strict original JSON and six-binding authoritative validation | Explicit legacy and raw/custom-schema interfaces remain separate |
| C15 | Exact separate B policy, Gemini/AGY REVIEW no-web controls and renderer restrictions | B1–B3 and A V1–V5 authenticated policy checks remain NOT RUN |
| C16, C18, C22 | Roster settings reach native arguments or CLI argv; selected binary/help/version and supported controls checked before inference | Requested/default/preflight settings are distinct from observed runtime identity |
| C19 | Diagnosed terminal failed-entry retry on the same basis, incremented attempt and retained sibling/history evidence | Valid negative verdicts are not transport failures; preparation failure invents no provider attempt |
| C20 | Source/conditions/toolkit binding and changed-basis full review with fenced prior findings/rebuttals | Normal runtime logs are excluded; policy/code/prompt changes remain bound |
| C21, C23 | All enabled entries count, independent family coverage and immutable name/attempt result/read evidence | Informational entries can block; missing/invalid/swapped/drifted evidence cannot admit |
| C24 | Separate deterministic macOS and Ubuntu verification | No installed or authenticated service matrix inferred |
| C25, C28 | Raw caller prompts/custom schema/settings/authorized roots, entry-cwd path resolution and existing masked evidence | No mandatory investigation envelope or permanent web archive |
| C26, C27 | Link-text evidence without implicit target access, frozen route/executable and honest version observations | Prompt controls are not OS path confinement; dormant AGY hook stays dormant |
| C29 | Both raw Google --web triggers append the common investigation clause last, including Gemini repair | KI-AGY-URL-BODY-PREFIX remains non-fatal incomplete evidence; no automatic retry, workaround or vendor-fix claim |

### Verification and publication evidence

The first P3 review (`triad-b-transport-p3-r1`) failed and cannot admit any
candidate. Leader adjudication accepted F1 (Google argv evidence), F2 (omitted
adapter selection) and F3 (Gemini version provenance). A separate dedicated RED
instance reproduced ten failures and five controls. The corrected candidate
passed 96 related leader tests. Clean-input dedicated GREEN passed 15 focused
and 1619 full macOS tests plus validator/lifecycle; Ubuntu passed 1617 with two
existing filesystem skips. Both recorded source equality and exact cleanup.
Subsequent input-refusal corrections passed a fresh 12-case RED, 56 related
leader tests, clean-input dedicated GREEN (27 focused / 1631 full macOS,
validator/lifecycle) and Ubuntu (1629 passed, 2 existing skips). Both full
suites retained unchanged-source and exact-cleanup receipts.
Current formal, distribution and publication outcomes are maintained in the
[P3 verification record](host-b-p3-verification.md).

P1/P2/P4 retain their published historical evidence. P4 `triad-b-p4-r1` was
ADMITTED_SAFE with four SAFE results, digest
`3b3f3414f05714417dd73d6d2ea600eabd19bfec12a06c305441e138fdcc3209`,
verified integrity and exact exported-root cleanup. Those receipts do not
certify later P3 bytes. P3 publication is now [add5805d8dec70f5e133164c49bc0fe3bff75095](https://github.com/codefoundry-io/triad-codex-dispatch/commit/add5805d8dec70f5e133164c49bc0fe3bff75095), with four SAFE
results in `triad-b-transport-p3-r3` and 1631 clean archive tests.
The [final implementation PRD](claude-host-v2-implementation-prd.md) is the
functional handoff; this record preserves execution history.

- [B1–B3](../contracts/gemini-readonly-b.verify.toml) and
  [A V1–V5](../contracts/gemini-readonly.verify.toml) remain NOT RUN. These are
  service-evidence gaps, not absent policy implementations.
- AGY 1.2.7 legacy-search compatibility remains unverified: the requested grep
  was not actually called. Model prose is not a tool-failure result.
- Accepted P4 diagnostic limits remain: an invalid extra-directory candidate
  may show entry cwd while its underlying error names the rejected path;
  missing required jsonschema during Gemini provenance parsing exits 1 rather
  than 3. Both refuse before inference and preserve masking.
- Clean committed distribution verification, feature publication, final merge,
  shared adoption and installation/release are distinct operations. The
  proposed repository-wide spec/drift checker is separate authoring tooling.

D-B1/D-B2/D-5 are settled: separate host policies, existing masking/failure
logging without a new web store, and the selected B project roster path.
The legacy workspace four-leg development gate stays separate from public
v2 roster and retry semantics.

### Log and review-resource lifecycle

The normative source is [R-CLEANUP](../reference/review-rules.md#R-CLEANUP), with
the terminal flow in [process.md](../reference/process.md) and C3/C4/C5/C7.
It requires verified export before temporary review-root deletion, proven
ownership, preserved uncertain residue, idempotence and a fresh-IPC age floor
even under caps. It does not prescribe common numeric thresholds or automatic
expiry for all retained evidence.

The complete B operational table is [README log retention](https://github.com/codefoundry-io/triad-codex-dispatch/blob/3d62b7cc370d2c72fc439a431d5f78ab76875b98/README.md#log-retention-and-lifecycle).
Source at B `8f12bd5`: `_common.py:260–280,2305–2392,3003–3136`;
`review_round.py:1221–1353`. Existing log/cleanup tests cover these paths.
No new cleaner, logger, timer or deletion was introduced.

A's next-run floor is 7,200 seconds at [A common:3676](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L3670-L3707);
B's is 3,600. That difference alone does not violate R-CLEANUP. A's cap loop at
[A common:3386–3395](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L3386-L3409)
still unlinks old-sorted entries without an age-floor check. Carry forward C3's
existing fresh-sibling requirement when A resumes, preserving read-audit
primary/copy semantics rather than copying B's storage layout.

Debug files, durable exports, task `_runs` records and provider-owned AGY brain
data are not covered by next-run failure-IPC cleanup. The
[known-issue disposition](2026-09-20-owner-follow-up.md#ki-agy-url-body-prefix-non-fatal-known-issue)
adds no permanent log and does not authorize deleting collected evidence.

### Updated A follow-up for completed P4

| Topic | A source at `92c8afd` | Follow-up; A stays unchanged in this step |
|---|---|---|
| C15 policy | `3rd-Agent/wrappers/policies/gemini-readonly.toml`, separate 100/200 profile | Preserve A profile; do not copy B's 999/998 policy merely for symmetry. Both manifests remain unrun. |
| C25 extra roots | `3rd-Agent/wrappers/antigravity_wrapper.py:108–109,1216` uses cwd-derived review grants; A Gemini/Claude parsers have no extra-root option | Preserve review grants and add separately authorized raw roots when A adopts C25. |
| C28 | `_common.py:1148–1190` still rejects relative prompt/cwd; B now resolves and records masked paths | Apply captured entry-cwd semantics to A's wrappers, including its Codex subprocess, retaining checks/masking. |
| C29 | `antigravity_wrapper.py:1381–1393` already appends its clause; A Gemini has no explicit web trigger | Preserve AGY research-agent selection; add authorized Gemini trigger when adopting that path. No permanent web archive. |
| AGY search | `antigravity_wrapper.py:277–280,317–321` custom legacy tool list and init-inventory caveat | Do not infer live availability from init/model prose; do not silently alter the common prompt. |

The archived A source pairs below remain useful at `92c8afd`; their B completion
labels and D-B1/D-B2 pending claims are superseded above. Recheck each A source
before its implementation. Preserve native Claude, Codex subprocess, raw admit,
read-audit, worktree and auth guards. Read this published commit plus latest
shared main; report disagreements on the same basis under R-AUTHORING-SYNC.

<details>
<summary>Preserved 0.2.555 release audit — historical basis, not current completion status</summary>

# B 0.2.555: contract audit and Claude implementation handoff

Status: informational source audit, 2026-09-20. This document neither changes the
shared contract nor accepts a pending proposal. B's release is complete; adoption
and complete implementation of the shared agreement are not.

## Historical release audit — superseded status snapshot

The following audit records its original release basis. Its open/deferred
labels and owner-decision list are historical; use the current status and
case register above for the P3 candidate. Evidence and source links below
are retained without rewriting their original findings.

## Basis and meaning of the historical result

| Surface | Verified basis |
|---|---|
| B source / released main | `bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd`, public and locally installed `v0.2.555` |
| A source, read-only | `92c8afd500499d8736afcc28b39a87a4f87fed50`; A was not changed by B's work or this audit |
| Latest fetched shared remote main | `2eb883fee59e66556ee7c7f87189b38231136622` |
| Agreed normative basis | `bd506054e62b9b1ba5ef5e156ae8928ac414e4bf`; later main commits are acknowledgements / runner notes |
| Authoring branch inspected | `codex/host-b-preimplementation-audit`, pre-audit HEAD `10e4af0a2e38c65fc4bd0279eddf2205c6d2a52f` |
| Adoption | Only `rev-0` exists in the fetched shared tags. No `rev-1` adoption or B `SPEC_REVISION` is claimed. This branch is not shared main. |

The agreement explicitly distinguishes design agreement from executable
conformance ([decisions/rev-1-agreement.md:3–7](https://github.com/codefoundry-io/triad-dispatch-spec/blob/2eb883fee59e66556ee7c7f87189b38231136622/decisions/rev-1-agreement.md#L3-L7)).
The owner subsequently authorized Codex-first implementation, integration and
deployment. Those instructions explain the B release; they do not imply that a
pending shared design was accepted or that unimplemented cases passed.

The earlier “five open findings” counts only reviewer-local IDs from the initial
25-finding diagnosis. It is **not** the count of all remaining contractual
obligations. C8, C18, C19, v2-dependent orchestration, adoption and verification
work remain in addition to D-B1/D-B2. No completion percentage is justified:
one case often contains several obligations and no complete common case runner
has produced a cross-host conformance result.

This audit used three independent fresh native Codex children (`gpt-5.6-terra`,
`high`, `fork_turns=none`) for transport/custody, Google/investigation, and A/B
comparison, followed by leader source adjudication. These are source audits,
**not** a new Claude/Google/Codex formal admission round. No provider or candidate
was run in this audit. Existing executed evidence is linked below.

## Complete case register

“Implemented locally” means the cited behavior is present with existing local
test evidence. It is not a declaration that every runtime/platform variant
passed. “Partial” names the retained obligation; “Open” is not an accepted host
exception. “Deferred” names an actual absent shared-v2 prerequisite.

| Case | Current B behavior / evidence | Assessment and remaining obligation |
|---|---|---|
| C1 | Reader completion/error, stdin outcome, child exit and owned process-group reconciliation: [bin/_common.py:1303–1530](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1303-L1530); [tests/test_terminal_transport.py:88–150](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_terminal_transport.py#L88-L150). | Implemented locally for bounded terminal transport. Synthetic evidence does not certify every authenticated provider/platform combination. |
| C2 | Partial thread setup is inside cleanup protection: [bin/_common.py:1419–1475](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1419-L1475); [tests/test_terminal_transport.py:162–200](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_terminal_transport.py#L162-L200). | Implemented locally; setup exceptions cannot silently leave success. |
| C3 | Age floor plus still-matching leaf identity during pruning: [bin/_common.py:2871–2918](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L2871-L2918); [tests/test_log_cleanup.py:898–939](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_log_cleanup.py#L898-L939). | Implemented locally; fresh siblings are not deleted just to reach a cap. |
| C4, C5, C7 | Proven allocation, verified export, inventory, allocation-bound resumable claim and revalidation before deletion: [bin/review_round.py:963–1005](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L963-L1005), [bin/review_round.py:1141–1351](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1141-L1351); [tests/test_review_cleanup_custody.py:36–56](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_review_cleanup_custody.py#L36-L56). | Implemented locally for B-owned disposable roots. Not a defense against malicious same-UID forgery or arbitrary open-FD concurrency. |
| C6 | Completed transcript survives settings-release failure, which cannot convert failure to success: [bin/antigravity_wrapper.py:666–697](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/antigravity_wrapper.py#L666-L697); [tests/test_antigravity_stream_json.py:1804](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_antigravity_stream_json.py#L1804). | Implemented locally. Preserve the primary failure when one already exists. |
| C8 | Local token map: [bin/_common.py:69–88](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L69-L88); pre-spawn encode failure is `unknown` / exit 1 at [bin/_common.py:1329–1340](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1329-L1340). | Open. No exhaustive shared emitted-token/direct-exit/alias membership test. The import assertion at [bin/_common.py:2303–2308](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L2303-L2308) cannot prove membership because the map has a non-null fallback. Shared phase exceptions and B migration delta remain at [contracts/exit-tokens.json:109–123](https://github.com/codefoundry-io/triad-dispatch-spec/blob/2eb883fee59e66556ee7c7f87189b38231136622/contracts/exit-tokens.json#L109-L123). |
| C9, C10 | Host-local audit and run-log fields remain: [bin/_common.py:1972–2039](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1972-L2039), [bin/_common.py:2747–2767](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L2747-L2767). | Deferred common receipt schema. `receipt-fields.json` does not yet exist; existing records are not an implementation of that missing common schema. |
| C11 | Common loader/interpreter scrub plus formal Google route-specific removal: [bin/_common.py:1208–1223](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1208-L1223), [bin/gemini_wrapper.py:43–53](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L43-L53); [tests/test_provider_wrappers.py:1770–1840](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_provider_wrappers.py#L1770-L1840). | Implemented local environment controls. This does not prove an empty environment or an authenticated account identity. |
| C12 | Fixed per-family render options: [bin/review_round.py:2272–2353](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L2272-L2353). | Open / shared-v2 dependency. No general roster loader, named override/unknown-key validation or resolved N-leg dispatch matrix. A paired Pro/Flash fixture is not N-leg support. |
| C13 | Blocking findings and open questions prevent SAFE; Minor-only SAFE is valid. [bin/verdict_schema.py:147–161](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/verdict_schema.py#L147-L161). | Partial. Minor-only non-affirmative verdicts are rejected, whereas the agreed mapping permits them with a recorded verdict-selection deviation. Common wire migration remains. |
| C14 | Duplicate keys rejected at the original JSON boundary; current review ID/family/digest binding checked: [bin/verdict_schema.py:107–112](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/verdict_schema.py#L107-L112), [bin/verdict_schema.py:214–230](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/verdict_schema.py#L214-L230); [tests/test_verdict_original_json.py:70–176](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_verdict_original_json.py#L70-L176). | Partial. Current lexical/binding defects fixed; v2 `leg_name`, `attempt`, `route`, `schema_version` and the common finding fields are not implemented. |
| C15 | All REVIEW renderers forbid web; formal AGY adds its web deny while raw investigation retains its behavior: [bin/review_round.py:63–91](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L63-L91), [tests/test_review_no_web.py:59–142](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_review_no_web.py#L59-L142). | Partial. B Gemini still explicitly allows both web tools at priority 999: [bin/policies/gemini-formal-readonly.toml:5–17](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/policies/gemini-formal-readonly.toml#L5-L17). Its bytes differ from the shared policy. Prompt prohibition is not mechanical Gemini denial. D-B1 open; V1–V5 NOT RUN. |
| C16 | Selected Gemini binary receives provider-free version/help checks, SemVer floor `>=0.34.0`, and observed-version receipt: [bin/gemini_wrapper.py:142–205](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L142-L205). | Partial. Local preflight implemented; supported live service/authentication identity is not established by mocks or version text. |
| C17 | API-key/ADC/Vertex/endpoint/model-selector removal on formal route: [bin/gemini_wrapper.py:43–53](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L43-L53); child-environment assertions: [tests/test_provider_wrappers.py:1770–1840](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_provider_wrappers.py#L1770-L1840). | Local scrub implemented/tested; live authenticated principal and subscription-route proof remain unverified. |
| C18 | AGY declares Pro-high/high at [bin/antigravity_wrapper.py:35](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/antigravity_wrapper.py#L35). Gemini refuses an explicit formal model at [bin/gemini_wrapper.py:314–324](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L314-L324) and dispatches Auto at [bin/gemini_wrapper.py:388](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L388). | Open. Gemini Auto does not satisfy the agreed Pro family + verifiable HIGH default. Model values remain code defaults, not a common roster. This is migration, not an accepted exception. |
| C19 | Public failure protocol keeps siblings as advisory findings, then uses a fresh ID and all three families: [skills/triad-cross-family-review/references/convergence.md:65–86](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/skills/triad-cross-family-review/references/convergence.md#L65-L86). | Open policy difference. Shared R-RETRY permits failed-leg-only retry on an unchanged basis. Current workspace formal exception also requires fresh complete rounds; it does not implement shared attempt/reuse semantics. |
| C20 | Objective, criteria, boundary, route/preflight, source/toolkit/schema conditions are digest-bound: [bin/review_round.py:1919–1924](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1919-L1924), [bin/review_round.py:1980–2025](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1980-L2025); [tests/test_review_conditions.py:39–98](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_review_conditions.py#L39-L98). | Partial. Changed-basis full review is preserved. No demonstrated mechanism delivers all prior findings/rebuttals as fenced residual data to the fresh roster. |
| C21 | Fixed required families all participate in admission: [skills/triad-cross-family-review/SKILL.md:100–108](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/skills/triad-cross-family-review/SKILL.md#L100-L108). | Partial. Arbitrary added/informational legs do not yet have the common roster and equal blocker-accounting machinery. Fixed four-leg workspace operation does not prove it. |
| C22 | Current model/effort/timeout invocations are explicit: [skills/triad-cross-family-review/references/reviewer-routing.md:9–24](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/skills/triad-cross-family-review/references/reviewer-routing.md#L9-L24). | Partial. No common roster-to-invocation mapping for every selectable leg; Gemini Auto remains, and the defaults are host-local. |
| C23 | Paired Google preflight custody tested: [tests/test_four_leg_custody.py:41](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_four_leg_custody.py#L41). | Partial. Same-family legs lack the full common wire identity/attempt/route and demonstrated independent bound read-evidence records. One family field is insufficient. |
| C24 | Separate release results: macOS 1,201 passed; Ubuntu 24.04 1,199 passed, two existing filesystem skips. [Executed release evidence](../spikes/2026-09-20-b-release-0555.md#verification). | Release suites verified separately. Full install/authenticated preflight/dispatch/collection matrix on both platforms is not certified. |
| C25 | Raw custom prompt/model/optional-schema routes remain; raw Gemini omits formal policy and AGY preserves its research behavior: [tests/test_provider_wrappers.py:1368](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_provider_wrappers.py#L1368), [tests/test_review_no_web.py:119–142](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/tests/test_review_no_web.py#L119-L142). | Preserved raw capabilities, partial common INVESTIGATION conformance. No uniform authorization/extra-read-root/perspective record bound to each actual call; C29 remains absent. No new mandatory investigation envelope was imposed. |
| C26 | Link-string fingerprint plus TASK-supplied link evidence and reviewer no-follow instruction: [bin/review_round.py:1549–1578](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1549-L1578), [bin/review_round.py:2214–2219](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L2214-L2219). | Implemented bounded guarded-worktree route. Prepared-directory link refusal remains. Evidence is leader-prepared and behavior is prompt-controlled; no new automatic collector or OS containment is claimed. |
| C27 | Frozen executable/route selection plus observed Gemini version: [bin/review_round.py:1949](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1949), [bin/gemini_wrapper.py:183](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L183). | Local route/version custody implemented; this is not runtime model/principal proof or a complete shared receipt. |
| C28 | Loader and cwd validation reject relative paths: [bin/_common.py:479–521](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L479-L521). | Not implemented. The agreement requires process-cwd resolution, preserved validation and resolved-path records. D-B2 covers redaction/evidence semantics; refusal is not equivalent behavior. |
| C29 | Ordinary audit truncates `prompt_head` and can redact prompt/cwd data: [bin/_common.py:2004–2039](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L2004-L2039). | Not implemented. No explicit authorized-web trigger, shared clause appended last, exact sent-prompt custody or fetched-page evidence chain. Raw web capability alone does not satisfy this. D-B2 open. |

Case inputs, expected results, rule anchors and summaries on the authoring branch
were compared with fetched main and are unchanged; only host test/status mappings
were updated earlier. This is evidence against silently weakening the cases,
not proof of their execution. Shared schema prerequisites are explicitly listed
at [contracts/README.md:7–12](https://github.com/codefoundry-io/triad-dispatch-spec/blob/2eb883fee59e66556ee7c7f87189b38231136622/contracts/README.md#L7-L12).

## What changed in the implementation approach

| Area | Chosen B mechanism / preserved feature | Contract meaning |
|---|---|---|
| Terminal supervision | Reused the existing supervisor; bounded reader/writer reconciliation and owned-group cleanup. Rejected an unbounded join or “stdout succeeded, ignore stderr” shortcut. | Internal correction toward C1/C2, not a new contract. |
| Cleanup | Allocation record, verified evidence export and resumable claim. Kept age floor and foreign-root refusal. | C4/C5/C7 implementation choice. No shared receipt schema was invented. |
| Review binding | Extended the existing digest with actual review conditions and toolkit bytes. Kept capture plus final fingerprint verification; did not add redundant render-time recapture. | C14/C20 local correction; no claim of complete v2 or prior-finding delivery. |
| C26 | Reused guarded worktree, TASK and renderer with visible link text; prepared copying still refuses unsafe links. | Host-local mechanism allowed by the agreement. Manual evidence and prompt-only controls are explicit limits. |
| AGY REVIEW web | Added `read_url(*)` to a **deny** list; omitted formal autoapproval while keeping raw investigation behavior. | “Drop read_url from builder” is misleading for B's deny-list builder. The implementation matches removal of web capability, not deletion of a deny. The existing [wording clarification](../spikes/2026-09-20-b-review-no-web.md#non-blocking-residuals-and-shared-wording-clarification) awaits shared reference correction. |
| Native/subprocess symmetry | Native Codex remains native; Claude remains subprocess. Dormant AGY hook was not activated. | Preserved host exception; no Codex exec leg added for visual symmetry. |
| Schema/adoption | Kept current v1 schema and host-local prompt implementation; did not manufacture rev-2 files or a `SPEC_REVISION`. | Transparent incompleteness, not completion by an alternative mechanism. |

The audit does not establish that every historical guard is necessary forever.
It establishes which current controls were preserved and which bounded fixes
have evidence. No claim of OS confinement follows from a prompt or digest.

## Actual design decisions still pending

1. **D-B1 — Gemini policy composition.** The current shared exact payload and B's
   canonical search/catch-all/Plan-transition controls are not identical.
   The [existing proposal](host-b-gemini-policy-composition-proposal.md) recommends
   an exact shared payload plus an enumerated B supplement; the alternative is
   one strengthened common file. Neither is implemented or accepted. B is not
   “stronger overall”: its current web allow is precisely the C15 gap.
   Combining the shared deny at 200 with B's unchanged allow at 999 would retain
   web access and is not a valid fix.
2. **D-B2 — exact evidence versus hardened audit masking.** The
   [existing proposal](host-b-evidence-custody-proposal.md) retains ordinary
   masking and uses an explicitly authorized private evidence destination for
   exact investigation bytes. Relative-path support must not require turning
   hardening off. This is proposed semantics, not a delivered C28/C29 fix.

These two decisions are not the whole backlog. C8 token alignment, C18 model
migration, C19 retry policy, the shared-v2 files and consumers, C20 residual
delivery, vendored prompt/contract adoption and live verification remain.
The desired behavior is already settled for many of them; they do not require
asking the owner again whether N legs, Pro/HIGH, full re-review after edits or
investigation web are wanted.

There is also an explicit operating-policy discrepancy: the shared
[reference/review-rules.md:163–172](https://github.com/codefoundry-io/triad-dispatch-spec/blob/2eb883fee59e66556ee7c7f87189b38231136622/reference/review-rules.md#L163-L172) retires Flash as a reviewer, while the
owner-workspace formal exception used for this B release requires Pro and Flash
as separate Google legs. The release correctly reports all four participants;
that local exception is not evidence of shared roster parity and should not be
copied into A as a common default.

## Claude handoff: current source pairs, not a mechanical port

A's source paths are from its `codefoundry-io/triad` source repository, not the
flattened plugin export. Preserve A's own adapters and worktree lifecycle.
Each row names the current difference, the smallest investigation/correction,
and a feature that must survive. Reproduce before changing A.

| Priority / topic | B evidence | A evidence and requested follow-up |
|---|---|---|
| High — terminal reader outcome and partial setup, C1/C2 | [bin/_common.py:1226–1244](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1226-L1244), [bin/_common.py:1418–1513](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1418-L1513) | [3rd-Agent/wrappers/_common.py:1954–1970](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1954-L1970), [3rd-Agent/wrappers/_common.py:2177–2277](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L2177-L2277): reader errors are logged without a returned outcome; thread start precedes the protected wait. Extend A's existing boundary and test valid stdout/corrupt stderr, held pipe and partial thread-start failure. Preserve saved PGID cleanup and tolerant newline-only NDJSON parsing. |
| High — export before cleanup, C4/C5/C7 | [bin/review_round.py:1240–1351](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1240-L1351) | [.claude/skills/triad-cross-family-review/lib/review_scratch.py:936–1082](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L936-L1082): warning about a packet without a worktree is followed by claim/rename/deletion without verified durable export. Add allocation-bound recovery and export proof. Preserve registered-worktree checks, delivery hashes, symlink fences and no-force removal at [.claude/skills/triad-cross-family-review/lib/review_scratch.py:3660–3868](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L3660-L3868). Do not port B's temp-root layout. |
| High — original JSON ambiguity, C14 | [bin/claude_wrapper.py:185–192](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/claude_wrapper.py#L185-L192), [bin/antigravity_wrapper.py:327–341](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/antigravity_wrapper.py#L327-L341) | [3rd-Agent/wrappers/_common.py:1590–1600](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1590-L1600), [3rd-Agent/wrappers/_common.py:1873–1885](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1873-L1885), [.claude/skills/triad-cross-family-review/lib/validate_verdict.py:304–320](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/validate_verdict.py#L304-L320): ordinary parse/normalize paths can lose duplicate members before validation. Add checks at the first lossy boundary, including valid nested and escaped duplicate names. Preserve existing raw `--admit` defense at [.claude/skills/triad-cross-family-review/lib/validate_verdict.py:409–441](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/validate_verdict.py#L409-L441). |
| High — REVIEW still enables Codex web, C15 | [bin/review_round.py:63–91](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L63-L91), [bin/review_round.py:2037–2046](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L2037-L2046) | [.claude/skills/triad-cross-family-review/SKILL.md:474–490](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/SKILL.md#L474-L490), [.claude/skills/triad-cross-family-review/references/leg-contracts.md:1046–1055](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/references/leg-contracts.md#L1046-L1055): formal instructions explicitly pass `--search`. Remove it from REVIEW construction/text and verify rendered argv. Preserve investigation search: [3rd-Agent/wrappers/codex_wrapper.py:365–380](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/codex_wrapper.py#L365-L380). A's AGY read-only adapter already uses `skip_permissions=False` at [3rd-Agent/wrappers/antigravity_wrapper.py:1203–1223](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/antigravity_wrapper.py#L1203-L1223); do not copy B's project/deny machinery for symmetry. |
| Medium — condition coverage, C20 | [bin/review_round.py:1919–1924](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1919-L1924), [bin/review_round.py:2008–2024](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L2008-L2024) | [.claude/skills/triad-cross-family-review/lib/review_scratch.py:4396–4425](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L4396-L4425): existing artifacts/metadata are hashed before family bodies are rendered. Test which actual rule/schema/render inputs are missing, then extend the current delivery record only for those. Do not claim every A criterion is unbound. |
| Medium — Gemini version/capability custody, C16/C27 | [bin/gemini_wrapper.py:142–205](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/gemini_wrapper.py#L142-L205), [bin/review_round.py:436–455](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L436-L455) | [3rd-Agent/wrappers/gemini_wrapper.py:158–192](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/gemini_wrapper.py#L158-L192) goes from binary resolution to dispatch without the B-style version/help preflight. Add A-native provider-free floor/capability evidence, preserving raw/optional-schema behavior. Do not copy B's Auto selection, receipt schema or policy shape as the common target. |
| Medium — visible link review, C26 | [bin/review_round.py:1549–1578](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L1549-L1578), [bin/review_round.py:2214–2219](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/review_round.py#L2214-L2219) | [.claude/skills/triad-cross-family-review/lib/review_scratch.py:1780–1813](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L1780-L1813) refuses untracked links. Adapt visible link-text review with tracked/staged/unstaged/deleted/dangling/ancestor cases before relaxing refusal. Retain no-follow copying and cleanup. B's fingerprint alone is not reviewer visibility. |
| Joint pending — paths and web evidence, C28/C29 | [bin/_common.py:479–521](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L479-L521), [bin/_common.py:2004–2039](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L2004-L2039) | [3rd-Agent/wrappers/_common.py:1148–1190](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1148-L1190) also rejects relative paths. A is ahead on the explicit web trigger and clause-last append at [3rd-Agent/wrappers/antigravity_wrapper.py:1381–1393](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/antigravity_wrapper.py#L1381-L1393); its hardened audit still removes exact text at [3rd-Agent/wrappers/_common.py:2646–2659](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L2646-L2659). Preserve the working append and resolve D-B2 jointly. |
| No A port — C6 and stdin phase exits | [bin/antigravity_wrapper.py:666–697](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/antigravity_wrapper.py#L666-L697), [bin/_common.py:1329–1340](https://github.com/codefoundry-io/triad-codex-dispatch/blob/bde3f77301af60c5d13d7fd14f2ed3ed1e8f26dd/bin/_common.py#L1329-L1340) | A already retains prior stream/stderr/read audit on guard failure at [3rd-Agent/wrappers/antigravity_wrapper.py:1241–1265](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/antigravity_wrapper.py#L1241-L1265) and has correct pre-spawn `input-delivery-failed` / exit 3 at [3rd-Agent/wrappers/_common.py:2096–2121](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L2096-L2121). Add any missing C6 release-failure regression, not a rewrite. Preserve the existing [rejected stdin finding](../spikes/2026-09-20-a-stdin-phase-exit.md); it was a source-attribution mistake, not an A defect. |

B is a source of tested corrections, **not** a normative template for all A
behavior. In particular, do not copy B's current Gemini web allow, Auto routing,
relative-path refusal, incomplete common wire or all-leg retry rule as parity
requirements.

## Evidence, remaining verification and next implementation boundary

The [release record](../spikes/2026-09-20-b-release-0555.md) contains prior executed
suite, four-leg admission, archive/cache equality, installed lifecycle and
fresh-process discovery evidence. Its formal SAFE result applies to the reviewed
bounded B changes and existing release criteria; it does not close the entire
case table above.

No new test run or provider run occurred for this documentation audit.
V1–V5 remain NOT RUN; model-written claims cannot replace their required runtime
attribution. A new C15 composition candidate needs its own effective-policy tests,
not a reused single-file result. Both hosts still need the revision adoption
record, exact vendored bytes/digests and the checks for their claimed revision.
The proposed shared `spec-check` and digest checker are also explicitly not yet
implemented in [reference/spec-authoring.md:65–69](https://github.com/codefoundry-io/triad-dispatch-spec/blob/2eb883fee59e66556ee7c7f87189b38231136622/reference/spec-authoring.md#L65-L69) at the remote-main basis.

Suggested continuation order, not authorization to bypass unresolved design:

1. Resolve D-B1/D-B2 at a shared commit; keep agreed outcomes unchanged.
2. Implement independent rev-1 gaps in bounded slices with existing gates:
   token mapping, Google Pro/HIGH dispatch, C28/C29 and residual-data delivery.
3. Produce the agreed rev-2 schemas, then migrate roster, wire, receipts,
   same-family identity and retry together with all prompt pins.
4. Reconcile the public retry/roster policy with the owner-workspace exception
   before claiming common behavior; retain current authority until then.
5. Run the applicable shared cases and platform/runtime checks, adopt the
   revision explicitly, and only then claim that revision's conformance.

### Message to Claude leader

Read this document at its published commit, fetch current shared main, and
record both SHAs. Review the source-paired handoff against your current A source
before modifying it. Confirm which findings reproduce, reject unsupported ones
with exact source evidence, and preserve the listed A-specific guards. Do not
treat B's release as whole-contract completion or D-B1/D-B2 as accepted decisions.
For a common design/contract/prompt change, record evidence/version, current and
proposed behavior, impact on both hosts, preserved features and verification in
the shared repository, and request review of that same commit. Keep the shared
expected outcomes intact; implementation and adoption remain distinct.

</details>
