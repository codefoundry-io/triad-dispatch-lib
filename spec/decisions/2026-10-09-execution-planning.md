# Shared implementation planning and new investigation evidence

Status: authoring follow-up, 2026-10-09. Facts and proposals below do not
claim merge, adoption, release, live service acceptance or a changed model-name
grammar. Current remote main `3afc4d7`, PR #12 `1a5ab9a`, PR #13 `cff8a20` were
rechecked. Both PRs remain open. Each host is implementing concurrently.

## Owner direction and cooperation

Owner, direct Codex session instruction, 2026-10-09:

> claude도 같은 스펙으로 구현을 진행중에 있다는 것을 참고로해 스펙만 존재하고 아직 반영 안된 부분이 있어

The owner requested specification review, a staged execution plan, and bounded
spikes or primary-source research for the five questions below. A pending host
implementation is not by itself a defect or evidence that the rule is wrong.
Check each current rule, code path and measured fact; amend a missing common
contract before dependent code. Claude code is evidence, not presumed authority.
Each host's native leg remains host-owned.

For prompt work the owner specified contextual defects and minimal instructions;
when repeated findings concern fine grammatical/wording nuance, observe choices
in fresh Luna/high scenario/control simulations. This is the Codex task's
development method, not a new shared reviewer-model requirement or an exemption
from either host's existing review gates.

## Evidence dispositions

| Question | Finding | Action and owner |
|---|---|---|
| AGY credits carrier | Vendor changelog 1.2.15 supplies the sentence, not channel/exit. General headless docs describe stdout responses, stderr diagnostics and structured errors; changelog 1.2.6/1.2.10 describes model/API failures with `AGY_ERROR`/3. The specific credits condition is not linked to that path. | Both hosts keep the phrase evidence and unmeasured carrier separate. Supply an existing sanitized capture or record a naturally occurring event; do not exhaust quota or infer the missing fields. |
| DL-103 AGY schema | Current dirty B `bin/verdict_v2.py:45-46` narrows the bound route to `['agy']`; the actual AGY v2 emission no longer has the old null enum. Other schema keywords remain. A's projection is not evidence that every omitted keyword is rejected by AGY. | Update DL-103's current observation when reconciling the rows. B retains a pending live acceptance check; do not reimplement the already-present narrowing. |
| DL-124..126 | Inspected A per-attempt hook attribution, stream simplification and single audit publication are present. Corresponding removed mechanisms are absent in B or already match the described parser behavior. | No new B port identified. A/spec maintainer reconciles historical pointers and cases without claiming total A/B stream-admission equivalence. |
| DL-110/121 | Four current spec descriptions still attribute a Claude CLI route/extractors/tests to A after that route's removal. PR #12 records but does not yet apply all corrections. | Keep `task-blocked` membership; identify B as Claude-wrapper producer; correct A extractor count and C35/37/43 references. A confirms surviving exact test axes/counts. No B Claude-wrapper removal. |
| Model strings shaped like options | Actual Gemini 0.63.0 parser, isolated from provider startup: separate `--model --help` activates help; `--model --yolo` fails parsing; equals-form values remain strings. AGY/Claude help-only observations do not expose resolved model values. | Proposed R-MODEL transport clarification below. No blanket syntax ban or product change in this follow-up. |

Current A source was inspected at `32124be528ab736cad6ac8d8f76990d99bdf3556`;
concurrent source may advance. The named hook/stream/audit files were clean at
inspection; another A test was dirty. B remains `632f426` plus preserved dirty
work. Provider-free B schema modules passed 95 tests with 4 skips, Python
3.12.13/pytest 9.0.3. Fixtures replace vendor execution; no live acceptance claim.

Primary references:

