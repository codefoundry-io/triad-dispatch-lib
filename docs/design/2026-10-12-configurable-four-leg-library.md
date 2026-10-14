# Configurable four-route library direction

Date: 2026-10-12. This records the owner's scope correction and the resulting
implementation direction. It supersedes any implication that Codex-only testing
defines the product boundary. The common APIs are now implemented and verified
with synthetic installed-package inputs; actual provider success and consumer
adoption remain separate claims.

## Product requirement

One common library must configure Codex, Claude, Gemini CLI and AGY review
entries, including all four together. Configuration includes named entries,
enable/disable selection, requested model/effort, explicit Google route and
timeouts. Deterministic roster, prompt, validation and agreement behavior belongs
here; host-specific execution translates those requests through its actual
supported interface. Codex is the initial live test environment. Claude-host
adoption will be performed separately by its owner.

All library implementation and integration tests stay in this repository.
Existing host repositories supply read-only reference material, not the place
to install the library or run the integration suite.

The owner explicitly retains the existing Gemini workaround after unsuccessful
0.63.0 non-interactive plan behavior and no available test path. Replacing or
retesting that workaround is not part of this design. MCP-based candidates are
excluded. The owner deferred the Codex SDK to TODO after initial research. If
reactivated, that optional experiment uses the direct local app-server protocol
without configured MCP servers or global settings changes; it is not a gate for
the four-route core.

## Canonical representation

