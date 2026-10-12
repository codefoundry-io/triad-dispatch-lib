#!/usr/bin/env python3
"""Validate local authoring maps without fetching or executing host code."""
import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "authoring" / "implementation-map.schema.json"
ANCHOR = re.compile(r'<a\s+id="([^"]+)"\s*></a>')


def load_json(path):
    def no_duplicates(pairs):
        data = {}
        for key, value in pairs:
            if key in data:
                raise ValueError(f"duplicate JSON member: {key}")
            data[key] = value
        return data

    with path.open(encoding="utf-8") as source:
        return json.load(source, object_pairs_hook=no_duplicates)


def schema_errors(data):
    schema = load_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [f"schema {'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in sorted(validator.iter_errors(data), key=str)]


def local_file(root, relative, label, errors):
    path = root
    for part in Path(relative).parts:
        path /= part
        if path.is_symlink():
            errors.append(f"{label}: symlink traversal: {relative}")
            return None
    if not path.is_file():
        errors.append(f"{label}: missing file: {relative}")
        return None
    return path


def anchor_ids(text):
    ids = []
    fence = None
    commented = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if fence:
            char, length = fence
            if re.fullmatch(r" {0,3}" + re.escape(char) + "{" + str(length) + r",}[ \t]*", raw_line):
                fence = None
            continue
        if commented:
            commented = "-->" not in line
        elif "<!--" in line:
            commented = "-->" not in line
        elif match := re.match(r" {0,3}(`{3,}|~{3,})(.*)$", raw_line):
            marker, suffix = match.groups()
            if marker[0] != "`" or "`" not in suffix:
                fence = (marker[0], len(marker))
        elif match := ANCHOR.fullmatch(raw_line.rstrip()):
            ids.append(match.group(1))
    return ids


def check_ref(root, ref, label, errors):
    document, anchor = ref.split("#", 1)
    path = local_file(root, document, label, errors)
    if path is None:
        return
    ids = anchor_ids(path.read_text(encoding="utf-8"))
    count = ids.count(anchor)
    if count == 0:
        errors.append(f"{label}: missing anchor: {ref}")
    elif count != 1:
        errors.append(f"{label}: duplicate anchor: {ref}")


def load_catalogs(root, errors):
    cases_path = local_file(root, "cases/cases.json", "cases", errors)
    units_path = local_file(root, "units.json", "units", errors)
    cases = load_json(cases_path).get("cases", []) if cases_path else []
    units = load_json(units_path).get("units", {}) if units_path else {}
    if not isinstance(cases, list):
        errors.append("cases: cases must be an array")
        cases = []
    if not isinstance(units, dict):
        errors.append("units: units must be an object")
        units = {}
    by_id = {}
    for case in cases:
        if not isinstance(case, dict):
            continue
        case_id = case.get("id")
        if case_id in by_id:
            errors.append(f"duplicate case id: {case_id}")
        else:
            by_id[case_id] = case
    return by_id, set(units)


def validate_map(root: Path, data: dict) -> list[str]:
    errors = schema_errors(data)
    if errors:
        return errors
    root = Path(root)
    prd = data["prd"]
    specs = data["specs"]
    requirements = data["requirements"]
    local_file(root, prd["document"], "prd.document", errors)
    for field in ("purpose_ref", "scope_ref", "acceptance_ref"):
        ref = prd[field]
        if ref.split("#", 1)[0] != prd["document"]:
            errors.append(f"prd.{field}: must target prd document")
        check_ref(root, ref, f"prd.{field}", errors)
    spec_documents = set()
    for index, spec in enumerate(specs):
        label = f"specs[{index}]"
        if spec["document"] in spec_documents:
            errors.append(f"duplicate spec document: {spec['document']}")
        spec_documents.add(spec["document"])
        local_file(root, spec["document"], f"{label}.document", errors)
        if spec["scope_ref"].split("#", 1)[0] != spec["document"]:
            errors.append(f"{label}.scope_ref: must target spec document")
        check_ref(root, spec["scope_ref"], f"{label}.scope_ref", errors)
    cases, units = load_catalogs(root, errors)
    requirement_ids = set()
    for index, requirement in enumerate(requirements):
        label = f"requirements[{index}]"
        ident = requirement["id"]
        if ident in requirement_ids:
            errors.append(f"duplicate requirement id: {ident}")
        requirement_ids.add(ident)
        prd_ref = requirement["prd_ref"]
        if prd_ref.split("#", 1)[0] != prd["document"]:
            errors.append(f"{label}.prd_ref: must target prd document")
        check_ref(root, prd_ref, f"{label}.prd_ref", errors)
        for ref in requirement["spec_refs"]:
            if ref.split("#", 1)[0] not in spec_documents:
                errors.append(f"{label}.spec_refs: must target a declared spec document: {ref}")
            check_ref(root, ref, f"{label}.spec_refs", errors)
        for ref in requirement["rule_refs"]:
            if not ref.startswith("reference/"):
                errors.append(f"{label}.rule_refs: must target reference/*.md: {ref}")
            check_ref(root, ref, f"{label}.rule_refs", errors)
        for ref in requirement["contract_refs"]:
            if not ref.startswith("contracts/"):
                errors.append(f"{label}.contract_refs: must target contracts/: {ref}")
            local_file(root, ref, f"{label}.contract_refs", errors)
        for case_id in requirement["case_ids"]:
            case = cases.get(case_id)
            if case is None:
                errors.append(f"{label}: unknown case id: {case_id}")
            elif case.get("surface") not in requirement["unit_ids"]:
                errors.append(f"{label}: case surface missing from unit_ids: {case_id} -> {case.get('surface')}")
        for unit_id in requirement["unit_ids"]:
            if unit_id not in units:
                errors.append(f"{label}: unknown unit id: {unit_id}")
    return errors


def main():
    maps = sorted((ROOT / "authoring" / "maps").glob("*.json"))
    invalid = 0
    for path in maps:
        try:
            errors = validate_map(ROOT, load_json(path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors = [str(exc)]
        if errors:
            invalid += 1
            for error in errors:
                print(f"{path.relative_to(ROOT)}: {error}", file=sys.stderr)
    print(f"authoring maps: {len(maps)} total, {len(maps) - invalid} valid, {invalid} invalid")
    return 0 if maps and not invalid else 1


if __name__ == "__main__":
    raise SystemExit(main())
