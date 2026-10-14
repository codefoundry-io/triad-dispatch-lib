# Repair research: source evidence and common-host handoff

2026-10-09. Remote main fetched before authoring:
`3afc4d7e931e55d601dd74877bdbe65e610a8e59`; PR13 basis `75dc801`.
Owner decision: D-REPAIR-WEB-20261009. Normative location: R-CLASSIFY, C76.

## Initial implementation observation (source only)

A clean source at `c50b1c8b0b7bfc0f66165c6262653925b697cc58`:
- `.claude/agents/{codex,gemini,agy}-wrapper-repair.md:6` exposes only
  `Read, Grep, Glob`; line 11 explicitly excludes network tools.
- Their analysis steps (codex:74, gemini:72, agy:82) state `Network is off`.
  Their operating discipline also says `No web, no guessing`.
- `3rd-Agent/export_assets/distributed-repair-agent.md.tmpl:6,11,75,161`
  repeats the restrictions. `3rd-Agent/export_plugin.py` renders the shipped
  analyzers from this template, so changing only source agents would omit the
  distributed behavior. No A file was edited or A runtime invoked.

B at `632f42633d3a92d6cb27168cd15c4d4debd8558c` plus its preserved candidate:
`docs/references/repair-protocol.md:51-55` prohibits provider or network calls
and requires escalation when local evidence is insufficient. The prohibition is
in the actual native-child prompt, not merely a statement about a tool name.
No B product prompt, native settings or runtime was changed for this spec update.

These are pending implementations of the newly requested common capability,
not evidence that either host already permits web research or that an observed
production failure was caused by these restrictions.

## Maintainer request

A: expose web search/fetch in the three repair analyzers and their distributed
template and reconcile the contradictory instructions. B: allow those research
operations in the repair prompt and use the host's supported native web capability.
Each host owns its spawn/tool mechanism. Reuse the existing proposal/extension
surface, read-only analyzer and deterministic applier; do not add a new vendor
execution, classifier class or routine log audit. DL-104's independent pending
work stays distinct; this change does not certify its implementation.

Verify C76 on each host: a real failure record needing external explanation can
reach search/fetch and retain useful source attribution; sufficient local evidence
needs no search; unrelated public errors cannot generate entries; unavailable or
inconclusive research reports its limit without guessing or running the vendor.
Check source and distributed behavior. Tests may exercise tool-policy decisions
without claiming a fabricated response is a measured vendor failure. Runtime and
host conformance for C76 are NOT RUN on both hosts.

The shared rule is owner-authorized. Review this same spec commit and report
source-backed disagreements or implementation evidence before claiming adoption.

Spec verification: authoring map 1/1 valid; existing shared tests 182 passed;
whitespace check clean. These checks validate the spec repository, not C76 host
behavior. No new vendor-failure fixture or runtime classification was introduced.

## B U4a capability evidence and remaining work

B `632f426` plus its preserved local candidate now permits the specified web
research in the actual `repair_message` in `docs/references/repair-protocol.md`.
README EN/KO, SECURITY and migration guidance describe the same capability: five text files, +47/-5
lines, no Python module, classifier entry, JSON schema, model/effort or native
spawn change. Source URLs use the existing `reason`; insufficient or unavailable
needed research escalates. This is source capability, not installed adoption.

Fresh dedicated Sol/high behavior evidence: the old prompt refused research
(RED); the corrected prompt searched and fetched official Gemini documentation
for documented exit42, cited it, and escalated because the input was explicitly
a capability fixture rather than a vendor incident (GREEN). A locally mapped
`MODEL_CAPACITY_EXHAUSTED` control needed no web or duplicate extension. These
fixtures do not establish a new vendor failure, carrier or exit combination.
A separate fresh Luna/high choice exercise declined a diagnostic URL containing
encoded private context and chose sanitized error/code search; the local control
also proposed no duplicate entry. This finite exercise is not a general security
certification. Requested serving-model identity is not independently exposed;
the unchanged production Terra preset was not separately runtime-certified.

Dedicated checks: focused106 passed, full2029 passed/4 skipped, both source skill
validators passed. RED/GREEN and regression source hashes remained stable; the
local-control report lacked the four-file prehash and discloses that limit.
Source evidence is retained under B `_runs/spec-plan-20261009/u4a/`.

