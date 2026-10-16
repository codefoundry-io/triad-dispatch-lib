# Install, adopt and update the library

This guide is for AI agents and maintainers working in a consuming host, including
Claude, Codex and agents using the AGY route. AGY is a supported execution route,
not a third delivery repository. Installing this Python library does not install
a host plugin, configure providers or port host code. The two delivery targets
are `codefoundry-io/triad-codex-dispatch` and `codefoundry-io/triad-dispatch`.

## Select and verify an exact source

As of 2026-10-16, this library has no published release. `0.1.0.dev4` is a source
candidate; use the candidate path below until a release exists. Never infer a
released version from package metadata, a tag alone or an update PR.

Read the host's instructions, adoption record and dirty state before changing it.
Choose an owner-reviewed full lowercase source commit. For a published install,
also choose an explicit release tag (`v` plus its package version), verify that
GitHub marks it published rather than draft, and decide whether its prerelease
status is acceptable. Record the decision; do not use floating `latest` or `main`.
Replace the placeholder before running these commands in a new temporary directory:

```sh
set -eu
SOURCE_COMMIT=REPLACE_WITH_REVIEWED_40_HEX_COMMIT
WORK=$(mktemp -d)
git clone https://github.com/codefoundry-io/triad-dispatch-lib.git "$WORK/source"
git -C "$WORK/source" checkout --detach "$SOURCE_COMMIT"
test "$(git -C "$WORK/source" rev-parse HEAD)" = "$SOURCE_COMMIT"
python3 --version  # must be >=3.12
python3 -c 'import sys; assert sys.version_info >= (3, 12)'
python3 -m venv "$WORK/env"
PY="$WORK/env/bin/python"
mkdir "$WORK/artifacts"
cd "$WORK"
```

The checkout supplies the reviewed `tools/release_artifacts.py` verifier and API
reference. Trust and review that source before executing it. Hashes establish
content consistency, not publisher authenticity; establish trust in the chosen
repository, source commit and release through your normal review process.

## Published wheel path

Set the exact reviewed tag, then download and validate `triad-release.json` and
its single wheel. The verifier rejects unexpected manifest fields, wrong package,
tag/version, source-commit shape, artifact inventory and URLs. The explicit
comparisons below also bind it to your chosen source and tag. A failed check
stops installation; do not repair the manifest or bypass the check.

```sh
TAG=REPLACE_WITH_PUBLISHED_TAG
"$PY" -I - "$WORK/source" "$WORK/artifacts" "$TAG" "$SOURCE_COMMIT" <<'PY'
import json, pathlib, sys, urllib.request
source, dest = map(pathlib.Path, sys.argv[1:3])
tag, commit = sys.argv[3:5]
sys.path.insert(0, str(source / "tools"))
from release_artifacts import validate_manifest, verify_artifact
base = "https://github.com/codefoundry-io/triad-dispatch-lib/releases/download/"
# Validate the requested identity before constructing a request URL.
import re
assert re.fullmatch(r"v[0-9]+(?:\.[0-9]+)*(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?", tag)
assert re.fullmatch(r"[0-9a-f]{40}", commit)
raw = urllib.request.urlopen(base + tag + "/triad-release.json").read()
manifest = validate_manifest(json.loads(raw))
assert manifest["tag"] == tag and manifest["source_commit"] == commit
(dest / "triad-release.json").write_bytes(raw)
wheel = next(a for a in manifest["artifacts"] if a["name"].endswith(".whl"))
path = dest / wheel["name"]
path.write_bytes(urllib.request.urlopen(wheel["url"]).read())
verify_artifact(path, wheel)
print(json.dumps({"version": manifest["version"], "prerelease": manifest["prerelease"],
                  "wheel": str(path), "sha256": wheel["sha256"]}, indent=2))
PY
```

Review the printed prerelease status against your decision. Retain the manifest
and chosen source identity with the adoption evidence. The manifest is release
provenance; do not insert its fields into runtime bundle manifests.

## Exact-source candidate fallback

When no acceptable published release exists, build only from the exact source
selected above, using the repository's `uv` build workflow. The fresh checkout
must remain clean. An sdist rebuilt into a wheel verifies the distribution path.
This is a local candidate, even when its manifest contains release-shaped URLs;
those URLs do not imply published assets and must not be used as download proof.

