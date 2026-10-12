# B REVIEW web separation and preserved AGY concurrency

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](../decisions/owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

Status: source `900ddc5` passed complete corrected round `triad-b-p5-web-r2`;
all four SAFE, matched integrity and ADMITTED_SAFE. [B PR 32](https://github.com/codefoundry-io/triad-codex-dispatch/pull/32).
No installation, shared revision adoption or deployment claim.
PR 32 merged after Analyze (python)/CodeQL passed; B live remote main and the
development checkout matched `14daa4da3755db5d5a70f203deb6b94bb5233e1b`.
Shared remote main refreshed before source change:
`2eb883fee59e66556ee7c7f87189b38231136622`.
B baseline `71388383de307fbccdf593f913bc36d562ee2e41` after the C16/C27 version fix.

## Basis and bounded implementation

R-CONTAIN already requires all-family REVIEW no-web and forbids a permissive
bypass on review. Original claude-05/codex-06/codex-08 identified positive web
allowances and missing AGY operation-level restrictions. The earlier D-B3 note
described current compatibility behavior to investigate; it does not require
preserving the flag on formal review against the settled common rule.

The current slice removes positive web allowances, adds one common no-web
sentence to prepared/guarded renderers, and keeps local read/search tools.
AGY reuses `selected_context` for formal bindings or preflight. It adds
`read_url(*)` to the five raw read-only denies, validates the same six rules in
an explicit owner-provisioned project, and omits headless autoapproval only for
formal dispatch. No owner project record is changed by this validation.

The source review found another affected consumer: `_shareable_deny` accepted
only the raw five-rule list. A naive sixth deny would serialize Pro/Flash and
risk a sibling's 30-second lock timeout. Recognize exactly the two known ordered
lists while retaining existing deny-key equality. Same formal lists share;
raw/formal mixes wait/refuse. Holder liveness, crash recovery and restoration
remain unchanged. No generic policy sharing framework is introduced.

Official sources: [headless permissions](https://antigravity.google/docs/cli/headless/)
and [permission rules](https://www.antigravity.google/docs/permissions?tab=cli).
These describe all-request autoapproval and explicit deny precedence separately,
but do not expressly attest their interaction in installed 1.2.7. Repeated current
Pro/Flash review success with env optout supports bounded compatibility. The new
formal invocation omits the flag directly; do not infer universal runtime tool
enforcement from a flag, source test or preflight alone.

## Preserved features and limits

Raw permissive/read-only calls retain their version/env-based headless adaptation,
five-rule web-compatible posture, prompts and optional schemas. Authorized
INVESTIGATION remains separate. No Codex subprocess, dormant AGY hook, A agent
setup, settings-default change, schema migration or shared revision adoption.

Gemini's existing policy bytes and named local read/documentation surface remain
unchanged pending D-B1. Every REVIEW prompt forbids Gemini web, but the current
policy still permits its web tools. Docs state that limitation explicitly; this
slice does not claim mechanical Gemini web denial or complete C15/V1–V5 evidence.
D-B2 exact investigation-prompt/fetch custody remains unresolved and unimplemented.

## A source comparison and handoff

A remains read-only at `92c8afd500499d8736afcc28b39a87a4f87fed50`. Its AGY wrapper
defines local REVIEW and web-capable RESEARCH tools at
`3rd-Agent/wrappers/antigravity_wrapper.py:268-283`, selects the agent at
`:1194-1197`, and passes `skip_permissions=False` on read-only at `:1214-1216`.
Permissive compatibility and an empty-rule exclusive guard are separate at
`:1228-1239`. Read-only does not enter B-style shared settings leases, so A needs
no mechanical port of the six-rule concurrency adaptation. Preserve its `--web`
validation and clause-last behavior at `:1381-1393`.

A's Codex wrapper defaults search off (`codex_wrapper.py:143-148,374-380`), but
its REVIEW invocation explicitly turns it on:
`.claude/skills/triad-cross-family-review/SKILL.md:474-490`,
`references/leg-contracts.md:967-972,1046-1055`, and
`lib/review_scratch.py:3076-3079`. When A resumes, remove that REVIEW switch and
contrary skill text, retaining raw investigation search. Do not claim all A
routes already comply merely because AGY's active review agent has local tools.

Claude leader: refresh remote main, review this containing authoring commit at
the owner-designated B completion handoff, compare the exact paths above, and
provide A's own test/gate evidence. B does not edit or attest A implementation.

## Verification status

Fresh dedicated Terra/high RED: 18 intended failures, 35 controls passed;
source unchanged and exact owned fixtures absent. After the bounded patch,
leader related regressions: 307 passed. Fresh GREEN, full macOS/Ubuntu and
all-required-leg review are pending; record terminal evidence before closure.

The first full GREEN exposed two stale documentation-contract expectations on
both platforms (macOS 1189 passed/2 failed; Ubuntu 1187 passed/2 failed/2 existing
filesystem skips). The runtime-focused 53 checks passed. A source search also
found old web/autoapproval guidance in the standalone AGY skill and five-rule
project guidance in the shipped consumer example. Preserve the failed receipts;
do not count that run as GREEN. A fresh instruction-contract RED observed both
intended failures with unchanged source and exact fixture cleanup. The correction
aligns these related documents and their contract tests with the same formal/raw
split; it introduces no new provider behavior. Leader doc contracts: 42 passed.
Final fresh GREEN and all-leg review remain pending.

## First implementation review findings

`triad-b-p5-web-r1` is not approved: fresh Codex found two current omissions,
independently verified by the leader while the remaining reviewer finishes.
At `bin/antigravity_wrapper.py:464-488`, the preflight branch validates the review
ID but misses the dispatch branch's read-only requirement; without the flag,
`:579-624` enters an empty-rule guard and emits a receipt. The bounded correction
is argument rejection before probing/guard entry, with a Pro/Flash regression.
`migration/AGENTS.recommended.md:43-48` still describes autoapproval generically;
align it with the formal/raw split and cover that consumer guidance explicitly.
These are missing enforcement/documentation within the approved behavior, not
a new policy or schema design. Complete every current leg, preserve the NOT-SAFE
round, then use fresh RED/GREEN and a complete fresh review ID after correction.

A comparison remains `92c8afd500499d8736afcc28b39a87a4f87fed50`: A's AGY parser
(`3rd-Agent/wrappers/antigravity_wrapper.py:1295-1325`) has no B-style
`--preflight-only` receipt route, so this exact missing preflight guard is B-only.
A's read-only dispatch still passes `skip_permissions=False` at `:1214-1216`;
its leg contract states the danger flag is absent at
`.claude/skills/triad-cross-family-review/references/leg-contracts.md:640-642`.
Do not mechanically port B's guard or its stale consumer text correction to A.

The first implementation round finished with Claude/Codex NOT-SAFE and both
Google legs SAFE; its final integrity matched and the ledger retained
ADMITTED_NOT_SAFE. All evidence was exported and hash-verified before exact
owned cleanup. The common consumer finding was independently reproduced once.
The missing preflight guard and consumer guidance produced fresh RED (3 intended
failures, 4 controls passed). The minimal patch now rejects missing read-only
preflight arguments and aligns the consumer instructions. Other verified minor
corrections clarify existing local-only documentation reads, raw-only headless
adaptation, and the command-builder test's name. Leader focused tests: 62 passed;
fresh full verification and complete r2 review remain pending.

One reviewer inferred that `search_web` is necessarily outside AGY's read_url
enforcement. The leader did not adopt that inference: the official permission
reference describes domain matching and read_url_content, but does not establish
the installed search_web mapping. SECURITY now states the evidence limit without
claiming either a demonstrated bypass or complete mechanical web denial. This
does not change shared contracts, permission rules, runtime defaults or A code.

The final correction verification includes the existing consumer-specific
`tests/test_migration_contract.py` instead of duplicating that contract in a
second test file. Its obsolete expectation was caught by the full suite and
retained as a failed run before correction. Final fresh Terra/high GREEN:
101 focused, 1194 full macOS (220.33s); both skill validators and provider-free
lifecycle passed, source identity unchanged, pytest fixture and all four lifecycle
roots absent. Ubuntu 24.04: 1192 passed, 2 existing filesystem skips (121.36s),
read-only source/rootfs with network disabled. Source fingerprint:
`4baac9341fed9eea0538f3b4bef8ec2e794ddd34b3baad11ad12b62b4859feba`.
Fresh complete round `triad-b-p5-web-r2` finished with Claude opus/xhigh, AGY
Pro/high, AGY Flash/high and fresh native Terra/xhigh all SAFE, no open questions.
Digest `30f7812c46c46e2409652cda624f8fd016baa76f54e420ff3104d86a9c809610`;
final integrity matched. All results were retained, custody export hashes verified
and the exact three owned review roots removed. No R1 approval was carried forward.

The measured Python delta is 38 additions / 27 deletions / +11 across the three
existing modules, including comments. No new runtime module or abstraction was
added. A's five cited source files were also checked clean at the stated commit;
the line comparisons are not inferred from HEAD alone.

## Non-blocking residuals and shared wording clarification

Claude retained two Minor suggestions. The leader confirmed the raw-project
five-rule integration-test coverage gap while tracing the current raw boolean,
subset check and separately tested raw builder to establish current correctness.
Keep that extra test as a follow-up. The get_internal_docs clause already permits
only approved local use and explicitly forbids external evidence; broader
disclosure/wording belongs with the pending D-B1 policy work. No reviewed bytes
changed after r2, consistent with unchanged Minor-only SAFE admission.

`reference/review-rules.md:97` and the old `units.json` description said to
"drop read_url" from B's builder. That builder emits deny rules, so removing its
deny would have the opposite effect. The settled outcome is REVIEW no-web:
B adds the deny for formal context. The implementation mapping now states the
actual behavior; the normative reference is not silently rewritten. Claude's
same-commit handoff should confirm this minimal reference clarification: replace
the obsolete builder description with "B adds read_url(*) to formal REVIEW's
deny list; raw investigations retain their existing permissions." No behavior or
new shared design is proposed by that correction.
