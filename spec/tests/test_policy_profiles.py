"""C15 payload invariants; these are not authenticated policy-engine results."""
import hashlib
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_c15_b_profile_preserves_read_plan_and_catchall_rules_without_web_allow():
    path = ROOT / "contracts/gemini-readonly-b.toml"
    assert path.is_file(), "the separate B contract is missing"
    data = tomllib.loads(path.read_text())
    allowed, denied = set(), set()
    for rule in data["rule"]:
        names = rule["toolName"]
        names = [names] if isinstance(names, str) else names
        if rule["decision"] == "allow":
            assert rule["priority"] == 999
            allowed.update(names)
        elif rule["decision"] == "deny" and rule["priority"] == 999:
            denied.update(names)
    assert allowed == {"read_file", "read_many_files", "list_directory", "glob",
                       "grep_search", "get_internal_docs"}
    assert denied == {"write_file", "replace", "run_shell_command", "enter_plan_mode",
                      "exit_plan_mode", "google_web_search", "web_fetch"}
    assert any(r["toolName"] == "*" and r["decision"] == "deny" and r["priority"] == 998
               for r in data["rule"])


def test_c15_a_payload_is_unchanged_by_b_profile_split():
    data = (ROOT / "contracts/gemini-readonly.toml").read_bytes()
    assert hashlib.sha256(data).hexdigest() == "6480a765ca2d32d3bdadd8f46be20f9bcd2b4de66d42bb075e4dcda1cad3d207"


def test_c15_b_manifest_binds_exact_profile_and_leaves_live_checks_unrun():
    path = ROOT / "contracts/gemini-readonly-b.verify.toml"
    assert path.is_file(), "B profile needs an independent unrun manifest"
    manifest = tomllib.loads(path.read_text())
    assert manifest["policy"] == "contracts/gemini-readonly-b.toml"
    assert manifest["policy_sha256"] == hashlib.sha256((ROOT / manifest["policy"]).read_bytes()).hexdigest()
    assert manifest["status"] == "NOT RUN"
    assert len(manifest["check"]) == 3
    assert all(row["status"] == "NOT RUN" and row["case"] == "C15" for row in manifest["check"])
    assert len({row["id"] for row in manifest["check"]}) == 3


WEB_TOOLS = {"google_web_search", "web_fetch"}


def _rule_rows(path):
    """(tool, decision, priority) per named tool; header comments are ignored."""
    rows = set()
    for rule in tomllib.loads(path.read_text())["rule"]:
        names = rule["toolName"]
        for name in [names] if isinstance(names, str) else names:
            rows.add((name, rule["decision"], rule["priority"]))
    return rows


def test_c32_a_web_profile_moves_only_the_two_web_tools_to_allow():
    no_web = _rule_rows(ROOT / "contracts/gemini-readonly.toml")
    web = _rule_rows(ROOT / "contracts/gemini-readonly-web.toml")
    assert {r for r in no_web if r[0] in WEB_TOOLS} == {(t, "deny", 200) for t in WEB_TOOLS}
    assert {r for r in web if r[0] in WEB_TOOLS} == {(t, "allow", 100) for t in WEB_TOOLS}
    assert {r for r in web if r[0] not in WEB_TOOLS} == {r for r in no_web if r[0] not in WEB_TOOLS}


def test_c32_review_web_manifest_names_both_host_web_profiles_unrun():
    manifest = tomllib.loads((ROOT / "contracts/review-web.verify.toml").read_text())
    profiles = {row["host"]: row.get("policy") for row in manifest["check"] if row.get("policy")}
    assert profiles == {"A": "contracts/gemini-readonly-web.toml", "B": "contracts/gemini-readonly-web-b.toml"}
    assert all(row["status"] == "NOT RUN" for row in manifest["check"] if row["id"] != "WEB-A-1")
    assert all((ROOT / p).is_file() for p in profiles.values())


def test_c32_web_a_1_run_records_its_evidence():
    manifest = tomllib.loads((ROOT / "contracts/review-web.verify.toml").read_text())
    row = next(r for r in manifest["check"] if r["id"] == "WEB-A-1")
    assert row["status"] == "RUN"
    assert row["evidence"].startswith("decisions/owner-register.md#")  # the manifest's result_channel: one record, a pointer here
    anchor = row["evidence"].split("#", 1)[1].split()[0]
    assert f'<a id="{anchor}"></a>' in (ROOT / "decisions/owner-register.md").read_text()


import pytest


@pytest.mark.parametrize("manifest_path, policy_path", [
    ("contracts/gemini-readonly-web.verify.toml", "contracts/gemini-readonly-web.toml"),
    ("contracts/gemini-readonly-web-b.verify.toml", "contracts/gemini-readonly-web-b.toml"),
])
def test_c32_web_profile_manifest_binds_exact_profile_and_leaves_checks_unrun(manifest_path, policy_path):
    manifest = tomllib.loads((ROOT / manifest_path).read_text())
    assert manifest["policy"] == policy_path
    assert manifest["policy_sha256"] == hashlib.sha256((ROOT / policy_path).read_bytes()).hexdigest()
    assert manifest["status"] == "NOT RUN"
    assert manifest["check"]
    for row in manifest["check"]:
        assert row["status"] == "NOT RUN" and row["case"] == "C32"
        assert all(row.get(key) for key in ("id", "what", "brief", "expect", "on_fail"))


def test_c32_review_web_checks_point_at_their_manifests():
    manifest = tomllib.loads((ROOT / "contracts/review-web.verify.toml").read_text())
    pointers = {row["id"]: row.get("manifest") for row in manifest["check"]}
    assert pointers["WEB-A-2"] == "contracts/gemini-readonly-web.verify.toml"
    assert pointers["WEB-B-1"] == "contracts/gemini-readonly-web-b.verify.toml"


def test_r_google_lists_every_verify_manifest():
    rules = (ROOT / "reference/review-rules.md").read_text()
    start = rules.index("Current manifests:")
    listed = rules[start:rules.index("This convention covers", start)]  # the policy-manifest list only
    for path in sorted((ROOT / "contracts").glob("*.verify.toml")):
        manifest = tomllib.loads(path.read_text())
        if "policy_sha256" in manifest:
            assert f"contracts/{path.name}" in listed
        else:
            assert f"contracts/{path.name}" not in listed


@pytest.mark.parametrize("path", sorted((ROOT / "contracts").glob("*.verify.toml")), ids=lambda p: p.name)
def test_every_verify_manifest_is_a_policy_manifest_or_names_its_result_channel(path):
    manifest = tomllib.loads(path.read_text())
    assert manifest.get("policy_sha256") or str(manifest.get("result_channel", "")).strip()


@pytest.mark.parametrize("path", sorted((ROOT / "contracts").glob("*.verify.toml")), ids=lambda p: p.name)
def test_every_verify_check_carries_the_convention_fields(path):
    manifest = tomllib.loads(path.read_text())
    assert manifest["check"]
    for row in manifest["check"]:
        missing = [k for k in ("id", "case", "what", "brief", "expect", "on_fail", "status") if not row.get(k)]
        assert not missing, (row.get("id"), missing)


def test_c32_web_a_3_false_condition_is_a_separate_unrun_live_check():
    manifest = tomllib.loads((ROOT / "contracts/review-web.verify.toml").read_text())
    row = next(r for r in manifest["check"] if r["id"] == "WEB-A-3")
    assert row["status"] == "NOT RUN"
