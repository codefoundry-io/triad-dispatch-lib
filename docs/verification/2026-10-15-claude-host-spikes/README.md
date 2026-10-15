# Claude host feasibility spikes — published record (2026-10-15)

The Claude host leader reports re-running scratch spikes S1-S4' into this folder.
Maintainers can inspect the scripts/results and replay them once the exact host
inputs are supplied. Scripts are in `scripts/`, captured outputs in `outputs/`,
input identities (SHA-256 of every host file read, the regenerated bundle ids, the
environment) in `input-identities.md`. The claude host's implementation branch is not yet
published; its file hashes above let a later publication be matched byte for byte.
The S4' working-copy roster override is uncommitted and supplied only as a hash;
publishing the host commit alone does not recover that measured input.

| spike | command (from the scratch root `R`; `A` = the host skill root) | result |
| --- | --- | --- |
| S1 floor probe (`scripts/s1_floor_probe.py`; the exact pytest selection is written into the output; full failure output in `outputs/s1-pytest-full.out`; wheel filenames, sizes and SHA-256 in `outputs/s1-wheel-inventory.md`) | apt-equivalent venv (`jsonschema==4.10.3`, `referencing==0.31.0`), `PYTHONPATH=src` of the library at `2d1e62e7` | `outputs/s1-floor-probe.out` |
| S2' render parity | `PYTHONPATH=$R/lib-A2/src:$A/lib python scripts/s2b_compare.py` where `lib-A2` is the library at `2d1e62e7` with `spec/prompts/*.md` and the three schemas replaced by the host's vendored bytes and `tools/sync_spec_assets.py --write` run | `outputs/s2-render-parity.out` |
| S3' admission parity | `PYTHONPATH=$R/lib/src:$A/lib python scripts/s3_verdict.py` | `outputs/s3-admission-parity.out` |
| S4' roster parity | `PYTHONPATH=$R/lib/src:$A/lib python scripts/s4b_roster.py` (the worktree path inside the script is the host checkout) | `outputs/s4-roster-parity.out` |

Limits the maintainer named and the host accepts: S2' compares the renderers over a bundle
rebuilt from host assets, not the packaged dev3 prompts (the host's vendored clauses are one
common-clauses line, one leg-claude line and one exit-tokens line behind the library's spec);
S3' compares decisions, not reason text; S4' compares sorted-JSON merged legs and
checks override `_comment`, not the complete document or native route resolution;
the reported manylinux wheel closure is CPython 3.12 x86-64 evidence only. These are
feasibility measurements for the host's own planning, not conformance or adoption evidence.

S1 supplies only a summary: its probe script, exact pytest selection, full failure
output and wheel inventory/hashes are absent. Its failure counts and wheel closure
remain attributed reports. S2-S4 are print-based probes; they do not enforce
conformance by failing on a mismatch. Captured S3 has 13 accepts and 34 rejections
(six for bindings); captured S4 has six merged legs, of which four are enabled.
