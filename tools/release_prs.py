"""Deliver verified published library releases as independent host update PRs."""

import argparse
import base64
import html
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from urllib.parse import quote, urlencode

try:
    from .release_artifacts import VERSION, build_manifest, validate_manifest, verify_artifact
except ImportError:  # Direct CLI execution.
    from release_artifacts import VERSION, build_manifest, validate_manifest, verify_artifact


SOURCE = "codefoundry-io/triad-dispatch-lib"
TARGETS = ("codefoundry-io/triad-codex-dispatch", "codefoundry-io/triad-dispatch")
SOURCE_API = f"/repos/{SOURCE}"


class GitHubAPI:
    """Small gh transport; tokens stay in the environment and never in arguments."""

    def __init__(self, *, source_token=None):
        self.source_token = source_token

    def request(self, method, path, payload=None):
        if not path.startswith("/repos/codefoundry-io/") or ":" in path or "\n" in path:
            raise ValueError("only GitHub repository API paths are supported")
        binary = bool(re.fullmatch(SOURCE_API + r"/releases/assets/[0-9]+", path))
        args = ["gh", "api", "--hostname", "github.com", "--method", method, path,
                "-H", "Accept: " + ("application/octet-stream" if binary else "application/vnd.github+json")]
        if payload is not None:
            args += ["--input", "-"]
        environment = dict(os.environ)
        if self.source_token is not None and (path == SOURCE_API or path.startswith(SOURCE_API + "/")):
            environment["GH_TOKEN"] = self.source_token
        result = subprocess.run(args, input=None if payload is None else json.dumps(payload).encode(),
                                capture_output=True, check=False, env=environment)
        if result.returncode:
            # Do not print provider output, headers or credential material.
            if method == "GET" and b"(HTTP 404)" in result.stderr:
                return None
            raise RuntimeError(f"GitHub {method} {path} failed; check token permissions and retry")
        return result.stdout if binary else json.loads(result.stdout or b"null")


def _target(target):
    if target not in TARGETS:
        raise ValueError("target must be one of the two supported host repositories")


def _release_metadata(release, manifest):
    validate_manifest(manifest)
    if (type(release.get("id")) is not int or release["id"] <= 0
            or release.get("draft") is not False or not release.get("published_at")
            or release.get("tag_name") != manifest["tag"]
            or release.get("html_url") != manifest["release_url"]
            or release.get("prerelease") is not manifest["prerelease"]):
        raise ValueError("release must be published, non-draft and match the manifest")


def resolve_tag(api, tag):
    """Resolve this library's numeric release tag, including annotated tag chains."""
    if not isinstance(tag, str) or not re.fullmatch("v" + VERSION, tag, flags=re.ASCII):
        raise ValueError("invalid release tag")
    obj = api.request("GET", f"{SOURCE_API}/git/ref/tags/{tag}")
    if not obj:
        raise ValueError("release tag is missing")
    obj = obj["object"]
    for _ in range(8):
        if obj["type"] == "commit":
            break
        if obj["type"] != "tag":
            raise ValueError("release tag must resolve to a commit")
        obj = api.request("GET", f"{SOURCE_API}/git/tags/{obj['sha']}")["object"]
    if obj["type"] != "commit" or not re.fullmatch(r"[0-9a-f]{40}", obj["sha"]):
        raise ValueError("release tag must resolve to a full commit SHA")
    return obj["sha"]


def validate_release(api, release, manifest):
    """Bind a manifest to current published metadata and the actual tagged commit."""
    _release_metadata(release, manifest)
    current = api.request("GET", f"{SOURCE_API}/releases/{release['id']}")
    if _release_identity(current) != _release_identity(release):
        raise ValueError("release metadata changed; reload the published release")
    if resolve_tag(api, manifest["tag"]) != manifest["source_commit"]:
        raise ValueError("release tag does not resolve to manifest source_commit")


