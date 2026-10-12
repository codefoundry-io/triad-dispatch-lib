# Claude Opus 5.5 default and host handoff

Owner request: "codex traid dispatch에 기본모델 opus 5.5로 업데이트하고 spen에도 업데이트해"
The leader interprets "spen" as the shared specification in this request.

## Evidence and change

Authoring base: remote `main` at
`af5533c6b412b60b3ef44750ddcd05bbedb8065a`, fetched before this change.
Codex host source base: `2d4d71b1a6df09b26fae44d228229cd9aa43218d`;
remote main merge: `5a12f822b6e19f5ecd162e4cc54888269ec0ffd9`.
The B implementation is commit `45e21f5d32fce88ba674f4783bd1391d678ef662`
in [PR #38](https://github.com/codefoundry-io/triad-codex-dispatch/pull/38).
The owner subsequently requested deployment and both repositories' `main`
updates: "배포랑 spec 업데이트까지 진행해줘 둘다 메인". The B release target
is `0.2.557`. See PR #38 and the linked release for delivery status.

Anthropic documents `claude-opus-5-5` in its
[Claude Code model guide](https://support.claude.com/en/articles/11940350-claude-code-model-configuration).
Its [effort table](https://code.claude.com/docs/en/model-config#adjust-effort-level)
lists `low`, `medium`, `high`, `xhigh` and `max` for Opus 5.5.
The locally observed Claude Code version was 2.1.282. Documentation and version
inspection establish supported controls, not account entitlement or inference.

Anthropic's [Claude Code 2.1.280 release](https://github.com/anthropics/claude-code/releases/tag/v2.1.280)
introduced Opus 5.5. B's installation prerequisite for this default is therefore
2.1.280+, with actual selection and a complete review invocation observed on
2.1.282. The generic preflight-interface floor is a separate compatibility check;
bootstrap checks executable presence, not model entitlement or effective effort.
The explicit-selection guard described in R-ROSTER covers catalogued IDs.
Uncatalogued deployment strings retain existing handling and are not certified
by C34 or this default-model change.

Before this change, B shipped `opus` in `contracts/review-legs.default.json` and in
`bin/claude_wrapper.py:FORMAL_CLAUDE_MODEL`. Its capability document recognized
Opus 5 but lacked Opus 5.5. A new capability row alone cannot pin the CLI alias.

The owner-selected behavior is defined once in
[R-ROSTER](../reference/review-rules.md#R-ROSTER) and exercised by C12/C34.
B updates the default roster, legacy formal pin, capability row and their
consuming skill/documentation/test surfaces. Raw calls keep their existing
passthrough; v2 overrides, null selection, older supported models, timeout,
web authorization, authentication and no-fallback guards retain their meanings.
No shared schema enum, prompt payload or adoption manifest needs changing.

## Host handoff and verification

B implements the requested default first. A's maintainer should review this
same shared commit and check the roster/agent defaults at the existing `roster`
unit paths in `units.json`; preserve its native topology and override behavior.
A's source and installed configuration have not been changed. A implementation,
acknowledgement and conformance remain pending; they are not inferred from B.

The read-only A inspection used `main` commit
`8efeb74d127a3ca90efe6ed22bbe39cb53719204`. Its standing Claude reviewer still
has `model: opus` and `effort: xhigh` in
[`agents/cross-family-review-reviewer.md:5`](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/agents/cross-family-review-reviewer.md#L5).
A's maintainer must verify exact-ID support in its native Agent frontmatter;
B's CLI selection preflight does not prove that interface supports the same ID.
A's current `review-legs.example.json` is its v1 advisory X-leg configuration,
not a v2 standing roster. Its
[`review_scratch.py:2522`](https://github.com/codefoundry-io/triad-dispatch/blob/8efeb74d127a3ca90efe6ed22bbe39cb53719204/skills/triad-cross-family-review/lib/review_scratch.py#L2522)
treats model/effort as opaque dispatch values and uses an agent type for a Claude
X-leg. The shared R-ROSTER text is the target contract: override/null evidence
here establishes B v2 behavior only, while A native-agent conformance remains
pending. This handoff does not authorize changing A's legacy schema or payload.

The case allocation reuses C12 for existing override/null compatibility and
adds C34 for explicit-pin selection and substitution refusal; B's corresponding
regressions use those same case IDs.

Verify no-file default selection, explicit older-model override, null selection,
Opus 5.5 capability recognition and refusal when that pin reports Opus 5.
For B, additionally verify legacy exact-model/effort/timeout/no-fallback behavior,
raw passthrough and the existing web/schema/transport regressions. Retain original
RED and final verification outcomes separately from provider or release claims.

Verification completed in B's existing source worktree:

- Fresh dedicated RED: 22 failed, 103 passed; the source skill still prescribed
  `opus`, and the new model selection/capability assertions failed.
- Final fresh dedicated GREEN: focused suite 127 passed; full suite 1,686 passed;
  both source skills passed validation. Source fingerprints stayed unchanged.
- One intervening failure came from a pre-existing AGENTS relocation. Its test
  now follows the explicitly linked verification guide, while retaining support
  for the original inline guide. Existing policy edits were preserved.
- Shared-spec suite: 106 passed. Authoring map check: 1 valid, 0 invalid.
- Actual B adapter preflight against installed Claude Code 2.1.282 recorded
  requested and selected `claude-opus-5-5`, requested effort `xhigh`, and
  `provider_started: false`. This was session-only selection, not inference.
- Independent read-only source audit found no actionable issues.

At the initial source-verification checkpoint, the multi-family gate was pending:
both existing AGY projects for
the selected B worktree lack the default-review `read_url(*)` deny and fail the
read-only project guard. Their bytes were unchanged and no review provider was
started at that checkpoint. That source-only evidence does not establish
permission changes, authenticated inference, installation, a revision tag,
host adoption or public release. Later delivery is tracked by PR #38 and
[release v0.2.557](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.557).
