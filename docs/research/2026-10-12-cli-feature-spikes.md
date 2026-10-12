# CLI feature spike results

Date: 2026-10-12. Base: `6592488`. This follows the
[feature assessment](2026-10-12-cli-feature-assessment.md).
The owner deferred `openai-codex` to TODO and requested experiments on the other
candidates. These are feasibility findings, not production adapter adoption.

Probes ran in this library repository or its ignored `_runs/cli-spikes/`
children. Consumer repositories were read-only references. No product code,
dependencies, global settings, credentials or installed CLI versions changed.
No SDK was installed or executed. The Gemini workaround was neither replaced
nor retested. MCP-based implementations remain excluded.

## Decision list

| Candidate | Evidence obtained | Recommendation |
| --- | --- | --- |
| **Codex Python SDK (`openai-codex`)** | Earlier authentication/file-access research only; no new SDK execution | **TODO by owner direction.** Remove it from the active experiment order and prerequisites for four-route library work. |
| **Codex invocation-local configuration** | 0.160.0 offline checks: invalid known sandbox values fail; a valid `-c` override wins over an invalid synthetic user value. Non-strict unknown keys succeed. `--strict-config features list` fails as unsupported; root `--ignore-user-config` fails while `exec` help accepts it. | **Conditional candidate.** Use command-specific capability checks. Argument acceptance is not proof a setting took effect; ignoring user config is not complete configuration or MCP isolation. |
| **Codex native schema/final output** | Installed `exec` help recognizes `--output-schema` and `--output-last-message`; no successful inference/output fixture | **Retain as a transport candidate.** Preserve final bytes and common admission. Native enforcement and final-file/JSONL correspondence remain unverified here. |
| **Claude unattended permissions** | 2.1.289 accepts `--permission-prompts none`; one run exposed native read/search and structured-output tools, then failed on weekly quota before tool execution | **Conditional candidate.** Actual read/search completion and automatic denial need a later available-quota run. Do not retry now or change the existing default. |
| **Claude native structured output** | Live failure has `subtype=success` alongside `is_error=true`, `terminal_reason=api_error`, HTTP 429 and process exit 1 | **Retain with terminal checks.** Success subtype alone must not admit a result. Successful schema extraction was not exercised. |
| **Claude vendor retry delay** | Official 2.1.296 adds `CLAUDE_CODE_OVERLOADED_RETRY_MAX_DELAY_MS`; installed 2.1.289 binary has no matching literal | **Defer until a supported version is tested.** No variable injection, overload experiment or full-CLI retry. Literal absence is supporting evidence only. |
| **Claude bare/restricted modes** | Vendor docs say bare mode omits subscription OAuth/keychain. A restricted invocation started with four native tools and no MCP servers; quota prevented actual work | **No transparent bare default.** Restricted mode remains an isolation candidate, not proven equivalent to the existing environment. |
| **Claude session `--agents` file** | Previously documented flag support; not executed in this spike | **Defer.** No need demonstrated for the current single review call. This does not reactivate the removed agent-resolver backlog. |
| **Claude Python Agent SDK** | Official source wraps CLI execution and forwards schema configuration; no demonstrated advantage for one structured call | **Defer.** Typed APIs alone do not justify another dependency or authentication change. No install/execution. |
| **AGY typed errors/partial failures** | 1.3.3 startup errors use plain stderr and exits 1/2; no actual `AGY_ERROR` captured. Release notes describe runtime carrier/exit 3 and partial responses | **Conditional candidate.** Obtain a real runtime carrier before fixing field names/mappings. Retain startup-error handling; answer/tool text is not provider error authority. |
| **AGY native schema** | Startup rejects primitive name `string` and root `array`; the latter explicitly requires object, matching 1.2.14 | **Retain object-root schemas.** Successful extraction remains unverified. Do not broaden supported shapes from stale documentation examples. |
| **AGY deadline/process cleanup** | Installed help says default `0s` (unlimited); no timeout fired in startup probes. Release notes describe cleanup fixes | **Keep explicit deadlines and existing cleanup.** No signal, child-tree or Ubuntu test supports removing descendant handling. |
| **AGY explicit native search profile** | Existing host profile remains a read-only reference; no new execution | **Retain the existing profile.** No evidence supports replacing its explicit tool discovery or containment behavior. |
| **Gemini policy/JSON envelope** | 0.60.0 exposes `--policy` and JSON output. Existing policy rules have no mode clauses. Thirteen synthetic envelope/admission cases pass | **Keep explicit policy and existing workaround.** Extract the response once and retain strict admission; JSON output is not supplied-verdict-schema enforcement. |
| **Gemini/AGY persistent reviewers** | No runtime probe; retained independence requirement | **Exclude from formal independent review.** Reusing reviewer context changes the contract rather than merely simplifying transport. |

A small provider-specific extraction layer feeding common strict admission is
still the useful direction. Check terminal errors independently of answer shape.
These findings establish no new production API or permission profile; common
four-route roster/prompt/agreement remains the next implementation scope.

## Codex: offline configuration

Installed version: 0.160.0. Synthetic settings stayed in the ignored experiment
directory. Every exit was captured; no model request was sent.

| Probe | Exit | Observation |
| --- | --- | --- |
| `--strict-config features list` with unknown synthetic key | 1 | Strict config explicitly unsupported for this command |
| Non-strict `features list`, unknown file key | 0 | Unknown key accepted by bootstrap |
| Non-strict `features list`, unknown `-c` key | 0 | Unknown override also accepted |
| Invalid known `sandbox_mode` in synthetic settings | 1 | Enum validation rejects value |
| Invalid known value through `-c` | 1 | Override value also validated |
| Valid `-c sandbox_mode=read-only` over invalid synthetic value | 0 | Override precedence observed; not runtime containment |
| Root `--ignore-user-config --help` | 2 | Unexpected argument at that position |
| Combined `exec` config/output flags with `--help` | 0 | Argument recognition only; absent schema path not read |

