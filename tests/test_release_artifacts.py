"""Release identity is derived from real archive metadata and bytes."""

from copy import deepcopy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import zipfile

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "release_artifacts.py"
COMMIT = "8a335f9" + "0" * 33
RELEASE = "https://github.com/codefoundry-io/triad-dispatch-lib/releases"


@pytest.fixture
def helper():
    # Missing implementation is an explicit behavioral failure during RED.
    assert SCRIPT.is_file(), "release artifact tooling is not implemented"
    spec = importlib.util.spec_from_file_location("release_artifacts", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def archives(root, version="1.2.3", wheel_name="triad-dispatch-lib", wheel_version=None,
             sdist_version=None):
    root.mkdir(exist_ok=True)
    wheel = root / f"triad_dispatch_lib-{version}-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(f"triad_dispatch_lib-{version}.dist-info/METADATA",
                         f"Metadata-Version: 2.4\nName: {wheel_name}\n"
                         f"Version: {wheel_version or version}\n\n")
    sdist = root / f"triad_dispatch_lib-{version}.tar.gz"
    metadata = (f"Metadata-Version: 2.4\nName: triad-dispatch-lib\n"
                f"Version: {sdist_version or version}\n\n").encode()
    with tarfile.open(sdist, "w:gz") as archive:
        member = tarfile.TarInfo(f"triad_dispatch_lib-{version}/PKG-INFO")
        member.size = len(metadata)
        archive.addfile(member, io.BytesIO(metadata))
    return wheel, sdist


def test_manifest_binds_archive_bytes_release_and_source(helper, tmp_path):
    wheel, sdist = archives(tmp_path)
    manifest = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    expected_artifacts = [{
        "name": path.name, "size": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "url": f"{RELEASE}/download/v1.2.3/{path.name}",
    } for path in sorted((wheel, sdist))]
    assert manifest == {
        "schema_version": 1, "name": "triad-dispatch-lib", "version": "1.2.3",
        "tag": "v1.2.3", "source_commit": COMMIT,
        "release_url": f"{RELEASE}/tag/v1.2.3", "prerelease": False,
        "artifacts": expected_artifacts,
    }
    assert helper.validate_manifest(manifest) == manifest
    for path in (wheel, sdist):
        helper.verify_artifact(path, next(a for a in expected_artifacts if a["name"] == path.name))


def test_manifest_is_fresh_and_deterministic(helper, tmp_path):
    archives(tmp_path)
    first = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    second = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    assert first == second
    first["artifacts"][0]["size"] = 0
    assert helper.build_manifest(tmp_path, "v1.2.3", COMMIT) == second


def test_prerelease_preserves_version_and_label(helper, tmp_path):
    archives(tmp_path, "1.2.3rc1")
    manifest = helper.build_manifest(tmp_path, "v1.2.3rc1", COMMIT, prerelease=True)
    assert manifest["version"] == "1.2.3rc1"
    assert manifest["prerelease"] is True


@pytest.mark.parametrize("tag", ["1.2.3", "v../1.2.3", "v1.2.3/evil", "v1.2.3?x", "v1.2.3\n", "v"])
def test_unsafe_or_nonversion_tags_are_rejected(helper, tmp_path, tag):
    archives(tmp_path)
    with pytest.raises(ValueError):
        helper.build_manifest(tmp_path, tag, COMMIT)


@pytest.mark.parametrize("commit", ["", "8a335f9", "z" * 40, "a" * 39, "a" * 40 + "\n"])
def test_invalid_source_commit_is_rejected(helper, tmp_path, commit):
    archives(tmp_path)
    with pytest.raises(ValueError):
        helper.build_manifest(tmp_path, "v1.2.3", commit)


@pytest.mark.parametrize("change", ["missing-wheel", "missing-sdist", "extra-wheel", "extra-file", "symlink"])
def test_inventory_is_exactly_one_regular_wheel_and_sdist(helper, tmp_path, change):
    wheel, sdist = archives(tmp_path)
    if change == "missing-wheel":
        wheel.unlink()
    elif change == "missing-sdist":
        sdist.unlink()
    elif change == "extra-wheel":
        (tmp_path / "other.whl").write_bytes(wheel.read_bytes())
    elif change == "extra-file":
        (tmp_path / "unexpected.txt").write_text("unexpected")
    else:
        target = tmp_path.parent / f"{tmp_path.name}-wheel"
        wheel.rename(target)
        wheel.symlink_to(target)
    with pytest.raises(ValueError):
        helper.build_manifest(tmp_path, "v1.2.3", COMMIT)


