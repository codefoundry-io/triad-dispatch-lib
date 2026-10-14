# Project review profile setup

Scope: the owner selected a trial for `triad-dispatch-lib` only on 2026-10-14.
This records project configuration and capability checks, not a complete formal
review, calibrated benchmark, host release or global plugin installation.

## Configuration

The project roster contains exactly three enabled required entries: Claude
`claude-opus-5-5/xhigh`, native Codex `gpt-6.1-sol/xhigh`, and AGY
`gemini-4-argon-high/high`. Astra `gpt-6-astra/high` is an independent native
comparison described in `docs/review-profile.md`, outside formal roster inputs.
No package code, generated assets, host defaults or shared workspace policy changed.

Source host `1122afa` and installed Codex plugin `0.2.559` both resolved the project
configuration to the same three required entries. Both correctly reported
`capabilities_checked: false`. The retained inactive Gemini block comes from
host defaults; the explicit `google.route = agy` selects only AGY.

Installed AGY `1.3.5` advertised `gemini-4-argon-high`. Claude Code `2.1.299`
advertised `xhigh`. These observations do not prove authenticated inference.
Source-host provider-free adapter preparation and focused library checks passed
as recorded below.

## Native instruction probe rubric

Freeze this rubric before dispatch. Give both fresh native children the same
three scenarios and the same project instructions/profile, without expected
answers. Requested settings are Sol 6.1/xhigh and Astra/high. Their outputs are
setup observations, not formal ballots or model-performance measurements.

Expected outcomes:

1. For a new review of this project, select explicit public v2, exactly the three
   required models above, and a separate fresh Astra comparison without a vote.
2. If required reviews approve while Astra reports a plausible bug, reproduce it
   before concluding. A confirmed material defect needs correction and a fresh
   required review; comparison failure by itself does not replace required results.
3. Control: a different project does not inherit this project trial; resolve that
   project's own instructions and review configuration.

Only actual native tool acceptance establishes that requested settings were
accepted. Unexposed effective backend model/effort remain `UNEXPOSED`.

## Results

All commands used `/bin/zsh -lic` with `sandbox_permissions=require_escalated`;
read-only file/Git inspections used the normal sandbox. The Python runtime was
3.12.13; uv was 0.11.8 and the locked project pytest was 9.1.1.

| Check | Observation |
| --- | --- |
| Source and installed `resolve-roster --project-root` | Same three enabled required entries; no Astra ballot |
| AGY catalog | 1.3.5 exposes `gemini-4-argon-high` |
| Source v2 `prepare_adapters` | All three prepared; AGY requested Argon/high with the existing read-only profile; provider inference not started |
| Claude session-only `/model` selection | 2.1.299 selected `claude-opus-5-5` with requested `xhigh`; provider inference not started |
| Native capability validation | Current spawn surface accepts Sol 6.1/xhigh and Astra/high |
| `uv run --locked pytest -q tests/test_roster.py tests/test_dispatch.py` | 64 passed in 8.69 seconds |
| Fresh `project_profile_sol_probe` | Requested `gpt-6.1-sol/xhigh`, `fork_turns=none`; completed all three scenarios correctly, no ambiguities |
| Fresh `project_profile_astra_probe` | Requested `gpt-6-astra/high`, `fork_turns=none`; completed all three scenarios correctly, no ambiguities |

Provider-free preparation artifacts are retained locally under
`_runs/20261014-review-profile-ml8nthgh/`, including `setup.json` and separate
Claude/Google receipts. Those checks were made without web authorization and
do not establish the web-enabled profile. Both native calls read only the
project AGENTS, roster and profile. They were separate prompt-controlled
read-only probes; neither could see the rubric, sibling output or review history.
The common scenario questions were:

1. Which workflow, reviewers/models/efforts and approval participants apply to a
   new implementation review here?
2. What follows a plausible concurrency defect reported by the comparison when
   required reviews approve, and what follows a comparison timeout without a finding?
3. Which configuration applies to a subsequent task in an unrelated repository?

Both distinguished the three required reviewers from the ballot-free Astra
comparison, required reproduction/correction of a material finding, kept timeout
separate from required approval, and retained the unrelated project's own rules.
Requested settings were accepted by the native spawn tool. Effective backend
settings were not independently exposed and remain `UNEXPOSED`.

The original setup probes used the following frozen instruction hashes and
their post-probe check matched them. This is a historical setup snapshot:
the subsequent owner-approved 40-minute deadlines and direct-native comparison
clarification change the profile files; these hashes do not attest those revisions.

| File | SHA-256 |
| --- | --- |
| `.agents/triad-review-legs.json` | `e1a35ae08b707c40b82c99243c51ffc926a6b4bac276c9ae9ed108b8a139adb6` |
| `AGENTS.md` | `626e4f98d7811999f590d262ddb42b2e14b2f460d70e1dfb48482c739d284b8d` |
| `docs/review-profile.md` | `3ea9ee2c7ff97338c9d807afba1cafb689860525e9ccf2fce8eefedb0abf7271` |

This verifies local setup and native instruction behavior. No actual Argon/Opus
review inference, complete three-provider review, benchmark, Ubuntu provider run,
global installation, package publication or merge is claimed.
