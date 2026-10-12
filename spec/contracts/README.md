# contracts/ — machine-readable contracts

| File | Status (current draft) | Consumers |
|---|---|---|
| `gemini-readonly.toml` | A's unchanged 100/200 no-web profile (the profile for a false R-REVIEW-WEB condition; its "review legs have no web tools" comments describe that profile), including D-9 explicit web denies. Vendored byte-for-byte; host notes stay outside the payload. Applied without a live run | A `gemini_wrapper.py` read-only posture; B selects its separate profile below under D-B1 |
| `gemini-readonly-web.toml` | A's complete web-enabled profile for a true R-REVIEW-WEB condition: A's no-web profile with only `google_web_search` / `web_fetch` moved to allow at 100; every other row unchanged. Live checks WEB-A-2 / WA1-WA2 NOT RUN | A `gemini_wrapper.py` review posture with a true condition: `3rd-Agent/wrappers/policies/gemini-readonly-web.toml`, byte-equal, attached under `--review-web` (triad `b53409b`) |
| `gemini-readonly-web-b.toml` | B's complete web-enabled profile for a true R-REVIEW-WEB condition. Live checks WEB-B-1 / WB1-WB2 NOT RUN | B `bin/policies/gemini-formal-web.toml` |
| `review-web.verify.toml` | R-REVIEW-WEB live checks: WEB-A-1 (the true condition on every route, live) RUN 2026-10-03 (host A b53409b); WEB-A-3 (absent / false / mismatched condition refuses web, live), WEB-A-2 and WEB-B-1 NOT RUN (result in `decisions/owner-register.md`) | host maintainers where the CLIs are in service |
| `gemini-readonly-web.verify.toml` | WA1-WA2 on A's web profile (web tools run; mutation/shell denied), exact policy digest; NOT RUN | A owner where Gemini is in service; results → C32 and owner register |
| `gemini-readonly-web-b.verify.toml` | WB1-WB2 on B's web profile, exact policy digest; NOT RUN | B owner where Gemini is in service; results → C32 B column and owner register |
| `gemini-readonly.verify.toml` | Verification procedure and evidence requirements for V1–V5; all runtime checks NOT RUN. It distinguishes attempted calls from authoritative pre-dispatch exclusion, canonical tool visibility from alias matching, and compatibility from catch-all effectiveness. See the manifest for the fixture, exact direct-CLI command and attribution rules | the owner, where gemini is in service; results → `decisions/owner-register.md` + C15 test column |
| `gemini-readonly-b.toml` | D-B1 separate B profile candidate: preserves existing 999/998 controls, canonical search and Plan Mode transition denies; moves both web tools into explicit denies. Byte equality applies to this complete selected profile; A payload is unchanged | B `bin/policies/gemini-formal-readonly.toml`, after explicit candidate integration; no overlay |
| `gemini-readonly-b.verify.toml` | B1–B3 live effects NOT RUN; independent exact policy digest and verification-only Plan Mode command. A V1–V5 remain unchanged | B owner where Gemini is in service; results → C15 B column and owner register |
| `exit-tokens.json` | seed = host A's 18-token map as data; B delta noted inside | both hosts' `_common.py` tables, membership-tested (D-11) |
| `vendor-failure-lines.json` | the vendor failure sentences known today: CLI, sentence, match phrase, token (R-CLASSIFY, C43) | both hosts' classifiers carry the same rows |
| `review-legs.example.json` | v2 illustrative roster template; placeholders make it non-runnable until the user's pin or a host's shipped default replaces them (R-MODEL: no model list is consulted) | both loaders; validates against `review-legs.schema.json` |
| `leg-verdict.schema.json` | Draft 2020-12 v2 canonical admission schema; materializes the aligned `leg-verdict-mapping.md` choices; candidate, not tagged/adopted | both validators; v2 prompt shape pins |
| `leg-verdict-mapping.md` | round r2 output: A↔B mapping table, losses per direction, the proposed v2 shape, the three release properties that must survive | both maintainers (D-3) |
| `review-legs.schema.json` | Draft 2020-12 named overrides and `$defs.resolvedRoster`; actual route/model/effort capability checks remain host adapters | both loaders |
| `review-kind.schema.json` | Draft 2020-12 scalar review stage: `formal-plan`, `pre-merge`, `implementation-review`; annotated omission default `pre-merge`; unknown/null refused. B omission/refusal fixtures passed; A implementation and host adoption remain separate | both review dispatchers after candidate adoption |
| `review-strategy.verify.toml` | C13/C20/C33/C60–C65: B provider-free PASS at `f6651121`; A provider-free fixtures at triad `ee011968`, including C65 (`t65` axes 1-5; `t57` axes 13/17/18), and C63 at triad `8404021`, verified at `d76ef23`. These are attributed host results; authenticated runtime and host adoption remain separate | host maintainers; no provider authorization |
| `cleanup-roots.schema.json` / `cleanup-roots.example.json` | Draft 2020-12 shape of the one configuration file that declares every folder a host's code may delete (role, root, ownership proof, age floor; R-CLEANUP, C69); the example is illustrative, not a runnable default. Missing / invalid file: nothing is deleted (the command refuses, prunes skip with a note); a host ships a default file | both hosts' deletion code (A fixed @ triad `b6fac284`, Task 23, DL-77; B to adopt) |
| `receipt-fields.json` | Draft 2020-12 common `transport` object for existing audit/run-log envelopes | both `_common.py` and native receipt producers |

Integration and legacy compatibility: [rev-2 implementation specification](../decisions/rev-2-implementation-spec.md).
Host-profile equality and investigation evidence semantics:
[D-B1/D-B2 amendment](../decisions/2026-09-20-host-policy-and-evidence-amendment.md).
Authoring validation uses `python3 -m pytest -q tests` with `requirements-dev.txt`; the suite exercises canonical
schema validity and boundary examples. It proves neither host adoption nor authenticated CLI behavior. Duplicate
JSON members must be rejected at the original-text boundary before schema validation; invocation binding and actual
adapter capabilities are checked separately. No remote schema resolution or custom validation engine is required.

Remaining proposals for `gemini-readonly.toml` land only after the manifest checks pass: a canonical `grep_search` allow
row for tool visibility (V3), and a `*` deny below the allows (V5). The exact adoption candidate must pass both read
compatibility and a discriminating deny control; model prose never proves a policy outcome. Effective source-derived
postures at v0.60.0: both hosts' no-web profiles (the profiles for a false R-REVIEW-WEB condition) deny both web tools by
explicit rows — On B, `bin/policies/gemini-formal-readonly.toml` is byte-equal to `gemini-readonly-b.toml` — and each
host's web profile allows them for a true condition. These are source observations, not live conformance results.
