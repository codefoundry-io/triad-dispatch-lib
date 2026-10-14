# Route-specific agent scope

Owner clarification, 2026-10-09. This clarifies existing route ownership and
scheduling; it does not remove optional CLI compatibility or adopt a revision.

Owner: "leg 별로 다르게 봐야지 ㅁgy는 agent를 써야하는 이유가 있는데 claude codex leg도 그게 필요하냐고"
Follow-up: "이걸 오해하지 않도록 스펙에 명확히 기록하고 다음 단계 가자"

The shared invariant binds controls actually used by a review. It does not require
the same provider mechanism for every family. R-AGENT-ROLES is the normative
clarification; C73 separates the default paths and optional-selection control.

Evidence: B `contracts/review-legs.default.json:7` has `agent: null`, and
`bin/review_adapters_v2.py:_claude` appends `--agent` only when non-null, otherwise
passing model and effort directly (632f426 plus current dirty source). On A,
`3rd-Agent/wrappers/codex_wrapper.py:352-354` passes model/reasoning CLI config;
its native Claude preset/spawn is host-owned (`lib/roster_v2.py:CLAUDE_WEB_TWINS`,
`references/leg-contracts.md:134-143`), inspected at 0e04d2a. AGY's distinct need
for native search tools and actual recovery proof are recorded under C72.

Current planning disposition: no named-agent need is established for B's Claude
CLI path. The owner removed the resolver task from active and deferred plans
under D-NO-CLAUDE-AGENT-BACKLOG-20261009. Existing optional support is not proof
of a requirement to develop it; no resolver research or re-entry checklist remains.
The existing optional interface and its conditional bind-or-refuse contract are
unchanged, without a full-conformance claim. No native-leg change or A port.

Claude maintainer: review the same clarification commit for the distinction
between your native Claude presets, your external Codex CLI, and AGY profiles.
No copying of native implementation or new agent prerequisite is proposed.

## Read/search capability verification

Owner follow-up: "codex claude 에서 읽기 도구 기본 활성화 맞지? 다시 웹검색 과 기능 여부 확인해봐"

Official pages fetched 2026-10-09:

- [Claude tools reference](https://code.claude.com/docs/en/tools-reference):
  Read reads file content. Current macOS/Linux/WSL defaults omit dedicated
  Glob/Grep, using shell search instead; their absence is not loss of search.
- [Claude CLI reference](https://code.claude.com/docs/en/cli-reference): `--tools`
  changes the tool inventory; `--allowedTools` controls prompt-free permission.
  [Plan mode](https://code.claude.com/docs/en/common-workflows#plan-before-editing)
  supports file inspection.
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode):
  `codex exec` supports codebase inspection, defaults to read-only, and exposes
  command-execution events. [Sandbox modes](https://learn.chatgpt.com/docs/sandboxing)
  separately govern permitted effects.

Bounded live diagnostic on macOS: Claude Code 2.1.289, model alias `opus`
(reported `claude-opus-5-5`), effort xhigh, permission mode plan; Codex CLI
0.160.0, requested `gpt-6.1-sol`/medium, sandbox read-only, approval never,
ignore-rules, web disabled. Neither command passed an agent definition or a
tool-enabling override. Existing vendor settings were inherited, not certified
absent. Each searched a synthetic `src` directory, discovered a randomized file,
read it and returned a random marker absent from the prompt. Claude executed
`Bash` (`rg`) then `Read`; its init inventory included Read/Bash and omitted
Glob/Grep. Codex completed native command executions for `rg` then `cat`.
Both exited 0, fixture hashes stayed unchanged, and the exact temporary fixture
directory was removed after both processes terminated. No delegation occurred.

Local evidence retained at B maintainer workspace
`_runs/infra/20261009-spec-to-code/leg-tool-probe/`: manifest, commands, captured
events, per-provider summaries and synthetic fixture; diagnostic runner is the
sibling `leg-tool-probe.py`. This is a one-off capability check, not a new routine
read audit, full wrapper/formal-round conformance, proof for every model/version,
or assurance that user tool-deny/settings overrides cannot disable reading.
