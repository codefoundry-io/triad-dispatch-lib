# Specification migration

The owner approved consolidating the shared specification in
[`triad-dispatch-lib/spec/`](README.md), alongside deterministic implementation
and tests. Consolidation merged in PR #1 at
`9489543ee24f338e9c6d0e3b032a1aa389986429`. Posting a notice in the former
`triad-dispatch-spec` repository remains separate work. That repository's history,
tags and URLs remain available; no remote retirement is claimed. Consolidation
does not itself adopt a package in a host; see the current adoption record below.

`import-origin.json` records the original repository, exact imported commit
`396a04dac310d5ff91dbe0a36982f7679aa00428` and original file hashes. It is immutable
ancestry evidence, not a current-content assertion after active guidance changes.
Historical decisions, changelog, cases and host snapshots retain their past
assertions; they are not refreshed by this migration.

`contracts/` and `prompts/` are the editable runtime sources. From the library
root, run `uv run --locked python tools/sync_spec_assets.py --write` after an
authorized source change, and `--check` before handoff. The generator needs no Git
or network access. Package data and its manifests are generated, never hand-edited.
Canonical payload bytes and legacy schema `$id` namespaces remain unchanged.

Each runtime manifest has exactly `schema_version`, `source_repository`,
`source_path`, `status`, `sha256` and `contract_id`. An ID covers one runtime
bundle, not all normative documents. It is SHA-256 of
`b"triad-dispatch-lib:bundle:v1\n"` followed by the UTF-8 encoding of
`json.dumps(sha256_map, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`.
IDs establish content consistency, not authenticity or a Git release identity.
Build commit and artifact hashes belong in external verification/release evidence.

Use [independent host adoption](../docs/host-adoption.md) for current adoption
status and future consumer ports. Shared semantics are authored here; native
spawning, model/effort controls, provider CLI setup and installer lifecycle remain
host-owned. The current unpublished `0.1.0.dev4` package, Codex's adopted dev3
source pin, candidate wire schema and historical specification tags are separate
version concepts. No new spec tag is implied.

## Old-repository notice, separate publication

PR #1 has merged; the prepared notice below records its actual merge commit.
Posting it is separate authorized work and is not claimed by this document.

> Shared specification authoring has moved to
> [triad-dispatch-lib/spec](https://github.com/codefoundry-io/triad-dispatch-lib/tree/main/spec)
> at consolidation merge commit `9489543ee24f338e9c6d0e3b032a1aa389986429`. Please submit new shared
> contract, prompt, case and deterministic implementation changes there.
> This repository remains available for its history, tags and existing links.
> Its imported source ancestry is recorded in the new repository's
> `spec/import-origin.json`. Existing host releases keep their adopted inputs;
> Claude and Codex hosts adopt and release independently. This notice does not
> announce host adoption, a new specification tag or package publication.
