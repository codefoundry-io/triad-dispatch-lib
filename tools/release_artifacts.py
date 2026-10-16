"""Describe and verify this repository's wheel/sdist release artifacts.

This checks release identity and archive metadata without extracting or installing
packages. Release tags use canonical numeric Python versions (including a/b/rc,
post and dev suffixes), prefixed by v.
"""

import argparse
from email.parser import BytesParser
from email.policy import compat32
import hashlib
import json
from pathlib import Path
import re
import tarfile
import zipfile


NAME = "triad-dispatch-lib"
RELEASES = "https://github.com/codefoundry-io/triad-dispatch-lib/releases"
VERSION = r"[0-9]+(?:\.[0-9]+)*(?:(?:a|b|rc)[0-9]+)?(?:\.post[0-9]+)?(?:\.dev[0-9]+)?"


def _version(tag: str) -> str:
    if not isinstance(tag, str) or not re.fullmatch("v" + VERSION, tag, flags=re.ASCII):
        raise ValueError("tag must be v followed by a canonical numeric Python version")
    return tag[1:]


def _commit(value: str) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("source_commit must be a full lowercase Git SHA-1")


def _kind(name: str, version: str) -> str:
    if not isinstance(name, str):
        raise ValueError("artifact name must be a filename")
    if re.fullmatch(r"triad_dispatch_lib-" + re.escape(version)
                    + r"-(?:[0-9][a-zA-Z0-9_]*-)?[a-zA-Z0-9_.]+-[a-zA-Z0-9_.]+-[a-zA-Z0-9_.]+\.whl", name):
        return "wheel"
    if name in (f"triad_dispatch_lib-{version}.tar.gz", f"triad-dispatch-lib-{version}.tar.gz"):
        return "sdist"
    raise ValueError("artifact filename must identify the tagged library wheel or sdist")


def _artifact(value: dict) -> None:
    if not isinstance(value, dict) or set(value) != {"name", "size", "sha256", "url"}:
        raise ValueError("artifact must contain name, size, sha256 and url")
    name = value["name"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]+", name) or name in (".", ".."):
        raise ValueError("artifact name must be a safe filename")
    if type(value["size"]) is not int or value["size"] <= 0:
        raise ValueError("artifact size must be a positive integer")
    if not isinstance(value["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", value["sha256"]):
        raise ValueError("artifact sha256 must be lowercase hexadecimal")
    if not isinstance(value["url"], str):
        raise ValueError("artifact url must be a string")


def validate_manifest(value: dict) -> dict:
    """Return a validated manifest; reject unbound release/artifact identities."""
    fields = {"schema_version", "name", "version", "tag", "source_commit",
              "release_url", "prerelease", "artifacts"}
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError("manifest has unexpected or missing fields")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1 or value["name"] != NAME:
        raise ValueError("unsupported manifest schema or package")
    version = _version(value["tag"])
    if value["version"] != version:
        raise ValueError("manifest version does not match tag")
    _commit(value["source_commit"])
    if type(value["prerelease"]) is not bool:
        raise ValueError("prerelease must be a boolean")
    if value["release_url"] != f"{RELEASES}/tag/{value['tag']}":
        raise ValueError("release_url does not match repository and tag")
    artifacts = value["artifacts"]
    if not isinstance(artifacts, list) or len(artifacts) != 2:
        raise ValueError("release must contain exactly one wheel and one sdist")
    kinds = []
    for artifact in artifacts:
        _artifact(artifact)
        kinds.append(_kind(artifact["name"], version))
        if artifact["url"] != f"{RELEASES}/download/{value['tag']}/{artifact['name']}":
            raise ValueError("artifact url does not match repository, tag and name")
    if sorted(kinds) != ["sdist", "wheel"]:
        raise ValueError("release must contain exactly one wheel and one sdist")
    return value


def _regular_file(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"artifact must be a regular file: {path.name}")


def _digest(path: Path) -> tuple[int, str]:
    _regular_file(path)
    with path.open("rb") as stream:
        size = 0
        digest = hashlib.sha256()
        while block := stream.read(1024 * 1024):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def verify_artifact(path: Path, artifact: dict) -> None:
    """Refuse a filename, size or digest mismatch for a local artifact."""
    _artifact(artifact)
    if path.name != artifact["name"]:
        raise ValueError("artifact filename mismatch")
    size, digest = _digest(path)
    if size != artifact["size"] or digest != artifact["sha256"]:
        raise ValueError(f"artifact size or sha256 mismatch: {path.name}")


def _metadata(raw: bytes, version: str) -> None:
    metadata = BytesParser(policy=compat32).parsebytes(raw, headersonly=True)
    if metadata.get_all("Name") != [NAME] or metadata.get_all("Version") != [version]:
        raise ValueError("archive metadata name/version must match library and tag")


def _check_archive(path: Path, kind: str, version: str) -> None:
    try:
        if kind == "wheel":
            with zipfile.ZipFile(path) as archive:
                members = [entry for entry in archive.infolist()
                           if entry.filename.endswith(".dist-info/METADATA")]
                expected = f"triad_dispatch_lib-{version}.dist-info/METADATA"
                if len(members) != 1 or members[0].filename != expected:
                    raise ValueError("wheel must contain one matching METADATA")
                _metadata(archive.read(members[0]), version)
        else:
            with tarfile.open(path, "r:gz") as archive:
                members = [entry for entry in archive.getmembers()
                           if entry.name.count("/") == 1 and entry.name.endswith("/PKG-INFO")]
                expected = path.name.removesuffix(".tar.gz") + "/PKG-INFO"
                if len(members) != 1 or members[0].name != expected or not members[0].isfile():
                    raise ValueError("sdist must contain one matching regular PKG-INFO")
                with archive.extractfile(members[0]) as stream:
                    _metadata(stream.read(), version)
    except (zipfile.BadZipFile, tarfile.TarError, EOFError) as error:
        raise ValueError(f"invalid {kind} archive: {path.name}") from error


def build_manifest(dist: Path, tag: str, source_commit: str, prerelease: bool = False) -> dict:
    """Build a deterministic manifest from exactly two tagged release archives."""
    version = _version(tag)
    _commit(source_commit)
    if type(prerelease) is not bool:
        raise ValueError("prerelease must be a boolean")
    if not dist.is_dir():
        raise ValueError("dist must be a directory containing a wheel and sdist")
    paths = sorted(dist.iterdir())
    if len(paths) != 2:
        raise ValueError("dist must contain exactly one wheel and one sdist")
    artifacts = []
    for path in paths:
        kind = _kind(path.name, version)
        _regular_file(path)
        _check_archive(path, kind, version)
        size, digest = _digest(path)
        artifacts.append({"name": path.name, "size": size, "sha256": digest,
                          "url": f"{RELEASES}/download/{tag}/{path.name}"})
    return validate_manifest({
        "schema_version": 1, "name": NAME, "version": version, "tag": tag,
        "source_commit": source_commit, "release_url": f"{RELEASES}/tag/{tag}",
        "prerelease": prerelease, "artifacts": artifacts,
    })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--prerelease", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        manifest = build_manifest(args.dist, args.tag, args.source_commit, args.prerelease)
        args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (ValueError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
