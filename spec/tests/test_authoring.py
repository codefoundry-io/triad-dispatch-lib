"""Offline checks for authoring implementation maps."""
import copy
import importlib
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools" / "check_authoring.py"


def checker():
    assert CHECKER.is_file(), "missing checker component: tools/check_authoring.py"
    if str(CHECKER.parent) not in sys.path:
        sys.path.insert(0, str(CHECKER.parent))
    return importlib.import_module("check_authoring")


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


@pytest.fixture
def authoring_repo(tmp_path):
    write(tmp_path / "decisions/prd.md", "<a id=\"PRD-PURPOSE\"></a>\n<a id=\"PRD-SCOPE\"></a>\n<a id=\"PRD-ACCEPTANCE\"></a>\n<a id=\"PRD-ONE\"></a>\n")
    write(tmp_path / "decisions/spec.md", "<a id=\"SPEC-SCOPE\"></a>\n<a id=\"SPEC-ONE\"></a>\n")
    write(tmp_path / "reference/rules.md", "<a id=\"R-ONE\"></a>\n")
    write(tmp_path / "contracts/shape.json", "{}\n")
    write(tmp_path / "cases/cases.json", json.dumps({"cases": [{"id": "C1", "surface": "unit-one"}]}))
    write(tmp_path / "units.json", json.dumps({"units": {"unit-one": {}}}))
    return tmp_path


def complete_map():
    return {
        "schema_version": 1,
        "prd": {
            "document": "decisions/prd.md",
            "status": "candidate",
            "purpose_ref": "decisions/prd.md#PRD-PURPOSE",
            "scope_ref": "decisions/prd.md#PRD-SCOPE",
            "acceptance_ref": "decisions/prd.md#PRD-ACCEPTANCE",
        },
        "specs": [{
            "document": "decisions/spec.md",
            "status": "draft",
            "scope_ref": "decisions/spec.md#SPEC-SCOPE",
        }],
        "requirements": [{
            "id": "REQ-ONE",
            "prd_ref": "decisions/prd.md#PRD-ONE",
            "spec_refs": ["decisions/spec.md#SPEC-ONE"],
            "rule_refs": ["reference/rules.md#R-ONE"],
            "contract_refs": ["contracts/shape.json"],
            "case_ids": ["C1"],
            "unit_ids": ["unit-one"],
        }],
    }


def test_complete_map_has_no_offline_errors(authoring_repo):
    assert checker().validate_map(authoring_repo, complete_map()) == []


def test_checked_in_authoring_maps_are_valid():
    maps = sorted((ROOT / "authoring/maps").glob("*.json"))
    assert maps, "missing checked-in authoring maps"
    module = checker()
    for path in maps:
        assert module.validate_map(ROOT, module.load_json(path)) == []


def test_missing_required_component_is_reported(authoring_repo):
    data = complete_map()
    del data["prd"]["purpose_ref"]
    assert any("purpose_ref" in error for error in checker().validate_map(authoring_repo, data))


def test_requirement_id_with_terminal_newline_is_rejected(authoring_repo):
    data = complete_map()
    data["requirements"][0]["id"] = "REQ-ONE\n"
    assert checker().validate_map(authoring_repo, data)


@pytest.mark.parametrize("field,value", [
    ("prd_ref", "decisions/prd.md"),
    ("rule_refs", ["reference/rules.md#bad anchor"]),
    ("contract_refs", ["contracts/../shape.json"]),
])
def test_malformed_reference_is_rejected(authoring_repo, field, value):
    data = complete_map()
    data["requirements"][0][field] = value
    assert checker().validate_map(authoring_repo, data)


@pytest.mark.parametrize("mutate,needle", [
    (lambda data: data["requirements"][0].update(prd_ref="decisions/missing.md#PRD-ONE"), "missing file"),
    (lambda data: data["requirements"][0].update(prd_ref="decisions/prd.md#MISSING"), "missing anchor"),
    (lambda data: data["requirements"][0].update(case_ids=["C2"]), "unknown case id"),
    (lambda data: data["requirements"][0].update(unit_ids=["unit-two"]), "unknown unit id"),
])
def test_missing_offline_target_is_reported(authoring_repo, mutate, needle):
    data = complete_map()
    mutate(data)
    assert any(needle in error for error in checker().validate_map(authoring_repo, data))


