# Approved adoption API verification

This record covers the remaining adoption APIs in [the approved design](../design/2026-10-15-adoption-apis.md)
and [execution plan](../superpowers/plans/2026-10-15-adoption-apis.md).
Implementation candidate: `6a7efa92093e95a5c4451a840b0db068c5c89931`.
The subsequent evidence-recording commit changes documentation only; its native
CI and formal review are recorded with the draft PR after source freeze.

## Implemented boundary

`merge_roster` exposes the validated-input merge before final resolved validation.
`validate_resolved` returns `None` after validation. `resolve_roster` retains its
dictionary result, validation/error ordering, copy behavior and one verified
schema snapshot. The intermediate document must be checked safely and validated
before consumption; native capabilities and host diagnostics remain host-owned.

`AdmissionError.missing` is `None` except for the selected canonical `required`
violation. Its value is the first absent name from that rule's trusted required
list. Existing messages, schema path and admission ordering remain unchanged.
Arbitrary duplicate `.member` is not exposed. Exception internals are outside
the documented value-free public diagnostic surface.

The installed four-route driver now exercises both roster APIs, and installed
raw replay checks root/finding missing diagnostics. Fault controls detect skipped
resolved validation and incorrect `.missing` values. Policy rule assertions pin
complete parsed rows, migration wording identifies the original consolidation,
and C15 points to the renamed test. The separate issue #5 document remains
[proposals only](../design/2026-10-15-adoption-boundary-proposals.md).

## Focused evidence

- Roster: initial missing-API RED 47 failed / 38 passed; core GREEN 85 passed;
  installed-driver guard RED 2 failed; final focused GREEN 97 passed.
- Diagnostics: missing-attribute RED 50 failed / 49 passed; runtime GREEN 127
  passed; driver control RED failed with `DID NOT RAISE`; final GREEN 160 passed.
- Policy: 24 focused tests passed. A copied `modes = ["autoEdit"]` qualifier
  escaped the old tuple comparison and failed the complete rule assertion;
  a prepended comment passed. Canonical policy bytes were never altered for
  these controls. All 11 policy/verification TOML and import-origin files were
  byte-equal to task start.
- Fresh scoped Sol reviewers found no specification or quality findings for
  the three tasks. These task reviews do not replace the project formal round.
- Static API/map audit found 29 unique documented exports and resolved 236
  file-qualified or same-line shorthand test references in the two coverage
  maps, including wildcard patterns. Standalone unqualified prose was excluded.

## Combined local execution

On macOS 26.6.2 ARM64, the frozen implementation head passed:

| Python | Source | Neutral unpacked sdist | Installed drivers |
| --- | --- | --- | --- |
| 3.12.13 | 1020 passed, 52.24 s | 1020 passed, 52.74 s | All four passed |
| 3.14.6 | 1020 passed, 52.09 s | 1020 passed, 52.56 s | All four passed |

Both source/archive environments used locked pytest 9.1.1 and passed canonical
authoring and generated-assets checks. Each sdist was built outside the checkout,
extracted with the tar data filter into its own neutral directory, tested and
rebuilt into a wheel. The four drivers were `verify_wheel.py`, `codex_smoke.py`
self-test, `four_route_smoke.py` and `native_codex_smoke.py --self-test`.
All commands returned exit 0; the complete matrix terminated without retries.

In both installed environments, the four-route report returned
`roster_split = {"validated_parity": true, "inherited_block_refused": true}`.
The new functions' origins were inside the isolated package's `site-packages`.
Raw replay passed `missing-root` and `missing-finding`, checking respectively
`review_id`/`["required"]` and `severity`/
`["properties", "findings", "items", "required"]`.

Measured artifact SHA-256 values (separate builds; no byte-reproducibility claim):

| Python | Artifact | SHA-256 |
| --- | --- | --- |
| 3.12.13 | sdist | `4de7372a3361d139f521908b304afb3be40878760b17dae7980288ab7788ec8b` |
| 3.12.13 | rebuilt wheel | `84d704d008b6b21e46e9a354b0228eaea73f3cb3c6501203a8cc0adbe73d3d99` |
| 3.14.6 | sdist | `a10d96ea20e3ec9161e172067c67fad3157b3b7a917256db6737aaa98cee6ba8` |
| 3.14.6 | rebuilt wheel | `b63bfeebf60a64393e5c4cc84f5b4f04b52da65dab533a43b0a9aeddd3691fad` |

Owner-managed evidence run `api-local-6a7efa9-r1` retains command/output logs,
eight driver reports, environment identities and before/after source custody.
HEAD, tracked/unignored source bytes, status and index remained unchanged during
the run. The recorded file inventory fingerprint is
`819150d94c7054fc4c9af299aa60b25847725c1b27725d94c66aba890d45caf0`.
These local artifacts are not part of the public package.

## Limits and next gates

All package drivers above use synthetic library inputs. They establish neither
actual provider execution nor independent consumer adoption. Source, archive,
installed wheel, native platform CI and formal review remain distinct evidence.
The package remains unpublished `0.1.0.dev4`; schema/prompt/runtime bundle bytes,
dependency floors and host/provider defaults are unchanged.

After the documentation-only record is committed, the exact PR head must pass
native Ubuntu/macOS Python 3.12/3.14 CI and a fresh public-v2 review by required
Opus 5.5/xhigh, Sol 6.1/xhigh and Argon/high, with a separate nonvoting Astra/high
comparison. Each reviewer receives 2400 seconds and current official-source web
authorization. Outcomes are retained externally with the PR so the reviewed
source remains frozen. No prior approval transfers. Merge, publication and host
adoption are separate actions.
