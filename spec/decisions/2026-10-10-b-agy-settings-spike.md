# B AGY settings interaction: bounded U7 evidence

Basis: B ed8b76f plus the unrelated U6a cleanup candidate; `_agy_settings.py`
unchanged. Shared d3a4412; read-only A c2f28ca2 plus its unrelated vendoring-test
edit. This is provider-free characterization, not a new isolation design.

The actual B `agy_settings_guard(_READ_ONLY_DENY)` was run against a synthetic
settings file inside one invocation-owned temporary fixture. Its caller used
project-a as cwd; a separate Python process in project-b read/wrote that same
fixture file while the guard was active. `AGY_SETTINGS_PATH` was overridden
only inside the diagnostic process; no real settings, auth or provider ran.

Observed control: without another writer, guard exit restores the original
bytes exactly. Observed interaction: project-b sees the temporary deny values;
its added fixture key exists before guard exit but is absent afterward, when
the original bytes are restored. This proves the current merge/restore behavior
across two folders. It is not evidence that a real concurrent AGY/Claude call
has lost settings or that A itself writes those files.

Source: B `bin/_agy_settings.py` `_shared_readonly_guard`, `_snapshot`, `_restore`
and `agy_settings_guard`. Evidence: workspace
`_runs/infra/20261010-spec-to-code/u7-state-spike.py` and `.json`; exit0 and exact
fixture `/private/tmp/triad-u7-state.sdqweauu` removed. No host code was edited.

A currently uses its setup-once custom agents and has no settings transaction
in `3rd-Agent/wrappers/antigravity_wrapper.py`; its agent/tool admission remains
A-owned. Its source also records that older AGY advertised tools beyond the
agent's `tools` list, so merely copying agent YAML is not established proof of
B's replacement containment. Native legs and the unused Claude-agent backlog
are unrelated.

U7's next decision must preserve B's existing read-only/web boundary, validate
the supported actual CLI path, and explain legacy/raw migration plus B-owned
stale backup handling. Collect independent diagnosis and Tier1/runtime evidence
before selecting a replacement. A substantive design/containment change returns
to the owner before dependent implementation. U6a proceeds independently; no
new classifier, environment override policy or generic locking framework follows
from this spike. Existing DL-107/112 remain the governing work items.

## Independent diagnosis and current-profile measurement

All three independent diagnoses (Claude opus/xhigh, Google Pro/high, fresh Codex
Astra/high) are terminal. The leader verified the common cause against B source:
formal preflight/dispatch and non-project raw read-only use the transaction;
raw permissive also locks and can perform stale snapshot recovery. Existing
explicit-project validation is read-only. Removing only one merge call would
leave other shared-file effects. Read-only A d3906f5 selects its profiles and
checks tool effects without a settings transaction; its native legs and hook
installation remain A-owned.

One actual current-CLI probe bypassed B's transaction and used its existing
installed no-web profile, plan/sandbox, no danger flag, and an explicitly granted
invocation-owned directory. It read the fixture and listed the directory, exited
0/SUCCESS and created no requested write-control file. No write-tool call was
attempted. The model's claim that write tools were unavailable is not provider
attestation: observed read-only behavior is confirmed, mechanical prevention of
an attempted write remains UNVERIFIED. No stronger repeated prompt campaign is
required. Settings bytes and installed profile matched before/after; the exact
fixture was removed. Evidence: B workspace
`_runs/infra/20261010-spec-to-code/u7/profile-probe/receipt.json` and
`command.json`. No real project content was sent.

Tier1 [CLI permissions](https://antigravity.google/docs/permissions?tab=cli)
describes workspace writes as normally allowed;
[modes](https://antigravity.google/docs/cli/modes) and
[agent definitions](https://antigravity.google/docs/subagents?tab=cli) do not
establish the complete current-runtime replacement by themselves. B's
`AGY_SETTINGS_PATH` helper injection is not established as a vendor-supported
settings-path override. Do not implement an isolated auth/settings root from
that unsupported suggestion. Historical registry exposure proves neither
current tool execution nor universal absence of enforcement.

The owner has been asked to choose between retaining the existing profile,
plan/sandbox and integrity with an explicit pre-execution-prevention limit, or
introducing an operator-provisioned project prerequisite. Raw read-only migration
and preservation of old backup evidence are part of that concrete choice.
Neither option is approved or implemented by this record. No new census,
read audit, hook or native-leg change follows automatically. U6 remains
independent; the shared containment wording stays unchanged pending resolution.