Freshly read shared-spec main is
[`396a04dac310d5ff91dbe0a36982f7679aa00428`](https://github.com/codefoundry-io/triad-dispatch-spec/tree/396a04dac310d5ff91dbe0a36982f7679aa00428).
Its [roster schema](https://github.com/codefoundry-io/triad-dispatch-spec/blob/396a04dac310d5ff91dbe0a36982f7679aa00428/contracts/review-legs.schema.json)
and [R-ROSTER](https://github.com/codefoundry-io/triad-dispatch-spec/blob/396a04dac310d5ff91dbe0a36982f7679aa00428/reference/review-rules.md#R-ROSTER)
already allow multiple named entries of the same family. No new `gemini` or `agy`
family is needed. One Google entry chooses one route for an invocation; select
two entries to run both routes.

| Execution choice | Canonical vendor/family | Verdict route | Existing configuration fields |
| --- | --- | --- | --- |
| Codex | `codex` | null | `codex.model`, `codex.reasoning` |
| Claude | `claude` | null | `claude.agent`, `claude.model`, `claude.effort` |
| Gemini CLI | `google` | `gemini` | `google.route`, `gemini.model`, `gemini.effort` |
| AGY | `google` | `agy` | `google.route`, `agy.model`, `agy.effort` |

Each entry also has `name`, `enabled`, `acceptance` and `timeout_s`. Four entries
cover three families. Family coverage does not collapse two Google results into
one vote. Enabled informational entries also must approve. Do not force exactly
four entries: the same common API supports any nonempty owner-selected roster.

Null/absent route retains the host's selection chain; the library does not
invent a universal AGY-first fallback. Explicit null model retains host-default
semantics. Model/effort strings stay opaque; actual support belongs to the
adapter, including host-native exceptions. A Gemini effort field must not create
a nonexistent CLI flag. Preserve requested and observed settings separately.

## Common code and host responsibilities

| Library responsibility | Host/adapter responsibility |
| --- | --- |
| Strict roster JSON, canonical schema, duplicate-name refusal and merge by name | Read configuration files and supply the host's defaults |
| Select enabled entries and refuse an empty selection before preparation | Resolve native model/effort/preset controls and supported CLI flags |
| Preserve explicit route and opaque model/effort values | Resolve unpinned Google routing under the host's existing policy |
| Render pinned common clauses for every supported family/host profile | Start native children or vendor CLI/SDK calls and observe/cancel its call |
| Extract supported common carriers and validate original verdict JSON plus six bindings | Observe transport/terminal state, remove native markers and adapt unsupported envelopes |
| Evaluate all selected entries' approval and shared failure rules | Supply observed terminal state and integrity evidence; own artifact I/O |

Delivered public operations include resolve_roster/select_entries,
render_review_clauses/render_investigation_prompt, ProviderOutput/extract_final/
admit_output, evaluate_agreement, run_review and run_investigations. See the
[public examples](../../README.md#async-host-callbacks) and
[verification record](../verification/2026-10-12-four-route-core.md). These APIs
do not add fields to the canonical wire schema.

Agreement requires every selected entry's current bound result to be explicitly
`SAFE TO MERGE`, without blockers or open questions, and with complete integrity
evidence. Valid negative results remain admitted and block agreement. Missing,
invalid, swapped or old-attempt results cannot count. There is no majority rule.
See [R-AGREE](https://github.com/codefoundry-io/triad-dispatch-spec/blob/396a04dac310d5ff91dbe0a36982f7679aa00428/reference/review-rules.md#R-AGREE).

## Implementation and verification order

1. **Roster core:** vendor the canonical roster schema with an explicit manifest;
   compare required assets to the currently packaged `fcd96a1` pin before changing
   provenance. Implement strict overrides, recursive object merge by name,
   scalar/array replacement, resolved validation and enabled selection. Tests
   cover four entries, simultaneous Google routes, partial/null overrides,
   duplicates, wrong-family fields, unknown fields, disabled entries and empty
   selection. Defaults are caller data rather than hard-coded provider models.
2. **All prompt profiles and agreement:** extend the current Codex/B restriction
   with canonical Claude/Google and host markers. Exercise every applicable
   route across formal-plan, implementation-review and pre-merge. Test one and
   multiple entries of the same family, informational dissent, negative verdicts,
   missing results, stale attempts and Google sibling swaps. Keep host spawning
   out of these deterministic tests.
3. **Installed-package matrix:** expand the repository driver to validate all
   four route contexts and packaged assets from an isolated wheel. Run source,
   unpacked-sdist and installed-wheel cases on native Ubuntu24.04 x86-64 and
   macOS15 ARM64. CI provider responses are synthetic and labelled as such.
4. **Optional transport experiments:** use the
   [CLI spike results](../research/2026-10-12-cli-feature-spikes.md) to choose
   supported CLI checks in this repository. Codex Python SDK execution is a
   deferred TODO and SDK dependencies stay outside the deterministic core.
   If reactivated, verify existing ChatGPT credential reuse independently of
   CLI login status; do not require an API key or MCP transport. Retain the
   Gemini workaround without a new plan-mode gate. Add real-provider checks with
   installed interfaces; record missing/quota-blocked routes honestly. Four-way
   replay is not proof of four real providers or either existing host's adoption.
5. **Classification:** test measured typed carriers and shared token/exit rules.
   Investigate AGY's documented structured errors before adding phrase matching.
   Never turn capacity/schema failure into automatic full-CLI re-execution.

## Current implementation and research limits

## Approved execution shape (2026-10-12 follow-up)

The owner authorized implementation, including adapting existing library code.
Use arbitrary named selected entries, bounded parallel calls and additional
perspective investigations. The caller supplies perspective-specific investigation
prompts; all formal reviewers still receive the same complete review scope.
Investigations return ordinary data and never become approval ballots. Adding a
formal reviewer requires a new bound round, not inserting a vote into an old one.

The library may coordinate async host callbacks but contains no CLI subprocess,
native-spawn implementation, credentials, permission defaults or SDK dependency.
Host callbacks own actual provider capability checks, spawning and cleanup.
Preflight every selected entry before any review call. A concurrency bound and
per-entry timeout cover calls; cancellation must be awaited and cooperatively
handled by callbacks, which remain responsible for their processes. Return one
ordered outcome per entry without retries or dropping failed/dissenting entries.
After formal calls, obtain a fresh host integrity result before agreement.

Four explicit output carriers feed the existing strict admission API: native
final response, Claude JSON with native structured output, Gemini JSON response
string, and AGY stream JSON with native structured output. Preserve original
embedded JSON spans, including duplicate-member evidence. Check completion,
timeout, delivery failure, process exit and authoritative terminal fields first.
For the new single-shot AGY carrier, require exactly one terminal result and valid
JSON records; ambiguous/malformed streams are refused. This is stricter than the
existing host's last-complete-result extraction and is an explicit new adapter
contract, not a claim that either host already behaves that way. The shared C23
same-run recovery obligation still applies to adopting hosts; its observation
and recovery judgement are not implemented by this strict carrier. See the
[adoption boundary](../host-adoption.md#required-adapter-contracts). Do not
generalize an arbitrary AGY error into successful transport.

Fresh spec main was checked again at `396a04dac310d5ff91dbe0a36982f7679aa00428`.
Required canonical assets match the current `fcd96a1` pin, including newly fetched
roster, Claude/Google and investigation assets checked against that older ref.
Retain byte-preserved provenance. The executable plan is
[four-route core](../superpowers/plans/2026-10-12-four-route-core.md).

### Historical baseline before this implementation

The existing admission API already accepts the canonical three families and
both Google routes. The renderer and repository driver are still Codex/B only;
roster resolution, common agreement and classification are not implemented yet.
Earlier passing tests establish those earlier capabilities only.

The [CLI assessment](../research/2026-10-12-cli-feature-assessment.md) lists
verified current features, newly released changes, already-adopted mechanisms
and conditional experiments. This direction changes no shared spec, package
contract pin, dependencies, host configuration or global CLI installation.
