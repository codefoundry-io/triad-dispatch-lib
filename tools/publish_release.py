"""Prepare reproducible archives and publish immutable GitHub release assets.

Only already-published releases in this repository are supported. This tool never
creates releases, changes tags, deletes assets or delivers host update PRs.
"""

import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import tarfile
import tempfile
import urllib.request
from urllib.parse import urlencode

try:
    from .release_artifacts import VERSION, build_manifest
    from .release_prs import GitHubAPI, SOURCE_API, resolve_tag, validate_release
except ImportError:  # Direct CLI execution.
    from release_artifacts import VERSION, build_manifest
    from release_prs import GitHubAPI, SOURCE_API, resolve_tag, validate_release


def normalize_sdist(path: Path, epoch: int) -> None:
    """Normalize tar/gzip build metadata, preserving member payloads and modes."""
    if type(epoch) is not int or not 0 <= epoch < 2**32:
        raise ValueError("epoch must be an unsigned 32-bit integer timestamp")
    if path.is_symlink() or not path.is_file():
        raise ValueError("sdist must be a regular file")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as output:
            temporary = Path(output.name)
            with tarfile.open(path, "r:gz") as source:
                with gzip.GzipFile(fileobj=output, mode="wb", filename="", mtime=epoch,
                                   compresslevel=9) as compressed:
                    with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as target:
                        for original in sorted(source.getmembers(), key=lambda member: member.name):
                            member = copy.copy(original)
                            member.mtime = epoch
                            member.uid = member.gid = 0
                            member.uname = member.gname = ""
                            member.pax_headers = {k: v for k, v in original.pax_headers.items()
                                                  if k not in ("mtime", "atime", "ctime", "uid", "gid", "uname", "gname")}
                            if original.isfile():
                                with source.extractfile(original) as payload:
                                    target.addfile(member, payload)
                            else:
                                target.addfile(member)
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Do not forward credentials or raw archive bytes to a redirect target."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class PublishAPI(GitHubAPI):
    """JSON/read transport plus one fixed official raw-asset upload endpoint."""

    def upload(self, release_id, name, raw):
        if (type(release_id) is not int or release_id <= 0
                or not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]+", name)
                or name in (".", "..") or not isinstance(raw, bytes)):
            raise ValueError("invalid release asset upload identity")
        token = os.environ.get("GH_TOKEN")
        if not token:
            raise ValueError("GH_TOKEN is required for source release uploads")
        url = f"https://uploads.github.com{SOURCE_API}/releases/{release_id}/assets?{urlencode({'name': name})}"
        request = urllib.request.Request(url, data=raw, method="POST", headers={
            "Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
            "Content-Type": "application/octet-stream", "X-GitHub-Api-Version": "2022-11-28",
        })
        try:
            with urllib.request.build_opener(NoRedirect()).open(request, timeout=60) as response:
                return json.loads(response.read())
        except (OSError, ValueError):
            raise RuntimeError(f"GitHub upload failed for {name}; inspect release assets and retry") from None


def release_context(api, tag):
    """Resolve only a non-draft, published numeric tag in the source repository."""
    if not isinstance(tag, str) or not re.fullmatch("v" + VERSION, tag, flags=re.ASCII):
        raise ValueError("invalid release tag")
    release = api.request("GET", f"{SOURCE_API}/releases/tags/{tag}")
    if (not isinstance(release, dict) or type(release.get("id")) is not int
            or release["id"] <= 0 or release.get("draft") is not False
            or not release.get("published_at") or release.get("tag_name") != tag
            or type(release.get("prerelease")) is not bool
            or release.get("html_url") != f"https://github.com/codefoundry-io/triad-dispatch-lib/releases/tag/{tag}"):
        raise ValueError("release must be published, non-draft and match the requested tag")
    if re.search(r"(?:a|b|rc)[0-9]+|\.dev[0-9]+", tag) and release["prerelease"] is not True:
        raise ValueError("development/prerelease versions require the GitHub prerelease flag before asset publication")
    return release, resolve_tag(api, tag)