def _release_identity(release):
    """Select release content/asset identity, excluding mutable usage counters."""
    if not isinstance(release, dict) or not isinstance(release.get("assets"), list):
        raise ValueError("invalid published release metadata")
    fields = ("id", "tag_name", "html_url", "draft", "prerelease", "published_at", "name", "body")
    asset_fields = ("id", "name", "size", "state", "browser_download_url", "url", "digest",
                    "created_at", "updated_at", "content_type", "label")
    assets = []
    for asset in release["assets"]:
        if not isinstance(asset, dict):
            raise ValueError("invalid published release asset metadata")
        assets.append({field: asset.get(field) for field in asset_fields})
    return ({field: release.get(field) for field in fields}, assets)


def _asset(release, name, url):
    matches = [a for a in release.get("assets", []) if a.get("name") == name]
    if (len(matches) != 1 or matches[0].get("browser_download_url") != url
            or matches[0].get("state") != "uploaded"
            or type(matches[0].get("id")) is not int or matches[0]["id"] <= 0):
        raise ValueError(f"release asset identity mismatch: {name}")
    return matches[0]


def load_manifest(api, release):
    tag = release["tag_name"]
    # Validate the tag before incorporating it into an expected URL.
    if not re.fullmatch("v" + VERSION, tag, flags=re.ASCII):
        raise ValueError("invalid release tag")
    asset = _asset(release, "triad-release.json",
                   f"https://github.com/{SOURCE}/releases/download/{tag}/triad-release.json")
    raw = api.request("GET", f"{SOURCE_API}/releases/assets/{asset['id']}")
    if not isinstance(raw, bytes) or len(raw) != asset["size"]:
        raise ValueError("manifest asset size mismatch")
    return validate_manifest(json.loads(raw))


def _verify_downloads(api, release, manifest):
    if load_manifest(api, release) != manifest:
        raise ValueError("attached manifest differs from the requested release identity")
    with tempfile.TemporaryDirectory(prefix="triad-release-") as directory:
        for artifact in manifest["artifacts"]:
            asset = _asset(release, artifact["name"], artifact["url"])
            if asset["size"] != artifact["size"]:
                raise ValueError("release asset size differs from manifest")
            raw = api.request("GET", f"{SOURCE_API}/releases/assets/{asset['id']}")
            if not isinstance(raw, bytes):
                raise ValueError("artifact download must return bytes")
            path = Path(directory) / artifact["name"]
            path.write_bytes(raw)
            verify_artifact(path, artifact)
        # Hashes alone cannot certify package identity: inspect archive metadata too.
        checked = build_manifest(Path(directory), manifest["tag"], manifest["source_commit"],
                                 manifest["prerelease"])
        if checked["artifacts"] != sorted(manifest["artifacts"], key=lambda a: a["name"]):
            raise ValueError("downloaded package identity differs from manifest")


def render_notice(release: dict, manifest: dict, target: str,
                  previous_version: str | None = None) -> str:
    """Render shared library retrieval guidance and release notes as inert data."""
    _target(target)
    _release_metadata(release, manifest)
    tag = manifest["tag"]
    prerelease = manifest["prerelease"] or bool(re.search(r"(?:a|b|rc)[0-9]|\.dev[0-9]", manifest["version"]))
    previous = (f"Recorded library version: `{html.escape(previous_version)}`."
                if previous_version else
                "Recorded library version: unrecorded; absence is not proof of no adoption.")
    artifacts = "\n".join(f"- [{a['name']}]({a['url']}): {a['size']} bytes; SHA-256 `{a['sha256']}`."
                          for a in manifest["artifacts"])
    return f"""# Library update request: {tag}{' (Prerelease/development package)' if prerelease else ''}

<!-- triad-library-update source={SOURCE} release={release['id']} target={target} -->

[Published release]({manifest['release_url']}); package pin
`triad-dispatch-lib=={manifest['version']}`;
[source commit `{manifest['source_commit']}`](https://github.com/{SOURCE}/tree/{manifest['source_commit']}).
{previous}

Pending host adoption. Application and release decisions belong to each
recipient; this notice supplies no host verification evidence.

## Release notes (data)

<pre>{html.escape(release.get('body') or '(No release notes supplied.)')}</pre>

## Downloads and source

[Release manifest](https://github.com/{SOURCE}/releases/download/{tag}/triad-release.json)
records the exact wheel/sdist identities below.

{artifacts}

For library installation or a source build, use the version-pinned
[installation and source-build guide](https://github.com/{SOURCE}/blob/{tag}/docs/installing.md)
and [API documentation](https://github.com/{SOURCE}/blob/{tag}/spec/reference/library-api.md).
Verify the exact version, source commit and downloaded artifact SHA-256 before use.

Discover other versions in [all releases](https://github.com/{SOURCE}/releases),
including prereleases, or [the latest stable release](https://github.com/{SOURCE}/releases/latest).
These discovery links do not replace this notice's exact pin and artifact URLs.
"""


