# Rev-2 implementation specification

Status: implementation candidate; not a revision tag or host conformance claim.
Basis: fetched main `2eb883fee59e66556ee7c7f87189b38231136622`, agreed design
`bd506054e62b9b1ba5ef5e156ae8928ac414e4bf`. Owner direction: write and publish
the shared schemas/specification first, then implement from that shared commit;
prefer maintained official libraries and supported CLI features. Complete the
testable remaining obligations before the final Claude implementation handoff.

<a id="SPEC-SCOPE"></a>
## Scope and authority

This materializes the already aligned v2 wire, named variable roster, receipt
vocabulary and host integration contract. Existing C1–C29 expected behavior
remains binding. B leads implementation; A is read-only until the owner resumes
its work. The [D-B1/D-B2/D-5 owner answers](2026-09-20-owner-follow-up.md) are now
recorded; their [profile and evidence wording amendment](2026-09-20-host-policy-and-evidence-amendment.md)
is a candidate requiring the same-commit cross-host check. Do not implement a
superseded proposal or claim runtime adoption.

The normative type definitions are the three files under `contracts/`, not a
second host model definition. Shared clauses remain in `prompts/`. This document
defines integration behavior that schemas cannot express; it links existing
review rules instead of replacing them.

## Libraries and supported interfaces

