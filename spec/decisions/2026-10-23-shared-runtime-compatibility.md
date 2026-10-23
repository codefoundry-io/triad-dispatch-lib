# Common runtime reuse and backward compatibility

Status: specification and dev6 library implementation candidate; Codex adoption follows its own gate. No common launcher deployment yet.
Authoring main fetched on 2026-10-23: `859f27c07c1123e87b50344f587999a0cbc172a6`.
Owner direction: [D-SHARED-RUNTIME-COMPAT-20261023](owner-register.md#D-SHARED-RUNTIME-COMPAT-20261023).

<a id="PRD-SHARED-PURPOSE"></a>
## Purpose

Let multiple consuming hosts use a compatible common runtime without losing
existing calls when another host installs, upgrades or removes its integration.
The owner asks for this compatibility contract rather than assuming separate
launcher copies are required. The normative behavior is written once in
[R-SHARED-RUNTIME-COMPAT](../reference/review-rules.md#R-SHARED-RUNTIME-COMPAT).

<a id="PRD-SHARED-SCOPE"></a>
## Scope and preserved features

This amendment defines observable compatibility, consumer binding and lifecycle
outcomes. The owner subsequently [authorized implementation, merge and deployment](owner-register.md#D-SHARED-RUNTIME-IMPLEMENTATION-20261023),
selecting library plus Codex adoption; Claude/AGY receive follow-up instructions.
The [Python interface](../reference/runtime-compatibility-api.md) and
[implementation plan](../../docs/superpowers/plans/2026-10-23-shared-runtime-compatibility.md)
now define additive deterministic validation, selection and retention APIs.
This does not select a cross-host registry or change provider schemas/prompts. Common
deterministic semantics still belong in this library; native spawning, provider
integration, installation and configuration stay in each host repository.

Preserve the existing caller's command/helper contracts, supported timeout and
refusal behavior, output admission, terminal/authentication precedence, roster
and model/effort resolution, native versus CLI execution, configuration and
classifier state, artifact identity and receipt/round custody. Shared defaults
remain governed by R-PARITY at the adopted revision; existing differences are
evidence to reconcile, not permission to create new undocumented exceptions.

The withdrawn [U8 investigation](owner-register.md#D-U8-WITHDRAWN-20261010) is
not resumed wholesale. This new owner request supplies a bounded specification
for common-runtime implementation and adoption. It does not authorize copying
one host's private adapter into another or replacing owner-authored files.

## Evidence and current behavior

During the owner-approved Codex PR #47 deployment, all four generic commands
under `~/.local/bin` were observed to be AGY-managed launchers targeting
`~/.gemini/config/plugins/agy-triad-dispatch/bin/`. Their runtime is host-bound,
not a neutral dispatcher: the launchers pin the interpreter, provider paths,
PATH and AGY classifier location. No launcher was changed. Original bytes and
identity hashes are retained in the deployment evidence.

| Observed boundary | Current evidence | Consequence for common reuse |
| --- | --- | --- |
| Shared command ownership | Codex `scripts/bootstrap.sh::preflight_install_command_targets` and `verify_installed_launchers` at released `89acf3a7c3deda49d0e48942020e5061e638aa61` preserve foreign launchers and require matching toolkit paths | A verified interoperability path is needed; removing the ownership guard alone would not provide it |
| Library pin | Installed AGY manifest records dev4 / `087af94a7078de0ae9701fb057840b5492f51f66`; Codex 0.2.563 records dev5 / `859f27c07c1123e87b50344f587999a0cbc172a6` | Same library family is not even an identical installed version here; both library and consumed adapter behavior need evidence |
| Native integration | Installed AGY `bin/review_adapters_v2.py::_codex` rejects `native-spawn-tool`; released Codex adapter validates its native capability context | Sharing cannot silently substitute a CLI for a native child or infer the caller from installer identity |
| Defaults and state | Installed AGY defaults name `gemini-3.1-pro-high`, while Codex 0.2.563 names `gemini-4-argon-high`; classifier defaults use different host configuration directories | Upgrading a common executable must not implicitly replace another consumer's adopted defaults or state |
| Custody | Codex `bin/review_round.py::load_google_selector_receipt` binds toolkit/wrapper paths; existing host admission and native callback contracts remain effective | Runtime selection must retain the caller's real toolkit and current invocation binding |

The AGY observations describe the installed snapshot, not a newly verified
AGY repository release or universal behavior. Claude's common-launcher behavior
was not executed in this investigation. Its existing A source/export mapping
in `units.json` remains an ownership pointer, not a new conformance claim.

Codex [PR #47](https://github.com/codefoundry-io/triad-codex-dispatch/pull/47)
is merged and [v0.2.563](https://github.com/codefoundry-io/triad-codex-dispatch/releases/tag/v0.2.563)
is published. Its reviewed head `facbaaf98c9b74ee7b8f8753f3e48175ab7b273d`,
merged head `89acf3a7c3deda49d0e48942020e5061e638aa61` and successful native
CI merge commit have identical source trees. This proves that host release's
basis, not compatibility of current AGY launchers with Codex.

<a id="PRD-SHARED-ACCEPTANCE"></a>
## Acceptance and host handoff

Use C81-C83 as the behavioral acceptance corpus and the
`shared-runtime-compatibility` unit as ownership. Each host maintainer should:

1. Inventory its consumed commands/helpers, supported older/current baselines,
   common contracts, declared exceptions and native/configuration bindings.
2. Review this exact specification commit with the other host maintainers under
   R-AUTHORING-SYNC before implementing a common behavior change. Resolve
   remaining interface choices in this shared specification; keep host adapter
   and installation mechanisms in their owning repositories.
3. Implement/reuse the common deterministic compatibility behavior once, then
   adapt each host. Preserve current working installs until candidate reuse and
   replacement meet the declared contract.
4. Run the claimed installer/consumer combinations in both relevant orders,
   supported older/current clients, positive and refusal controls, failed update,
   removal and active invocation. Use the host's existing macOS/Ubuntu evidence
   policy. Record exact source/artifact identities and remaining NOT RUN axes.

Current C81-C83 results: **NOT RUN** for Claude, Codex and AGY. Library authoring
and Python API checks establish only their own scope. Review, implementation,
host adoption, publication and local installation remain separate steps.

Do not reclassify the current Codex bootstrap's foreign-launcher refusal as a
regression: it preserves a working installation while interoperability is
unproven. Do not claim that a directory split, marker change, identical package
version or PATH override implements this compatibility contract.
