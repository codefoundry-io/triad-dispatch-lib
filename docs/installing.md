# Obtain and install the library

This guide covers obtaining and verifying `triad-dispatch-lib` for Python consumers,
including AI agents. A published GitHub Release distributes a wheel, source
distribution (sdist) and `triad-release.json` manifest containing their identities,
sizes and SHA-256 hashes. This repository distributes the library; consuming
projects own their integration, deployment and plugin lifecycle.

Discover the [latest stable release](https://github.com/codefoundry-io/triad-dispatch-lib/releases/latest)
or browse [all releases](https://github.com/codefoundry-io/triad-dispatch-lib/releases).
The latest-release URL is for discovery only and may be unavailable before a
stable release exists; inspect the release list for prereleases. Select an
acceptable exact tag and source commit before downloading or installing assets.

## Select and verify an exact source

Use the published path when your chosen tag has an acceptable published GitHub
release and verified assets; otherwise use the exact-source candidate path.
A development version such as `0.1.0.dev4` may be a local candidate or a published
prerelease: inspect the chosen release rather than inferring publication from
package metadata, a tag alone or an update PR.

Before running the selection script, provide Python >=3.12 with working `venv`
and `ensurepip`; [venv bootstraps pip through ensurepip by default](https://docs.python.org/3.12/library/venv.html).
For Ubuntu 24.04's distro Python 3.12, this requires
[`python3.12-venv`](https://packages.ubuntu.com/noble/all/python3.12-venv/filelist).
For other Debian/Ubuntu interpreters, use the venv package matching that Python
version. Arrange any missing OS prerequisite separately before continuing; this
guide does not install OS packages. The source-build `uv` prerequisite is separate.

Choose an owner-reviewed full lowercase source commit. For a published install,
also choose an explicit release tag (`v` plus its package version), verify that
GitHub marks it published rather than draft, and decide whether its prerelease
status is acceptable. Record the decision; do not use floating `latest` or `main`.
Assemble the selection block below, exactly ONE of the published/candidate blocks,
and the install/smoke block into ONE dedicated shell script, then run that script
as a separate process (for example, `sh /path/to/install-library.sh`). Replace its
placeholders first. Do not paste `set -eu` into the user's interactive shell.
All selected blocks must share the same process: `WORK`, `PY` and `SOURCE_COMMIT`
are its shell variables. If your tool starts a fresh shell for every call,
combine the selected blocks in that one script before executing it. Never
concatenate both source alternatives. The script creates a new temporary directory.

```sh
#!/bin/sh
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
: "${WORK:?Run source selection first in the same dedicated script}"
: "${PY:?Run source selection first in the same dedicated script}"
: "${SOURCE_COMMIT:?Run source selection first in the same dedicated script}"
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

This build path requires a compatible `uv` on `PATH`; the documented commands
were tested with `uv 0.11.8` (an observation, not an exact-version requirement or
minimum supported version). If it is unavailable, follow the
[official uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/)
before using this path. Check availability/version before building:

```sh
: "${WORK:?Run source selection first in the same dedicated script}"
: "${PY:?Run source selection first in the same dedicated script}"
: "${SOURCE_COMMIT:?Run source selection first in the same dedicated script}"
command -v uv
uv --version
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
for repeatable consumer packaging rather than assuming these ranges are a lock.

```sh
: "${WORK:?Run source selection first in the same dedicated script}"
: "${PY:?Run source selection first in the same dedicated script}"
: "${SOURCE_COMMIT:?Run source selection first in the same dedicated script}"
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

## Platform dependencies and offline installation

Collect wheels while online on each supported native OS/architecture/Python/ABI
combination. Use the verified local library wheel from either path above, rather
than asking an index for a library package name. This example uses the same
dedicated script variables; the collection environment's Python selects its
native dependency wheels. Keep both optional blocks below in that same dedicated
script/process so their variables remain available:

```sh
: "${WORK:?Run source selection first in the same dedicated script}"
: "${PY:?Run source selection first in the same dedicated script}"
set -- "$WORK/artifacts/"*.whl
test "$#" -eq 1
LIB_WHEEL="$1"
WHEELHOUSE="$WORK/wheelhouse"
mkdir "$WHEELHOUSE"
"$PY" -I -m pip --isolated --disable-pip-version-check download \
  --only-binary=:all: --dest "$WHEELHOUSE" "$LIB_WHEEL"
```

Pin and hash every collected wheel, and retain the library manifest/source pin.
Transfer those verified files to the offline target with the same native Python
and platform combination. For a local offline-install check, create another fresh
environment and install the exact collected library wheel without an index:

```sh
: "${WORK:?Run source selection first in the same dedicated script}"
: "${PY:?Run source selection first in the same dedicated script}"
: "${WHEELHOUSE:?Run online collection first in the same dedicated script}"
: "${LIB_WHEEL:?Run online collection first in the same dedicated script}"
"$PY" -I -m venv "$WORK/offline-env"
OFFLINE_PY="$WORK/offline-env/bin/python"
"$OFFLINE_PY" -I -m pip --isolated --disable-pip-version-check install \
  --no-index --find-links "$WHEELHOUSE" --only-binary=:all: \
  "$WHEELHOUSE/$(basename "$LIB_WHEEL")"
"$OFFLINE_PY" -I -m pip check
```

Run the existing Python smoke heredoc above using `"$OFFLINE_PY" -I -
"$WORK/offline-env" "$WORK/artifacts"` as its invocation; skip the online install
line. Keep the verified manifest and original artifact available for its checks.
See the official [pip download](https://pip.pypa.io/en/stable/cli/pip_download/)
and [pip install](https://pip.pypa.io/en/stable/cli/pip_install/) references.
`rpds-py` contains native code: one manylinux CPython wheel set proves neither
macOS nor a different Python ABI. Do not silently compile or remove offline
Registry checks when a binary wheel is unavailable.

## Consumer integration and library updates

See the [public API](../spec/reference/library-api.md),
[conformance coverage](../spec/reference/library-conformance.md) and
[host-adoption contracts](host-adoption.md) for integration boundaries. Consumers
own API mapping, native adapters, provider setup, deployment and plugin lifecycle.
Installing this library alone does not change a consuming application.

For a library update, select and verify another exact release/source pin, create
a fresh environment and repeat the installation/smoke checks. Retain the previous
library artifact, source pin and dependency inventory for a library rollback;
restore them in a fresh environment and repeat the checks. Consumer deployment
and application rollback remain the consuming project's responsibility.

Record the selected tag/full source commit and published-or-candidate status;
manifest and artifact size/hash; installed library path/version; dependency
inventory and native platform/Python; verified bundle IDs/digest maps; smoke
commands/results; previous library pin; and explicitly unrun checks. Library
installation evidence does not establish consumer integration or provider execution.
