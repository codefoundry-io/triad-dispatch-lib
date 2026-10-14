# Specification and library consolidation

## Decision and scope

The owner approved keeping `triad-dispatch-lib`, moving the shared specification
into it, and distributing the Claude and Codex hosts independently. The source
repository becomes the common development home for contract, prompts, cases,
deterministic Python implementation and their tests. Host-native spawning,
model/effort selection, CLI installation and host configuration remain owned by
`triad-dispatch` and `triad-codex-dispatch`.

This change implements the library side of that decision. Existing host projects
and the old specification repository are not rewritten as a side effect. Their
adoption and the old repository's migration notice follow the consolidated PR's
merge. The old repository's history, tags and URLs remain available.

## Evidence and behavior

The library currently has three generated-looking resource bundles but treats
them as manually pinned copies from `triad-dispatch-spec` commit
`fcd96a15d18f3131c1f0111bdb10c3faceae34f8`. Its verifier hardcodes that repository
and commit; roster schema identity is coupled to the source repository URL.
Moving the spec without changing this mechanism would preserve two authoring
locations and misreport current provenance. Pinning the library's containing
Git commit inside its own tracked manifest would be self-referential.

On 2026-10-13 the source repository's main was fetched at
`396a04dac310d5ff91dbe0a36982f7679aa00428`. Import the complete source tree under
`spec/`, retaining its local relative paths and historical records. Record the
upstream URL, exact imported commit and original file SHA-256 values separately
in `spec/import-origin.json`. That record describes ancestry, not an assertion
that later edited documents still equal upstream. New authoring instructions
must identify this distinction and the migration's pending-merge status.

## Canonical assets and generated resources

`spec/contracts/` and `spec/prompts/` are the only editable sources of the
runtime schema and prompt bytes. Keep the established package resource paths so
runtime consumers need no new file layout. `tools/sync_spec_assets.py --write`
copies bytes unchanged and produces all three manifests. `--check` performs no
writes and fails for missing, stale or unexpected files in the owned generated
resource tree. Refuse symlinks in source or generated paths rather than writing
through them. Do not require Git or network access to generate, test or build.

The explicit mapping covers the verdict schema, roster schema, review-kind
schema, common clauses, Codex/Claude/Google leg prompts and investigation prompt.
No Markdown/JSON normalization or line-ending conversion is allowed. Existing
canonical schema `$id` values stay unchanged, including their old repository
namespace. Source location and schema identity are separate constants.

Each manifest has exactly these fields:

| Field | Value |
| --- | --- |
| `schema_version` | integer `1`, excluding Boolean values |
| `source_repository` | `https://github.com/codefoundry-io/triad-dispatch-lib` |
| `source_path` | `spec` |
| `status` | `candidate` |
| `sha256` | exact bundle-relative resource names mapped to lowercase SHA-256 |
| `contract_id` | lowercase SHA-256 of the bundle identity serialization |

The identity serialization is the UTF-8 encoding of
`json.dumps(sha256_map, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`
prefixed with the bytes `triad-dispatch-lib:bundle:v1\n`. This is an individual
runtime bundle ID, not an ID for every normative specification document. The
generator and loader share this small deterministic algorithm. The loader
checks the exact manifest shape, values, digest syntax, expected resource set,
recomputed identity and each payload digest before returning fresh data.
Integrity checks establish consistency, not authenticity. Current build commit
identity belongs in external CI/release evidence, outside the tracked manifest.

## Distribution and versions

Keep Python 3.12, current dependencies, four configurable routes and native host
callback contracts. Bump the unpublished package to `0.1.0.dev3` for the changed
resource provenance format. Wire schema v2, candidate status, package version
and historical spec revision are separate concepts; do not invent a published
spec tag. The wheel contains runtime assets. The sdist additionally contains
the canonical specification, its checkers/tests and generation inputs.

Claude and Codex keep independent release versions. Their future adoption
records should name the library version, bundle IDs and host adapter version.
They can adopt different compatible releases. A shared semantic change belongs
in one library PR with spec, implementation and cases together; host-specific
changes belong in the owning host repository.

## Applying the distribution research

Apply Superpowers' shared source and separate host manifests pattern to the
ownership boundary. Apply OpenSpec's common content plus small native adapters
to host ports. Apply Spec Kit's managed-file hashes and preservation of user
changes to future host installers. Use GSD's runtime-specific setup as a warning
against duplicating common orchestration logic in each host. These installer
and adapter changes are documented handoff work, not consumer mutations here.

References: [Superpowers](https://github.com/obra/superpowers),
[OpenSpec command generation](https://github.com/Fission-AI/OpenSpec/tree/main/src/core/command-generation),
[Spec Kit upgrades](https://github.github.io/spec-kit/upgrade.html),
[GSD runtime installation](https://github.com/open-gsd/gsd-core/blob/next/docs/how-to/install-on-your-runtime.md).

## Verification and limits

Compare imported original hashes and generated bytes, then test deterministic
regeneration, drift/symlink rejection and malformed manifest rejection. Run the
existing library suite together with the imported specification suite and
authoring checker. Build an sdist, rebuild its wheel, rerun both suites from the
unpacked sdist and verify all installed bundles from a neutral directory.
Retain the four existing isolated integration drivers. CI runs the same paths
on Ubuntu 24.04 and macOS 15 with Python 3.12. Report local results separately
from remote platform results and actual provider observations.

This migration changes no canonical prompt behavior, Gemini workaround, MCP
integration, SDK TODO, provider permissions or real-host deployment. It does
not establish host adoption, publication, final merge or release.
