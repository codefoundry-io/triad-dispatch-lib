import hashlib
import importlib
from importlib.resources import files
from pathlib import Path
import re
import shutil

import pytest

from triad_dispatch_lib import ContractError, PromptError
from tests.test_prompts import VALUES, render

SPEC = Path(__file__).resolve().parents[1] / "spec" / "prompts"
PROFILES = [(family, host, route, False)
            for family, route in [("codex", None), ("claude", None),
                                  ("google", "agy"), ("google", "gemini")]
            for host in ("A", "B")] + [("google", "A", "agy", True)]


def source_blocks(text, host):
    # Independent extraction of the canonical fenced bytes, not parse_clauses.
    blocks = {}
    for heading, body in re.findall(r"^## ([^\n]+)\n(.*?)(?=^## |\Z)", text, re.M | re.S):
        if ("B-only" if host == "A" else "A-only") in heading:
            continue
        match = re.search(r"^```text\n(.*?)^```$", body, re.M | re.S)
        if match:
            blocks[heading.split()[0]] = match[1].rstrip("\n")
    return blocks


def row(name, source):
    return {"name": name, "sha256": hashlib.sha256(source.encode("utf-8")).hexdigest()}


def expected_manifest(family, host, kind, web, hook):
    common = source_blocks((SPEC / "common-clauses.md").read_text(), host)
    leg_text = (SPEC / f"leg-{family}.md").read_text()
    purpose = "plan-purpose" if kind == "formal-plan" else "code-purpose"
    leg = source_blocks(leg_text, host)
    if not hook:
        leg.pop("google-a-hook-audit", None)
    order = re.findall(r"^\d+\. (\S+)", leg_text, re.M)
    result, web_seen = [], False
    for name in order:
        name = name.replace("<review-purpose>", purpose)
        source = common.get(name[7:]) if name.startswith("common:") else leg.get(name)
        if source is None:
            continue
        result.append(row(name, source))
        if "<review-web-policy>" in source and not web_seen:
            web_name = "review-web-permission" if web else "review-no-web"
            result.append(row("common:" + web_name, common[web_name]))
            web_seen = True
    return result


@pytest.mark.parametrize("family,host,route,hook", PROFILES)
@pytest.mark.parametrize("kind", ["formal-plan", "pre-merge", "implementation-review"])
@pytest.mark.parametrize("web", [False, True])
def test_profiles_have_exact_source_hashes_and_identical_rendering(family, host, route, hook, kind, web):
    values = VALUES | ({"gated-patch-file": '"/tmp/patch"'} if family == "google" else {})
    kwargs = dict(family=family, host=host, route=route, agy_hook_active=hook,
                  review_kind=kind, review_web_authorized=web, replacements=values)
    text, manifest = render(**kwargs, with_manifest=True)
    assert text == render(**kwargs) == render(**kwargs, with_manifest=False)
    assert manifest == expected_manifest(family, host, kind, web, hook)
    names = [entry["name"] for entry in manifest]
    assert names.count("common:review-web-permission" if web else "common:review-no-web") == 1
    assert ("google-a-hook-audit" in names) == hook


@pytest.mark.parametrize("flag", [None, 0, 1, "true", [], {}])
def test_manifest_flag_requires_actual_boolean(flag):
    with pytest.raises(PromptError):
        render(with_manifest=flag)


def test_manifest_is_fresh_and_independent_of_substitutions():
    text, manifest = render(with_manifest=True)
    changed_text, changed_manifest = render(with_manifest=True, review_date="2026-10-15",
        replacements=VALUES | {"worktree": '"literal <review-web-policy> <review-kind> 한글"'})
    assert text != changed_text
    assert '"literal <review-web-policy> <review-kind> 한글"' in changed_text
    assert changed_manifest == manifest
    manifest[0]["name"] = "mutated"
    manifest[1]["sha256"] = "mutated"
    manifest.clear()
    assert render(with_manifest=True)[1] == changed_manifest


@pytest.mark.parametrize("fault", ["missing", "digest", "manifest"])
def test_manifest_still_refuses_tampered_verified_bundle(tmp_path, monkeypatch, fault):
    module = importlib.import_module("triad_dispatch_lib.prompts")
    original = files("triad_dispatch_lib").joinpath("data/prompt-bundle")
    root = tmp_path / "data/prompt-bundle"
    shutil.copytree(str(original), root)
    if fault == "missing":
        (root / "prompts/leg-codex.md").unlink()
    elif fault == "digest":
        (root / "prompts/leg-codex.md").write_text("changed")
    else:
        (root / "source-manifest.json").write_text("{}")
    monkeypatch.setattr(module, "files", lambda _: tmp_path)
    with pytest.raises(ContractError):
        render(with_manifest=True)


def test_nested_web_dependency_recorded_after_first_parent_once(monkeypatch):
    module = importlib.import_module("triad_dispatch_lib.prompts")
    bundle = module._bundle()
    bundle["prompts/leg-codex.md"] = bundle["prompts/leg-codex.md"].replace(
        "You are the codex leg", "<review-web-policy> You are the codex leg")
    monkeypatch.setattr(module, "_bundle", lambda: bundle)
    text, manifest = render(with_manifest=True)
    assert manifest[0]["name"] == "codex-intro"
    assert manifest[1]["name"] == "common:review-no-web"
    assert sum(entry["name"] == "common:review-no-web" for entry in manifest) == 1
    assert text == render()