def _check_assets(api, release, expected):
    """Verify every present asset before any missing asset is uploaded."""
    assets = release.get("assets")
    if not isinstance(assets, list):
        raise ValueError("invalid release asset inventory")
    present = set()
    for asset in assets:
        if not isinstance(asset, dict) or asset.get("name") not in expected:
            raise ValueError("unexpected release asset; inspect the published inventory")
        name = asset["name"]
        raw, url = expected[name]
        if name in present:
            raise ValueError(f"duplicate release asset: {name}")
        if asset.get("state") == "starter":
            raise ValueError(f"incomplete starter asset: {name}; an operator must inspect and remove it before retry")
        if (asset.get("state") != "uploaded" or type(asset.get("id")) is not int
                or asset["id"] <= 0 or asset.get("browser_download_url") != url
                or type(asset.get("size")) is not int or asset["size"] != len(raw)):
            raise ValueError(f"existing release asset identity differs: {name}")
        downloaded = api.request("GET", f"{SOURCE_API}/releases/assets/{asset['id']}")
        if not isinstance(downloaded, bytes) or downloaded != raw:
            raise ValueError(f"existing release asset bytes differ: {name}; refusing overwrite")
        present.add(name)
    return present


def publish(api, dist: Path, tag: str, source_commit: str) -> dict:
    """Attach missing verified assets; reuse exact bytes and refuse replacements."""
    release, resolved = release_context(api, tag)
    if resolved != source_commit:
        raise ValueError("tag does not resolve to the verified source commit")
    manifest = build_manifest(dist, tag, source_commit, release["prerelease"])
    validate_release(api, release, manifest)
    expected = {artifact["name"]: ((dist / artifact["name"]).read_bytes(), artifact["url"])
                for artifact in manifest["artifacts"]}
    for artifact in manifest["artifacts"]:
        raw = expected[artifact["name"]][0]
        if len(raw) != artifact["size"] or hashlib.sha256(raw).hexdigest() != artifact["sha256"]:
            raise ValueError("local artifact changed after manifest verification")
    raw_manifest = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    expected["triad-release.json"] = (raw_manifest,
        f"https://github.com/codefoundry-io/triad-dispatch-lib/releases/download/{tag}/triad-release.json")
    present = _check_assets(api, release, expected)
    missing = [name for name in expected if name not in present]
    if missing and release.get("immutable") is True:
        raise ValueError("GitHub immutable release is missing assets; this published-event workflow cannot add them. "
                         "Use a separately planned draft-build-publish release flow")
    # The manifest is last, so it never advertises artifacts we have not uploaded.
    for name in missing:
        api.upload(release["id"], name, expected[name][0])
    current = api.request("GET", f"{SOURCE_API}/releases/{release['id']}")
    validate_release(api, current, manifest)
    if _check_assets(api, current, expected) != set(expected):
        raise ValueError("release upload incomplete; retry the same verified artifacts")
    return {"status": "published" if missing else "reused", "release_url": manifest["release_url"],
            "source_commit": source_commit, "uploaded": missing}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    normalize = commands.add_parser("normalize", help="normalize an sdist locally, without credentials")
    normalize.add_argument("--sdist", type=Path, required=True)
    normalize.add_argument("--epoch", type=int, required=True)
    resolve = commands.add_parser("resolve", help="resolve a published release to its exact source SHA")
    resolve.add_argument("--tag", required=True)
    resolve.add_argument("--github-output", type=Path)
    upload = commands.add_parser("publish", help="publish missing immutable assets after CI")
    upload.add_argument("--tag", required=True)
    upload.add_argument("--source-commit", required=True)
    upload.add_argument("--dist", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "normalize":
            normalize_sdist(args.sdist, args.epoch)
            return
        if not os.environ.get("GH_TOKEN"):
            raise ValueError("GH_TOKEN is required for source release API access")
        api = PublishAPI()
        if args.command == "resolve":
            release, commit = release_context(api, args.tag)
            result = {"tag": args.tag, "source_commit": commit}
            if args.github_output:
                with args.github_output.open("a", encoding="utf-8") as output:
                    output.write(f"tag={args.tag}\nsource_commit={commit}\n")
        else:
            result = publish(api, args.dist, args.tag, args.source_commit)
        print(json.dumps(result, indent=2))
    except (ValueError, OSError, RuntimeError, KeyError, TypeError, tarfile.TarError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
