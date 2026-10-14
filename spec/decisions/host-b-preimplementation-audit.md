# Host B preimplementation audit and Claude handoff

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

Status: preimplementation functionality/design diagnosis; the owner directs Codex-first execution and a read-only A
comparison throughout. No functional patch is included; the concrete common-design conflicts below remain unresolved. This document
does not extend the old agreement's signatures, claim revision adoption, or authorize a merge, tag or installation.

## 1. Verified basis and authorization

| Surface | Observed state |
|---|---|
| Latest shared remote main | `2eb883fee59e66556ee7c7f87189b38231136622`; fetched at entry, before the three-family review, and before this authoring proposal |
| Tags / accepted normative basis | Only `rev-0` exists; no `rev-1` tag. Both leaders acknowledged `bd506054` under `decisions/rev-1-agreement.md` |
| Codex development host B | `520caa9beb9f126838d25c7ff4d68528cc2d0eb0`, branch `codex/triad-release-0.2.554`, initially clean |
| B Git identity | Development checkout `workspace/triad-codex-dispatch-reliability`; Git common directory `workspace/triad-codex-dispatch/.git`, verified through Git metadata |
| Claude host A, comparison only | Initial `7a4082342c3d389c9d87f99df670e9d7755817e8`; refreshed `92c8afd500499d8736afcc28b39a87a4f87fed50` adds only A's feature-audit document; functional bytes unchanged. Unrelated untracked owner material preserved, not inspected |
| Owner's current request | Audit every existing function/case first; draft the common coordination rule; brief before changing functional code; implement B only after specification/start conditions are settled |
| Subsequent sequencing instruction | B develops and verifies first; inspect A's corresponding source and update line-based findings at every change; A stays unchanged until B's update handoff. A's implementation or reply is not a prerequisite for settled B work |
| Current runtime checks | Gemini policy V1–V5 still **NOT RUN**; common verdict, roster and receipt schemas still absent (rev-2 dependency) |
| Local tools | Python 3.12.13, pytest 9.0.3; AGY preflight 1.2.7, catalog-confirmed `gemini-3.1-pro-high` / `high`; Gemini installed 0.60.0 |
| Official version check | GitHub's latest Gemini release was [v0.60.0](https://github.com/google-gemini/gemini-cli/releases/tag/v0.60.0), published 2026-09-15; no CLI update performed |

`cases/cases.json` contains exactly C1–C29 at this basis. The short commitment table in the agreement is not the whole
implementation scope. Existing local plans are evidence of their original scope, not authority to overwrite later
shared decisions. In particular A's old parity plan §6 still mentions a generic `legs` command, forced test-tree moves,
and blocking cross-host drift; current `units.json`, R-PARITY and README adoption rule supersede those points.

## 2. Function and case mapping

All B paths below are relative to the pinned B checkout. A listed test is evidence of its actual covered behavior,
not proof that the entire shared case passes. The unchanged repository suite ran on macOS: **1,020 passed in 213.22s**.
Ubuntu 24.04 and new contract-specific regressions were not run. Historical rationale is explicitly UNKNOWN where it
could not be established. Existing S1–S11 plans refer to `docs/superpowers/` in B.

