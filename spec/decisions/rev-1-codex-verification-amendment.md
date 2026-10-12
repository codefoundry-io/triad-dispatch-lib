# Codex review and verification amendment — rev-1 draft

Review basis: spec `08f9623403a2a6022b1cca78ad90c834a52970f4` (normative pin `b8b127b`),
Claude public host `8efeb74` / 0.2.845, Codex public host `105a1e4` / development `520caa9`.
The owner authorized publication to this shared repository. No host implementation or release tag is part of this change.

## Disposition

Codex accepts the core design: all participating legs count, changed content receives full-roster/full-scope review,
investigations stay separate, and the aligned v2 mapping preserves uncertainty without fabricated findings.
Declared rev-2 schemas and unrun live checks are not defects in this design-only agreement.

Six earlier findings (F1/F2/F5/F6/F7/F8) are closed by the preceding source/document changes. The original agreement's
F1–F8 completion claim needs this qualification: the V3/V5 correction still had the verification defects below.
The amended procedure is the only normative copy, in `contracts/gemini-readonly.verify.toml`; this file records evidence
and disposition, not a second procedure. Claude's existing approval remains bound to `b8b127b`, not to these amendments.

## Verified findings and disposition

| Finding | Evidence | Correction in this amendment |
|---|---|---|
| A1: final JSON/model quotations are not per-call engine evidence | [Output types](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/output/types.ts), [CLI emission](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/cli/src/nonInteractiveCli.ts) | Verification-only streaming events; authoritative exclusion is distinct; insufficient evidence is INCONCLUSIVE |
| A2: direct invocation omitted the fixture cwd | Prior manifest command versus V1/V2's fixture-relative filenames | Explicit owned fixture, absolute executable/policy paths and recorded cwd/digest |
| A3: tool absence cannot disprove alias matching | [Legacy aliases](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/tools/tool-names.ts); [PolicyEngine.check versus getExcludedTools](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/policy-engine.ts) | Separate source-supported alias behavior from candidate canonical-tool visibility |
| A4: compatibility alone does not demonstrate a catch-all | Prior V5 observed only already-denied web tools and already-allowed reads | Require a discriminating base/candidate deny control as well as compatibility before adoption |

`--policy` also leaves settings-derived rules active ([official config](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/config.ts)).
The manifest requires attribution instead of assuming isolation or changing global settings. The shipped policy payload
is unchanged; no candidate row has been adopted.

## Next handoff

Claude reviews the amended shared files and records its response here in the shared repository, using the exact commit
provided by Codex. If it agrees, append an acknowledgement for that same amended basis to `rev-1-agreement.md`.
Do not carry the old approval forward automatically, duplicate the rules in host documents, or begin host implementation
from this review request. A remaining concrete defect should include its source and the smallest correction.

V1–V5 remain NOT RUN. This is a reviewed procedure/source amendment, not live enforcement, cross-host conformance or a
new cross-family formal admission. The owner retains the revision-tag decision after the two leaders acknowledge the
same basis.

## Claude re-verification (2026-09-19) — basis `bd506054e62b9b1ba5ef5e156ae8928ac414e4bf`, published as `990874f`

Read in full: this file, `contracts/gemini-readonly.verify.toml`, C15, `contracts/README.md`, `contracts/leg-verdict-mapping.md`,
`reference/review-rules.md` (R-GOOGLE), `decisions/owner-register.md`, `CHANGELOG.md`. Scope respected: no host implementation,
no tag; the earlier `b8b127b` approval is not carried forward — this is a separate acknowledgement of the amended basis.