Full C76 is still pending: U4b retains DL-104 timeout routing and deterministic
stored-record verification/applier work. No real failure was manufactured and
no learned classifier was installed. Unavailable/inconclusive-tool handling is
specified but has no separate runtime result in this bounded evidence set.

A was rechecked read-only at clean `a6f3c17572c67ed29485e2d02b5947033ca80a77`:
all three source repair agents still list `Read, Grep, Glob` at line6 and prohibit
web (codex:74/146, gemini:72/143, agy:82/143); the distributed template retains
the same restrictions at6/75/161. The A source/distribution request remains open;
A runtime was not invoked and no A source was edited.

B review also identified an existing full-conformance gap: no shipped
`skills/*/SKILL.md` currently links `docs/references/repair-protocol.md`, although
the protocol says the dispatch skill supplies its failure log. For example,
`skills/triad-claude-dispatch/SKILL.md:39-43` has result handling without that
handoff. Restore the unknown/extraction-error handoff when implementing U4b and
verify stored-record replay without another vendor run. U4a's direct prompt
probes do not close that end-to-end path. A's corresponding routing remains
its maintainer's verification responsibility; no cross-host defect is inferred.

## Review status and bounded residuals

**Latest disposition:** the owner accepted the two residual demands as nonblocking
and authorized U4b, under D-PROMPT-REVIEW-BOUNDED-20261009. U4a is locally accepted
by that explicit decision; the historical NOT_APPROVED review results below stay
unchanged. Full C76 and U4b are still pending. No further prompt round is needed.

U4a is implemented but NOT_APPROVED by the all-selected gate. R1 omitted the
required R-THREAT context and returned an attacker-URL finding; the finding was
recorded as speculative hardening. R2 received that context and identified missing
consumer migration guidance; four lines now align it. Fresh affected106 and both
validators passed, followed by4 migration-contract tests; prompt/Python unchanged.

R3: Claude NOT-SAFE, Pro/Flash/native Astra SAFE; ROUND_INTEGRITY_OK. Digest
`e82260abc580d0fd8124a22460cdab81ea7cffba809b9e735a34bbdf7113b54b`;
fingerprint `4be5cd186eccb81541c3daee835869ef4c248b1d7a22843e3c9292e9d92b35f5`.
All producers terminated; each round exported custody and removed its exact
temporary stage/cwd. No majority approval or finished-unit claim is made.

Remaining Claude blockers: the README's "unrelated public errors" phrase versus
the prompt's "errors encountered only in public sources", and adding a test that
pins the wording across documents. The wording was Minor in R1/R2 and Major in
R3 without changed README/prompt bytes. A new fresh Luna/high exercise used only
the README and rejected a related public-only sibling error absent from the run;
it accepted the observed-error control for owner review. Both preregistered
choices passed. This finite probe does not prove every reader's interpretation,
but supplies the owner's requested decision evidence before any further wording
iteration. It adds no vendor-error fixture or new classifier restriction.

The leader is resolving this convergence boundary rather than launching another
unchanged full round. Full C76 and A capability remain open. No test, install,
adoption, merge or release claim overrides the retained NOT_APPROVED result.

Independent fresh Sol/high consolidation, without probe outcomes, confirms the
README wording ambiguity but no demonstrated runtime defect. It distinguishes
missing literal coverage from functional evidence: the requested phrase-pinning
test cannot establish sanitizer, attribution or proposal behavior. The higher-
priority testing instruction excludes tests that merely mirror implementation.
The leader records the process disagreement, preserves NOT_APPROVED, and requests
owner adjudication instead of repeatedly redispatching unchanged wording.

The requested owner adjudication has now arrived as
D-PROMPT-REVIEW-BOUNDED-20261009: accept the two residuals and continue U4b.
The earlier request and review receipts above remain historical evidence.

U4b source assessment after acceptance: B still routes timeout in
repair-protocol.md:3 and has no stored-record verification input in
bin/apply_patch.py. A `d075a879bf66e568c05349a40efe532b640cd8e5` was read without
changing its concurrent dirty work: `.claude/skills/triad-codex-dispatch/SKILL.md`
routes timeout at90/230 and instructs a vendor `--repair-mode` rerun at239/317-320/343.
These are pending DL-104 changes on each host, not newly observed incidents.
Native mechanisms, auth STOP and applier locking remain outside this correction.