| Case | Current behavior / reason for retaining it | Spec requirement / gap | Source and existing tests | Disposition / regression risk |
|---|---|---|---|---|
| C1 | Byte-counted stdin, concurrent output drains, saved-group timeout/interruption cleanup; S1/S3 prevent truncation/backpressure and orphaned descendants | Normal success also needs completed error-free readers and group reconciliation | `bin/_common.py:1216,1336-1456`; `tests/test_stdin_transport.py`, `tests/test_provider_wrappers.py` descendant tests | PARTIAL. Extend terminal checks; preserve bounded cleanup and concurrent drains |
| C2 | Spawn errors produce failure; worker-thread setup after spawn is not enclosed by the same cleanup path | Partial reader/writer startup must terminate owned resources and preserve a terminal failure | `bin/_common.py:1336-1396`; existing spawn/interrupt tests do not cover thread-start failure | GAP. Reuse existing unwind, no new process supervisor |
| C3 | Fresh files survive count/byte cap pruning, including refreshed-stat checks; intentional concurrency protection | Preserve the age floor and no-follow checks | `bin/_common.py:2790-2838`; `test_run_log_count_cap_prunes_only_stale_files_and_allows_fresh_overflow`, byte-cap counterpart | PRESENT for existing covered axes; do not replace with oldest-first cap deletion |
| C4 | Exact/stale cleanup checks path shape, type, UID and age; reason this was sufficient ownership proof is UNKNOWN | Foreign/original content preserved; allocation provenance required | `bin/review_round.py:929-977,1059-1083`; `test_cleanup_rejects_foreign_uid_managed_root`, `test_prepare_sweeps_partial_roots_by_root_mtime` | GAP. Existing tests also encode deletion without provenance |
| C5 | Partial cleanup has no independent allocation claim | Resume only when ownership remains provable | `bin/review_round.py:1059-1083`; no complete resume/provenance case | GAP. Share C4's bounded ownership evidence, retain uncertain legacy residue |
| C6 | AGY restoration errors fail, but return before completed raw output is persisted; guard itself preserves owner settings | Failure stays failure and captured transcript survives guard release failure | `bin/antigravity_wrapper.py:634-667`, `bin/_agy_settings.py:430-507`; `tests/test_agy_settings.py` | GAP. Preserve raw result before release without making advisory logging authoritative |
| C7 | Missing-root cleanup is a no-op; no verified-export precondition | Verify exported evidence before disposal, including failed/stopped rounds | `bin/review_round.py:1059-1083`; `test_cleanup_removes_only_the_exact_review_root` | PARTIAL. Add closure evidence without a daemon or global registry |
| C8 | Shared map and fallback exist; local membership assertion is vacuous; direct `route-mismatch` and stdin behavior differ | Inventory emitted tokens, direct exits and compatibility aliases against common table | `bin/_common.py:69-88,2205-2227`, `bin/antigravity_wrapper.py:314-320`; no complete contract-membership test | GAP. Retain intentional aliases; do not silently remap existing exits |
| C9 | Route/preflight and audit receipts already carry useful but different facts | Common transport vocabulary awaits `receipt-fields.json` | `bin/_common.py:1891-1987`, `bin/review_round.py:200-257` | DEFERRED rev-2. Preserve existing receipts; do not invent a B schema |
| C10 | Durable audit and detailed failure IPC have different custody/retention purposes | Common field conformance cannot be tested before receipt schema exists | `bin/_common.py:1891-1987,2634-2787`; `tests/test_claude_receipt.py`, `tests/test_log_cleanup.py` | DEFERRED rev-2. Do not collapse both logs or turn audit failure into provider failure |
| C11 | Shared loader/interpreter scrub plus route-specific credential/selector removal; PATH/auth continuity intentional | Preserve effective sets and approved authentication boundary | `bin/_common.py:1190-1213`, `bin/gemini_wrapper.py:40-51`, `bin/antigravity_wrapper.py:33-45`; formal env tests and diagnostic fake | PRESENT for existing sets; no basis for an empty-environment rewrite. Whole future shared vocabulary not claimed |
| C12 | Fixed three-family instructions and special paired Google path; no general roster loader | Resolve default/override/unknown keys before dispatch; print every selected leg; unselected legs never start | `bin/review_round.py:2004+`, skill and `references/reviewer-routing.md`; selector/paired-custody tests | GAP, loader schema deferred rev-2. Thin adapters, no new orchestration framework |
| C13 | SAFE excludes blockers/open questions; Minor-only NOT-SAFE is rejected | Shared unchanged-byte Minor-only release and deviation record | `bin/verdict_schema.py:139-153`; `test_safe_accepts_minor_finding`, `test_not_safe_requires_blocker_or_open_question` | PARTIAL, semantic/wire migration deferred rev-2; preserve open-question blocking |
| C14 | Raw result-file duplicate guard plus review/family/digest binding; S11 deliberately excluded earlier provider parsing | Reject duplicate members before first lossy parse; add leg/attempt/route only with v2 | `bin/_common.py:873-883`, `bin/verdict_schema.py:212-225`; `test_raw_file_rejects_duplicate_members_before_semantic_validation` | PARTIAL. Wrapper duplicate gap reproduced; v2 identity deferred |
| C15 | B Gemini exact 999/998 allow/deny validator, AGY deny transaction/project guard, review renderers permitting web | REVIEW has no web across all routes; shared bytes conflict with B's stricter current shape | `bin/gemini_wrapper.py:56-121`, `bin/policies/gemini-formal-readonly.toml`, `bin/_agy_settings.py:34-43`, `bin/review_round.py:62-89,1771-1776` | GAP plus shared design question D-B1 below. Preserve investigations and project route |
| C16 | Gemini provider-free help/policy check; no explicit version-floor check; requested auth class is not runtime identity proof | Check >=0.34.0 and capabilities; do not invent verified account identity | `bin/gemini_wrapper.py:142-190`; `test_gemini_formal_preflight_is_provider_free_and_scrubs_competing_auth` | PARTIAL. Add observed version/refusal tests; authentication evidence remains limited |
| C17 | Formal Gemini removes keys, ADC, Vertex, endpoints and competing model selectors | Preserve approved account/auth class without reading credentials | `bin/gemini_wrapper.py:45-54,385-396`; formal preflight/dispatch env tests | PRESENT for tested removals; scrub alone never proves actual OAuth principal |
| C18 | AGY Pro-high/high is catalog-checked; Gemini hardcodes Auto | Roster-supplied route-valid Pro + verifiable HIGH; explicit future-model evaluation | `bin/antigravity_wrapper.py:29-33`, `bin/gemini_wrapper.py:364-383`; AGY preflight tests | GAP, data-driven defaults depend on roster work; no AGY slug copied into Gemini |
| C19 | Failed-round sibling findings retained as advisory, but fresh full roster required; original purpose was avoiding failed-round salvage | Retry only failed leg when all inputs/conditions unchanged; record attempt | `references/convergence.md:59-81`; distribution contract tests freeze current wording | GAP. Keep current historical results; change public retry and formal workspace policy separately |
| C20 | Changed code requires full fresh round; guarded renderer binds criteria/custody; prepared renderer does not bind all conditions | Changed prompts/criteria/roster/model/effort/route/policy require new basis; prior findings fenced as data | `bin/review_round.py:1651-1665,1752-1764,1880-1915`; digest tests in `tests/test_review_round.py` | PARTIAL. Prepared-condition replay gap verified; retain both basis modes |
| C21 | All fixed-family blockers/open questions matter; no arbitrary informational roster entry | Every participating leg's blocker matters regardless of label | `bin/verdict_schema.py:139-153`, skill result boundary | PARTIAL; arbitrary-leg accounting deferred with roster, no vote or exemption |
| C22 | Claude/AGY explicit model and effort forwarded; native Codex contract fixed; Gemini Auto | Each selected roster value reaches actual argv/native spawn and is adapter-validated | `bin/claude_wrapper.py:330-360`, AGY builder/preflight, `references/leg-contracts.md:286+` | PARTIAL. Preserve native Codex and formal one-call behavior |
| C23 | Paired Pro/Flash receipts bind one digest; result binds family only, not separate leg identity | Independent result/evidence identity for each same-family leg | `bin/review_round.py:1893-1919`; `tests/test_four_leg_custody.py` | PARTIAL, v2 identity deferred; dormant hook remains dormant |
| C24 | macOS baseline now executed; no Ubuntu evidence in this audit | macOS and Ubuntu 24.04 results kept separate for install/preflight/dispatch/collection/validation/cleanup | Full B suite above; platform source claims alone are not execution | macOS baseline PASS; Ubuntu 24.04 NOT RUN; no overall C24 conformance claim |
| C25 | Raw wrappers accept custom prompt, optional schema and model; AGY also effort, one cwd and web capability; perspective/extra authorized roots can be carried by caller prompt | Preserve selected investigations and authorized roots/web without verdict or roster accounting | raw branches in all wrappers; `test_gemini_route_keeps_native_json_without_review_protocol` | PRESENT but partial mechanical evidence. Missing dedicated flags do not prove the capability absent; no mandatory new investigation envelope |
| C26 | Guarded fingerprint binds untracked link text without reading target; prepared copy refuses symlinks; cleanup no-follow tests exist | Link text visible; target never implicitly inspected; coverage gap disclosed | `bin/review_round.py:710-746,1147-1149,1300-1307`; fingerprint and internal-symlink cleanup tests | PARTIAL reviewer-delivery/no-follow evidence. Preserve safe refusal; no mandatory materializer inferred from spec |
| C27 | B's auth-gated selector freezes executable/route; AGY preflight adds version/model; Gemini lacks observed version | Preserve shipped selection and no post-start fallback; freeze/version per attempt | `bin/review_round.py:1690+`; selector tests, AGY preflight tests | PARTIAL. Record Gemini version without changing fallback/auth semantics |
| C28 | Relative prompt/cwd rejected intentionally after wrong-cwd incidents; resolved prompt source is not in success receipt | Process-cwd resolution with all validations and auditable resolved candidate | `bin/_common.py:478-523`; wrapper nonempty guards; `tests/test_effective_cwd_receipt.py` | GAP; reconcile path visibility with hardened redaction (D-B2) |
| C29 | No explicit authorized web-investigation trigger/clause tail; ordinary success audit is capped/redactable; current AGY telemetry counts local views | Append shared clause LAST, record sent prompt, verify fetched URLs; never apply to REVIEW | `bin/_common.py:1934-1936,2634-2755`, raw wrappers, `prompts/investigation.md` | GAP plus custody question D-B2; view counts are not page-fetch evidence |

