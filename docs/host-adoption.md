# Independent host adoption

`triad-dispatch-lib` owns common contracts, prompt clauses, cases and deterministic
behavior. The Claude host (`triad-dispatch`) and Codex host
(`triad-codex-dispatch`) own native spawning, model/effort resolution, native
callback adapters, provider CLI setup, permissions, installation and configuration.
The four configurable routes and native callback interfaces remain supported.
Implement a shared semantic change once here with its specification, code and
cases; implement host mechanisms in their owning repository.

Neither host has adopted this consolidation. Adoption follows the library PR
merge as separately scoped work. Host versions and release dates are independent;
hosts may adopt different compatible library releases. The unpublished library
`0.1.0.dev3`, candidate schema status and historical spec tags are distinct.

## Adoption record

Each host should retain the following with its adapter/release evidence:

- Exact library package version, artifact SHA-256 and source/build commit when known.
- All consumed bundle names and `contract_id` values, plus the verified payload
  digest maps. An ID identifies one bundle, not every normative document.
- Host adapter version/commit and independent host release version.
- Supported routes, platform/Python combination, native controls, explicit host
  exceptions and case/conformance results with unrun checks named.

`spec/import-origin.json` records original import ancestry only. It does not pin
newly edited guidance. Legacy schema `$id` values remain wire identities even
though authoring moved. Runtime manifests have exactly six fields:
`schema_version`, `source_repository`, `source_path`, `status`, `sha256`,
`contract_id`; release provenance belongs outside them. Content integrity does
not prove artifact authenticity. A live main URL never changes adopted behavior.

## Generated content and installers

Edit canonical runtime sources only in `spec/contracts/` and `spec/prompts/`.
Generate `src/triad_dispatch_lib/data/` with `tools/sync_spec_assets.py --write`;
verify with `--check`. Do not copy divergent common orchestration into either
host. Small native adapters consume the same common implementation and clauses.

For the Claude installer, retain a managed-file hash ledger for installed common
assets and separately identify Claude-native instructions/settings. For the Codex
installer, retain the same kind of ledger for common plugin assets and separately
identify Codex-native dispatch/configuration. Each ledger should name the source
library/bundle version, installed relative path and hash last written by that
installer. It is installer metadata, not an extra runtime-manifest field.

Before either installer replaces or removes a managed file, compare its current
hash with the ledger. If the user changed it, preserve it and report the conflict
with the proposed replacement; do not overwrite, reset or delete user content.
Update the ledger only after successful writes, retain unrelated files and
support recovery from interrupted upgrades. These are recommendations for future
host work; this library slice changes no installer or global installation.

## Verification boundaries

Source tests, authoring validation, deterministic generation, unpacked-sdist
tests and isolated wheel drivers establish static/synthetic library behavior.
The installed probe verifies verdict, roster and prompt bundle identities and
all eight payload digests from an isolated interpreter. Four-route synthetic
responses exercise carriers and shared orchestration; they do not establish
provider authentication, permissions, effective model controls or host adoption.

Each host port additionally needs its own installer preservation/upgrade checks,
native route execution and cancellation/cleanup evidence on the claimed platform,
followed by its separate review and release. Earlier native Codex observations
remain evidence for their recorded dev2 build only. This slice does not run real
providers, publish packages, merge PRs, archive the old repository or port hosts.
