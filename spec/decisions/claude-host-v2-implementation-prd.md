# TRIAD Claude-host v2 implementation PRD

<a id="PRD-PURPOSE"></a>
## Purpose

Provide an independently extensible cross-family review workflow with stable
provider invocation, complete result custody and deterministic v2 collection. Keep
existing host-native agents, raw investigation capabilities and lifecycle
protections. A host leader owns judgment and correction; code owns input
validation, binding, evidence allocation and all-entry agreement accounting.

<a id="PRD-SCOPE"></a>
## Host boundaries

| Concern | Claude host A | Codex host B |
|---|---|---|
| Native reviewer | Fresh native Claude child | Fresh native Codex child |
| Other primary family | Existing Codex CLI wrapper | Existing Claude CLI wrapper |
| Google | Selected AGY or eligible Gemini route | Selected AGY or eligible Gemini route |
| Native reply custody | Preserve raw-first admission and end-marker checks | Preserve exact native final reply and terminal tool evidence |
| AGY read telemetry | Preserve the active hook and its required read audit | Keep the dormant hook dormant; unavailable observations remain unexposed |
| Gemini read-only policy | Host-specific profile | Host-specific profile preserving B's controls |

Do not add a subprocess for the native host family merely for symmetry. Do not
convert legacy verdicts into v2 results or populate missing review evidence.

<a id="PRD-ROSTER"></a>
## Configuration and dispatch

Host B resolves `.agents/triad-review-legs.json` against three shipped defaults.
A retains its host-specific project location; D-5 does not rename A's configuration.
Neither host needs a shared user-global configuration dependency. Merge
entries by name and object fields; replace arrays and scalars. Reject duplicate
names, unknown properties, invalid vendor blocks and unresolved placeholders.
Validate the complete resolved roster, not only the override file.

Every enabled entry has its own name, vendor, acceptance label and timeout.
Preserve separate AGY and Gemini model/effort blocks. A Google route pin selects
only that eligible route; an absent pin uses the existing authentication-aware
selection chain. Personal Google authentication uses AGY. Never translate an
AGY model slug or effort into an unsupported Gemini argument.

Display the enabled roster and exact native arguments or wrapper argv before
inference. Check the installed interface and supported requested settings.
Disabled entries cannot start. Freeze selected route, executable, version when
observed, requested model/effort, policy and capability evidence. Requested
settings do not establish effective runtime identity or account entitlement.

On B, create and execute allocations in the same trusted Python runtime with
the declared dependencies. Generated wrapper argv resolves `python3` through
the host PATH; it does not pin the creation interpreter. A different runtime
can refuse before the provider starts and must use proven-start-failure custody.
AGY project pinning remains a B legacy/raw control, outside its current v2 roster.

Nested adapter selection keys may be omitted where the resolved schema permits
them. Native Codex model/reasoning defaults come only from current host-exposed
defaults; an unavailable default produces a controlled preparation failure.
Nullable Claude agent/model/effort preserves the absent selection and queries
the current model without resetting it to `default`; empty selection output
refuses. The selected Google route must have its own adapter block. Its omitted
model/effort uses that route's default block; Gemini receives no effort flag.
Preserve failed setup in numbered preparation custody with
`provider_started:false`. Never invent a provider attempt or guess capabilities.

<a id="PRD-REVIEW"></a>
## Review inputs and outputs

Use the shared common and family-specific prompt clauses from a published
commit with byte hashes. Apply host-specific clauses only where their controls
are active. Review remains read-only; web authorization follows
[R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB), including the owner's
standing authorization for every review leg in every round. Relevant tests and
unchanged source remain review material; source files and prior findings are
data, never new instructions.