Automatic approval review rejected an earlier batch of `codex exec` diagnostics:
intended early errors did not establish that authenticated requests could not
start without proven MCP isolation. None executed. The completed replacement
used offline commands; actual native output remains unverified.

Sources: [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli),
[non-interactive output](https://learn.chatgpt.com/docs/non-interactive-mode),
[configuration layers](https://learn.chatgpt.com/docs/config-file/config-basic).

## Claude: one quota-blocked live attempt

Installed version: 2.1.289. The invocation combined `--restricted --safe-mode`,
plan mode, `--permission-prompts none`, explicit Read/Grep/Glob tools, an empty
strict MCP configuration and an object schema. The only target was a synthetic
file in this repository's experiment directory.

The process exited **1 after 2.619 seconds**. Startup listed
`Glob,Grep,Read,StructuredOutput`, `mcp_servers=[]` and no slash commands/skills.
The weekly quota rejection had HTTP 429, zero input/output tokens and no tool
calls. It was not retried. These final-event fields occurred together:

```json
{"subtype":"success","is_error":true,"terminal_reason":"api_error","api_error_status":429}
```

The leader independently checked those fields and process metadata. This is a
terminal-error boundary case, not successful file access or schema extraction.
Built-in plugins remained listed; empty MCP startup does not mean every provider
internal was disabled. Effective inference model/effort were UNEXPOSED.

Sources: [CLI options](https://code.claude.com/docs/en/cli-reference),
[headless/bare behavior](https://code.claude.com/docs/en/headless),
[2.1.296 retry setting](https://github.com/anthropics/claude-code/releases/tag/v2.1.296),
[SDK transport source](https://github.com/anthropics/claude-agent-sdk-python/blob/main/src/claude_agent_sdk/_internal/transport/subprocess_cli.py).
The [SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) separately
restricts third-party products offering claude.ai login/rate limits without
prior approval. Personal CLI login does not establish a deployable SDK auth path.

## AGY: three startup validations

Installed version: 1.3.3.

| Probe | Exit | Elapsed | Output |
| --- | --- | --- | --- |
| Unknown option | 2 | 0.0467 s | Plain stderr usage error |
| `--json-schema string --output-format json` | 1 | 0.0432 s | Invalid JSON error |
| `--json-schema '{"type":"array"}' --output-format stream-json` | 1 | 0.0475 s | Object-root requirement |

Schema probes specified `--print-timeout 1s`. Every stdout was empty; none
emitted `AGY_ERROR` or reached a deadline. These prove startup validation only.
Checked invocation/profile interfaces did not establish suppression of every
inherited MCP/hook startup surface, so no inference request was submitted.

The [release history](https://raw.githubusercontent.com/google-antigravity/antigravity-cli/main/CHANGELOG.md)
documents runtime carriers from 1.2.6, partial-error exit 3 from 1.2.10,
object-root schemas from 1.2.14 and earlier process cleanup changes. The
[headless guide](https://antigravity.google/docs/cli/headless/) disagrees with the
installed binary about primitive names and the default deadline. No real typed
failure fixture or new classifier was invented for this spike.

## Gemini: offline response extraction

Installed version: 0.60.0; version/help only, no plan-mode or inference run.
Static inspection found three mode-independent policy rules and SHA-256
`01a267f591518964e30f94ffc45d496aae594435678380179b679d1aa8de189b`.
This did not execute the vendor policy engine.

A throwaway driver parsed a synthetic envelope, checked terminal/error state,
and passed its original `response` string to `validate_verdict` without parsing
and re-serializing the inner string. **13/13 cases passed**: valid and negative
verdicts; prose/fences; stale attempt/sibling route; inner/outer duplicate members;
error alongside answer; nonzero exit alongside answer; missing response; object
instead of response string; truncated envelope. Negative verdicts stayed admitted
negatives rather than approval or parse failure.

Sources: [headless envelope](https://geminicli.com/docs/cli/headless/),
[policy engine](https://geminicli.com/docs/reference/policy-engine/).
Workspace policy loading is still documented as inactive. Keep explicit injection
and the owner's workaround rather than assuming project-directory loading.

## Evidence and limits

Throwaway scripts, exact commands, help and results remain in ignored
`_runs/cli-spikes/{codex,claude,agy,gemini}/`; they are not shipped code, public
provider logs, permanent fixtures or CI tests. Aggregate results above remain
readable without those local files. Provider/Python commands used the required
`/bin/zsh -lic` and `sandbox_permissions=require_escalated`; all launched command
sessions terminated.

This workstation is macOS 26.6.2 ARM64, Python 3.12.13. No Ubuntu CLI run occurred.
Earlier native Ubuntu/macOS library CI is separate evidence and does not certify
provider features. No host adoption, CLI upgrade, release or global installation
follows from these experiments.

Repository verification after the documentation changes: `uv sync --locked`,
`uv run --locked pytest -q` (**157 passed**), `git diff --check`, and **16**
relative documentation links checked. These are library/documentation checks,
not additional provider runs. Independent scoped review identified two minor
documentation gaps: omitted candidate dispositions and imprecise schema wording;
both were corrected without changing experiment results.

## Deferred TODO: openai-codex

When reactivated, use a separate optional experiment here: existing ChatGPT login
reuse; MCP-free startup; explicit cwd, read/write roots and approvals; original
final bytes and schema handling; cancellation; native macOS/Ubuntu behavior.
Compare complexity against the fresh native test path before adding dependencies.
This TODO is not a prerequisite for deterministic four-route library work.