def _context(api, target, base_sha=None):
    repo = f"/repos/{target}"
    default = api.request("GET", repo)["default_branch"]
    base = base_sha or api.request("GET", f"{repo}/git/ref/heads/{quote(default, safe='/')}")["object"]["sha"]
    record = api.request("GET", f"{repo}/contents/contracts/library-adoption.json?ref={quote(base, safe='')}")
    previous = None
    if record is not None:
        if (not isinstance(record, dict) or record.get("type") != "file"
                or record.get("encoding") != "base64" or not isinstance(record.get("content"), str)):
            raise ValueError("adoption record must be a regular JSON file")
        value = json.loads(base64.b64decode(record["content"]))
        if not isinstance(value, dict):
            raise ValueError("invalid existing library adoption record: expected a JSON object")
        previous = value.get("version")
        if value.get("name") != "triad-dispatch-lib" or not isinstance(previous, str) or not previous:
            raise ValueError("invalid existing library adoption record")
    return default, base, previous


def _files(release, manifest, target, previous):
    prefix = f"docs/library-updates/{manifest['tag']}/"
    return {prefix + "release.json": json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            prefix + "README.md": render_notice(release, manifest, target, previous)}


def _tree(api, repo, sha):
    value = api.request("GET", f"{repo}/git/trees/{sha}?recursive=1")
    if not isinstance(value, dict) or not isinstance(value.get("tree"), list):
        raise ValueError("cannot inspect missing or invalid Git tree")
    if value.get("truncated") is not False:
        raise ValueError("cannot safely inspect a truncated Git tree")
    return {e["path"]: {k: e[k] for k in ("mode", "type", "sha")}
            for e in value["tree"] if e["type"] != "tree"}