## 3. Findings reproduced by the leader

The leader used provider-free, disposable fixtures without changing product bytes:

- `_common.validate_response` accepted a verdict containing `NOT-SAFE` followed by duplicate `SAFE`, normalizing it to
  `SAFE`. The later raw-file check cannot recover discarded duplicate evidence.
- A local Python child wrote invalid UTF-8 and exited 0. `_drain` logged the decode exception, while `_run_once` returned
  `exit_code=0`, `vendor_exit_code=0`, `extraction_error=null`. This proves the transport gap; it is not a claim that an
  empty answer passes every downstream wrapper.
- A second local child emitted complete bound SAFE terminal JSON on stdout and invalid UTF-8 on stderr. The actual AGY
  interpretation returned `exit_code=0`, `classification=ok`, `verdict=SAFE`, `extraction_error=null` despite the reader
  exception. This refutes the claim that terminal extraction necessarily makes reader errors nonblocking; it is not a
  live-provider or formal-round admission claim.
- `cleanup_review_workspace` removed an owned disposable fixture representing a same-UID foreign root with no helper
  allocation/export evidence. Only that exact fixture was affected and its enclosing directory was removed afterwards.
- Feeding the byte-identical shared Gemini policy to B's current `_validate_formal_policy` produced
  `formal Gemini policy is not the exact fail-closed rule set`.

