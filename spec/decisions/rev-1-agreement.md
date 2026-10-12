# rev-1 agreement — TRIAD host parity, shared specification

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

**Status (2026-09-19, final):** BOTH leaders acknowledge the SAME basis `bd506054e62b9b1ba5ef5e156ae8928ac414e4bf` (codex's
verification amendment on top of `b8b127b`) and have declared "no further items" — codex at `ccd3d10`, claude at `30b8360`
(signature rows in § 5). Commits after `bd506054` are acknowledgements and runner notes only; no normative file, contract,
prompt or case changed. The `rev-1` tag is the owner's decision (owner Q-T). This is a DESIGN and CONTRACT agreement; it is
not a claim of executable conformance (§ 4) — V1–V5 remain NOT RUN.

Owner's instruction (verbatim, 2026-09-19): "푸시하고 더 이상 논의할 것이 없이 상호 만족이면 OK 싸인 넣어서 최종 합의서 줘".

## 1. What is agreed — pinned

| Artifact | Pin |
|---|---|
| Shared specification | `codefoundry-io/triad-dispatch-spec` — normative basis `bd506054` (= `b8b127b` + codex's verification amendment: `gemini-readonly.verify.toml`, C15, R-GOOGLE wording, `contracts/README.md`, mapping table); main at signing `30b8360` (acknowledgements only after `bd506054`); `rev-0` tag = `dfbeb60` |
| Host A (claude host) | `codefoundry-io/triad` `parity/phase0-review` `cf37d68`; public plugin `triad-dispatch` 0.2.845 `8efeb74` |
| Host B (codex host) | public `triad-codex-dispatch` `105a1e4`; codex development HEAD `520caa9` (codex's rev-1 review) |

Content of the specification at `bd506054`, each in exactly one place (`reference/README.md` table):

- Rules with anchors — `reference/review-rules.md` (R-AGREE, R-REREVIEW, R-RETRY, R-ROSTER, R-INVEST, R-GOOGLE incl.
  the apply-and-verify convention, R-SMELL, R-STOP, R-CONTAIN incl. the operation-level no-web rule, R-TERMINAL,
  R-TOKENS, R-RECEIPT, R-BIND, R-PREPARE, R-VERIFY, R-CLEANUP, R-NOCOST, R-PARITY, R-PLATFORM) and `process.md` (R-DIAG).
- Method — `reference/spec-authoring.md` (cases first; revisions; untestable-here changes ship with a verification
  manifest; results written once).
- Prompts — `prompts/` (shared clauses, three review legs, `investigation.md` with `web-evidence`); the one editable copy.
- Contracts — `contracts/gemini-readonly.toml` (vendored byte-for-byte), `gemini-readonly.verify.toml` (V1–V5),
  `exit-tokens.json`, `review-legs.example.json`, `leg-verdict-mapping.md` (superset v2 wire; leader-level choices aligned).
- Cases C1–C29 (`cases/cases.json`), `units.json`, `decisions/owner-register.md`, `spikes/`.

Owner rulings in force: D-3, D-9, D-10, D-13, D-14/Q4, Q-A … Q-W, Q1–Q3 (codex session), and the 2026-09-19 directives
(mechanical prompt-file resolution; web evidence; apply first and verify where the capability is in service; rulings
written once). Their effects are the register's rows; nothing in this file adds a rule.

## 2. Settled in this round — nothing further to discuss

1. **Agreement and re-review** — no unresolved blocking finding from any leg; Minor-only MERGE WITH FIXES counts on the
   unchanged bytes; any change is a new basis reviewed by the full participating roster (R-AGREE, R-REREVIEW).
2. **Roster** — a plain list of legs with recommended defaults; three families by default; no per-leg special rules;
   `acceptance` is data (R-ROSTER).
3. **Result wire** — the superset v2 (`leg-verdict-mapping.md`): A's three canonical verdicts (`SAFE` / `Major` as
   import aliases only), A's four severities, the union of finding fields with the one path field `path`, required
   `summary` / `trigger` / `evidence`, optional `correction`, B's `affected_surfaces_inspected` and `open_questions`
   (an unresolved open question blocks; an uncertainty-only negative is DO NOT MERGE with a nonempty `open_questions`,
   no fourth token), binding `review_id` / `family` / `content_digest` + `leg_name` / `attempt` / `route` /
   `schema_version: 2`. Both leaders recommend the same spellings — aligned 2026-09-19.
4. **Web** — the REVIEW operation has no web on any family (D-9); authorized INVESTIGATIONS keep web and carry the
   `web-evidence` clause (R-INVEST, C29); gemini's explicit deny rows are the contract, verified where gemini is in
   service (V1–V5).
5. **Symlinks** — the link itself is reviewed, its target never followed automatically (Q4; mechanism per host).
6. **Google leg** — one family, two CLIs; each host keeps its shipped resolution; Pro family + verifiable HIGH default;
   the owner tests gemini where it is in service and briefs (R-GOOGLE, R-NOCOST).
7. **Review framing** — evidence-centred; a no-defect conclusion is allowed (D-10 closed).
8. **Codex's rev-1 addendum review** — eight bounded findings (F1–F8) verified and applied at `b8b127b`; codex's rejection
   of the "no `--web` flag = no research" reading accepted (B's raw dispatch is its investigation path).

## 3. Commitments after the tag (work, not disagreement)

| Party | Commitment | Case / anchor |
|---|---|---|
| Host A (claude) | Accept relative `--prompt-file` / `--cwd` as specified (NOT applied yet) when the owner OKs the slice | C28, R-CONTAIN |
| Host A | v2 wire slice with EVERY schema-shaped prompt pin (incl. the Google pin) when the schema file lands; `leg-contracts.md` alignment items | D-3, `leg-verdict-mapping.md` § Migration notes |
| Host B (codex) | Review operation without web: 999 allow list, agy read-only builder for review dispatch only, review prompt renderers | C15, R-CONTAIN |
| Host B | `web-evidence` clause on the authorized web investigation invocation; the trigger named | C29, R-INVEST |
| Host B | Relative prompt-file resolution in B's loader; B columns in `cases/cases.json` and `units.json`; B's command for the verification manifest | C28; codex-fill rows |
| Both | `contracts/leg-verdict.schema.json` written from the aligned mapping; `review-legs.schema.json`; `receipt-fields.json` | rev-2 scope (declared NOT YET) |
| Owner | Runs V1–V5 where gemini is in service; each result becomes a register row and flips the C15 test column | `contracts/gemini-readonly.verify.toml` |

## 4. Not run, not claimed

- Runtime enforcement of the gemini read-only policy (V1–V5) is NOT RUN; the deny rows are applied on evidence from
  version-pinned source (v0.60.0), not from a live run.
- The web-evidence spike is one observed pair per output contract (n = 1 each); it supports the clause, it is not a
  failure rate. Fetched pages still need leader adjudication.
- No cross-host conformance run has happened; drift between hosts stays an informational report (Q-P).
- No engine or skill change is authorized by this agreement beyond the two owner-directed fixes already shipped (C29,
  C15 on A) — implementation follows the agreed spec (owner Q-F).

## 5. Signatures

| Party | Decision | Date | Basis read |
|---|---|---|---|
| claude leader (host A) | **OK — agreed; nothing further to discuss on the design and contracts above** | 2026-09-19 | spec `b8b127b`; codex's consolidated document incl. "Rev-1 addendum review"; A `cf37d68`; plugin 0.2.845 |
| codex leader (host B) | _appends its row after reading `b8b127b`_ | | |
| owner | _tags `rev-1` when both rows read OK_ | | |
| codex leader (host B), amended basis | **OK — core design and corrected verification procedure; Claude acknowledgement of this SAME amended basis is pending, so this is not tag readiness or runtime conformance** | 2026-09-19 | `bd506054e62b9b1ba5ef5e156ae8928ac414e4bf`; [amendment and evidence](rev-1-codex-verification-amendment.md); V1–V5 NOT RUN |
| both leaders — closing | **No further items on basis `bd506054`** (codex `ccd3d10`; claude `30b8360`, after confirming codex's runner-note correction). Tag readiness is the owner's call; V1–V5 NOT RUN | 2026-09-19 | `decisions/rev-1-codex-verification-amendment.md` (evidence and dispositions of both leaders) |
| claude leader (host A), amended basis | **OK — re-verified the amended verification procedure on this SAME basis; A1–A4 and the isolation note confirmed against v0.60.0 source and the installed CLI's `--help`; no additional defect; the earlier `b8b127b` row is not carried forward, this row stands on its own. Both leaders now acknowledge the same basis; V1–V5 NOT RUN, so this is not tag readiness, live enforcement or cross-host conformance — the tag remains the owner's decision** | 2026-09-19 | `bd506054e62b9b1ba5ef5e156ae8928ac414e4bf` (published `990874f`); [Claude re-verification](rev-1-codex-verification-amendment.md#claude-re-verification-2026-09-19--basis-bd506054e62b9b1ba5ef5e156ae8928ac414e4bf-published-as-990874f); A `cf37d68` / plugin 0.2.845 unchanged |

A later change to any rule, prompt or contract is a new revision with its own `CHANGELOG.md` entry (spec-authoring § 5);
this file is not edited afterwards except to add signature rows.
