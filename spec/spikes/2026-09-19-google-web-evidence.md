# Spike — the Google research leg never fetched its web evidence (2026-09-19)

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](../decisions/owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

Owner directive (2026-09-19, after the web-search complaint of the same day): fix the agy web search and test it;
deliver the spike record — lines and cause — to the other leader too, so both hosts fix the same seam
(`decisions/owner-register.md`). Produced: rule sentence under `R-INVEST`, clause `web-evidence`
(`prompts/investigation.md`), case C29, this record. Host A (claude host, SoT `~/triad`, branch `parity/phase0-review`
at `0d59558` before the fix) measured and fixed; host B (codex host, public `triad-codex-dispatch` `105a1e4`, still the
public HEAD on 2026-09-19 by `ls-remote`) is read-only for the author — § 6 names its lines.

## 1. Observation (host A, agy Pro-high tier, `--sandbox read-only --web`, host-parity rounds)

| Round (UTC) | agy | `search_web` | `read_url_content` | files read | input tokens | web citations in the answer |
|---|---|---|---|---|---|---|
| r1 2026-09-19 02:25 | 1.2.6 | 4 | 0 | 10 | 61,196 | "`geminicli.com` 2026" — no URL, no page date (A `gate-r1/agy-r1.out:8`) |
| r2 2026-09-19 09:07 | 1.2.7 | 1 | 0 | 19 | 140,784 | placeholder URLs "https://github.io/..." and "https://geminicli.com/...", a bare "2026" (A `gate-r2/agy-r2.out:18-19`) |

Sources: A `docs/reviews/2026-09-19-host-dispatch-comparison-material/gate-r{1,2}/agy-read-audit-r{1,2}.json` (`web`
list, `usage`), A `3rd-Agent/wrappers/_logs/antigravity/audit.jsonl` rows (`vendor_version`, `cmd`). Both briefs demanded
URL + page date (r2 `brief-spec-r2.md:19-20`). The r1 "dated" facts (v0.60.0, 2026-09-15) were the brief's own facts
echoed back, not fetched.

## 2. Cause chain (with lines)

1. **Nothing told the research agent what web evidence is.**
   - A's wrapper passes the caller's prompt verbatim: `3rd-Agent/wrappers/antigravity_wrapper.py` `_dispatch` →
     `_build_cmd(args.prompt, …)` (pre-fix `:1191`); `_build_cmd` (`:84-114`) adds flags only.
   - The embedded research-agent body says "fetch web pages with read_url_content / search_web only when the prompt
     allows it" (`AGENT_BODIES`, pre-fix `:345-353`) — a permission, not a procedure.
   - A's dispatch skill § Routing (`.claude/skills/triad-antigravity-dispatch/SKILL.md:185-199`) explains grounding, not how
     to cite.
2. **agy `search_web` returns a model-written summary with grounding-redirect links, never a page** (A measurement
   2026-09-16: its `read_url_content` calls went to `vertexaisearch.cloud.google.com/grounding-api-redirect/...`); only a
   page fetch exposes a date or version. So "search, then answer" cannot satisfy "URL + page date".
3. **Load.** The r2 brief made the leg read 19 files across `spec/`, `host-a/`, `host-b/` (Q5 host truth with `path:line`)
   — 140k input tokens against 61k in r1 — and it spent one search on the web question.
4. **Placement.** A's own review renderer documents the constraint-drop shape — a rule at the START of a long prompt is the
   one most likely dropped by the time the model acts (`.claude/skills/triad-cross-family-review/lib/review_scratch.py`
   `_render_agy_prompt` docstring `:2420-2428`) — while both ad-hoc research briefs carried their web rule near the top.
5. **Not the cause.** The vendor version (1.2.6 → 1.2.7 between the rounds; `agy changelog` for 1.2.7 lists no
   web-tool change); the host permission (`read_url(*)` is allowed in the host's agy settings); the gemini REVIEW
   policy (D-9 concerns review legs; this is the research path, `R-INVEST`).

## 3. Fix on host A

- `antigravity_wrapper.py`: constant `AGY_WEB_EVIDENCE_CLAUSE` (860 bytes, after `AGY_WEB_TOOLS_ADMIT`); in `main`, after
  the empty-prompt check and the `--web`-requires-read-only check: `args.prompt = args.prompt + "\n\n" +
  AGY_WEB_EVIDENCE_CLAUSE` when `--web`. The audit row (`cmd`, `prompt_len`) and the run-log therefore record the prompt
  AS SENT. A review dispatch (no `--web`) is untouched.
- Test `tests/unit/wrappers/t49-agy-web-evidence-c29.sh`, 6 axes over a fake agy (RED observed as "constant missing",
  GREEN after the change): clause LAST with the caller's bytes untouched / no clause without `--web` / audit `cmd[2]` +
  `prompt_len` show the prompt as sent / `--prompt-file` route / clause content pins / an empty prompt with `--web` is
  still refused pre-spawn. Regressions green: t16, t28, t45, t46, t48, integration f9 (163 checks).
- Docs: `3rd-Agent/wrappers/README.md` § `antigravity_wrapper.py`, dispatch skill 0.16.4 § Routing, `3rd-Agent/CLAUDE.md`
  cross-reference row, both test catalogs.
- Spec: C29, `R-INVEST` web-evidence sentence, `prompts/investigation.md` (`web-evidence`, byte-identical to the
  constant), `units.json` selected-investigations.

## 4. Live before / after (agy 1.2.7, Pro-high tier, `--effort high`, cwd = A's `wrappers/policies/`, 2026-09-19 ~11:00 UTC)

The "before" arm is the pre-fix wrapper extracted from A's HEAD (`git archive 0d59558 3rd-Agent/wrappers`); the "after"
arm is the fixed working tree. Same brief, same flags, concurrent dispatch. Raw material: A
`docs/reviews/2026-09-19-host-dispatch-comparison-material/spike-web-evidence/` (`brief-*.md`, `agy-*.out/.err`,
`agy-*-read-audit.json`).

**Pair 1 — brief `brief-web-evidence.md`, output contract = one line per fact
`claim | URL fetched | date or version on the page | fetched: yes/no`.**

| Arm | wall | `search_web` | `read_url_content` | files | input tokens | unfetched claims | facts wrong on adjudication |
|---|---|---|---|---|---|---|---|
| pre-fix | 315.6 s | 5 | 10 | 17 | 387,683 | 2 — Q1 both tools: "UNSURE \| 2026 \| fetched: no" (the r2 shape: no URL, bare year) | 0 |
| fixed | 292.9 s | 4 | 14 | 19 | 137,695 | 0 — every line names a fetched URL; undatable pages marked UNSURE | 1 — Q3 attributed the headless `web_fetch` deny to `non-interactive.toml` (`ask_user` deny at 999); the rule is `write.toml:96-108` (§ 5) |

Reading: this output contract itself drives fetching (both arms fetched the release page and the v0.60.0 policy files),
so pair 1 measures the residual only — the clause removed the unfetched bare-year lines and cut input tokens by 65%, but
it does not make a fetched page read correctly: adjudication of every web fact stays with the leader (A standing rule
2026-09-16).

**Pair 2 — brief `brief-web-evidence-prose.md`, the r2-like contract ("answer in prose; cite `URL (page date or tag)`").**

| Arm | wall | `search_web` | `read_url_content` | files | input tokens | citations | facts wrong on adjudication |
|---|---|---|---|---|---|---|---|
| pre-fix | 150.9 s | 13 | 2 (`plan.toml` at `main`, then at `v0.60.0` — the only page it read) | 4 | 72,761 | Q1 "https://github.com/google-gemini/gemini-cli (2026)" — repo root + bare year, unfetched; Q2 "https://geminicli.com (v0.60.0)" — never fetched; Q3 cites `plan.toml` for the read-only tier | 2 — Q3 names `plan.toml` as the read-only tier (it is `read-only.toml`) and places the headless `web_fetch` deny in `plan.toml` (it is `write.toml:96-108`); the "priority 50" came from a comment in `plan.toml:28` |
| fixed | 384.9 s | 6 | 16 (release page; `read-only.toml`, `non-interactive.toml`, `write.toml`, `sandbox-default.toml`, `plan.toml` at `v0.60.0`; tool definitions `gemini-3.ts`, `web-search.ts`, `coreTools.ts` at `v0.60.0`) | 22 | 274,692 | every web fact cites a URL that appears in the fetch log, tagged `(v0.60.0)`; Q1 from the tool definitions file at the tag | 0 — read-only tier `read-only.toml` priority 50; headless `web_fetch` deny = `write.toml` "Headless Denial Rule" priority 10; `v0.60.0` 2026-09-15; A's TOML names neither tool |

Reading: under the r2-like contract the pre-fix arm reproduced the r2 failure class (search-summary answers, unfetched or
placeholder-grade citations, a bare year, wrong file attribution) and the fixed arm did not — every cited URL was fetched
and version-tagged, and all four answers survive the leader's adjudication (§ 5). The price is wall time (151 → 385 s) and
input tokens (×3.8): a research dispatch that must fetch pages costs a fetch per fact. Both arms found the local-file fact
(Q4) correctly; the clause changed only the web half, as intended.

**Conclusion (scope per codex's rev-1 review).** One observed pair per contract (n = 1 each): the spike shows the clause is a practical
improvement, not a general failure rate, and it does not prove the missing procedure was the ONLY possible cause; the fixed arm of pair 1
still misread one fetched page, so page-fetch evidence and correct interpretation are separate — leader fact-checking stays. Within that
scope: the cause was the missing procedure, not the vendor or the permission: told what web evidence is, the same
model on the same version fetched 16 pages instead of 2 and stopped inventing citations. One measurement pair per contract
(n = 1 each) — a repeatable case (C29) plus the audit's `web` list make the next regression visible without re-running
this study.

## 5. Facts adjudicated by the leader (Tier 1 — GitHub API and the official docs site, 2026-09-19)

- Latest stable release: `v0.60.0`, published 2026-09-15T20:31:02Z (`gh api repos/google-gemini/gemini-cli/releases/latest`);
  stable tags end `v0.58.0`, `v0.59.0`, `v0.60.0` (nightlies excluded). Both arms of pair 1 got this right.
- `packages/core/src/policy/policies/read-only.toml` @ `v0.60.0`: the read-only rule `:30-55` lists `google_web_search`
  (`:36`), `decision = "allow"` (`:54`), `priority = 50` (`:55`) — the DEFAULT tier allows search.
- `write.toml` @ `v0.60.0` `:96-108` "Headless Denial Rule (Priority 10)": `web_fetch` (`:104`), `decision = "deny"`
  (`:106`), `priority = 10` (`:107`), `interactive = false` (`:108`). `non-interactive.toml` `:3-7` denies the `ask_user`
  TOOL at 999 — it is not the `web_fetch` rule.
- `https://geminicli.com/docs/reference/tools` exists, "Last updated: Sep 1, 2026"; its one-liners for both tools match
  what both arms reported.
- Host A `3rd-Agent/wrappers/policies/gemini-readonly.toml` (66 lines) names neither web tool (its only search row is
  `search_file_content` `:34`); host B `bin/policies/gemini-formal-readonly.toml` @ `105a1e4` allows `google_web_search`
  (`:12`) and `web_fetch` (`:13`) at priority 999 (`:17`) with a `*` deny at 998 (`:31-35`). These are D-9's inputs and
  are unchanged by this spike.

## 6. What host B should touch (codex decides the placement; lines at public HEAD `105a1e4`)

- B has no research (`--web`) dispatch mode: `bin/antigravity_wrapper.py` contains no web / research / `read_url_content`
  / `search_web` handling.
- B's Google REVIEW prompt permits web reads conditionally: `bin/review_round.py:72-74` (agy — "Approved AGY native
  official-web reads remain available only when the review objective and authorized external data boundary expressly
  permit them") and `:81-82` (gemini — "Use google_web_search, web_fetch, and get_internal_docs only when …").
- Wherever a B prompt permits web reads, append `web-evidence` LAST (gemini tool names `web_fetch` /
  `google_web_search` substituted, nothing else changed), record the prompt as sent in B's receipt, and name B's test after
  C29. Whether B's REVIEW leg should permit web at all is D-9 — a separate owner decision; the evidence clause applies
  wherever web is permitted, whatever D-9 decides.

## 7. Open and deliberately not done

- D-9 was RULED later the same day (review legs have no web tools on any family; `decisions/owner-register.md`); this spike did not decide it — it fed the `R-INVEST` side.
- A mechanical read-audit NOTE ("search_web > 0 and read_url_content == 0") was considered and NOT added: the digest
  already lists every web call and the leader reads it; no new machinery without a repeated manual check
  (`reference/spec-authoring.md § 6`).
