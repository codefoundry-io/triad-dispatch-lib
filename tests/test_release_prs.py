"""Release notices and GitHub state transitions, without live mutations."""

import base64
from copy import deepcopy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import subprocess
import tarfile
import zipfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "codefoundry-io/triad-dispatch-lib"
TARGET = "codefoundry-io/triad-codex-dispatch"
CLAUDE = "codefoundry-io/triad-dispatch"
SHA = "a" * 40
TAG = "v1.2.3"
BRANCH = "automation/triad-lib/v1.2.3"
PREFIX = "docs/library-updates/v1.2.3/"


@pytest.fixture
def helper():
    script = ROOT / "tools/release_prs.py"
    assert script.is_file(), "release PR delivery is not implemented"
    sys.path.insert(0, str(script.parent))
    try:
        spec = importlib.util.spec_from_file_location("release_prs", script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


def fixture():
    url = f"https://github.com/{SOURCE}/releases"
    wheel, sdist = archive_bytes()
    artifacts = [{"name": name, "size": len(data),
                  "sha256": hashlib.sha256(data).hexdigest(),
                  "url": f"{url}/download/{TAG}/{name}"}
                 for name, data in [("triad_dispatch_lib-1.2.3-py3-none-any.whl", wheel),
                                    ("triad_dispatch_lib-1.2.3.tar.gz", sdist)]]
    manifest = dict(schema_version=1, name="triad-dispatch-lib", version="1.2.3",
                    tag=TAG, source_commit=SHA, release_url=f"{url}/tag/{TAG}",
                    prerelease=False, artifacts=artifacts)
    assets = [dict(id=i + 1, name=a["name"], size=a["size"],
                   browser_download_url=a["url"], state="uploaded")
              for i, a in enumerate(artifacts)]
    raw = json.dumps(manifest).encode()
    assets.append(dict(id=3, name="triad-release.json", size=len(raw), state="uploaded",
                       browser_download_url=f"{url}/download/{TAG}/triad-release.json"))
    release = dict(id=7, tag_name=TAG, html_url=manifest["release_url"], draft=False,
                   prerelease=False, published_at="2026-10-16T00:00:00Z",
                   target_commitish="main", body="A fix.\n$(touch /tmp/never)\n```sh\nevil\n```",
                   assets=assets)
    return release, manifest, {1: wheel, 2: sdist, 3: raw}


def archive_bytes(version="1.2.3"):
    metadata = f"Metadata-Version: 2.4\nName: triad-dispatch-lib\nVersion: {version}\n\n".encode()
    wheel = io.BytesIO()
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("triad_dispatch_lib-1.2.3.dist-info/METADATA", metadata)
    sdist = io.BytesIO()
    with tarfile.open(fileobj=sdist, mode="w:gz") as archive:
        member = tarfile.TarInfo("triad_dispatch_lib-1.2.3/PKG-INFO")
        member.size = len(metadata)
        archive.addfile(member, io.BytesIO(metadata))
    return wheel.getvalue(), sdist.getvalue()


class FakeAPI:
    """Model the GitHub endpoints that delivery is permitted to use."""

    def __init__(self):
        self.release, self.manifest, self.assets = fixture()
        self.calls = []
        self.prs = []
        self.branch = None
        self.adoption = None
        self.trees = {"base-tree": {}}
        self.commits = {"base": {"sha": "base", "tree": {"sha": "base-tree"}, "parents": []}}
        self.blobs = {}
        self.deny = None

    @property
    def writes(self):
        return [(m, p, v) for m, p, v in self.calls if m != "GET"]

    def request(self, method, path, payload=None):
        self.calls.append((method, path, deepcopy(payload)))
        if self.deny and f"/repos/{self.deny}/" in path:
            raise RuntimeError("permission denied")
        if path.startswith(f"/repos/{SOURCE}/"):
            tail = path.split(f"/repos/{SOURCE}/")[1]
            if tail in ("releases/7", f"releases/tags/{TAG}"):
                return deepcopy(self.release)
            if tail == f"git/ref/tags/{TAG}":
                return {"object": {"type": "commit", "sha": SHA}}
            if tail.startswith("releases/assets/"):
                return self.assets[int(tail.rsplit("/", 1)[1])]
        for target in (TARGET, CLAUDE):
            if path == f"/repos/{target}":
                return {"default_branch": "main"}
            prefix = f"/repos/{target}/"
            if not path.startswith(prefix):
                continue
            tail = path[len(prefix):]
            if method == "GET":
                if tail.startswith("pulls?"):
                    assert "state=all" in tail and "head=codefoundry-io%3Aautomation%2Ftriad-lib%2Fv1.2.3" in tail
                    return deepcopy(self.prs)
                if tail == "git/ref/heads/main":
                    return {"object": {"sha": "base"}}
                if tail == f"git/ref/heads/{BRANCH}":
                    return None if self.branch is None else {"object": {"sha": self.branch}}
                if tail.startswith("git/commits/"):
                    return self.commits[tail.split("/")[-1]]
                if tail.startswith("git/trees/"):
                    tree = self.trees[tail.split("/")[-1].split("?")[0]]
                    return {"truncated": False, "tree": [dict(path=p, **entry) for p, entry in tree.items()]}
                if tail.startswith("git/blobs/"):
                    raw = self.blobs[tail.split("/")[-1]]
                    return {"encoding": "base64", "content": base64.b64encode(raw).decode()}
                if tail.startswith("contents/contracts/library-adoption.json?"):
                    return None if self.adoption is None else {"type": "file", "encoding": "base64",
                        "content": base64.b64encode(json.dumps(self.adoption).encode()).decode()}
                if tail.startswith("compare/"):
                    return {"status": "identical"}
            if method == "POST":
                if tail == "git/blobs":
                    sha = f"blob{len(self.blobs)}"
                    self.blobs[sha] = payload["content"].encode()
                    return {"sha": sha}
                if tail == "git/trees":
                    assert payload["base_tree"] == "base-tree"
                    tree = deepcopy(self.trees["base-tree"])
                    tree.update({e["path"]: {k: v for k, v in e.items() if k != "path"}
                                 for e in payload["tree"]})
                    self.trees["new-tree"] = tree
                    return {"sha": "new-tree"}
                if tail == "git/commits":
                    self.commits["new-commit"] = {"tree": {"sha": payload["tree"]},
                        "parents": [{"sha": s} for s in payload["parents"]]}
                    return {"sha": "new-commit"}
                if tail == "git/refs":
                    assert payload == {"ref": f"refs/heads/{BRANCH}", "sha": "new-commit"}
                    self.branch = "new-commit"
                    return {}
                if tail == "pulls":
                    self.prs.append({"number": 12, "html_url": "https://github.com/example/pull/12", "state": "open"})
                    return self.prs[-1]
        raise AssertionError(f"unexpected request: {method} {path}")


@pytest.mark.parametrize("target,guide,command", [
    (TARGET, "docs/installation.md", "codex plugin"),
    (CLAUDE, "README.md", "/plugin update")])
def test_notice_preserves_data_and_explains_host_boundaries(helper, target, guide, command):
    release, manifest, _ = fixture()
    notice = helper.render_notice(release, manifest, target)
    for text in (guide, command, "1.2.3", SHA, "Pending host adoption", "Host CI: pending",
                 "Pre-merge", "Post-host-release", "Rollback", "unrecorded",
                 "docs/installing.md", "$(touch /tmp/never)"):
        assert text in notice
    for artifact in manifest["artifacts"]:
        assert artifact["sha256"] in notice and artifact["url"] in notice
    assert "not proof" in notice
    assert "```\nevil" not in notice  # Notes remain escaped inert quoted data.


def test_notice_marks_prerelease_and_previous_version(helper):
    release, manifest, _ = fixture()
    release["prerelease"] = manifest["prerelease"] = True
    notice = helper.render_notice(release, manifest, TARGET, "0.1.0.dev3")
    assert "Prerelease" in notice and "0.1.0.dev3" in notice
    assert "restores the existing pin" in notice


@pytest.mark.parametrize("version", ["1.2.3rc1", "1.2.3.dev1", "1.2.3a1", "1.2.3b2"])
def test_prerelease_version_is_marked_even_when_github_flag_is_false(helper, version):
    release, manifest, _ = fixture()
    manifest["version"] = version
    manifest["tag"] = release["tag_name"] = "v" + version
    manifest["release_url"] = release["html_url"] = f"https://github.com/{SOURCE}/releases/tag/v{version}"
    for artifact in manifest["artifacts"]:
        artifact["name"] = artifact["name"].replace("1.2.3", version)
        artifact["url"] = f"https://github.com/{SOURCE}/releases/download/v{version}/{artifact['name']}"
    assert "Prerelease/development package" in helper.render_notice(release, manifest, TARGET)


def test_hash_matching_archive_with_wrong_metadata_is_refused(helper):
    api = FakeAPI()
    api.assets[1], api.assets[2] = archive_bytes("9.9.9")
    for i, artifact in enumerate(api.manifest["artifacts"], 1):
        artifact["size"] = api.release["assets"][i - 1]["size"] = len(api.assets[i])
        artifact["sha256"] = hashlib.sha256(api.assets[i]).hexdigest()
    api.assets[3] = json.dumps(api.manifest).encode()
    api.release["assets"][2]["size"] = len(api.assets[3])
    with pytest.raises(ValueError):
        helper.deliver(api, api.release, api.manifest, TARGET)
    assert not api.writes


@pytest.mark.parametrize("target", [TARGET, CLAUDE])
def test_create_adds_only_two_regular_files_without_force(helper, target):
    api = FakeAPI()
    result = helper.deliver(api, api.release, api.manifest, target)
    assert result["status"] == "created"
    tree = next(v for _, p, v in api.writes if p.endswith("git/trees"))
    assert {e["path"] for e in tree["tree"]} == {PREFIX + "README.md", PREFIX + "release.json"}
    assert all(e["mode"] == "100644" and e["type"] == "blob" for e in tree["tree"])
    assert all(m == "POST" and "force" not in (v or {}) for m, _, v in api.writes)
    body = next(v["body"] for _, p, v in api.writes if p.endswith("pulls"))
    assert f"source={SOURCE} release=7 target={target}" in body
    assert all(any(p.endswith(f"releases/assets/{i}") for _, p, _ in api.calls[:api.calls.index(api.writes[0])])
               for i in (1, 2, 3))


@pytest.mark.parametrize("state", ["open", "closed", "merged"])
def test_any_prior_pr_is_metadata_only_skip(helper, state):
    api = FakeAPI()
    api.prs = [{"number": 4, "state": "closed" if state == "merged" else state,
                "merged_at": "now" if state == "merged" else None, "html_url": "https://example/pr/4"}]
    assert helper.deliver(api, api.release, api.manifest, TARGET)["status"] == "existing"
    assert not api.writes
    assert not any("releases/assets/" in p for _, p, _ in api.calls)


def test_matching_interrupted_branch_recovers_without_rewriting(helper):
    api = FakeAPI()
    helper.deliver(api, api.release, api.manifest, TARGET)
    api.prs.clear()
    api.calls.clear()
    assert helper.deliver(api, api.release, api.manifest, TARGET)["status"] == "created"
    assert [p for _, p, _ in api.writes] == [f"/repos/{TARGET}/pulls"]


@pytest.mark.parametrize("conflict", ["content", "unrelated", "mode", "extra-commit", "base-collision", "base-directory"])
def test_conflicting_branch_or_base_is_preserved(helper, conflict):
    api = FakeAPI()
    helper.deliver(api, api.release, api.manifest, TARGET)
    api.prs.clear()
    api.calls.clear()
    if conflict == "content":
        api.blobs["blob0"] = b"maintainer edit"
    elif conflict == "unrelated":
        api.trees["new-tree"]["unrelated.txt"] = {"mode": "100644", "type": "blob", "sha": "extra"}
    elif conflict == "mode":
        api.trees["new-tree"][PREFIX + "README.md"]["mode"] = "120000"
    elif conflict == "extra-commit":
        api.commits["new-commit"]["parents"] = [{"sha": "other"}]
        api.request_original = api.request
        api.request = lambda m, p, v=None: {"status": "diverged"} if "/compare/" in p else api.request_original(m, p, v)
    else:
        api.branch = None
        path = "docs" if conflict == "base-collision" else PREFIX + "README.md/existing.txt"
        api.trees["base-tree"][path] = {"mode": "100644", "type": "blob", "sha": "extra"}
    with pytest.raises(ValueError):
        helper.deliver(api, api.release, api.manifest, TARGET)
    assert not api.writes


@pytest.mark.parametrize("damage", ["draft", "unpublished", "tag", "commit", "manifest", "wheel", "sdist", "url"])
def test_invalid_release_or_download_refused_before_target_writes(helper, damage):
    api = FakeAPI()
    release = deepcopy(api.release)
    if damage == "draft":
        release["draft"] = api.release["draft"] = True
    elif damage == "unpublished":
        release["published_at"] = api.release["published_at"] = None
    elif damage == "tag":
        release["tag_name"] = api.release["tag_name"] = "v9.9.9"
    elif damage == "commit":
        api.manifest["source_commit"] = "b" * 40
    elif damage in ("manifest", "wheel", "sdist"):
        api.assets[{"manifest": 3, "wheel": 1, "sdist": 2}[damage]] = b"tampered"
    else:
        release["assets"][0]["browser_download_url"] = api.release["assets"][0]["browser_download_url"] = "https://evil.invalid/a"
    with pytest.raises(ValueError):
        helper.deliver(api, release, api.manifest, TARGET)
    assert not api.writes


@pytest.mark.parametrize("record,expected", [(None, "unrecorded"),
    ({"name": "triad-dispatch-lib", "version": "0.1.0.dev3"}, "0.1.0.dev3")])
def test_preview_reads_previous_adoption_and_never_mutates_github(helper, tmp_path, record, expected):
    api = FakeAPI()
    api.adoption = record
    helper.preview(api, api.release, api.manifest, TARGET, tmp_path)
    assert not api.writes
    files = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*") if p.is_file())
    assert files == [TARGET + "/" + PREFIX + "README.md", TARGET + "/" + PREFIX + "release.json"]
    assert expected in (tmp_path / TARGET / PREFIX / "README.md").read_text()


def test_delivery_targets_fail_independently(helper):
    api = FakeAPI()
    api.deny = TARGET
    results = helper.deliver_targets(api, api.release, api.manifest, (TARGET, CLAUDE))
    assert results[TARGET]["status"] == "error"
    assert results[CLAUDE]["status"] == "created"
    assert not any(f"/repos/{TARGET}/" in p for _, p, _ in api.writes)


def test_unknown_target_is_refused_without_requests(helper):
    api = FakeAPI()
    with pytest.raises(ValueError):
        helper.deliver(api, api.release, api.manifest, "codefoundry-io/agy")
    assert not api.calls


def test_annotated_tag_is_resolved_instead_of_trusting_main(helper):
    api = FakeAPI()
    original = api.request

    def request(method, path, payload=None):
        if path == f"/repos/{SOURCE}/git/ref/tags/{TAG}":
            return {"object": {"type": "tag", "sha": "b" * 40}}
        if path == f"/repos/{SOURCE}/git/tags/{'b' * 40}":
            return {"object": {"type": "commit", "sha": SHA}}
        return original(method, path, payload)

    api.request = request
    assert helper.deliver(api, api.release, api.manifest, TARGET)["status"] == "created"


def test_truncated_tree_refuses_writes(helper):
    api = FakeAPI()
    original = api.request
    api.request = lambda m, p, v=None: {"truncated": True, "tree": []} if "/git/trees/" in p else original(m, p, v)
    with pytest.raises(ValueError, match="truncated"):
        helper.deliver(api, api.release, api.manifest, TARGET)
    assert not api.writes


def test_cli_dry_run_writes_previews_for_both_targets(helper, monkeypatch, tmp_path, capsys):
    api = FakeAPI()
    credentials = []

    def client(*, source_token):
        credentials.append(source_token)
        return api

    monkeypatch.setattr(helper, "GitHubAPI", client)
    monkeypatch.setenv("GH_TOKEN", "fixture-secret")
    monkeypatch.setenv("SOURCE_GH_TOKEN", "fixture-source-secret")
    monkeypatch.setattr(sys, "argv", ["release_prs.py", "--tag", TAG, "--dry-run-dir", str(tmp_path)])
    helper.main()
    output = json.loads(capsys.readouterr().out)
    assert {target: result["status"] for target, result in output.items()} == {TARGET: "preview", CLAUDE: "preview"}
    assert not api.writes
    assert len(list(tmp_path.rglob("release.json"))) == 2
    assert credentials == ["fixture-source-secret"]
    assert not any("fixture-secret" in p.read_text() for p in tmp_path.rglob("*") if p.is_file())


def test_cli_missing_token_is_actionable_and_has_no_network(helper):
    result = subprocess.run([sys.executable, str(ROOT / "tools/release_prs.py"), "--tag", TAG],
                            env={k: v for k, v in os.environ.items() if k != "GH_TOKEN"},
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert "GH_TOKEN is required" in result.stderr and "GitHub App" in result.stderr


def test_transport_keeps_release_data_out_of_shell_and_credentials_out_of_arguments(helper, monkeypatch):
    calls = []

    def run(args, **kwargs):
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, 0, stdout=b'{"sha":"new"}', stderr=b"")

    monkeypatch.setenv("GH_TOKEN", "fixture-secret")
    monkeypatch.setattr(helper.subprocess, "run", run)
    payload = {"body": "$(touch /tmp/never); `do-not-execute`"}
    helper.GitHubAPI().request("POST", f"/repos/{TARGET}/pulls", payload)
    args, options = calls[0]
    assert args[:6] == ["gh", "api", "--hostname", "github.com", "--method", "POST"]
    assert "fixture-secret" not in str(args)
    assert "$(touch" not in str(args)
    assert not options.get("shell")
    assert json.loads(options["input"]) == payload


@pytest.mark.parametrize("record", [{"name": "other", "version": "1"},
                                    {"name": "triad-dispatch-lib", "version": None}])
def test_invalid_adoption_record_is_preserved_and_refuses_writes(helper, record):
    api = FakeAPI()
    api.adoption = record
    with pytest.raises(ValueError):
        helper.deliver(api, api.release, api.manifest, TARGET)
    assert not api.writes


def counting_api():
    """GitHub increments asset counters while target repositories stay independent."""
    source = FakeAPI()
    targets = {target: FakeAPI() for target in (TARGET, CLAUDE)}
    for asset in source.release["assets"]:
        asset["download_count"] = 0
    original = source.request

    def request(method, path, payload=None):
        if path.startswith(f"/repos/{SOURCE}/"):
            result = original(method, path, payload)
            if "/releases/assets/" in path:
                asset_id = int(path.rsplit("/", 1)[1])
                next(a for a in source.release["assets"] if a["id"] == asset_id)["download_count"] += 1
            return result
        target = next(t for t in targets if path == f"/repos/{t}" or path.startswith(f"/repos/{t}/"))
        return targets[target].request(method, path, payload)

    source.request = request
    return source, targets


def test_cli_manifest_download_counter_change_does_not_invalidate_release(helper, monkeypatch, tmp_path, capsys):
    api, targets = counting_api()
    monkeypatch.setattr(helper, "GitHubAPI", lambda **kwargs: api)
    monkeypatch.setenv("GH_TOKEN", "fixture-secret")
    monkeypatch.setenv("SOURCE_GH_TOKEN", "fixture-source-secret")
    monkeypatch.setattr(sys, "argv", ["release_prs.py", "--tag", TAG, "--dry-run-dir", str(tmp_path)])
    helper.main()
    result = json.loads(capsys.readouterr().out)
    assert [result[t]["status"] for t in (TARGET, CLAUDE)] == ["preview", "preview"]
    assert all(not target.writes for target in targets.values())
    assert api.release["assets"][2]["download_count"] >= 3


def test_first_target_download_counters_do_not_block_second_target(helper):
    api, targets = counting_api()
    release = deepcopy(api.release)
    results = helper.deliver_targets(api, release, api.manifest)
    assert [results[t]["status"] for t in (TARGET, CLAUDE)] == ["created", "created"]
    assert all(any(p.endswith("/pulls") for _, p, _ in target.writes) for target in targets.values())
    assert all(a["download_count"] == 2 for a in api.release["assets"])


@pytest.mark.parametrize("field", ["body", "name", "id", "published_at", "asset-id", "asset-name",
                                   "asset-url", "asset-size", "asset-state", "asset-digest"])
def test_meaningful_release_or_asset_changes_still_refuse_writes(helper, field):
    api = FakeAPI()
    release = deepcopy(api.release)
    if field.startswith("asset-"):
        key = {"url": "browser_download_url"}.get(field[6:], field[6:])
        api.release["assets"][0][key] = "changed"
    else:
        api.release[field] = "changed"
    with pytest.raises(ValueError, match="metadata changed"):
        helper.deliver(api, release, api.manifest, TARGET)
    assert not api.writes


@pytest.mark.parametrize("record", [[], None, "invalid", 1, {"library": []},
    {"name": "triad-dispatch-lib", "version": []},
    {"name": "triad-dispatch-lib", "version": {}},
    {"name": "triad-dispatch-lib", "version": 1},
    {"name": "triad-dispatch-lib", "version": False},
    {"name": "triad-dispatch-lib", "version": ""}])
def test_bad_adoption_shape_is_target_local_and_second_target_continues(helper, record):
    api, targets = counting_api()
    original = api.request

    def request(method, path, payload=None):
        if path.startswith(f"/repos/{TARGET}/contents/contracts/library-adoption.json?"):
            return {"type": "file", "encoding": "base64",
                    "content": base64.b64encode(json.dumps(record).encode()).decode()}
        return original(method, path, payload)

    api.request = request
    results = helper.deliver_targets(api, deepcopy(api.release), api.manifest)
    assert results[TARGET]["status"] == "error"
    assert "adoption record" in results[TARGET]["error"]
    assert results[CLAUDE]["status"] == "created"
    assert not targets[TARGET].writes


def test_source_and_target_credentials_use_separate_child_environments(helper, monkeypatch, capsys):
    calls = []
    monkeypatch.setenv("GH_TOKEN", "host-app-secret")
    monkeypatch.setenv("SOURCE_GH_TOKEN", "workflow-source-secret")
    before = dict(os.environ)

    def run(args, **kwargs):
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args, 0, stdout=b"{}", stderr=b"")

    monkeypatch.setattr(helper.subprocess, "run", run)
    api = helper.GitHubAPI(source_token="workflow-source-secret")
    paths = [f"/repos/{SOURCE}/releases/7", f"/repos/{SOURCE}/releases/assets/1",
             f"/repos/{TARGET}/pulls", f"/repos/{CLAUDE}/git/refs"]
    for path in paths:
        api.request("GET" if path.startswith(f"/repos/{SOURCE}/") else "POST", path)
    assert [options["env"]["GH_TOKEN"] for _, options in calls] == [
        "workflow-source-secret", "workflow-source-secret", "host-app-secret", "host-app-secret"]
    assert dict(os.environ) == before
    assert all("host-app-secret" not in str(args) and "workflow-source-secret" not in str(args)
               for args, _ in calls)
    assert capsys.readouterr() == ("", "")