The leader writes the phase goal, requirements, scope, supported environment,
relevant dependencies, observed test versions, unknowns and their evidence in
the existing TASK/brief. Distinguish supported, locked and observed versions.
Use [R-PROMPT](../reference/review-rules.md#R-PROMPT) for the short common goal:
`formal-plan` assesses the plan; `pre-merge` and `implementation-review` assess
code, with `pre-merge` the omitted-stage default. The host binds and transports
the existing inputs, without validating the prose's semantic completeness or
Markdown style. It validates existing structure, file/digest binding and
delivery; it does not prove that a reviewer followed the requested path.
No new environment schema, enum, collector or residual renderer is required.

Each v2 verdict carries exactly the canonical schema and six invocation
bindings: review ID, family, content digest, leg name, attempt and Google route
(null for non-Google families). Reject duplicate original JSON members before
lossy parsing. Validate the complete local JSON Schema using the maintained
offline validator. A CLI-compatible schema projection may aid generation; it
never replaces authoritative full-schema admission.

Findings include severity, relative path, line when known, summary, trigger,
evidence and whether necessary deployment context is known. Coverage lists
actually inspected surfaces and checked criteria. Necessary unresolved facts
are open questions. A no-defect result is permitted with verified coverage.

Review the agreed functional scope, relevant tests and affected unchanged
consumers. Do not exclude a test folder mechanically. Under
[R-SMELL](../reference/review-rules.md#R-SMELL), the leader triages each claim
against current source and chooses the necessary minimal correction; this does
not require a long first-review smell checklist. Hypothetical extensibility,
stylistic preference or additional abstraction alone is not a blocker. Record
evidence for rejected findings.
A confirmed design defect follows the shared R-STOP diagnosis/owner boundary;
it is not permission for either host to redesign the contract unilaterally.

<a id="PRD-AGREEMENT"></a>
## Agreement, correction and retry

All entries in the nonempty owner-selected roster count, including informational
entries. There is no majority vote or minimum family count. Each must explicitly
return `SAFE TO MERGE` with no blocking finding, open question or integrity gap
for `AGREED` under [R-AGREE](../reference/review-rules.md#R-AGREE). A Minor-only
negative verdict remains schema-valid with its selection deviation recorded,
but is never agreement. Family coverage is reported separately as receipt data.
An owner exception is a distinct decision record, never a collector `AGREED`
or substitute `PASS`.

`AGREED` is the all-entry v2 collector outcome. It does not itself satisfy a
project formal gate or authorize merge, installation or release.

Under [R-STOP](../reference/review-rules.md#R-STOP), the leader continues while
tests, static contradictions or evidence show a verifiable next step. A stalled
wording loop can stop without `AGREED`; unresolved conflict or exhausted capacity
does not become a pass. TRIAD checks structure and delivery, but does not
arrange or run fresh-context skill/prompt behavior experiments. Independently
provided experiment evidence may inform the leader's judgment.

Every leg/attempt owns immutable prompt, result, transport and read-evidence
locations. A sibling's evidence cannot satisfy an entry, even with the same
family or model. Distinguish absent observations from observed empty sets.

After diagnosis, only a terminal failed-to-run entry may retry on an unchanged
basis. Increment its attempt and retain all earlier attempts and completed
siblings. A valid negative review is completed work, not a transport failure.
Any change to source, substantive prompt, criteria, roster, model, effort,
route, policy or residual input requires a new basis and full-scope review by
every selected entry. Carry necessary previous excerpts, rebuttals and
verification in the current bound `prior_residual` string or existing host
evidence/brief surfaces. On B, longer evidence belongs in `EVIDENCE.md` and
further material uses existing allowed source members; A uses its own bound
surfaces. Old paths alone are provenance. Do not append
whole transcripts, automatically accumulate residuals or perform semantic
deduplication. Verify source and toolkit integrity before admission.

<a id="PRD-INVESTIGATION"></a>
## Raw investigation

Raw investigation retains the caller's prompt, optional schema, selected model
and effort, web authorization and additional authorized read roots. It does not
require a review verdict or round. Resolve prompt-file and child cwd separately
against the wrapper process cwd captured at entry. Preserve containment, file
type, existence and UTF-8 checks before inference.

Only a web-enabled Google investigation appends the shared web
evidence clause last. A URL cited in prose is not proof that it was fetched.
AGY can return an incomplete URL body without a corresponding failed exit;
treat that known limitation as incomplete source evidence, not an automatic
repair/retry trigger or a claim that the provider has been fixed.

<a id="PRD-CUSTODY"></a>
## Process, evidence and cleanup

Preserve supported stdin/argv transport, terminal child status, writer/readers
and process-group cleanup, existing exit vocabulary, redaction and failure
diagnostics. The common transport object records observed stdin delivery,
execution route, executable/version when available and invocation attempt.
Native transport has null executable and CLI version.
Owner ruling 2026-09-27 (DL-18): a native same-family sub-agent leg records no
transport receipt at all — the host CLI's own diagnostics stand in, and only the
review history is kept; the native acceptance values above describe B's native
route.

A failed vendor call is classified by the vendor's own error sentence. The known
sentences are data in `contracts/vendor-failure-lines.json` (rule R-CLASSIFY,
case C43); both hosts carry the same rows.

Interpret delivery according to the actual route. A successful AGY/Gemini
wrapper receipt accepts `stdin_delivery:"not-used"`; a successful Claude CLI
receipt requires `"complete"`; native host observations accept `"not-used"` or
`"unexposed"`. A's Codex CLI retains complete-stdin validation for its stdin
transport. Other success-path values refuse. A proven start failure has its
separate `not-started` path. Preserve failed/invalid raw custody and never rewrite
an observation to imitate another route. A schema-optional key must not escape
as an uncaught lookup exception or lose preparation evidence.

Preserve fingerprint, guarded-worktree and prepared-directory review paths.
Inspect symlink text without implicitly reading its target. Cleanup requires
proven ownership and evidence export; it must preserve external targets,
unrelated files and active/fresh artifacts. Do not delete prior retry evidence.
Use existing bounded audit/failure-log retention. Durable exported evidence has
no automatic expiry unless an explicit lifecycle contract supplies one.

<a id="PRD-ACCEPTANCE"></a>
## Acceptance and compatibility

Verify macOS and Ubuntu 24.04 independently. Cover original duplicate JSON,
all six binding mismatches, legacy isolation, per-route requested arguments,
invalid settings before inference, same-family evidence swaps, informational
blockers, failed-entry retry, every changed-basis axis, residual delivery,
terminal process/reader handling, safe export/cleanup and raw investigation.
Preserve exact schema/prompt/policy provenance in source and distribution.

Separate deterministic tests, real service execution, source integrity,
revision adoption, installation and release evidence. An unrun authenticated
policy test remains unrun. Published candidate bytes do not change installed
revision pins or establish a revision tag.
Adoption of the 2026-10-02 review-strategy amendment on either host is `NOT RUN`.

<a id="PRD-OPERATIONS"></a>
## Operational interfaces and artifact ownership

Host B's existing opt-in v2 interface uses `bin/review_round.py`. The operation
names and custody shapes below describe that interface; the `v2-collect`
agreement result is the target after this amendment is adopted, not a claim
that the current shipped collector already implements R-AGREE:

| Operation | Required inputs | Observable result |
|---|---|---|
| `resolve-roster` | Project root | Resolved named entries, enabled names, distinct families and config provenance; no inference |
| `v2-create` | Managed root and request JSON | Bound source/packet, complete roster, installed capability receipts, immutable basis and content digest |
| `v2-allocate` | Basis, enabled leg name; diagnosis for retry | Exclusive attempt directory, six bindings, rendered prompt, exact native tool arguments or wrapper argv/env/output paths |
| `v2-record-cli` | Basis/name and actual owned wrapper run log | Original CLI envelope and wrapper outputs retained and hash-bound to that attempt |
| `v2-record-native` | Basis/name, host terminal receipt and untouched final-message bytes | Native terminal status, available identity observations and locally validated original verdict |
| `v2-record-start-failure` | Basis/name and proven no-start host observation | Terminal failed-to-run record without invented provider identity/version |
| `v2-collect` | Basis | Target after adoption: INCOMPLETE, BLOCKED or AGREED under R-AGREE, with all-entry results and separate family coverage; an owner exception remains a separate decision record |
| Existing `export` / `cleanup` | Matching review ID and owned root; new durable destination for export | Verified evidence retention before exact owned deletion |

Equivalent A integration may retain its established native APIs and lifecycle
command names. It must implement these behaviors and the common wire without
adding a native-leader subprocess for symmetry. B's source procedure defines
its exact host-receipt shapes; those host envelopes are not reviewer output or
another shared verdict schema.

Owner ruling 2026-09-27 (shared dev log DL-17): on host A, refusing before any
write plus the committed review ledger is the equivalent of the start-failure
record, the numbered preparation custody and the export step; A adds no command
for them.

The managed review root contains a fixed shared packet and separate mutable
custody. A basis binds packet/source/toolkit/roster/controls. Numbered
`preflight-v2/preparation-N` directories preserve partial setup evidence.
`results/<name>/attempt-N` owns immutable prompt/allocation, raw result,
provider receipt, read observations and terminal accounting; wrapper logs stay
under that attempt. Retries never delete or overwrite earlier artifacts.
Host input files use names separate from collector-owned prompt, output and
metadata files, including their digest sidecars. Refuse collisions before writing any
result, read evidence or terminal record so a corrected input can complete the
same allocated attempt. Malformed review identifiers and root-path values use
the command's controlled refusal before capability preparation. Other invalid
controls retain their established validation and preparation-evidence boundaries.
An unchanged native observation timeout is not a provider deadline; no unsupported
spawn argument or invented native cancellation rule is introduced.

CLI preflight versions and actual runtime versions are distinct observations.
Preflight is capability/selection evidence, never a substitute for a transport
runtime version. Preserve it separately; runtime `cli_version` stays null unless
the actual wrapper observes it. A disclosed contradictory runtime identity is not accepted
as the selected reviewer. A start failure is recorded only after proving no
provider started; uncertain starts require collecting all possibly live work.

<a id="PRD-RETENTION"></a>
## Retention requirements

| Artifact | Host B lifecycle |
|---|---|
| Audit JSONL | Append-triggered rotation after 10 MiB; at most five eligible archives / 50 MiB, active file separate; no age sweep |
| Ordinary failure IPC | Next dispatch sweeps eligible records at least one hour old; eligible stale entries are also pruned at 100 files / 20 MiB; preserve fresh siblings and the new record |
| V2 success/failure raw review records | Existing format in per-attempt roots; retain through collection and export, then owned review cleanup |
| Opt-in debug | No automatic expiry; hardened redaction mode skips it |
| Managed temporary review root | Verified export before explicit cleanup; stale reclaim requires proven ownership, export and inactivity beyond 30 days |
| Durable exports and investigation spikes | No automatic deletion; destination owner controls retention |
| Provider-owned artifacts | Outside TRIAD cleanup ownership |

No scheduled cleaner, unconditional directory sweep or new permanent web-evidence
database is part of this contract. Symlink cleanup preserves external targets.

Host A (owner rulings 2026-09-17 and 2026-09-26/27; DL-19): the committed review
ledger is the export; the managed review root is deleted by an ownership-proven
`close` and stale round trees are reclaimed after 7 days; every other log or
worktree the program creates expires after a period (audit rotation, failure-IPC
caps, 30-day test-run and debug expiry), so storage never grows without bound.

Every deletion above is done by host code, from roots declared in one configuration file
([R-CLEANUP](../reference/review-rules.md#R-CLEANUP), `contracts/cleanup-roots.schema.json`, C69); no prompt, skill,
agent text or printed remedy carries its own removal command (owner, D-DELETION-BY-CODE-20261004). Host A: done
(triad `b6fac284`, Task 23, DL-77, attributed PR12 host evidence); host B: DL-77.

## Functional coverage map

| Capability | Shared acceptance cases |
|---|---|
| Terminal process, stdin/readers and signal cleanup; setup failure custody | C1, C2, C6 |
| Safe resume, ownership, stale retention and export/cleanup | C3, C4, C5, C7 |
| Existing error vocabulary and phase-specific exceptions | C8 |
| Known vendor failure sentences, each classified on its own CLI | C43 |
| Actual transport observations and native/CLI envelope preservation | C9, C10 |
| Authentication/route-specific environment controls | C11, C17 |
| Three defaults, named override resolution, enabled roster and capability checks | C12, C16, C18, C22 |
| Canonical verdict, pinned shared clauses, six-field binding and legacy isolation | C13, C14, C30 |
| Independent host Gemini no-web policies; standing owner-authorized all-leg review web verification | C15, C32 |
| Diagnosed retry, full review after changed conditions and prior-finding delivery | C19, C20 |
| All-entry agreement, informational participation and exclusive sibling custody | C21, C23 |
| Independent macOS / Ubuntu 24.04 verification | C24 |
| Custom raw investigation, selected models/schema/web and additional authorized roots | C25 |
| Link-text evidence and frozen route/binary/version observations | C26, C27 |
| Entry-cwd path resolution, validation and masked evidence | C28 |
| Explicit Google web-evidence trigger and qualified fetched-source evidence | C29 |
| Phase/purpose, context transport, current residual, materialized evidence, stalled nonapproval and CLI-version evidence | C60, C61, C62, C63, C64, C65 |

## A implementation seams and preservation requirements (deferred)

The A paths below are source entry points at `92c8afd500499d8736afcc28b39a87a4f87fed50`,
not authorization to edit A from the Codex host. Recheck its actual checkout at
implementation start after shared-spec adoption and separate planning. The
following source pointers are historical handoff references, not verification
of A's current checkout. B's APIs illustrate the required behavior; A may retain
its native command names and storage layout while satisfying the same contracts.

| Area | A source entry point | Required migration and preservation |
|---|---|---|
| Terminal transport | [3rd-Agent/wrappers/_common.py:1954](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1954), [3rd-Agent/wrappers/_common.py:2058](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L2058) | Verify C1/C2/C6 on A's real process/reader boundary, retain completed transcripts on cleanup failure and add the common transport object to existing envelopes. Preserve primary vendor errors and owned process-group cleanup, including catchable parent signals. |
| Roster | [.claude/skills/triad-cross-family-review/lib/review_scratch.py:2618](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L2618), [.claude/skills/triad-cross-family-review/lib/review_scratch.py:2744](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L2744) | Move the opt-in v2 path to the canonical nested vendor schema, three defaults, merge by name and all enabled entries; preserve explicit legacy discovery/override behavior and A's project location. |
| Result admission | [.claude/skills/triad-cross-family-review/lib/validate_verdict.py:342](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/validate_verdict.py#L342), [.claude/skills/triad-cross-family-review/lib/validate_verdict.py:563](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/validate_verdict.py#L563); [review_scratch.py:3082](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L3082) | Consume canonical v2 bindings and findings together with the renderer; preserve native Claude's verbatim raw-first admission and end-marker controls. Do not add a native Claude subprocess for symmetry. |
| Dispatch and model settings | [review_scratch.py:3016](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L3016) | Generate each enabled entry's actual native or wrapper call from capability-checked controls. Reject unsupported Gemini effort instead of silently recording it. Preserve Codex stdin transport. |
| Agreement | [review_scratch.py:3100](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L3100) | Remove the v2 advisory exemption: informational entries block on findings/questions or missing results like every other entry. Keep family coverage separate from entry count. |
| REVIEW web boundary | [review_scratch.py:3078](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L3078); [3rd-Agent/wrappers/antigravity_wrapper.py:268](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/antigravity_wrapper.py#L268), [3rd-Agent/wrappers/antigravity_wrapper.py:1381](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/antigravity_wrapper.py#L1381); [3rd-Agent/wrappers/policies/gemini-readonly.toml](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/policies/gemini-readonly.toml) | v2 REVIEW passes codex `--search` only under a true bound R-REVIEW-WEB condition (never inherited from the legacy X-leg dispatch). Preserve AGY review/research agent separation (a true condition selects the research agent and the hook's web allow set), the raw-only `web-evidence` clause (never appended in REVIEW), web-enabled investigations and A's complete host-specific Gemini profiles (no-web `gemini-readonly.toml`, web `gemini-readonly-web.toml`). |
| Capture and re-review | [review_scratch.py:1858](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L1858), [review_scratch.py:2009](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L2009) | Bind the complete scope/criteria/roster/controls and prior residual input; source or review-condition changes require all participating entries to inspect the complete scope again. |
| AGY read evidence | [review_scratch.py:3037](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L3037); [.claude/skills/triad-cross-family-review/lib/agy_hook.py](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/agy_hook.py) | Preserve active A hook/load/read-audit controls. Isolate every named leg and attempt; another same-family leg's audit cannot satisfy it. B's dormant hook is not an A migration template. |
| Relative paths | [3rd-Agent/wrappers/_common.py:1148](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L1148) | Resolve prompt-file and child cwd independently against captured process-entry cwd, retaining regular-file/UTF-8/existence checks and redaction in all wrappers, including Codex. |
| Web investigations | [3rd-Agent/wrappers/antigravity_wrapper.py:1381](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/antigravity_wrapper.py#L1381); [gemini_wrapper.py](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/gemini_wrapper.py) | Preserve AGY's existing explicit trigger and research-agent route; implement the equivalent web-enabled Gemini clause-last path, including custom-schema retry. Add no permanent page log. |
| Cleanup | [3rd-Agent/wrappers/_common.py:3386](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L3386), [3rd-Agent/wrappers/_common.py:3676](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/3rd-Agent/wrappers/_common.py#L3676); [review_scratch.py:708](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L708), [review_scratch.py:936](https://github.com/codefoundry-io/triad/blob/92c8afd500499d8736afcc28b39a87a4f87fed50/.claude/skills/triad-cross-family-review/lib/review_scratch.py#L936) | Apply the fresh-sibling age floor even under count/byte caps; preserve proven ownership, verified export, partial-cleanup recovery and external symlink targets. Numeric host floors may differ. |

## B implementation references

These references identify the concrete B behavior to preserve or adapt.
A keeps its own native interfaces and enforcement mechanisms.

| Behavior | Exact B source |
|---|---|
| Roster resolution | [bin/review_roster.py:42](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_roster.py#L42) |
| Adapter defaults, selection and preparation refusal | [bin/review_adapters_v2.py:187](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_adapters_v2.py#L187) |
| Native defaults and controls | [bin/review_adapters_v2.py:61](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_adapters_v2.py#L61) |
| Claude defaults and controls | [bin/review_adapters_v2.py:75](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_adapters_v2.py#L75) |
| Google selection and controls | [bin/review_adapters_v2.py:134](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_adapters_v2.py#L134) |
| Immutable basis | [bin/review_round_v2.py:127](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L127) |
| Invocation allocation and retry | [bin/review_round_v2.py:257](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L257) |
| Wrapper launch arguments and runtime boundary | [bin/review_round_v2.py:196](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L196) |
| Delivery and runtime observation validation | [bin/review_round_v2.py:299](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L299) |
| Original CLI custody | [bin/review_round_v2.py:417](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L417) |
| Original native custody | [bin/review_round_v2.py:439](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L439) |
| Proven start failure | [bin/review_round_v2.py:479](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L479) |
| All-entry collection | [bin/review_round_v2.py:497](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round_v2.py#L497) |
| Strict original v2 JSON validation | [bin/validate_v2.py:74](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/validate_v2.py#L74) |
| Shared prompt loading and rendering | [bin/review_prompts_v2.py:60](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_prompts_v2.py#L60) |
| Terminal process ownership | [bin/_common.py:1427](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/_common.py#L1427) |
| Common transport observations | [bin/_common.py:327](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/_common.py#L327) |
| Path evidence and masking | [bin/_common.py:563](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/_common.py#L563) |
| Fresh-record retention under caps | [bin/_common.py:3014](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/_common.py#L3014) |
| Verified export and cleanup | [bin/review_round.py:1242](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/bin/review_round.py#L1242) |
| Operational procedure and host receipt shapes | [skills/triad-cross-family-review/references/public-v2-review.md:1](https://github.com/codefoundry-io/triad-codex-dispatch/blob/add5805d8dec70f5e133164c49bc0fe3bff75095/skills/triad-cross-family-review/references/public-v2-review.md#L1) |

## Shared references

The commit-pinned prompt and contract links below are pre-amendment provenance,
not the current review-strategy payload. Resolve current rules and payloads through
the [current strategy handoff](claude-review-strategy-handoff.md) and record the
adopted shared main SHA as described below.

- [Integration contract](https://github.com/codefoundry-io/triad-dispatch-spec/blob/aef3adee863fd90fdfab60ae2253717cf1b4d303/decisions/rev-2-implementation-spec.md)
- [Canonical contracts](https://github.com/codefoundry-io/triad-dispatch-spec/tree/055204c83e57bf87eeac5b2422f2b17340f7c53b/contracts)
- [Shared prompts](https://github.com/codefoundry-io/triad-dispatch-spec/tree/6bef14c0c42a13678594e8f2f039d1793b7cb127/prompts)
- [Authoring synchronization](https://github.com/codefoundry-io/triad-dispatch-spec/blob/main/reference/spec-authoring.md)

Read the latest remote shared main at session start, before common changes and
before final review, recording its SHA. Share common design/contract/prompt
changes with the other host leader on the same published basis. Preserve
installed revision and digest adoption as a separate operation.

Execution results, service-policy checks and publication records are kept
separately in the [B verification record](host-b-p3-verification.md).
