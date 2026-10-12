# AGY current capabilities before the U7 choice

2026-10-10 Asia/Seoul. The owner requested independent Claude Opus/xhigh and
fresh Astra/xhigh research with web search. Both completed. This is research,
not formal admission or a selected implementation. Remote main3afc4d7; shared
basis c55dca6; B dc952d1 and read-only A404eb0ab unchanged during the external
research. No installed profile, settings, auth, runtime or native-leg change.
No AGY inference trial was run. Hidden native model metadata is UNEXPOSED.

## Current evidence

Local CLI and official GitHub latest release both show1.3.3, published
2026-10-10T03:06:26Z. The docs changelog UI lags at CLI1.3.1/Oct7;
desktop2.22.0 is a separate release. Leader/Astra obtained local help/version;
Claude's own attempts were denied, so its report has no local CLI measurement.
The leader did not change permissions to enable Claude's commands.
[Latest release](https://github.com/google-antigravity/antigravity-cli/releases/tag/1.3.3).

A smaller candidate was missing from B's earlier profile-versus-project choice:
CLI1.2.1/Sep11 adds `excludeDefaultComponents: true`, excluding default prompt
components and built-in tools. CLI1.1.14 documents `inheritCustomizations` for
ambient skills, rules, plugins, subagents and MCP. Both current A embedded and
B shipped profiles lack these switches. Explicit native read/search/finish and
the authorized web twin could be retained while testing exclusion. Turning
inheritance off also removes rules: it must not silently discard applicable
owner/project guidance. Treat that semantic choice separately.
[CLI history](https://github.com/google-antigravity/antigravity-cli/blob/main/CHANGELOG.md),
[dated history](https://antigravity.google/docs/changelog).

CLI1.2.11 fixes project `.agents/agents/` discovery under --agent/headless;
1.3.1 fixes relative agent component paths including hooks. Old global-only
discovery comments need version qualification, not a speculative loader rewrite.
The official Sep28 `permissionMode: plan` example is AGY-native but does not
establish full field semantics or write/command prevention.
[Official example](https://www.antigravity.google/blog/custom-agents-in-google-plugins).

Current help advertises no generic per-call settings/permission-rule overlay;
this does not rule out undocumented mechanisms. `AGY_SETTINGS_PATH` is only
established as a B helper seam. Plan mode adds instructions; terminal sandbox
allows workspace writes. Neither name proves general read-only enforcement.
[Modes](https://antigravity.google/docs/cli/modes/),
[sandbox](https://antigravity.google/docs/sandbox?tab=cli),
[permissions](https://antigravity.google/docs/permissions?tab=cli).

## Diagnosis adjudication

[Issue1015](https://github.com/google-antigravity/antigravity-cli/issues/1015)
is open but does not establish exclusion failure on1.3.3. Earlier reports are
startup inventories. The Oct4 actual command attempt on1.2.16 was denied and
explicitly lacked excludeDefaultComponents. The Oct7 macOS1.3.1 finish-only
plus exclusion report supplied zero prompt bytes and made no tool call.
Catalog, request and effect are different facts.

Claude's claim that the candidate already fails is unsupported by those cited
facts. Its disposable-cwd/new-census recommendation is not selected: it adds B
architecture and cannot prevent effects outside a copied tree. A shorter wrapper
is not evidence that the current checkout is older. Unrelated connector notices
are irrelevant. Astra's candidate-first recommendation is supported as the next
research step, with inheritance semantics qualified above, not as a guarantee.

A's formal review uses an additional active PreToolUse hook. At A404eb0ab,
`.claude/skills/triad-cross-family-review/lib/review_scratch.py:2124` renders
enabled `.agents/hooks.json`; sibling `agy_hook.py` allows the selected review
tools, conditionally adds web, denies other names and checks per-attempt loading.
Its standalone wrapper does not install that hook. B inspected current source,
not a fresh runtime trial. Automated event checks are distinct from the routine
human read audits the owner rejected. B's dormant helper cannot simply be
enabled: it includes web unconditionally and omits finish. No wholesale A
hook/census/native-leg port follows. [Hook contract](https://antigravity.google/docs/hooks/).

## Next action; no design selected

Replace the premature binary choice with one bounded1.3.3 exclusion-profile
comparison. Use task-owned fixture profiles/data, preserve user settings/auth/
installed profiles, and restrict deliberate effects to the fixture. Compare
existing/exclusion profiles with the same model, effort and invocation posture.
Required evidence: profile loading beyond echoed name; useful actual read/search;
result completion; undeclared fixture-only command/file request handling;
unchanged outside state. Optional web uses existing authorization only. No
attempt/model refusal remains inconclusive; do not intensify prompts repeatedly
or treat startup inventory as proof. Assess inherited guidance explicitly.

No fixture execution, version-floor increase, profile installation, hook,
project prerequisite or reduced-protection choice is approved by this record.
If exclusion fails or remains inconclusive, return the concrete project,
scoped-hook or disclosed-limit trade-off to the owner. U7 code stays paused.
SDK transport migration is broader than needed.

Local evidence: B workspace `_runs/infra/20261010-spec-to-code/u7-current-research/`:
Claude terminal exit0/matching source fingerprints and original report; Astra
task `/root/u7_astra_current_research` final and leader-preserved summary; leader
primary-source adjudication and local help. Both original conclusions remain.
