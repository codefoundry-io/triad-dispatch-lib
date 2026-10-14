# D-B1: bounded Gemini policy composition proposal

> **Historical record; its REVIEW no-web statements are superseded on 2026-10-03.** REVIEW web now follows the owner's
> standing authorization in current [R-REVIEW-WEB](../reference/review-rules.md#R-REVIEW-WEB)
> ([D-REVIEW-LEGS-20261003](owner-register.md#D-REVIEW-LEGS-20261003)); the no-web posture applies only to a false
> condition.

Status: owner directed separate policies where usage differs; see the
[current decision](2026-09-20-owner-follow-up.md#d-b1-preserve-separate-policies-where-usage-differs).
The precise composition below is still a proposal requiring the shared contract
check; the owner answer alone does not adopt this exact supplement. No C15 expected
result, host policy, adopted revision or provider configuration is changed.
Shared remote basis: `2eb883fee59e66556ee7c7f87189b38231136622`.
A remains read-only at `92c8afd500499d8736afcc28b39a87a4f87fed50`.

## Confirmed conflict

C15 requires shared policy byte identity and equal allow/deny sets. B's existing
policy has stronger priority-999 read/deny rules and a priority-998 catch-all,
canonical `grep_search`, `get_internal_docs`, and explicit Plan transition denies.
The current shared policy has priority-100 reads, priority-200 explicit denies,
an alias search name, and no catch-all. Copying it into B would fail B's shape
validator and remove existing controls. Keeping B's bytes alone violates shared
byte identity. The original three-family diagnosis and leader source comparison
record this under D-B1; it is not a new request to reconsider REVIEW no-web.

## Official source evidence

Gemini CLI **v0.60.0** accepts repeated `--policy` arguments and merges the files
as user-tier rules. A higher-priority rule wins, while administrator policy still
outranks the user tier:

- [CLI config.ts L328-L335](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/cli/src/config/config.ts#L328-L335)
- [policy config.ts L100-L120 and L315-L358](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/config.ts#L100-L120)
- [TOML loader L449-L504](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/toml-loader.ts#L449-L504)

Execution-time alias expansion and canonical tool exposure are distinct. Retain
canonical search permission and verify both paths:
[tool names](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/tools/tool-names.ts#L202-L224),
[policy engine](https://github.com/google-gemini/gemini-cli/blob/v0.60.0/packages/core/src/policy/policy-engine.ts#L596-L668).

## Recommended bounded decision

Permit B to vendor the exact shared file and pass a second, B-owned supplementary
policy preserving only the enumerated existing guards, with the agreed web
allow-to-deny change. This is a narrow C15 conformance exception, not permission
for arbitrary host overlays. Shared byte identity and effective-policy behavior
are recorded as separate checks.

The proposed B supplement has exactly these three rules:

```toml
[[rule]]
toolName = ["read_file", "read_many_files", "list_directory", "glob", "grep_search", "get_internal_docs"]
decision = "allow"
priority = 999

[[rule]]
toolName = ["write_file", "replace", "run_shell_command", "enter_plan_mode", "exit_plan_mode", "google_web_search", "web_fetch"]
decision = "deny"
priority = 999

[[rule]]
toolName = "*"
decision = "deny"
priority = 998
```

Do not combine the shared file with B's unchanged current policy: B's current
web allow at 999 would override the shared web deny at 200. Both explicit web
denies and the existing catch-all must remain effective in the composition.

Proposed contract amendment, if the owner selects this option:

> C15 permits Host B's enumerated supplementary user-tier policy alongside the
> unchanged shared payload. Host B records both digests and exact invocation,
> rejects any other supplement shape, and verifies the effective decisions for
> the composed policies. This exception preserves the named existing B guards;
> it does not claim that B's effective policy is identical to the single shared
> file or authorize other additional allows.

The alternative is to revise the shared policy itself so both hosts adopt the
same stronger rules. That also requires a shared-contract decision and later A
adoption; B must not silently impose it while A is paused.

## Host impact and preserved features

- A keeps its existing file and dispatch route under the recommended option.
  No A edit or immediate adoption is required. Its unrun verification remains
  unrun; B evidence never supplies A conformance.
- B verifies two exact policy artifacts in formal dispatch, and keeps auth
  selection, environment scrubbing, Plan request, single-call behavior, local
  binding and raw investigation behavior. Model selection is separate work.
- Shared original bytes and SHA-256
  `13d25f61a430cbee082b756a04b6d872d225e1749eeaad55f95e22ad21fa6980`
  remain unchanged in the recommended option.

## Verification before affected implementation/admission

Use the actual v0.60.0 loader and PolicyEngine without authenticated provider
inference: prove the six read decisions and canonical search exposure; explicit
web/write/shell/Plan-transition denials; ordinary/MCP catch-all denial; and
administrator precedence. Compare current B versus candidate: the only intended
capability change is REVIEW web becoming denied. No fixture executes a forbidden
tool to prove denial.

Then test exact bytes/digests, missing/corrupt/extra/mode-scoped rule refusal, both
policy argv paths, and unchanged raw investigation. Keep single-file V1-V5 results
separate from composed B policy evidence; no retroactive PASS. Record the chosen
contract basis and request Claude leader review of that same authoring commit.