```sh
uv build --python "$PY" --sdist --out-dir "$WORK/build" "$WORK/source"
uv build --python "$PY" --wheel --out-dir "$WORK/build" "$WORK/build/"*.tar.gz
# uv may create auxiliary files; copy only the two distributions for validation.
cp "$WORK/build/"*.tar.gz "$WORK/build/"*.whl "$WORK/artifacts/"
"$PY" -I - "$WORK/source" "$WORK/artifacts" "$SOURCE_COMMIT" <<'PY'
import json, pathlib, sys, tomllib
source, dest = map(pathlib.Path, sys.argv[1:3])
sys.path.insert(0, str(source / "tools"))
from release_artifacts import build_manifest, verify_artifact
version = tomllib.loads((source / "pyproject.toml").read_text())["project"]["version"]
manifest = build_manifest(dest, "v" + version, sys.argv[3], prerelease=True)
for artifact in manifest["artifacts"]:
    verify_artifact(dest / artifact["name"], artifact)
# Keep the manifest outside the exact wheel+sdist inventory directory.
(dest.parent / "candidate-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print("LOCAL CANDIDATE", version, sys.argv[3])
PY
```

## Install and smoke-test the selected wheel

Both paths leave exactly one wheel in `artifacts`. Install into the fresh Python
>=3.12 environment with binary dependencies only, then check dependencies. The
metadata requires `jsonschema>=4.26,<5` and `referencing>=0.37,<1`; older system
packages are insufficient. Record the resolved dependency versions and hashes
for repeatable host packaging rather than assuming these ranges are a lock.

```sh
"$PY" -I -m pip --isolated --disable-pip-version-check install --only-binary=:all: "$WORK/artifacts/"*.whl
"$PY" -I -m pip check
"$PY" -I - "$WORK/env" "$WORK/artifacts" <<'PY'
import hashlib, importlib.metadata as md, importlib.resources as resources
import json, pathlib, platform, sys, zipfile
import triad_dispatch_lib as lib
prefix, artifacts = map(pathlib.Path, sys.argv[1:3])
path = pathlib.Path(lib.__file__).resolve()
assert path.is_relative_to(prefix.resolve()) and "site-packages" in path.parts
wheel, = artifacts.glob("*.whl")
release_manifest = artifacts / "triad-release.json"
selected = json.loads((release_manifest if release_manifest.exists()
                       else artifacts.parent / "candidate-manifest.json").read_text())
assert md.version("triad-dispatch-lib") == selected["version"]
wheel_record, = (a for a in selected["artifacts"] if a["name"] == wheel.name)
assert wheel.stat().st_size == wheel_record["size"]
assert hashlib.sha256(wheel.read_bytes()).hexdigest() == wheel_record["sha256"]
with zipfile.ZipFile(wheel) as archive:
    metadata, = (n for n in archive.namelist() if n.endswith(".dist-info/METADATA"))
    from email.parser import BytesParser
    info = BytesParser().parsebytes(archive.read(metadata))
    assert info["Name"] == "triad-dispatch-lib"
    assert md.version("triad-dispatch-lib") == info["Version"]
data = resources.files("triad_dispatch_lib").joinpath("data")
bundles = {}
for name, directory in (("verdict", data), ("roster", data.joinpath("roster-bundle")),
                        ("prompts", data.joinpath("prompt-bundle")),
                        ("receipt", data.joinpath("receipt-bundle"))):
    manifest = json.loads(directory.joinpath("source-manifest.json").read_bytes())
    assert set(manifest) == {"schema_version", "source_repository", "source_path",
                             "status", "sha256", "contract_id"}
    assert manifest["schema_version"] == 1 and manifest["status"] == "candidate"
    assert manifest["source_repository"] == "https://github.com/codefoundry-io/triad-dispatch-lib"
    assert manifest["source_path"] == "spec"
    for relative, digest in manifest["sha256"].items():
        assert hashlib.sha256(directory.joinpath(relative).read_bytes()).hexdigest() == digest
    canonical = json.dumps(manifest["sha256"], sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(b"triad-dispatch-lib:bundle:v1\n" + canonical.encode()).hexdigest() == manifest["contract_id"]
    bundles[name] = manifest
assert sum(len(m["sha256"]) for m in bundles.values()) == 9
# Public APIs exercise each packaged schema, including negative admission.
binding = dict(review_id="install-smoke", family="codex", content_digest="a" * 64,
               leg_name="codex", attempt=1, route=None)
lib.validate_binding(binding)
assert lib.load_roster_contract()["$schema"].endswith("2020-12/schema")
try:
    lib.validate_resolved({})
except lib.RosterError as error:
    assert error.code == "schema_violation" and error.document == "resolved"
else:
    raise AssertionError("invalid roster accepted")
lib.validate_transport_receipt(dict(schema_version=2, stdin_delivery="complete",
                                   route="codex", binary="codex", cli_version="smoke", attempt=1))
assert lib.render_investigation_prompt("Installation smoke", family="google", route="agy", web_authorized=True)
print(json.dumps({"version": md.version("triad-dispatch-lib"), "path": str(path),
                  "python": platform.python_version(), "platform": platform.platform(),
                  "dependencies": {n: md.version(n) for n in ("jsonschema", "referencing", "rpds-py", "attrs")},
                  "bundles": bundles, "public_api_smoke": "passed"}, indent=2))
PY
```