- Use [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-validation)
  with the maintained [python-jsonschema validator](https://python-jsonschema.readthedocs.io/en/stable/validate/)
  for local authoritative schema validation. Use its standard offline registry;
  no remote reference retrieval during review, custom schema engine or plugin
  keyword vocabulary. Schemas contain only local references.
- Preserve [Pydantic v2](https://docs.pydantic.dev/latest/concepts/json_schema/)
  at existing wrapper boundaries where required. A thin model adapter can load
  the vendored canonical schema; it must not become a second editable copy of
  its fields or relax validation.
- Use existing CLI-native structured output/policy/permission/model controls.
  [Claude Code CLI](https://code.claude.com/docs/en/cli-reference) exposes
  `--json-schema`; [Anthropic's structured-output documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  describes a smaller schema subset than the full local contract. CLI acceptance
  must be tested separately from API documentation. Use a thin, explicit producer
  projection for this verdict only when a CLI cannot accept the full contract;
  it is a generation aid, never the admission validator. Locally reject output
  that violates the unchanged full contract. Do not add a vendor SDK dependency
  or hand-build a general schema-to-schema translation engine.
  Measured producer refusals of the full contract (A's live probes, 2026-09-21;
  the vendor messages are quoted at lib/roster_v2.py:88-122 @ triad e0b15f1).
  Codex `--output-schema` refuses `not` ("In context=('not',), schema must have
  a 'type' key"). It also requires every property in `required` ("... Missing
  'correction'"). agy `--json-schema` refuses a `null` member inside `enum`
  ("INVALID_ARGUMENT (code 400): ...properties[route].enum[2]: cannot be
  empty"). On A the producer projection for the codex and agy wrapper routes
  drops `$schema`, `$id` and the top-level `allOf`. It drops `not` and
  `uniqueItems` at any depth and the optional `finding.correction`. It rewrites
  `route` as `anyOf [{type string, enum [agy, gemini]}, {type null}]`
  (lib/roster_v2.py:97-122, :903-949 @ triad e0b15f1). Admission still
  validates every reply against the full contract. On B the agy v2 route sends
  the full contract, binding consts included, as `--json-schema`
  (bin/verdict_v2.py:39-45, bin/antigravity_wrapper.py:499, :697-723, :148-149
  @ 7f75863). Its `route` enum carries `null`
  (contracts/leg-verdict.schema.json:59-65). Case C30; authoring/shared-dev-log.md DL-103.
- Keep native host agents native. Do not add Codex subprocess on B or Claude
  subprocess on A for symmetry. Preserve authentication selection and refuse
  unsupported model/effort settings before inference, without provider fallback.
- Record dependency/tool versions with verification. Current local authoring
  evidence is Python 3.12.13, jsonschema 4.26.0, referencing 0.37.0 and Pydantic
  2.13.3. This is not an authenticated provider compatibility claim.

<a id="SPEC-VERDICT"></a>
## Verdict and legacy boundary

`contracts/leg-verdict.schema.json` implements the aligned
[wire mapping](../contracts/leg-verdict-mapping.md): three canonical verdicts,
four severities, required evidence/coverage/uncertainty, optional correction,
strict field names and complete binding. A Minor-only non-affirmative result is
schema-valid and recorded as a selection deviation, but never establishes
agreement. Every selected entry must explicitly return `SAFE TO MERGE` without
blockers or open questions under [R-AGREE](../reference/review-rules.md#R-AGREE).
Original JSON duplicates are rejected before the first lossy parse.

An existing host-local v1 validator may remain as an explicitly selected
compatibility entry point for historical records and existing development gates.
Its legacy invocation and rejection behavior stay intact. A v1 result never
admits a v2 round, and v2 is never translated to SAFE/NOT-SAFE to satisfy a
legacy gate. The v2 public path is selected explicitly and switches its validator,
all schema-shaped prompt clauses, render binding and collectors together.

B's current workspace four-leg gate remains a development-only legacy consumer.
Its copied standalone validator, paired Google receipts and identity/integrity
controls must keep working. This requires no change to workspace governance.
The public v2 roster follows the shared rules, including informational legs.

<a id="SPEC-ROSTER"></a>
## Roster resolution

`contracts/review-legs.schema.json` validates a named override document. Its
`$defs.resolvedRoster` validates the complete resolved entries. An override can
omit fields supplied by the named default; a new name must supply the required
resolved fields. Merge objects by field name; replace scalars and arrays.
Reject duplicate leg names before merging, unknown keys, wrong-vendor blocks,
unresolved template strings and unsupported adapter values before paid dispatch.

Without a file, use the host's shipped data file containing exactly three
enabled entries, one per family. Model slugs and recommended effort/timeout are
data, not orchestration constants. Optional extra legs are ordinary named
entries. The schema describes field types; the adapter checks actual installed
capabilities, authentication and route constraints. In the Google block,
`google.route` is an optional explicit `agy`/`gemini` pin; absent/null uses
the host's shipped selection chain. Preserve both per-CLI model blocks so the
selected route can consume its own settings. Do not reinterpret an AGY slug as
a Gemini CLI model argument or invent an unsupported Gemini effort flag.

Show all resolved enabled entries and exact wrapper argv/native agent arguments
before inference. Disabled or unselected entries cannot start. Freeze the chosen
route, executable and requested model/effort in the bound round inputs. An exposed
runtime identity is an observation; an unexposed identity is not inferred.

The three-family default is convenience data under
[R-ROSTER](../reference/review-rules.md#R-ROSTER), not an agreement threshold.
The owner chooses a nonempty roster. Family coverage is receipt data; R-AGREE
imposes no minimum leg or family count. A failed selected entry cannot be
removed by the leader to turn that basis into agreement; changing the roster
requires a new basis.

<a id="SPEC-CUSTODY"></a>
## Transport receipts and evidence ownership

`contracts/receipt-fields.json` defines the common `transport` object attached
unchanged to successful audit rows and failure run-log records. Keep existing
host-specific envelopes. Its `route` names the actual execution route
(`native`, `claude`, `codex`, `agy`, `gemini`), not a model family.
Native execution has no binary or CLI version: these fields are null, not guessed.
An unavailable version is null; a null field never proves a provider capability.

`stdin_delivery` distinguishes not-used, not-started, complete, failed and
unexposed. A child that failed before spawn is not-started; an incomplete write,
flush or close is failed. Do not overwrite an observed vendor error or timeout
merely to normalize this field. `attempt` is the per-leg invocation counter,
starting at one. Existing error tokens/direct exits stay governed by
`contracts/exit-tokens.json`; aliases and direct wrapper exceptions are tested
separately from classifier-patch eligibility.

Formal collection owns the tuple review_id/leg_name/family/digest/attempt/route;
this is the verdict route from R-BIND (agy/gemini for Google, null otherwise),
distinct from the transport execution route above. Both observations remain bound.
Each leg and attempt gets exclusive result and read-evidence locations bound to
that tuple. A sibling's read audit, result, preflight or receipt cannot satisfy
another entry even if the family/model is identical. Preserve raw provider
evidence and distinguish missing/unexposed observations from observed empty
sets. Do not activate dormant hooks to manufacture evidence.

<a id="SPEC-RETRY"></a>
## Same-basis retry and changed-basis review

Reuse existing lifecycle operations; add only the named-entry/attempt accounting
needed by R-RETRY and R-BIND, not a second scheduler or provider engine.

- A failed-to-run attempt is terminally recorded. After diagnosis, retry only
  that entry when the bound source, prompt body, criteria, roster, model,
  effort, route and policy are unchanged. Increment its attempt; completed
  siblings retain their original bound results. Attempt metadata may change
  without changing the substantive prompt/body basis.
- A valid negative verdict is a completed review, not a transport retry.
- Any change to reviewed content or review conditions creates a new basis and
  full-scope review by every selected entry. The leader carries the prior
  excerpts, rebuttals and verification needed for the current judgment in the
  existing bound `prior_residual` string or host evidence/brief surfaces. On B,
  use `EVIDENCE.md` for longer material and existing allowed source members for
  additional sources; A uses its own existing bound surfaces. An old file path
  alone is provenance, not delivered evidence. Bind current input bytes; do not
  automatically append transcripts, accumulate prior residuals or deduplicate
  their meaning. Prior approval is not transferred.
- All participating legs count. Acceptance labels do not exempt findings,
  uncertainty or absent results. All must explicitly return `SAFE TO MERGE`
  without blockers or open questions for `AGREED`. Record family coverage
  separately from leg count, without a minimum-family gate. Verify final
  source/toolkit integrity before admission.
- Keep cleanup ownership/export/failure retention. No retry deletes prior
  evidence or overwrites immutable result files. Only host code deletes, from
  roots declared in one configuration file (R-CLEANUP, C69).

<a id="SPEC-INVESTIGATION"></a>
## Paths, investigations and unresolved decisions

C28 resolves both prompt-file and child cwd independently against the wrapper
process cwd captured at entry. Keep current root/type/UTF-8/existence checks.
The child's cwd is never the base for loading the prompt. A malformed argument
fails before inference. C28 success evidence uses existing host redaction and log
surfaces under D-B2; no unmasked-path expansion or new logger is required.

C25/C29 extend the existing raw invocation: caller prompt, optional arbitrary
schema, selected model/effort/perspective and authorized read roots remain usable
without a review verdict/round. Only a web-enabled Google
investigation appends the shared web-evidence clause last, with route-specific
tool-name substitution. REVIEW never uses that trigger. Exact sent-prompt and
fetched-page evidence custody follows the recorded D-B2 choice; do not infer a
fetch from a URL in final prose.

Gemini REVIEW adopts the recorded D-B1 choice and preserves its no-web profile
controls; [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB) selects the
web-enabled profile under the owner's standing authorization. Provider-free policy-engine/argv/receipt tests are distinct from
V1–V5. An unrun authenticated or effective-policy test remains NOT RUN.

<a id="SPEC-VERIFICATION"></a>
## Sequence and verification

1. Author schemas, aligned shared prompt pins and explicit behavioral fixtures.
   Run schema meta-validation and meaningful accept/reject examples using the
   maintained library. Review the complete shared change and publish one commit.
2. Vendor that exact commit's consumed files and adjacent hashes into B.
   Implement tokens/paths, roster/invocation, v2 validation, receipts/retry and
   investigations as bounded plans after a separate implementation plan. Use TDD
   and current required plan-level reviews. Skill/prompt behavior experiments,
   when a project requires them, are separately owned; TRIAD does not arrange or
   run them. Defer A source inspection until shared-spec adoption and A planning.
3. Verify both macOS and Ubuntu 24.04. Test offline source/archive payload equality
   and altered/missing contract refusal. Update case mappings with actual named
   tests and evidence; do not change expected outcomes to match code.
4. Final Claude handoff records B implementation and, after deferred A inspection,
   verified A source lines, preserved
   behavior, actual deviations and remaining untestable checks. Revision tagging
   and `SPEC_REVISION` adoption remain explicit: a candidate commit/digest
   manifest is not an uncreated rev-N tag.

A complete v2 result/schema test matrix includes blocking/open-question cases,
Minor-only negative, malformed paths, duplicate original members, missing/extra
fields, wrong binding/attempt/route, and legacy/v2 isolation. Roster tests cover
partial overrides, duplicate names, wrong blocks, placeholders, disabled entries,
both Google CLIs, unsupported settings and actual invocation arguments. Receipt
and retry tests cover successful/failed transport, unexposed observations,
same-family evidence swaps, unchanged single-leg retry, every changed-condition
axis and residual-data delivery. Use synthetic providers for deterministic
boundaries; never describe them as real service execution.

## Authoring evidence and cross-host handoff

The scope is contract/schema/prompt authoring, not a B implementation slice.
Production host delta: +0/-0; novel host core: 0. The expected authoring budget is
about 750 schema/test lines and 250 documentation/prompt lines; line counts are
review planning information, not acceptance criteria. The complete affected
contract and unchanged rule consumers are review scope.

Provider-free macOS authoring evidence: initial missing-schema RED, 65 failed;
independent source review identified terminal-newline acceptance through the
Python regular-expression end anchor; reproduced RED, 6 failed / 65 passed;
after explicit schema newline rejection and example validation, 72 passed.
Ubuntu 24.04.4 in a task-specific container with jsonschema 4.26.0: 72 passed;
source/root filesystem read-only, network disabled during execution. The older
verification image lacked jsonschema; its dependency check failed before tests,
then the declared dependency was installed in the task image only.
These historical runs used `tests/test_schemas.py` with the versions recorded
above. They are not verification of this 2026-10-02 amendment, provider
execution, B behavior-test certification or V1–V5 evidence.

First full review (`triad-shared-v2-r1`) completed with all four valid results
and matching integrity, outcome NOT-SAFE. A pinned Google route lacking its own
configuration block reproduced in both directions (RED: 2 failed / 75 passed).
The bounded schema fix retains unpinned single-route configurations; current
macOS and Ubuntu 24.04.4 suites each pass 77 cases. Stale C9/C10 status text and
the omitted B Claude timeout fact were corrected without changing case outcomes.
The corrected whole scope requires a fresh complete review; prior approvals do
not transfer.

The Claude leader reviews this complete shared-spec candidate commit against
the aligned mapping before adoption. Inspection of A's actual host-code checkout
is deferred until shared-spec adoption and separate implementation planning.
Earlier source pointers in [the 0.2.555 compliance handoff](host-b-0555-contract-compliance-handoff.md)
are historical provenance, not current A verification.
Preserve A's raw-reply admission marker, native Claude invocation and live AGY
hook/read-audit checks; preserve B's native Codex, legacy development gate and
dormant hook. Both hosts need the v2 validator, every shaped prompt and bound
named-entry collection to switch together. Neither host may populate missing
legacy evidence/coverage/uncertainty by conversion. D-B1/D-B2 owner decisions are
settled; their linked common amendment is reviewed/published before host adoption.