Additional source-verified facts: normal-success group/reader checks are absent; AGY guard release can return before
captured transcript persistence; prepared digest excludes changed objective/criteria/boundary/kind; the old S11 plan
explicitly limited duplicate coverage to raw result files. These are bounded gaps, not permission to rewrite the engine.

## 4. Independent review and leader adjudication

Three fresh native audits covered transport (Terra/high), lifecycle/overdesign (Astra/medium), and Google/investigation
(Terra/high), all with `fork_turns=none`. Runtime model/effort metadata was not exposed; requested settings are recorded.
Then Claude Opus/xhigh, Google AGY Pro-high/high and fresh Codex Terra/xhigh reviewed the same guarded basis with
review ID `host-b-start-audit-r1`, digest `5872fdd162e44ae04aef5c8785427a7513fcd6e74988abc51eecb2aff7be6572`.
All were instructed read-only and no-web; this is prompt-controlled containment, not an OS sandbox claim. Final integrity
and terminal results are recorded in the local receipt linked from the owner briefing, not inferred from a wait timeout.

All three completed: Claude **NOT-SAFE** (9 findings, 1 open question), Google **NOT-SAFE** (4 findings), fresh Codex
**NOT-SAFE** (12 findings, 1 open question). Packaged schema and binding validation passed for each. Before/after source
fingerprints matched `ad509a6c7183b20e6282a0bbb7e10551a602fe094ffb963385d84e8d5534143f`; custody and embedded shared
specification hashes also matched. Evidence was exported and hash-checked before exact owned temporary roots were
removed. Findings overlap and are not additive defect counts. This is completed diagnosis, not admission or proof of
runtime containment; the existing AGY flag in D-B3 was used and its enforcement still requires investigation.

