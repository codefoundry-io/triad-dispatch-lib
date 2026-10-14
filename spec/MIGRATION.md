# Specification migration

The owner approved consolidating the shared specification in
[`triad-dispatch-lib/spec/`](README.md), alongside deterministic implementation
and tests. This branch is a candidate: repository cutover awaits PR merge and a
notice in the former `triad-dispatch-spec` repository. That repository's history,
tags and URLs remain available. No remote retirement or host adoption is claimed.

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

Use [independent host adoption](../docs/host-adoption.md) for future consumer
ports. Shared semantics are authored here; native spawning, model/effort controls,
provider CLI setup and installer lifecycle remain host-owned. The unpublished
`0.1.0.dev3` package, candidate wire schema and historical specification tags are
separate version concepts. No new spec tag is implied.

## Old-repository notice, for use after merge

Copy the following only after the consolidated PR has merged, replacing the
placeholder with its actual merge commit. Posting it is separate authorized work.

> Shared specification authoring has moved to
> [triad-dispatch-lib/spec](https://github.com/codefoundry-io/triad-dispatch-lib/tree/main/spec)
> at consolidation merge commit `<actual-merge-commit>`. Please submit new shared
> contract, prompt, case and deterministic implementation changes there.
> This repository remains available for its history, tags and existing links.
> Its imported source ancestry is recorded in the new repository's
> `spec/import-origin.json`. Existing host releases keep their adopted inputs;
> Claude and Codex hosts adopt and release independently. This notice does not
> announce host adoption, a new specification tag or package publication.