- [AGY changelog](https://github.com/google-antigravity/antigravity-cli/blob/main/CHANGELOG.md)
  (1.2.15 sentence; 1.2.6/1.2.10 general model/API failure behavior).
- [AGY headless errors](https://antigravity.google/docs/cli/headless/#handle-exit-codes-and-errors).
- [Gemini 0.63.0 parser source](https://github.com/google-gemini/gemini-cli/blob/v0.63.0/packages/cli/src/config/config.ts).
- [Official 0.63.0 npm artifact](https://registry.npmjs.org/@google/gemini-cli/-/gemini-cli-0.63.0.tgz),
  SHA-256 `97a6edfc10645463b517f0518d46a8c72efbdc12558a9a948607f726284a0420`.

## Proposed clarification: preserve an opaque model value

Existing requirement: R-MODEL passes the user's explicit pin as written, without
catalog membership gating. Current B uses separate model-option/value tokens
both at Python-wrapper boundaries and in vendor argv. Separate tokens avoid
shell expansion, but do not alone establish lossless option-parser transport.

Evidence: the spike preserved the actual bundled yargs and `parseArguments`
from Gemini 0.63.0, with external startup helpers inert. Separate `-m --help`
and `--model --help` exit 0 through help; separate `--yolo`/`--made-up-model`
values exit 1 for a missing model argument. `--model=...` preserves those values
and does not set yolo. Unknown names and spaces/newlines/tabs inside one token
are also preserved by the measured parser. No inference or permission escalation
was demonstrated. NUL and arbitrary other controls were not tested.

Proposed observable requirement: each host transports the pin as one opaque
model-option value across every wrapper/vendor parser boundary; a value that
resembles another option does not activate that option. A vendor may still
reject the model as unavailable, producing the existing one terminal outcome.
This adds no supported-model list or shared naming grammar. Equals encoding is
a candidate implementation, not a mandated universal spelling: verify each
actual parser before using it.

Features to preserve: unknown ordinary pins, requested/observed identity
separation, CLI floor and capability checks, authentication/containment, exact
receipt bindings, no silent model/route substitution and no repair retry merely
for an unavailable model. Test the Python-wrapper boundary as well as the vendor.

Request to the other maintainer: review this evidence against the same shared
revision, inspect A's model argv construction, and identify an existing common
case or add the boundary to C18/C34 after agreement. Report exact parser/version
evidence for AGY/Claude if available; a help-only exit cannot prove the model
value that inference would receive. Codex keeps dependent product changes out
until the shared disposition and applicable gates are satisfied.

## Documentation reconciliation requests

### U1a selection-observation boundary (Codex implementation candidate)

R-ROSTER requires refusal of a **reported contradiction**, while R-MODEL
forbids catalog admission. For the bounded B correction, separate the requested
pin, raw selection output, and identity components actually exposed by that
output. A known display label may retain a display-only catalog alias in the
receipt; catalog omission must neither refuse the request nor fabricate an ID.
An unrecognized label is retained as an observation, not asserted to match the
requested identity. Absence of a demonstrated contradiction is not identity
attestation. A display label without a dated suffix cannot attest that suffix.
Likewise, an explicit reported effort contradiction refuses; silence is not
proof of per-model effort support. Keep the required CLI controls and vendor
refusal boundary. This interpretation adds no model-name grammar or model list.

B's U1a candidate compares exposed full IDs exactly and recognized family/version
components independently of the packaged table. It retains raw output and the
unchanged request; its receipt scope is `cli-selection`. Synthetic adapter tests
exercise missing catalog rows, alias/full-ID contradictions, unknown labels and
effort observations. These tests do not establish new vendor output formats.
The candidate is not yet reviewed, adopted or released. Default alias migration
and external-agent binding remain separate U1b work.

Maintainer request: check this observation/attestation distinction against the
common contract and flag contradictory evidence or a required fail-closed rule
for unexposed identity before broader adoption. A's native Claude path exposes
no selection to compare and is not asked to acquire a new probe or change its
host leg. The candidate does not claim complete C34 or per-model support.

U1a completion, 2026-10-09: B's local candidate at base `632f426` now removes
the Claude model/effort catalog admission gate, retains the wrapper effort
vocabulary and CLI control checks, and refuses exposed selection contradictions.
Requested values and raw output remain separate. Final production delta is
+60/-19/net +41. Adapter SHA-256:
`aa7444dcbf5ca1c7ecd4c3c2339b55363be06e1c1cf8a4790ab23a8427376747`.
The product candidate remains uncommitted, uninstalled and unreleased.

The first review found two header-parsing defects, reproduced and corrected.
Final affected suite: 99 passed, including 32 selection cases, Python 3.12.13 /
pytest 9.0.3 on macOS arm64. The earlier full run passed 1,881 tests with 4 skips;
that full run precedes the bounded parser corrections. Historical CLI 2.1.282
receipt output was located: `Set model to \`Opus 5.5\` for this session only\n`
under explicit `claude-opus-5-5` / `xhigh`, `provider_started: false`. This
establishes that historical format, not current-version or runtime attestation.

Fresh round `triad-claude-selection-20261009-r2`: Claude, Google Pro, Google
Flash and fresh Codex Astra all SAFE, matching final fingerprint, exact temporary
stage/cwd cleanup complete. Digest:
`8ebf2c475aa49fd9c32606a1f0763c839dbb7de4c5f52d58fdcaa345455895db`.
An optional proposal to parse unobserved version-less labels remains deferred.
U1b alias defaults / external-agent binding and the rest of the execution plan
remain pending. Neither host's native leg was changed. This is bounded B
implementation evidence, not a shared revision adoption or complete conformance.

- PR #12's body/title only names early phases while its files now record
  DL-118..126. Distinguish completed source work from pending rule/case edits.
- PR #13's original body says no normative change and cites the first failed
  C43 round. Its later commits contain D-GEMINI-FLOOR-20261009 and successful
  bounded review evidence. Rewrite the description around the final scope when
  publishing this follow-up; do not erase historical failed evidence.
- DL-121: update the exit-token note, A's extractor description and C35/37/43
  test pointers. Confirm remaining test axes with A rather than guessing counts.
- DL-124..126: preserve earlier DL-6/10/11/12/13 as history and append the
  current limits/removals; align C1/C23/C36 and the `read-audit-file:` custody
  description with A's actual code.
- Current B findings and completed Google/quota work supersede stale OPEN-B
  observations only within their demonstrated scope. Neither PR is full host
  conformance, and a pending A implementation is not a reason for B to diverge.

## Execution entry: B parser and selection diagnostics

After the owner approved proceeding, B ran provider-free checks against current
source (`632f426` plus the existing dirty candidate), Python 3.12.13/pytest 9.0.3.
No product code or native-leg behavior changed for these diagnostics.

The real `argparse` parser in each of B's three wrappers was invoked, then
stopped immediately after parsing and before binary resolution or any dispatch.
Across 24 combinations (three wrappers, four values, two encodings), separate
`--help`/`--yolo` model values refused with parser exit 2; equals encodings
preserved every tested value. Ordinary unknown names and a spaced value were
preserved in both forms. This extends the Gemini-vendor evidence to the B
wrapper boundary; it is not AGY/Claude vendor parser evidence.

The current Claude adapter also produced **3 expected RED failures / 2 passing
controls** against C34/R-MODEL:

1. An `opus` request accepts the contract's contradictory Sonnet selection.
2. Omitting the informational Opus 5.5 data row makes its otherwise-valid
   existing selection fail the table-dependent identity/capability path.
3. With that row omitted, requested `claude-opus-5-5` can match the shorter
   `claude-opus-5` row and accept reported Opus 5.

Controls retain the normal Opus alias selection and explicit null selection.
The fixture uses existing selection forms and the C34 negative example, not
invented vendor error carriers. The data-row omission tests local catalog
dependency, not a live vendor release or service result.

Before removing the table gate, resolve how C34 treats unexposed selection or
effort evidence: never infer an identity from a label not established by evidence.
R-ROSTER still expressly names B's selection check; R-MODEL disallows a model
availability probe. The implementation must preserve their intended distinction,
not silently remove selection validation or add paid probing. Current official
[Claude model documentation](https://code.claude.com/docs/en/model-config)
describes aliases and interactive `/model` persistence; it does not by itself
establish the side effects of B's print-mode invocation. Historical B 2.1.282
selection evidence remains historical, not proof for every installed version.

The three RED cases are concrete B findings; A's native Claude path is not
implicated. Required independent diagnosis and bounded unit review remain
before treating a remedy as admitted. Detailed diagnostics and the copyable
maintainer request are retained by B at `_runs/spec-plan-20261009/u1/`,
`_runs/spec-plan-20261009/model-argv/wrapper-boundary-results.json`, and
`docs/status/2026-10-09-claude-maintainer-prompt.md`.

The Codex execution plan is in its source repository at
`docs/superpowers/plans/2026-10-09-shared-spec-execution.md`; its live SoT remains
`docs/status/spec-to-code-sot.md`. Detailed local parser and schema evidence is
retained under `_runs/spec-plan-20261009/`. Those files are evidence, not an
additional shared runtime interface or installed instruction.