| Claim or recommendation | Leader disposition and evidence |
|---|---|
| Cleanup ownership/export gap (Google, Codex, native audits) | ACCEPT gap. Path/UID/age is not allocation proof. A plausible marker alone is also insufficient; use evidence tied to the helper's allocation. Do not promise resistance to a malicious same-UID process without a threat-model change |
| Reader/normal-group completion gap (Google, Codex, transport audit) | ACCEPT gap. REJECT Google's unbounded `join()` correction: a surviving pipe holder can hang forever. Preserve deadlines and add explicit completion/error checks plus owned-group cleanup |
| Shared policy rejected by B validator (Google, Codex) | ACCEPT incompatibility. REJECT adopting the weaker shape just by relaxing validation: D-B1 must preserve current controls and exact shared payload obligations |
| Environment must be fully cleared under C25 (Google) | REJECT. C25 concerns investigations; C11 requires injection/route scrub, not an empty environment. `bin/_common.py:1190-1213` intentionally preserves PATH and authentication compatibility |
| An investigation envelope is mandatory because dedicated flags are absent (native audit) | REJECT necessity. The raw route is an existing capability; prompt-carried perspective/roots remain valid within authorization. Only the explicit C29 web trigger and missing evidence need design |
| Prepared route must automatically materialize symlinks (native audit) | NOT REQUIRED. R-PREPARE/units explicitly preserve B's copy refusal and guarded mode; improve link visibility and disclose coverage without silently following targets |
| v2 wire/roster gaps imply rev1 must implement new schemas now (possible broad reading) | REJECT. Record each gap, preserve existing schema until the common files land, then migrate all shape pins and validators together |
| Reader errors are Minor because incomplete terminal JSON cannot pass (Claude) | REJECT the general downgrade. The second leader fixture supplies complete stdout and corrupt stderr and reaches `ok` / `SAFE`; transport must independently account for both readers |
| Existing custody-looking files or a successful integrity check alone authorize cleanup (possible correction) | REJECT sufficiency. Plausible files do not prove allocation; unchanged input does not prove exported results. Failed rounds need preserved evidence too |
| AGY project route would miss a web-deny change made only to the transient builder (Claude) | ACCEPT. `bin/antigravity_wrapper.py:556-560` selects `agy_project_guard`; `bin/_agy_settings.py:80-86` validates existing owner setup. C15 must cover both paths without silently mutating that setup |
| AGY reserved LegVerdict accepts no expected binding triple (Claude) | ACCEPT bounded interface gap at `bin/antigravity_wrapper.py:436-487`; retain arbitrary raw schemas, but reject incomplete reserved review bindings before dispatch |
| Every renderer must immediately rehash a caller-supplied fingerprint (Claude, Minor) | Not required by current contract: `test_worktree_prompt_uses_captured_fingerprint_without_rehashing` deliberately pins the current capture/use protocol, followed by final integrity. Keep as a possible wasted-work diagnostic, not a mandatory extra pipeline |
| All B raw Google dispatch uses a packaged read-only policy (units wording) | CORRECT the inventory. Gemini's raw branch supplies no formal policy; AGY's read-only guard is a different route. C29 authorization must not be inferred merely from a policy filename |

### 4.1 Claude-host counterpart register for the Codex-first handoff

All A references below are source paths at `92c8afd500499d8736afcc28b39a87a4f87fed50`. Two fresh Terra/high children
performed the additional read-only comparison; the leader re-read the cited critical branches and corrected the
overbroad conclusions below. This is source evidence, not an A test run, a new three-family admission, or authorization
to change A. Refresh A's actual commit/lines when each B fix lands. A remains unchanged until the B completion handoff.

