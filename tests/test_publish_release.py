"""Immutable release replay and deterministic archive preparation, offline."""

from copy import deepcopy
import gzip
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import zipfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
SHA = "a" * 40
TAG = "v1.2.3"
API = "/repos/codefoundry-io/triad-dispatch-lib"
URL = "https://github.com/codefoundry-io/triad-dispatch-lib/releases"


@pytest.fixture
def helper():
    script = ROOT / "tools/publish_release.py"
    assert script.is_file(), "release publisher is not implemented"
    sys.path.insert(0, str(script.parent))
    try:
        spec = importlib.util.spec_from_file_location("publish_release", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def archives(root):
    root.mkdir(exist_ok=True)
    metadata = b"Metadata-Version: 2.4\nName: triad-dispatch-lib\nVersion: 1.2.3\n\n"
    with zipfile.ZipFile(root / "triad_dispatch_lib-1.2.3-py3-none-any.whl", "w") as archive:
        archive.writestr("triad_dispatch_lib-1.2.3.dist-info/METADATA", metadata)
    with tarfile.open(root / "triad_dispatch_lib-1.2.3.tar.gz", "w:gz") as archive:
        member = tarfile.TarInfo("triad_dispatch_lib-1.2.3/PKG-INFO")
        member.size = len(metadata)
        archive.addfile(member, io.BytesIO(metadata))


class FakeAPI:
    """Only the source release endpoints and raw upload boundary are available."""

    def __init__(self):
        self.release = dict(id=7, tag_name=TAG, html_url=f"{URL}/tag/{TAG}",
                            draft=False, published_at="2026-10-16T00:00:00Z",
                            prerelease=False, body="Notes", assets=[])
        self.assets = {}
        self.uploads = []
        self.sha = SHA
        self.fail_at = None
        self.change_after_upload = False

    def request(self, method, path, payload=None):
        assert method == "GET", "publisher must never mutate release metadata"
        if path in (f"{API}/releases/tags/{TAG}", f"{API}/releases/7"):
            return deepcopy(self.release)
        if path == f"{API}/git/ref/tags/{TAG}":
            return {"object": {"type": "commit", "sha": self.sha}}
        if path.startswith(f"{API}/releases/assets/"):
            return self.assets[int(path.rsplit("/", 1)[1])]
        raise AssertionError(path)

    def upload(self, release_id, name, raw):
        assert release_id == 7
        if self.fail_at == len(self.uploads):
            raise RuntimeError("interrupted upload")
        asset = self.attach(name, raw)
        self.uploads.append(name)
        if self.change_after_upload:
            self.sha = "b" * 40
        return deepcopy(asset)

    def attach(self, name, raw):
        number = len(self.assets) + 1
        asset = dict(id=number, name=name, state="uploaded", size=len(raw),
                     browser_download_url=f"{URL}/download/{TAG}/{name}")
        self.release["assets"].append(asset)
        self.assets[number] = raw
        return asset


def test_publish_uploads_two_verified_archives_then_manifest(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    result = helper.publish(api, tmp_path, TAG, SHA)
    assert result["status"] == "published"
    assert len(api.uploads) == 3 and api.uploads[-1] == "triad-release.json"
    manifest = json.loads(api.assets[3])
    assert manifest["source_commit"] == SHA and manifest["version"] == "1.2.3"
    assert {a["name"] for a in manifest["artifacts"]} == set(api.uploads[:2])
    assert helper.publish(api, tmp_path, TAG, SHA)["status"] == "reused"
    assert len(api.uploads) == 3


def test_interrupted_upload_resumes_only_missing_assets(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    api.fail_at = 1
    with pytest.raises(RuntimeError, match="interrupted"):
        helper.publish(api, tmp_path, TAG, SHA)
    first = api.uploads[0]
    api.fail_at = None
    helper.publish(api, tmp_path, TAG, SHA)
    assert len(api.uploads) == 3 and api.uploads.count(first) == 1


@pytest.mark.parametrize("partial", [False, True])
def test_server_immutable_release_with_missing_assets_refuses_before_upload(helper, tmp_path, partial):
    archives(tmp_path)
    api = FakeAPI()
    api.release["immutable"] = True
    if partial:
        path = next(tmp_path.glob("*.whl"))
        api.attach(path.name, path.read_bytes())
    with pytest.raises(ValueError, match="immutable"):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


def test_complete_server_immutable_release_can_be_verified_and_reused(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    helper.publish(api, tmp_path, TAG, SHA)
    api.release["immutable"] = True
    assert helper.publish(api, tmp_path, TAG, SHA)["status"] == "reused"
    assert len(api.uploads) == 3


@pytest.mark.parametrize("change", ["bytes", "size", "url", "starter", "duplicate", "extra"])
def test_existing_conflicting_assets_refuse_before_any_upload(helper, tmp_path, change):
    archives(tmp_path)
    api = FakeAPI()
    path = next(tmp_path.glob("*.whl"))
    asset = api.attach(path.name, path.read_bytes())
    if change == "bytes":
        api.assets[asset["id"]] = b"x" * asset["size"]
    elif change == "size":
        asset["size"] += 1
    elif change == "url":
        asset["browser_download_url"] = "https://example.com/untrusted"
    elif change == "starter":
        asset["state"] = "starter"
    elif change == "duplicate":
        api.attach(path.name, path.read_bytes())
    else:
        api.attach("another-package.whl", b"unrelated")
    with pytest.raises(ValueError):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


def test_changed_manifest_refuses_before_uploading_missing_archives(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    api.attach("triad-release.json", b'{"source_commit":"changed"}')
    with pytest.raises(ValueError):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


@pytest.mark.parametrize("field,value", [("draft", True), ("published_at", None),
                                          ("tag_name", "v1.2.4"), ("id", True),
                                          ("html_url", "https://example.com")])
def test_invalid_release_refuses_before_upload(helper, tmp_path, field, value):
    archives(tmp_path)
    api = FakeAPI()
    api.release[field] = value
    with pytest.raises((ValueError, TypeError)):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


def test_tag_commit_must_match_verified_source(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    api.sha = "b" * 40
    with pytest.raises(ValueError):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


def test_tag_movement_after_upload_is_not_reported_success(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    api.change_after_upload = True
    with pytest.raises(ValueError):
        helper.publish(api, tmp_path, TAG, SHA)


def test_local_archive_version_mismatch_prevents_upload(helper, tmp_path):
    archives(tmp_path)
    api = FakeAPI()
    path = next(tmp_path.glob("*.whl"))
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("triad_dispatch_lib-1.2.3.dist-info/METADATA",
                         "Name: triad-dispatch-lib\nVersion: 9.0\n")
    with pytest.raises(ValueError):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


def test_archive_change_after_manifest_build_prevents_upload(helper, tmp_path, monkeypatch):
    archives(tmp_path)
    api = FakeAPI()
    original = helper.build_manifest

    def changing_manifest(*args):
        manifest = original(*args)
        next(tmp_path.glob("*.whl")).write_bytes(b"changed after verification")
        return manifest

    monkeypatch.setattr(helper, "build_manifest", changing_manifest)
    with pytest.raises(ValueError):
        helper.publish(api, tmp_path, TAG, SHA)
    assert api.uploads == []


def noisy_sdist(path, timestamp, reverse=False):
    with path.open("wb") as output:
        with gzip.GzipFile(fileobj=output, mode="wb", filename="noisy", mtime=timestamp) as stream:
            with tarfile.open(fileobj=stream, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for name in (["b", "a"] if reverse else ["a", "b"]):
                    member = tarfile.TarInfo(f"source/{name}")
                    member.mtime = timestamp
                    member.uid, member.gid = timestamp, timestamp
                    member.uname, member.gname = "builder", "staff"
                    member.mode = 0o755 if name == "b" else 0o644
                    member.pax_headers = {"mtime": str(timestamp + .5), "atime": "8", "ctime": "9",
                                          "uid": str(timestamp), "gid": str(timestamp),
                                          "uname": "builder", "gname": "staff"}
                    member.size = len(name)
                    archive.addfile(member, io.BytesIO(name.encode()))
                link = tarfile.TarInfo("source/link")
                link.type, link.linkname = tarfile.SYMTYPE, "a"
                archive.addfile(link)


def test_normalization_removes_build_metadata_but_preserves_members(helper, tmp_path):
    first, second = tmp_path / "one.tar.gz", tmp_path / "two.tar.gz"
    noisy_sdist(first, 101)
    noisy_sdist(second, 202, reverse=True)
    helper.normalize_sdist(first, 1700000000)
    helper.normalize_sdist(second, 1700000000)
    assert first.read_bytes() == second.read_bytes()
    once = first.read_bytes()
    helper.normalize_sdist(first, 1700000000)
    assert first.read_bytes() == once
    with tarfile.open(first) as archive:
        assert archive.getnames() == ["source/a", "source/b", "source/link"]
        for member in archive:
            assert (member.mtime, member.uid, member.gid, member.uname, member.gname) == (1700000000, 0, 0, "", "")
            assert not {"mtime", "atime", "ctime", "uid", "gid", "uname", "gname"} & member.pax_headers.keys()
        assert archive.extractfile("source/a").read() == b"a"
        assert archive.getmember("source/b").mode == 0o755
        assert archive.getmember("source/link").issym()
        assert archive.getmember("source/link").linkname == "a"


@pytest.mark.parametrize("epoch", [-1, True, 2**32, "10"])
def test_invalid_epoch_preserves_original_archive(helper, tmp_path, epoch):
    path = tmp_path / "source.tar.gz"
    noisy_sdist(path, 101)
    original = path.read_bytes()
    with pytest.raises(ValueError):
        helper.normalize_sdist(path, epoch)
    assert path.read_bytes() == original


def test_normalize_cli_is_offline(helper, tmp_path):
    path = tmp_path / "source.tar.gz"
    noisy_sdist(path, 101)
    env = {k: v for k, v in os.environ.items() if k not in ("GH_TOKEN", "GITHUB_TOKEN")}
    result = subprocess.run([sys.executable, str(ROOT / "tools/publish_release.py"), "normalize",
                             "--sdist", str(path), "--epoch", "1700000000"], env=env, capture_output=True)
    assert result.returncode == 0, result.stderr
    with tarfile.open(path) as archive:
        assert archive.getmember("source/a").mtime == 1700000000


def test_upload_adapter_restricts_endpoint_and_hides_credentials(helper, monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "never-print-this-token")
    captured = []

    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def read(self):
            return b'{"id":1}'

    class Opener:
        def open(self, request, timeout):
            captured.append(request)
            return Response()

    monkeypatch.setattr(helper.urllib.request, "build_opener", lambda *args: Opener())
    assert helper.PublishAPI().upload(7, "triad-release.json", b"bytes") == {"id": 1}
    assert captured[0].full_url == "https://uploads.github.com/repos/codefoundry-io/triad-dispatch-lib/releases/7/assets?name=triad-release.json"
    assert captured[0].data == b"bytes"
    for release_id, name in [(True, "safe"), (7, "../escape"), (7, "x?url=evil")]:
        with pytest.raises(ValueError):
            helper.PublishAPI().upload(release_id, name, b"bytes")
    assert len(captured) == 1


def test_upload_error_does_not_expose_provider_body_or_token(helper, monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "secret-token")

    class Opener:
        def open(self, request, timeout):
            raise OSError("secret-token provider body")

    monkeypatch.setattr(helper.urllib.request, "build_opener", lambda *args: Opener())
    with pytest.raises(RuntimeError) as error:
        helper.PublishAPI().upload(7, "triad-release.json", b"bytes")
    assert "secret-token" not in str(error.value)


def test_upload_redirect_is_not_followed(helper):
    assert helper.NoRedirect().redirect_request(None, None, 302, "redirect", {},
                                                "https://example.com") is None