@pytest.mark.parametrize("options,tag", [
    ({"wheel_name": "another-project"}, "v1.2.3"),
    ({"wheel_version": "1.2.4"}, "v1.2.3"),
    ({"sdist_version": "1.2.4"}, "v1.2.3"),
    ({}, "v1.2.4"),
])
def test_archive_identity_must_match_tag(helper, tmp_path, options, tag):
    archives(tmp_path, **options)
    with pytest.raises(ValueError):
        helper.build_manifest(tmp_path, tag, COMMIT)


@pytest.mark.parametrize("field,value", [
    ("schema_version", True), ("name", "another-project"), ("version", "1.2.4"),
    ("release_url", "https://example.com/release"), ("prerelease", "false"),
    ("source_commit", "main"), ("tag", "v../1.2.3"),
])
def test_manifest_rejects_wrong_release_identity(helper, tmp_path, field, value):
    archives(tmp_path)
    manifest = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    manifest[field] = value
    with pytest.raises(ValueError):
        helper.validate_manifest(manifest)


@pytest.mark.parametrize("field,value", [
    ("name", "../evil.whl"), ("name", "evil\\file.whl"),
    ("size", True), ("size", 0), ("sha256", "x" * 64),
    ("url", "https://example.com/file"),
])
def test_manifest_rejects_invalid_artifact_record(helper, tmp_path, field, value):
    archives(tmp_path)
    manifest = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    manifest["artifacts"][0][field] = value
    with pytest.raises(ValueError):
        helper.validate_manifest(manifest)


def test_manifest_rejects_duplicate_and_missing_artifacts(helper, tmp_path):
    archives(tmp_path)
    manifest = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    for artifacts in (manifest["artifacts"][:1], [manifest["artifacts"][0]] * 2):
        candidate = deepcopy(manifest)
        candidate["artifacts"] = artifacts
        with pytest.raises(ValueError):
            helper.validate_manifest(candidate)


@pytest.mark.parametrize("tamper", ["bytes", "size", "name"])
def test_verify_artifact_refuses_tampering(helper, tmp_path, tamper):
    wheel, _ = archives(tmp_path)
    manifest = helper.build_manifest(tmp_path, "v1.2.3", COMMIT)
    artifact = next(a for a in manifest["artifacts"] if a["name"] == wheel.name)
    if tamper == "bytes":
        data = wheel.read_bytes()
        wheel.write_bytes(b"X" + data[1:])
    elif tamper == "size":
        wheel.write_bytes(wheel.read_bytes() + b"X")
    else:
        artifact["name"] = "wrong.whl"
    with pytest.raises(ValueError):
        helper.verify_artifact(wheel, artifact)


def test_cli_writes_valid_manifest(helper, tmp_path):
    dist = tmp_path / "dist"
    archives(dist, "1.2.3rc1")
    output = tmp_path / "triad-release.json"
    result = subprocess.run([sys.executable, str(SCRIPT), "--dist", str(dist),
                             "--tag", "v1.2.3rc1", "--source-commit", COMMIT,
                             "--prerelease", "--output", str(output)],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    manifest = json.loads(output.read_text())
    assert helper.validate_manifest(manifest)["prerelease"] is True


@pytest.mark.parametrize("collision", ["wheel", "sdist", "new-file", "symlink", "directory-alias", "hardlink"])
def test_cli_refuses_output_collision_and_preserves_artifacts(helper, tmp_path, collision):
    dist = tmp_path / "dist"
    wheel, sdist = archives(dist)
    before = {path: path.read_bytes() for path in (wheel, sdist)}
    if collision == "wheel":
        output = wheel
    elif collision == "sdist":
        output = sdist
    elif collision == "new-file":
        output = dist / "triad-release.json"
    elif collision == "directory-alias":
        alias = tmp_path / "alias"
        alias.symlink_to(dist, target_is_directory=True)
        output = alias / wheel.name
    else:
        output = tmp_path / "triad-release.json"
        if collision == "symlink":
            output.symlink_to(wheel)
        else:
            output.hardlink_to(wheel)
    result = subprocess.run([sys.executable, str(SCRIPT), "--dist", str(dist),
                             "--tag", "v1.2.3", "--source-commit", COMMIT,
                             "--output", str(output)], capture_output=True, text=True)
    assert {path: path.read_bytes() for path in before} == before
    assert result.returncode != 0
    assert "output" in result.stderr.lower()
    if collision == "new-file":
        assert not output.exists()