| B change / case | A current evidence and difference | A instruction to retain for the final handoff |
|---|---|---|
| Terminal completion / C1 | SAME gap: `3rd-Agent/wrappers/_common.py:1954-1970` logs but does not propagate reader errors; strict UTF-8 pipes at `2123-2135`; joins at `2234-2235`, rc-based success at `2250-2277` without drain completion checks | Port the bounded terminal contract and add invalid-stderr/valid-stdout plus held-pipe fixtures. Preserve tolerant NDJSON noise handling; that is a different question |
| Partial thread startup / C2 | SAME: `_common.py:2177-2202` starts threads before the cleanup-protected wait at `2204-2232` | Guard post-spawn partial setup. If changing `preexec_fn` to `start_new_session`, also change the saved-pgid predicate at `2157`; keep group cleanup proven |
| Completed transcript on guard failure / C6 | ALREADY IMPLEMENTED: `3rd-Agent/wrappers/antigravity_wrapper.py:1241-1265` preserves prior stream/stderr/read-audit; `1480-1528` routes it to persistence | Do not replace this with B's older behavior. Add a post-call release-failure regression if missing; existing stream-retention tests do not exercise that exception |
| Allocation/export and partial cleanup / C4/C5/C7 | SAME contract gaps, different fences: `.claude/skills/triad-cross-family-review/lib/review_scratch.py:668-705` has magic-marker validation, but `720-725` reclaims `.pruning` by shape; `996-1068` warns about unchecked records, then `1069-1082` deletes | Keep existing symlink/registered-worktree protections and claim-rename recovery. Add allocation-bound recovery and verified evidence export; never infer export from an integrity check alone |
| Original JSON duplicate rejection / C14 | SAME lexical gap: `3rd-Agent/wrappers/_common.py:1590-1600` accepts via Pydantic before failure-only duplicate probing; `.claude/skills/triad-cross-family-review/lib/validate_verdict.py:317` uses ordinary `json.loads` on the file route | Test an otherwise-valid duplicate verdict, not only duplicates plus another shape error; reject before the first lossy parse. Preserve A's separate raw-reply admission |
| Reserved-schema binding / C14 | DIFFERENT boundary: A's `review_scratch.py:3004-3013,3024-3039` prints external admission for wrapper legs; `validate_verdict.py:540-562,607-619,692-700` checks required/matching bindings | No mechanical port of B's expected-binding flags. Generic wrapper success is not A formal admission; preserve and verify the admission step |
| Complete condition binding / C20 | PARTIAL: A `review_scratch.py:4394-4422` hashes its brief and delivery artifacts, already binding brief context/questions; leg prompts are rendered afterwards at `4423-4425`, and external execution settings need condition coverage | Do not claim all A criteria are unbound or mandate a new metadata framework. Test each actual changed condition, then extend the existing delivery record only where necessary |
| REVIEW web / C15; A proposed C30 | AGY/Gemini controls differ, but not all A routes comply: `review_scratch.py:3076-3079` adds Codex `--search`; `.claude/skills/triad-cross-family-review/SKILL.md:475-490` defaults it ON. AGY local-tool clause at `review_scratch.py:1313-1329`; Gemini deny rows at `3rd-Agent/wrappers/policies/gemini-readonly.toml:80-92` | Remove search from A REVIEW invocation when A resumes; retain its investigation search option. A's proposed C30 is not yet in shared remote cases; carry it into shared case review instead of treating 29 cases as complete future coverage |
| AGY route containment / D-B3 | DIFFERENT: `antigravity_wrapper.py:1214-1223` explicitly uses `skip_permissions=False` on A read-only; `1228-1239` retains the historical adaptation only on its permissive path. No B-style `--project` route | Evaluate the proven A separation as a B option without blindly importing setup/hooks. Do not add B's flag or project guard to A for symmetry; retain A investigations |
| Gemini policy / D-B1 | DIFFERENT: A consumes shared priority 100/200 policy bytes; `3rd-Agent/wrappers/gemini_wrapper.py:131-180` does not enforce B's 999/998 exact-shape validator | A must assess any agreed shared policy revision and validator coverage independently; retaining the same current bytes does not prove V1–V5 |
| Relative paths and privacy / C28 | SAME migration gap: `3rd-Agent/wrappers/_common.py:1148-1190` refuses relative paths. Redaction at `2646-2659` is a feature to preserve, not evidence that C28 is implemented | Apply process-cwd resolution with all path/UTF-8/type/root checks; use the shared custody decision for resolved-path records |
| Investigation clause and sent prompt / C29 | PARTIAL, ahead of B: `antigravity_wrapper.py:1381-1393` validates the web route and appends the clause last; `tests/unit/wrappers/t49-agy-web-evidence-c29.sh:93-100` checks the full prompt in unredacted audit argv. `_common.py:2657-2659` removes that in hardened mode and caps prompt_head | Preserve the working explicit trigger and clause order. Extend hardened-mode evidence custody under D-B2; do not claim the existing successful unredacted test covers that mode |

The initial additional audits incorrectly equated hash-checked delivery with complete C26 link-review semantics,
absolute-path refusal with C28 completion, and the AGY/Gemini web controls with all-family C15 completion. Those
conclusions are rejected. A still refuses untracked symlinks (`review_scratch.py:1807-1808`); retain its no-follow and
delivery-integrity checks while separately designing visible link-text review and coverage disclosure. The A audit's
statement that Google is merely advisory also conflicts with the owner's all-participating-leg agreement rule; its
plan §6 must be corrected when A resumes, not used to weaken either host's gate.

## 5. Shared design questions to resolve before functional changes

These are concrete source/spec conflicts, not reopened owner choices about voting, web in REVIEW, native Codex,
authentication, Pro-high defaults or the number of legs.