def deliver(api, release: dict, manifest: dict, target: str) -> dict:
    """Create one proposal, preserving all prior PR states and conflicting branches."""
    _target(target)
    validate_release(api, release, manifest)
    repo = f"/repos/{target}"
    branch = f"automation/triad-lib/{manifest['tag']}"
    query = urlencode({"state": "all", "head": f"{target.split('/')[0]}:{branch}", "per_page": 100})
    prs = api.request("GET", f"{repo}/pulls?{query}")
    if prs:
        return {"status": "existing", "url": prs[0]["html_url"]}
    _verify_downloads(api, release, manifest)
    default, base, previous = _context(api, target)
    existing = api.request("GET", f"{repo}/git/ref/heads/{branch}")
    if existing:
        commit = api.request("GET", f"{repo}/git/commits/{existing['object']['sha']}")
        if len(commit["parents"]) != 1:
            raise ValueError("existing branch has unexpected ancestry")
        parent = commit["parents"][0]["sha"]
        comparison = api.request("GET", f"{repo}/compare/{parent}...{base}")
        if comparison["status"] not in ("ahead", "identical"):
            raise ValueError("existing branch contains unrelated commits")
        # Render against the branch's original adoption record, even if main advanced.
        _, _, previous = _context(api, target, parent)
        files = _files(release, manifest, target, previous)
        original = api.request("GET", f"{repo}/git/commits/{parent}")
        before = _tree(api, repo, original["tree"]["sha"])
        after = _tree(api, repo, commit["tree"]["sha"])
        changed = {p for p in before.keys() | after.keys() if before.get(p) != after.get(p)}
        if changed != set(files) or any(p in before for p in files):
            raise ValueError("existing branch changes differ from the two generated additions")
        for path, content in files.items():
            entry = after[path]
            if entry["mode"] != "100644" or entry["type"] != "blob":
                raise ValueError("existing notice must contain regular files")
            blob = api.request("GET", f"{repo}/git/blobs/{entry['sha']}")
            if not isinstance(blob, dict) or not isinstance(blob.get("content"), str):
                raise ValueError("cannot inspect missing or invalid Git blob; preserving branch")
            if blob.get("encoding") != "base64" or base64.b64decode(blob["content"]) != content.encode():
                raise ValueError("existing branch notice differs; preserving maintainer edits")
    else:
        files = _files(release, manifest, target, previous)
        commit = api.request("GET", f"{repo}/git/commits/{base}")
        before = _tree(api, repo, commit["tree"]["sha"])
        if any(path == old or path.startswith(old + "/") or old.startswith(path + "/")
               for path in files for old in before):
            raise ValueError("generated notice collides with existing target content")
        entries = []
        for path, content in files.items():
            blob = api.request("POST", f"{repo}/git/blobs", {"content": content, "encoding": "utf-8"})
            entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        tree = api.request("POST", f"{repo}/git/trees", {"base_tree": commit["tree"]["sha"], "tree": entries})
        new = api.request("POST", f"{repo}/git/commits", {"message": f"Record library update proposal {manifest['tag']}",
                          "tree": tree["sha"], "parents": [base]})
        api.request("POST", f"{repo}/git/refs", {"ref": f"refs/heads/{branch}", "sha": new["sha"]})
    pr = api.request("POST", f"{repo}/pulls", {"title": f"Library update request: {manifest['tag']}",
                    "head": branch, "base": default, "body": files[f"docs/library-updates/{manifest['tag']}/README.md"]})
    return {"status": "created", "url": pr["html_url"]}


def preview(api, release, manifest, target, directory):
    """Read and verify live metadata, then write only a local preview."""
    _target(target)
    validate_release(api, release, manifest)
    _verify_downloads(api, release, manifest)
    _, _, previous = _context(api, target)
    for path, content in _files(release, manifest, target, previous).items():
        output = Path(directory) / target / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
    return {"status": "preview", "directory": str(directory)}


def deliver_targets(api, release, manifest, targets=TARGETS, dry_run_dir=None):
    results = {}
    for target in targets:
        try:
            results[target] = (preview(api, release, manifest, target, dry_run_dir)
                               if dry_run_dir is not None else deliver(api, release, manifest, target))
        except (ValueError, RuntimeError, OSError, KeyError, TypeError) as error:
            results[target] = {"status": "error", "error": str(error)}
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--target", choices=TARGETS)
    parser.add_argument("--dry-run-dir", type=Path)
    args = parser.parse_args()
    if not os.environ.get("GH_TOKEN"):
        parser.error("GH_TOKEN is required; configure a GitHub App token for the two host repositories")
    source_token = os.environ.get("SOURCE_GH_TOKEN")
    if not source_token:
        parser.error("SOURCE_GH_TOKEN is required; use the source workflow GITHUB_TOKEN separately from the host App token")
    if not re.fullmatch("v" + VERSION, args.tag, flags=re.ASCII):
        parser.error("invalid release tag")
    api = GitHubAPI(source_token=source_token)
    try:
        release = api.request("GET", f"{SOURCE_API}/releases/tags/{args.tag}")
        if not release:
            raise ValueError("published release was not found")
        manifest = load_manifest(api, release)
        results = deliver_targets(api, release, manifest,
                                  (args.target,) if args.target else TARGETS, args.dry_run_dir)
    except (ValueError, RuntimeError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(results, indent=2))
    if any(result["status"] == "error" for result in results.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