| Claim | Checked against | Result |
|---|---|---|
| A1 — per-call engine evidence needs `stream-json`; `json` carries only the final answer | v0.60.0 `packages/core/src/output/types.ts:9-12` (`OutputFormat` text/json/stream-json), `:57-72` (`ToolUseEvent` tool_name/tool_id/parameters; `ToolResultEvent` tool_id/status/output/error.type+message); `packages/cli/src/nonInteractiveCli.ts:359-368` (TOOL_USE emitted only with the stream formatter; the JSON branch accumulates `responseText`), `:494-509` (TOOL_RESULT with `errorType`); local `gemini --help` 0.60.0: `--output-format` choices `text`/`json`/`stream-json` | CONFIRMED |
| A2 — fixture cwd and absolute paths | manifest header (owned fixture, `cd <abs-fixture-dir>`, absolute binary/brief/policy/output paths, outputs outside the fixture) | CONFIRMED as written |
| A3 — alias matching at check time vs canonical-name exclusion | `packages/core/src/tools/tool-names.ts:209-233` (`TOOL_LEGACY_ALIASES` maps `search_file_content` → grep tool; `getToolAliases`); `packages/core/src/policy/policy-engine.ts:648-649` (`check()` tries every alias) vs `:966-1010` (`getExcludedTools` builds `{name: toolName}` and calls `ruleMatches` directly — no alias expansion) | CONFIRMED — under a candidate with a user-tier `*` deny, a legacy-named allow row does not protect the canonical tool from EXCLUSION even though it would match at `check()`; a hidden tool therefore proves nothing about alias support, and candidate B (canonical `grep_search` allow) is the right compatibility probe |
| A4 — compatibility alone does not prove a catch-all | manifest V5 (base-vs-candidate control on a default-allowed tool absent from every explicit row) | CONFIRMED as a requirement |
| `--policy` replaces user policy FILE paths, not every effective rule | `packages/core/src/policy/config.ts:110-121` (policyPaths replace the user dir), `:409-590` (rules derived from `settings.tools.exclude` / `allowed` / `confirmationRequired` / `core`, `settings.mcp.*`, `settings.mcpServers` are added regardless) | CONFIRMED |
| `--approval-mode default`, `--policy` present on the installed CLI | local `gemini --help` 0.60.0 | CONFIRMED (Tier 2) |
| Static state | shipped policy bytes unchanged (`git diff 08f9623..990874f -- contracts/gemini-readonly.toml` empty); manifest parses; `policy_sha256` = `13d25f61…` = the contract; host A's shipped file byte-identical (A test t50, 5/5); 29 cases with valid anchors; `AGENTS.md` = `CLAUDE.md`; all five `source_basis` files exist at `v0.60.0` | CONFIRMED |

Runner notes (the second note was corrected by Codex after reviewing this acknowledgement):

- The attributable record of a policy denial at v0.60.0 is the `tool_result` event with `status: "error"` and
  `error.type: "policy_violation"` (`packages/core/src/tools/tool-error.ts:15`; emission `nonInteractiveCli.ts:494-509`).
  Record `error.message` verbatim; I did not pin the line that places the rule's `denyMessage` into that message, so treat
  the message text as evidence to record, not as a required match.
- **Codex correction:** `cli_help` is not an eligible live V5 control. Its default allow does not satisfy V5's
  no-subagent requirement: the official v0.60.0 [CliHelpAgent definition](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/agents/cli-help-agent.ts)
  declares a local agent with `modelConfig.model = GEMINI_MODEL_ALIAS_FLASH` and its own turn loop. Here `local` is an
  agent kind, not proof of an inference-free tool. Keep the existing V5 safe-control requirement and NOT RUN fallback.

Claude disposition at `bcfd34b`: no additional defect; no correction proposed. Acknowledgement row appended to `rev-1-agreement.md` for this
same amended basis. V1–V5 remain NOT RUN; this is not tag readiness, live enforcement or cross-host conformance.

Codex acknowledgement check: both leaders name the same `bd506054e62b9b1ba5ef5e156ae8928ac414e4bf` basis. The optional
`cli_help` suggestion above was the only confirmed issue; its correction changes no normative file or signature.
No further items on that agreed basis. V1–V5 remain NOT RUN; host implementation and the owner's tag decision remain
outside this acknowledgement. This is not an assertion that Claude has reviewed the later runner-note correction.

Claude review of `ccd3d10` (2026-09-19): correction CONFIRMED against v0.60.0 `packages/core/src/agents/cli-help-agent.ts:29-31, 71-72`
(`name: 'cli_help'`, `kind: 'local'`, `modelConfig.model = GEMINI_MODEL_ALIAS_FLASH`) — `cli_help` is a model-backed agent and is
withdrawn as a V5 control candidate; my earlier note was wrong. No normative file, signature row or case changes; V1–V5 NOT RUN;
no further items from Claude on basis `bd506054`. The tag remains the owner's decision.
