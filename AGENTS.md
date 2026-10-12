# TRIAD dispatch library development

- Work in this repository's Git root. Read [current status](docs/status.md)
  before continuing; historical research is evidence, not an execution plan.
- Implement shared deterministic behavior against the adopted
  [TRIAD specification](https://github.com/codefoundry-io/triad-dispatch-spec).
  Preserve canonical schemas, pinned source provenance, and explicit host exceptions.
- Keep native agent spawning, model/effort integration, installation, and host
  configuration in their owning projects. Changes to either consumer or the
  specification require their own scoped work; do not modify them as a side effect.
- Preserve existing work and make the smallest coherent change. State the issue,
  proposed change, and impact before material edits. Write repository documentation
  in English and use the owner's language in conversation.
- Use `uv sync --locked`, `uv run --locked pytest -q`, and `git diff --check`.
  For package changes also build an sdist, rebuild its wheel and run
  `uv run --locked python tools/verify_wheel.py <wheel>`; see README commands.
  Do not claim macOS/Ubuntu compatibility without native platform results.
- Keep changing progress in `docs/status.md` and research/design records under
  `docs/`; keep this instruction file small. The first slice uses ordinary
  independent Codex review; it is not formal multi-family TRIAD admission.

## Owner-managed workspace

When this checkout is under the owner's `workspace/` directory, follow the
existing workspace procedures below. They are workstation instructions, not
dependencies of this public library; standalone contributors need no such tree.

- [Working rules and authority](../../docs/agent-policies/common.md)
- [Git, Python, build and test execution](../../docs/agent-policies/execution-environment.md)
- [Native delegation and long-running commands](../../docs/agent-policies/development-agents.md)
- [Prompt or instruction changes](../../docs/agent-policies/prompt-testing.md)

On that workstation, run Python, tests, builds, Git/GitHub mutations and provider
CLIs through `/bin/zsh -lic` with `sandbox_permissions="require_escalated"` on the
first call. Include this requirement in delegated development tasks. Read-only
file and Git inspection may use the default sandbox.
