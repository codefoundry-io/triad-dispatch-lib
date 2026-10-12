# CLI features and simplification assessment

Date: 2026-10-12. Research only. The owner requested concurrent web research of
Codex, Claude Code, Gemini CLI and Antigravity CLI (AGY) before choosing useful
updates for the common library. Official pages were opened after search; three
independent research children covered Codex, Claude and Google, and the leader
checked the primary sources and local version-only output.

## Evidence and release status

The source comparison uses B commit
[`d0f32ad89be037884d39a48bfcec123358e8f4c3`](https://github.com/codefoundry-io/triad-codex-dispatch/tree/d0f32ad89be037884d39a48bfcec123358e8f4c3).
It is a read-only comparison, not a new execution of B's wrappers. Library HEAD
before this documentation change was `80a2fc4f76db9d5af8cd343b9fc1ec6c3314eb53`.
No inference, upgrades, installation, authentication inspection or host tests
were performed for this assessment.

| CLI | Installed, version-only observation | Latest stable release evidence |
| --- | --- | --- |
| Codex | 0.160.0 | Not independently settled. Official documentation search reports 0.162.1 dated October 9, but the opened changelog HTML omitted CLI entries and its Markdown endpoint returned 404. Treat that number as a search observation, not a verified upgrade target. |
| Claude Code | 2.1.289 | [2.1.296, October 9](https://github.com/anthropics/claude-code/releases/tag/v2.1.296), also checked through the repository's latest-release API. |
| Gemini CLI | 0.60.0 | [0.63.0, October 6](https://github.com/google-gemini/gemini-cli/releases/tag/v0.63.0), confirmed by the [stable documentation](https://geminicli.com/docs/changelogs/latest/). |
| AGY | 1.3.3 | [1.3.3, October 10](https://github.com/google-antigravity/antigravity-cli/releases/tag/1.3.3). The vendor website's CLI changelog still labels 1.3.1 latest; prefer the actual upstream release for this comparison. |

Current documentation support is distinct from a newly introduced feature.
Where an introduction version is not established below, do not advertise it as
a recent release addition. An installed flag also does not prove account access
or effective model/effort selection.

## Ranked candidates

Priorities are recommendations for experiments, not adopted dependencies or
permission changes. "Already used" refers to the inspected B host.

| Priority | Feature and evidence | Current state and proposed benefit | Constraint / disposition |
| --- | --- | --- | --- |
| High | **Codex Python SDK**: stable `openai-codex`, `Codex` / `AsyncCodex`, thread calls and `Sandbox.read_only`. [SDK](https://learn.chatgpt.com/docs/codex-sdk) | A candidate for the library repository's optional Codex test transport; could remove hand-written subprocess or JSON-RPC handling. Introduction version unconfirmed. | SDK builds pin a CLI runtime; an explicit `CodexConfig(codex_bin=...)` selects a different local binary. Keep it out of the deterministic core until an isolated comparison proves value. B's current Codex path is native spawning, not a CLI wrapper. |
| High | **AGY typed failures**: 1.2.6 adds stderr `AGY_ERROR` JSON; 1.2.10 fixes partial-response failures to exit 3. [Changelog](https://raw.githubusercontent.com/google-antigravity/antigravity-cli/main/CHANGELOG.md) | No dedicated `AGY_ERROR` parser was found in B's common helper. A versioned adapter could extract typed failure evidence before shared classification, reducing phrase matching. | Verify real carrier fixtures and mapping before changing classification. The common core must not classify arbitrary answer or tool text as provider errors. |
| High | **Gemini 0.63.0 headless plan execution and reliability fixes**. [Stable notes](https://geminicli.com/docs/changelogs/latest/) | Current B already requires stable >=0.63.0 and uses plan mode; installed 0.60.0 is below that floor. Evaluate the supported version before designing compatibility machinery. | Autonomous plan execution is not proof of read-only containment. Retain explicit tool policy; no upgrade was performed. |
| Medium | **Claude 2.1.296 vendor backoff control**: `CLAUDE_CODE_OVERLOADED_RETRY_MAX_DELAY_MS`; headless disabled-MCP handling also fixed. [Release](https://github.com/anthropics/claude-code/releases/tag/v2.1.296) | Vendor request retry control supports keeping the outer adapter to one invocation. | Do not inject this environment variable by default or restart an entire CLI as a substitute. Preserve the shared terminal/retry contract. |
| Medium | **Codex invocation-local configuration**: `--ignore-user-config`, `-c key=value`, `--strict-config`. [CLI reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli) | Candidate for reproducible library tests and early rejection of unsupported keys. First release unconfirmed. | Ignoring user config does not erase every project/managed layer; authentication still uses `CODEX_HOME`. Preserve effective permissions and owner settings. |
| Medium | **Claude unattended permission handling**: `--permission-prompts none`, since 2.1.259. [CLI reference](https://code.claude.com/docs/en/cli-reference) | Vendor denies unanswered permission requests, avoiding a custom permission conversation in unattended adapters. Not currently passed by B. | It changes denial behavior and is separate from plan mode. Probe the actual review read/search workflow before adoption. |
| Medium | **AGY native process and deadline behavior**, including 1.1.24 pipe inheritance and 1.2.9 headless cleanup fixes. [Changelog](https://raw.githubusercontent.com/google-antigravity/antigravity-cli/main/CHANGELOG.md) | Evaluate whether compatibility code is still needed at the supported version. `--print-timeout` is already passed. | Keep direct-call cancellation and complete-result validation. A changelog cannot prove all descendants terminate after every crash. |
| Retain | **Native structured output**: Codex `--output-schema` / `--output-last-message`; Claude and AGY `--json-schema`. [Codex automation](https://learn.chatgpt.com/docs/non-interactive-mode), [Claude output](https://code.claude.com/docs/en/agent-sdk/structured-outputs), [AGY headless](https://antigravity.google/docs/cli/headless/) | Claude/AGY already use native schema output. Prefer one final-result extraction and shared strict admission over extra formatting-repair loops. Codex CLI controls are a test-transport option. | Gemini's JSON envelope is not equivalent to enforcing a supplied verdict schema. All routes still need TRIAD's six bindings and negative-verdict handling. |
| Retain | **Gemini policy engine** and **AGY explicit native search profile**. [Gemini policy](https://geminicli.com/docs/reference/policy-engine/), [AGY permissions](https://antigravity.google/docs/permissions?tab=cli) | Already used. Preserve supported native controls rather than duplicate a tool-policy engine in Python. | Gemini workspace policy tier is documented as inactive; do not replace explicit policy injection with a project-directory assumption. AGY's explicit discovery profile remains necessary under the current contract. |
| Conditional | **Claude `--bare` / `--restricted` and session `--agents` file**. [Bare mode](https://code.claude.com/docs/en/headless#start-faster-with-bare-mode), [CLI](https://code.claude.com/docs/en/cli-reference) | Useful for explicit isolated experiments. Complete bare-mode behavior is documented from 2.1.286; `--agents` file form with print mode from 2.1.281. | Bare mode omits subscription OAuth/keychain; restricted mode changes tool access. Neither is a transparent default for current subscription-backed review. Do not reactivate the removed optional Claude agent-resolver backlog. |
| Conditional | **Claude Python Agent SDK**. [SDK release 0.2.165](https://github.com/anthropics/claude-agent-sdk-python/releases/tag/v0.2.165), [Python API](https://code.claude.com/docs/en/agent-sdk/python) | Typed results/settings/permissions can help a richer client. That SDK release bundles CLI 2.1.294, below latest standalone 2.1.296. | An SDK still uses CLI execution and does not replace TRIAD admission/agreement. No demonstrated benefit over B's existing single structured call yet. |
| Defer for formal review | **Persistent conversations/resume** in Gemini and AGY. [Gemini CLI](https://geminicli.com/docs/cli/cli-reference/), [AGY headless](https://antigravity.google/docs/cli/headless/) | Can reduce startup cost for ordinary multi-turn investigations. | Do not reuse reviewer context across independent legs or new review bases. This would change independence, not merely optimize transport. |

## Findings that alter the previous research basis

The prior B audit cited AGY 1.1.28 daemon preservation. AGY 1.2.9 later changed
headless daemon termination and background waiting. That older statement must
not justify current process-management design. The headless documentation also
describes a five-minute default while the 1.2.6 changelog says unlimited;
continue passing an explicit deadline. These are documentation/version findings,
not live reproductions. See the [version history](https://raw.githubusercontent.com/google-antigravity/antigravity-cli/main/CHANGELOG.md).

Requested effort is not necessarily effective effort. Claude's
`CLAUDE_CODE_EFFORT_LEVEL` can override `--effort`, and organization limits can
clamp effort without a JSON-mode warning. Keep requested settings distinct from
observed runtime fields, leaving unexposed values unknown. Do not add an alias
catalog or assume an argv proves the effective model.
[Environment precedence](https://code.claude.com/docs/en/env-vars#precedence),
[organization limits](https://code.claude.com/docs/en/model-config#organization-effort-limits).

## Implications for the library and tests

Keep Python 3.12 and the existing deterministic dependency set. None of the
verified features establishes a reason to rewrite the core in Rust. A Python
SDK makes a Python transport experiment more attractive, but is not itself a
reason to add runtime dependencies for users who only validate verdicts.

Use four named test entries, with both Google routes explicitly pinned. Test
roster resolution, prompt profiles, strict result admission and unanimity in the
library repository first. Then compare one optional Codex SDK transport against
the current fresh native test path, measuring raw-result preservation, startup,
settings, terminal failures and cancellation. Provider-specific versions and
capabilities belong to adapters; unsupported options must be reported, not
silently translated or dropped. CLI envelope extraction and common classification
are distinct responsibilities.

The library's existing native CI evidence covers Ubuntu 24.04 x86-64 and macOS15
ARM64 with Python3.12. It does not certify every CLI/SDK. Gemini documents
macOS15+, Ubuntu20.04+ and Node20+; the Codex Python SDK needs Python3.10+; AGY
documents native macOS/Linux support without an exact minimum OS on the opened
CLI installation page. Validate adapters on both target platforms separately.
[Gemini requirements](https://geminicli.com/docs/get-started/installation/),
[Codex SDK](https://learn.chatgpt.com/docs/codex-sdk),
[AGY installation](https://antigravity.google/docs/cli/install/).

Recommended order: four-route core configuration and agreement; optional Codex
SDK experiment; typed AGY failure fixtures; supported-version CLI checks. Consumer
ports, global upgrades and adoption of new permission modes remain separate from
this research. No runtime or dependency change is claimed by this document.