**D-B1 — Shared policy bytes versus B's existing enforcement profile.** C15 requires the shared file byte-for-byte.
B's actual validator and policy require canonical `grep_search`, `get_internal_docs`, explicit Plan Mode transition
denies, and a catch-all at 998 below its 999 rules. The shared file lacks several of those controls and has different
priorities; its canonical-search/catch-all additions await V3/V5. Simply removing web from B's 999 list still fails byte
identity; copying the shared file both fails today's validator and changes the remaining enforcement profile.

Recommendation: preserve the stronger existing constraints until a common adoption design is agreed. First assess a
verified shared candidate under the existing V1–V5 manifest; if a host overlay is necessary, specify its exact ownership,
composition, digest and conformance semantics jointly before coding. Do not silently add an overlay, weaken B, or declare
V3/V5 green. This is a shared design decision for both leaders; surviving incompatible options go to the owner.

**D-B2 — Evidence custody versus existing redaction.** C28 requires resolved paths in successful audit rows; C29 requires
the prompt AS SENT. B intentionally redacts prompt-bearing argv/paths and text in hardened mode (`_audit_redact_enabled`,
`_redact_prompt_args`, `audit`) and caps the general `prompt_head` to 200 characters. Failure run-logs are separate,
temporary, and absent on success. A hash-only record does not satisfy the current C29 text; adding the complete prompt to
the general durable audit loses an existing privacy behavior.

Recommendation: define one explicit, authorized, bounded investigation-evidence location for exact sent bytes and fetch
records; keep ordinary durable audit redaction and point to the retained evidence under the agreed custody rule. Decide
how hardened path redaction satisfies C28. This proposal is not an implemented exception or permission to log more data.