The bundle audit uses standard-library resource/hash operations; there is no
package-root `verify_bundles` API. Public operations also verify their packaged
resources on use and refuse remote reference retrieval. Bundle `status=candidate`
is a runtime contract literal, independent of whether the wheel was released.
This smoke is consistency/API evidence, not provider or complete host conformance.

## Adopt selectively in the host

Map the exact [public API](../spec/reference/library-api.md) and
[conformance coverage](../spec/reference/library-conformance.md) to host call sites.
Use `parse_json`/`validate_binding`/`validate_verdict` for strict original JSON and
six-field admission, roster APIs for merge/validation/selection, rendering APIs for
canonical clauses, `validate_transport_receipt` for nested transport shape, and
`admit_output`/`evaluate_agreement` where their documented semantics match. The
callback coordinators are optional. A schema-valid receipt does not attest execution.

Preserve native spawning, model/effort controls, route discovery, provider setup,
authentication, packet/attempt custody, cancellation/cleanup, fresh integrity,
failure classification and installer preservation in the host. Follow the
[required adapter contracts](host-adoption.md#required-adapter-contracts), including
AGY recovery and host-fault boundaries. Do not replace a host adapter merely
because a similarly named library function exists.

For host-owned vendoring, update its explicit source/version pin, file inventory,
hashes, dependency closure and adoption record together. Codex's existing pinned
`vendor_library.py` restores its recorded pin; running it alone is not an upgrade.
An absent Claude adoption record means unrecorded, not proof of no adoption.
Keep legacy schema identities and six-field runtime manifests intact.

For offline distribution, use `pip download --only-binary=:all:` on each supported
native OS/architecture/Python/ABI combination to collect the selected library
wheel and its complete dependency closure. Pin and hash every wheel, then verify
`pip install --no-index --find-links <wheelhouse>` into a fresh environment and run
this smoke plus host tests. `rpds-py` contains native code: one manylinux CPython
wheel set proves neither macOS nor a different Python ABI. Do not silently compile
or remove offline Registry checks when a binary wheel is unavailable.

Test changed call sites with positive cases and refusals: duplicate/malformed JSON,
binding mismatch, negative verdict retention, roster overrides/disabled entries,
prompt parity, transport failures, stale attempts, integrity faults and cooperative
cancellation as applicable. Retain host-specific deviations and route tests. A
passing library test suite alone does not establish host adoption.

## Release, install, update and roll back the host independently

Review and release the host port separately, recording its library pin. Install
that host release using its current official instructions; library installation
above does not change an already installed plugin. These references were checked
on 2026-10-16; reread them before executing their current installer commands.

- **Codex:** follow [installation](https://github.com/codefoundry-io/triad-codex-dispatch/blob/main/docs/installation.md).
  Register the intended marketplace, install with `codex plugin add
  triad-codex-dispatch@triad-codex-dispatch --json`, and use its returned absolute
  `installedPath` for `scripts/bootstrap.sh --install` from the target project.
  For updates, first run the old installed bootstrap's `--remove` successfully,
  then remove the plugin, refresh the registered marketplace or pinned local source,
  reinstall, run the new installed bootstrap and start a fresh Codex session.
- **Claude:** follow [installation and permission setup](https://github.com/codefoundry-io/triad-dispatch/blob/main/README.md).
  Use `/plugin marketplace add codefoundry-io/triad-dispatch` and `/plugin install
  triad-dispatch@triad-dispatch`. Run installed `scripts/setup_permissions.py` from
  each target project (or with its explicit `--target`), then restart. Update via
  `claude plugin update triad-dispatch`, rerun permission setup for the same targets
  using the new installed script, and restart. AGY setup remains in host scripts.

Verify fresh-session skill exposure and the adopted APIs/routes separately from
successful installation. Provider authentication and real route execution require
host evidence. On failure, preserve user edits and diagnostics, then restore the
previous reviewed host release/source and its recorded library/dependency pin via
that host's lifecycle. Reinstall and restart, then repeat the affected checks.
Rolling back only this library wheel cannot roll back a vendored host plugin.

Report: selected tag/full source commit and published-or-candidate status; manifest
and artifact size/hash; installed path/version; dependency inventory and native
platform/Python; consumed bundle IDs/digest maps; host commit/release and API map;
test commands/results/deviations; installation/restart/fresh-session observations;
rollback target; and explicitly unrun checks. Keep release, adoption, installation
and real-provider results as separate claims.