@pytest.mark.parametrize("concealed_anchor", [
    "Example: `<a id=\"PRD-ONE\"></a>`",
    "```markdown\n<a id=\"PRD-ONE\"></a>\n```",
    "<!--\n<a id=\"PRD-ONE\"></a>\n-->",
    "    <a id=\"PRD-ONE\"></a>",
    "\t<a id=\"PRD-ONE\"></a>",
    "````markdown\n```\n<a id=\"PRD-ONE\"></a>\n````",
    "```markdown\n~~~\n<a id=\"PRD-ONE\"></a>\n```",
    "```markdown\n```not-a-close\n<a id=\"PRD-ONE\"></a>\n```",
])
def test_inline_or_example_anchor_is_not_a_reference_target(authoring_repo, concealed_anchor):
    write(authoring_repo / "decisions/prd.md", "\n".join([
        '<a id="PRD-PURPOSE"></a>', '<a id="PRD-SCOPE"></a>',
        '<a id="PRD-ACCEPTANCE"></a>', concealed_anchor,
    ]))
    assert any("missing anchor: decisions/prd.md#PRD-ONE" in error
               for error in checker().validate_map(authoring_repo, complete_map()))


def test_duplicate_requirement_ids_are_rejected(authoring_repo):
    data = complete_map()
    duplicate = copy.deepcopy(data["requirements"][0])
    duplicate["contract_refs"] = []
    data["requirements"].append(duplicate)
    assert any("duplicate requirement id: REQ-ONE" in error
               for error in checker().validate_map(authoring_repo, data))


def test_case_surface_must_be_owned_by_requirement_unit(authoring_repo):
    write(authoring_repo / "cases/cases.json",
          json.dumps({"cases": [{"id": "C1", "surface": "other-unit"}]}))
    assert any("case surface missing from unit_ids: C1 -> other-unit" in error
               for error in checker().validate_map(authoring_repo, complete_map()))


def test_duplicate_case_ids_are_rejected(authoring_repo):
    write(authoring_repo / "cases/cases.json", json.dumps({"cases": [
        {"id": "C1", "surface": "unit-one"},
        {"id": "C1", "surface": "other-unit"},
    ]}))
    assert any("duplicate case id: C1" in error
               for error in checker().validate_map(authoring_repo, complete_map()))


def test_prd_reference_must_belong_to_prd_document(authoring_repo):
    data = complete_map()
    data["requirements"][0]["prd_ref"] = "decisions/spec.md#SPEC-ONE"
    assert any("must target prd document" in error
               for error in checker().validate_map(authoring_repo, data))


def test_spec_reference_must_belong_to_declared_spec(authoring_repo):
    data = complete_map()
    data["requirements"][0]["spec_refs"] = ["decisions/prd.md#PRD-ONE"]
    assert any("must target a declared spec document" in error
               for error in checker().validate_map(authoring_repo, data))


def test_symlink_reference_is_rejected(authoring_repo):
    alias = authoring_repo / "decisions" / "alias"
    alias.symlink_to(authoring_repo / "decisions", target_is_directory=True)
    data = complete_map()
    data["prd"].update(
        document="decisions/alias/prd.md",
        purpose_ref="decisions/alias/prd.md#PRD-PURPOSE",
        scope_ref="decisions/alias/prd.md#PRD-SCOPE",
        acceptance_ref="decisions/alias/prd.md#PRD-ACCEPTANCE",
    )
    data["requirements"][0]["prd_ref"] = "decisions/alias/prd.md#PRD-ONE"
    assert any("symlink traversal" in error
               for error in checker().validate_map(authoring_repo, data))


def test_duplicate_json_members_are_rejected(authoring_repo):
    path = authoring_repo / "authoring/maps/duplicate.json"
    write(path, '{"schema_version": 1, "schema_version": 1}')
    with pytest.raises(ValueError, match="duplicate JSON member: schema_version"):
        checker().load_json(path)