def test_default_source_only_client_preserves_existing_token_context(helper, monkeypatch):
    credentials = []
    monkeypatch.setenv("GH_TOKEN", "publisher-source-secret")

    def run(args, **kwargs):
        credentials.append(kwargs.get("env", os.environ)["GH_TOKEN"])
        return subprocess.CompletedProcess(args, 0, stdout=b"{}", stderr=b"")

    monkeypatch.setattr(helper.subprocess, "run", run)
    helper.GitHubAPI().request("GET", f"/repos/{SOURCE}/releases/7")
    assert credentials == ["publisher-source-secret"]


def test_cli_missing_source_token_reports_credential_boundary_before_network(helper, monkeypatch, capsys):
    monkeypatch.delenv("SOURCE_GH_TOKEN", raising=False)
    monkeypatch.setenv("GH_TOKEN", "host-app-secret")
    monkeypatch.setattr(sys, "argv", ["release_prs.py", "--tag", TAG])
    monkeypatch.setattr(helper, "GitHubAPI", lambda: pytest.fail("credentials must be checked before transport"))
    with pytest.raises(SystemExit) as error:
        helper.main()
    assert error.value.code == 2
    output = capsys.readouterr()
    assert "SOURCE_GH_TOKEN is required" in output.err
    assert "source workflow GITHUB_TOKEN" in output.err
    assert "host-app-secret" not in output.out + output.err
