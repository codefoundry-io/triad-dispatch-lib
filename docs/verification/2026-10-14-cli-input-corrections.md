# CLI input corrections

Date: 2026-10-14. Baseline: `81748d7` plus the preserved R1-R4 corrections and
specification/interface documentation. R4 completed `AGREED`; its approvals do
not transfer to these changed bytes.

## Authorized work and scope

1. Reproduce and fix oversized native-driver timeout input before publication.
2. Normalize cyclic CLI wheel/run-parent path errors to existing controlled
   refusal, with actual cyclic-file regression cases.
3. Verify the combined source, unpacked sdist and rebuilt installed wheel on
   local macOS and native Ubuntu CI.
4. Review a fresh frozen basis with Opus 5.5/xhigh, Sol 6.1/xhigh and Argon/high;
   retain a separate Astra/high comparison, with 2400 seconds for each.

Expected incremental production delta: about 15 additions / 5 deletions (net 10),
under 20 novel core lines, across three repository-only drivers. Tests and
documentation are counted separately. The core library timeout domain, schema,
provider defaults and host execution ownership are unchanged.

The incremental production change is 15 additions / 6 deletions (net 9).
Six CLI regression cases failed before correction and pass afterward: two native
cases and cyclic wheel leaf/ancestor cases in each of the two smoke CLIs.
The new tests add 91 lines. Full source verification passes **686 tests** on
macOS 26.6.2 ARM64 / Python 3.12.13, with authoring, generated assets, diff and
27-export / 53-test-reference checks passing.

An adjacent public `verify_wheel.py` path was checked independently. Its existing
`is_file()` guard already rejects both cyclic cases with exit 2, empty stdout
and no traceback, so no source change was needed there. Hidden
`--installed-prefix` values are internally generated identity handoffs, outside
this public input correction; invalid internal identity remains a failed probe.

Unpacked-sdist verification also passed **686 tests**, authoring and generation
checks. Its rebuilt wheel passed the isolated bundle probe, Codex prompt/admission
driver, four-route synthetic matrix and supervised-native synthetic driver.
Measured local artifacts:

- sdist: `f0604de8b975fed2895ad857439007d1f2620b054356a415395bf4b759549abb`
- wheel: `9b97c728d85d5dddaff00b70adf614e5cf80c25fbf117ed50a4abab4807ed4b1`

The measurement paragraphs were added after the local build; runtime, tests and
generated assets are unchanged. The temporary build environment was removed.
Native CI builds the subsequent committed candidate independently. Its exact
head, job results and logs belong to the external run record below and the
[draft PR](https://github.com/codefoundry-io/triad-dispatch-lib/pull/1) checks.

A fresh Sol/medium decision probe followed the new external-evidence instruction
for a recent-model scenario and retained local contract inspection for a pure
arithmetic control. This is prompt-only, child-reported behavior evidence; it
does not establish actual provider success or review-tool containment.

Web is authorized for all reviews. The project review profile now requires
current official sources for changing external facts, recording URL, access
date and applicable versions; unavailable evidence remains an explicit limit.
Python 3.12 documentation was consulted on 2026-10-14 for the supported baseline:
[Path.resolve](https://docs.python.org/3.12/library/pathlib.html#pathlib.Path.resolve)
reports cyclic resolution with `RuntimeError`. Current
[Python documentation](https://docs.python.org/3/library/pathlib.html#pathlib.Path.resolve)
records a changed loop behavior from Python 3.13; current-version documentation
must not be substituted for the project's tested 3.12 behavior.

## Evidence boundaries

Fresh task evidence is retained under the owner's external run directory
`_runs/reviews/20261014-lib-minor-fixes/`. RED/GREEN results, platform and package
identities, CI URL/head, fresh review ID and adjudication are recorded there.
Historical 680-test R4 results precede these corrections. A completed review,
native platform test, real provider exercise, host adoption and release are
separate claims. This work authorizes neither final merge nor publication.