**D-B3 — AGY headless compatibility fact.** R-CONTAIN says no permissive-route flag is on a review route. B actually
adds `--dangerously-skip-permissions` for AGY >=1.1.3 unless `AGY_NO_HEADLESS_AUTOAPPROVE=1`, including formal mode
(`antigravity_wrapper.py:109-140,628`). Its README/SECURITY explicitly describe this adaptation, and the 1.2.7 audit call
used it with plan/sandbox and the existing deny transaction. Thus the shared description of today's behavior is wrong.
The official [headless documentation](https://antigravity.google/docs/cli/headless/#permissions-in-headless-mode)
describes the flag as auto-approving tool requests; the fetched page is not version-pinned and does not prove the
precedence of B's explicit denies in 1.2.7. No observed mutation is claimed. Record the existing exception accurately and
verify a narrowly scoped replacement against current CLI behavior before removing a compatibility guard. No new bypass
or dormant-hook activation is proposed; any new review invocation must explicitly assess this route first.

Current B status: the settled formal/raw separation is implemented and reviewed
in `900ddc5`, round `triad-b-p5-web-r2` (all four SAFE). See
[the P5 spike](../spikes/2026-09-20-b-review-no-web.md) for source, compatibility
evidence and the remaining vendor-enforcement limits. The paragraph above is
the original observed baseline, not a requirement to retain formal autoapproval.

**D-B4 — Conditions, lifecycle and symlink delivery.** C20's complete review-condition binding and C4–C7's allocation/export
sequence need concrete host mechanisms. C26 currently proves fingerprint no-follow, not that all reviewer tools never
follow a link. Preserve existing guarded/prepared paths and fail-closed copy refusal; specify the smallest visible link
record and reviewer restriction, not a third review pipeline. These are adaptation designs for already-agreed behavior.

## 6. Minimal implementation sequence (proposal, not execution approval)

No functional patch is included. Reuse the existing S1–S11 designs as historical scope and regression evidence. New
implementation plans must include exact RED/GREEN cases after the shared questions are resolved. Each complete plan
gets its required multi-family review before the next functional plan; any reviewed-byte/condition change requires full-scope
re-review. Line figures below are estimates, not gates or permission requests.
P0 is an authoring-record step outside that functional sequence; delivery of its Claude review request is recorded
separately and does not block settled B work.

| Order / coherent outcome | Reused work / cases | Expected production additions / deletions / net; novel core | Verification and preserved constraints |
|---|---|---|---|
| P0: authoring and audit records only | Shared rule, B case/unit mappings | 0 / 0 / 0; 0 | Entry equality, links/anchors, JSON/TOML parse, unchanged policy digest; same-commit Claude review request prepared for relay, not a prerequisite for settled B work |
| P1: reliable terminal completion and captured failure | S1 process cleanup + S3 stdin; C1/C2/C6 | ~120 / 35 / +85; <120 | Thread-start/decode/held-pipe/normal-descendant/guard-release fixtures; preserve stdin backpressure, bounded waits, one provider call, advisory audit |
| P2: owned cleanup after evidence export | Existing lifecycle; C4/C5/C7 | ~140 / 40 / +100; <140 | Foreign/false-marker/partial/allocation/export-failure/idempotence fixtures; original dirty checkout and symlink targets survive |
| P3a: original-text result integrity | Extend S11 boundary; C14 lexical portion and reserved-schema binding | ~65 / 15 / +50; <65 | Raw duplicate fixtures before normalization, missing/partial reserved binding rejection; arbitrary raw schemas and legacy valid output retained; no v2 schema flip or repair loop |
| P3b: complete review-condition binding | Existing two renderers; C20 | ~55 / 25 / +30; <55 | Each objective/criterion/boundary/prompt/route/policy axis changes basis; all families share intended basis; prepared/guarded routes both retained |
| P4: mechanical relative paths | S5 effective-cwd receipt; C28 | ~65 / 25 / +40; <65 | Process cwd differs from child cwd; missing/directory/non-UTF8/empty/outside-root inputs; D-B2 custody agreement first |
| P5: operation-level web separation | Existing adapters and common clause; C15/C25/C29 | ~120 / 45 / +75; <120 | Formal and raw paths for both CLIs; AGY project and transient-guard paths; clause-last actual prompt + page-fetch evidence; D-B1–B3 first |
| P6: explicit emitted-token contract | Existing classification map; C8 | ~20 / 10 / +10; <20 | Membership and actual exits including wrapper-only/phase-specific exceptions; preserve supported aliases |
| Deferred: shared v2 wire/roster/receipts | C9/C10/C12/C13/C14 identity/C18/C19/C21/C22/C23/C27 receipts | Estimate after common schemas land | Strict schema + every prompt pin + adapters migrate atomically per host; no legacy evidence fabrication, no extra leader subprocess |

Tests are expected to dominate each patch (roughly 80–220 added lines per functional plan); narrative docs typically
20–60 lines. Record measured additions/deletions/net separately for production, tests/fixtures and docs, revising these
estimates where coherent scope needs it. A line increase alone does not stop work or promote a size class.

C3/C11/C17 and existing C25 behavior remain regression obligations, not rewrite tasks. C16/version checks fit the Google
preflight plan after its exact supported range is written. C24 is an obligation of every relevant plan: separate macOS
and Ubuntu 24.04 runs; a missing platform stays NOT RUN. Installed-skill behavior requires the dedicated fresh
Terra/high executor RED/GREEN, validator and relevant regression protocol; today's baseline is not that certification.

## 7. Claude leader handoff (relay the containing commit)

The owner has directed B to implement and verify first. A remains unchanged until B's development handoff. Read the
latest remote main first and state its SHA. This authoring proposal is on top of `2eb883f`; verify the containing
commit, not an earlier acknowledgement. Review `reference/spec-authoring.md#R-AUTHORING-SYNC` and its identical AGENTS/CLAUDE
entry pointers; the owner asked for one normative copy and same-commit cross-host sharing. Adopt only the pointer in
your own host instructions at the owner-designated A update point; Codex will not edit Claude-host files.

Review the full C1–C29 B mapping and D-B1–D-B4 against your current source. For each question return evidence/source
version → actual A/B behavior → smallest proposed behavior → both-host effect → features retained → exact verification.
In particular decide the Gemini policy composition without dropping B controls, reconcile exact investigation evidence
with hardened redaction, and correct the AGY current-route description only on verified CLI evidence. Do not treat a
shared-reference draft or a clean baseline suite as runtime conformance. V1–V5 and absent rev-2 schemas retain their
recorded state. Keep all owner-decided semantics and every existing justified feature, however small.

The operational three-family diagnosis is evidence for the leader discussion. B proceeds first under settled contracts;
A's implementation or acknowledgement is not a prerequisite for those B changes. B will inspect A's corresponding code
at every change and maintain commit/file/line findings and verification instructions for the final handoff. Resolve
actual contract conflicts before changing common behavior. Each host retains its own TDD and gates. No tag, merge,
publication or installation is implied.
