"""Test adapter for pinned Codex prompts and raw responses, without spawning."""

import argparse
import errno
import hashlib
from importlib.metadata import version
from importlib.resources import files
import inspect
import json
from pathlib import Path
import platform
import runpy
import shutil
import subprocess
import sys
import tempfile


def helpers():
    # Load this exact repository helper without adding the checkout to sys.path.
    return runpy.run_path(str(Path(__file__).with_name("verify_wheel.py")))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def packet_records(root: Path, paths: list[Path]) -> list[dict]:
    return sorted([{"path": path.relative_to(root).as_posix(), "sha256": sha256(path.read_bytes())}
                   for path in paths], key=lambda record: record["path"])


def packet_digest(records: list[dict]) -> str:
    return sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode())


def prepare_context(context: dict) -> dict:
    import triad_dispatch_lib as lib

    required = {"expected", "worktree", "brief_file", "packet_files", "review_date",
                "objective", "criteria", "approved_boundary"}
    allowed = required | {"review_kind", "review_web_authorized", "residual"}
    if not isinstance(context, dict) or not required.issubset(context) or not set(context).issubset(allowed):
        raise ValueError("Invalid context fields.")
    lib.validate_binding(context["expected"])
    if context["expected"]["family"] != "codex":
        raise ValueError("The test adapter supports only the Codex/B profile.")
    if (not isinstance(context["objective"], str) or not context["objective"].strip()
            or not isinstance(context.get("residual", ""), str)
            or any(not isinstance(context[key], list) or not context[key]
                   or any(not isinstance(value, str) or not value.strip() for value in context[key])
                   for key in ("criteria", "approved_boundary"))):
        raise ValueError("Invalid review scope.")
    if (not isinstance(context["worktree"], str) or not isinstance(context["brief_file"], str)
            or not isinstance(context["packet_files"], list) or not context["packet_files"]
            or any(not isinstance(value, str) for value in context["packet_files"])):
        raise ValueError("Invalid packet paths.")
    root = Path(context["worktree"])
    paths = [Path(value) for value in context["packet_files"]]
    try:
        resolved_root = root.resolve(strict=True) if root.is_absolute() else None
    except RuntimeError:
        raise ValueError("Worktree must be a canonical absolute directory.") from None
    except OSError as error:
        if error.errno not in (errno.ENOENT, errno.ENOTDIR, errno.ELOOP):
            raise
        raise ValueError("Worktree must be a canonical absolute directory.") from None
    if resolved_root != root or not root.is_dir():
        raise ValueError("Worktree must be a canonical absolute directory.")
    if len(set(paths)) != len(paths) or Path(context["brief_file"]) not in paths:
        raise ValueError("Brief must belong to a unique bound packet.")
    for path in paths:
        try:
            resolved_path = path.resolve(strict=True) if path.is_absolute() else None
        except RuntimeError:
            raise ValueError("Packet must contain canonical regular files inside the worktree.") from None
        except OSError as error:
            if error.errno not in (errno.ENOENT, errno.ENOTDIR, errno.ELOOP):
                raise
            raise ValueError("Packet must contain canonical regular files inside the worktree.") from None
        if (resolved_path != path or not path.is_relative_to(root)
                or path.is_symlink() or not path.is_file()):
            raise ValueError("Packet must contain canonical regular files inside the worktree.")
    records = packet_records(root, paths)
    if packet_digest(records) != context["expected"]["content_digest"]:
        raise ValueError("Packet digest mismatch.")
    return {"context": dict(context), "packet_hashes": records}


def render_prompt(context: dict) -> str:
    import triad_dispatch_lib as lib
    from triad_dispatch_lib.contracts import load_contract

    prepared = prepare_context(context)
    context = prepared["context"]
    expected = context["expected"]
    kind = context.get("review_kind", "pre-merge")
    replacements = {
        "worktree": json.dumps(context["worktree"], ensure_ascii=True),
        "brief-file": json.dumps(context["brief_file"], ensure_ascii=True),
        "packet-files": json.dumps(context["packet_files"], ensure_ascii=True),
        "review-id": expected["review_id"], "content-digest": expected["content_digest"],
        "leg-name": expected["leg_name"], "attempt": str(expected["attempt"]),
    }
    clauses = lib.render_review_clauses(family="codex", host="B", review_kind=kind,
        review_date=context["review_date"], review_web_authorized=context.get("review_web_authorized", False),
        replacements=replacements)
    metadata = expected | {"review_kind": kind, "review_web_authorized": context.get("review_web_authorized", False)}
    scope = {key: context[key] for key in ("objective", "criteria", "approved_boundary")}
    schema = load_contract()
    for key, value in expected.items():
        schema["properties"][key]["const"] = value
    return ("Review v2 metadata: " + json.dumps(metadata, sort_keys=True) + "\n\n" + clauses
            + "\n\nBound review scope:\n" + json.dumps(scope, ensure_ascii=True)
            + "\n\nPrior findings and rebuttal evidence:\n" + lib.render_data(context.get("residual", ""))
            + "\n\nComplete authoritative output schema:\n" + json.dumps(schema, sort_keys=True) + "\n")


def admit_result(raw: bytes, context: dict, prompt: bytes) -> dict:
    import triad_dispatch_lib as lib

    if render_prompt(context).encode() != prompt:
        raise ValueError("Prepared prompt mismatch.")
    return lib.validate_verdict(raw, expected=context["expected"])


def identity(prefix: Path, expected_version: str) -> dict:
    import triad_dispatch_lib as lib

    observed = version("triad-dispatch-lib")
    if observed != expected_version:
        raise ValueError("Installed package version mismatch.")
    verifier = helpers()["verify_import"]
    module_path, entrypoint_path = Path(lib.__file__), Path(inspect.getfile(lib.validate_verdict))
    verifier(module_path, prefix)
    verifier(entrypoint_path, prefix)
    data = files("triad_dispatch_lib").joinpath("data")
    return {"package_path": str(module_path), "entrypoint_path": str(entrypoint_path),
            "entrypoint": "triad_dispatch_lib.validate_verdict", "version": observed,
            "python": platform.python_version(), "platform": platform.platform(), "machine": platform.machine(),
            "schema_provenance": json.loads(data.joinpath("source-manifest.json").read_bytes()),
            "prompt_provenance": json.loads(data.joinpath("prompt-bundle/source-manifest.json").read_bytes())}


def synthetic_smoke() -> dict:
    import triad_dispatch_lib as lib

    fixture = Path(__file__).resolve().parents[1] / "tests/fixtures/codex"
    with tempfile.TemporaryDirectory(prefix="triad-codex-fixture-") as temporary:
        root = Path(temporary).resolve()
        for name in ("brief.md", "example.py"):
            shutil.copyfile(fixture / name, root / name)
        paths = [root / "brief.md", root / "example.py"]
        expected = {"review_id": "synthetic-smoke", "family": "codex",
                    "content_digest": packet_digest(packet_records(root, paths)),
                    "leg_name": "codex-leg", "attempt": 1, "route": None}
        context = {"expected": expected, "worktree": str(root), "brief_file": str(paths[0]),
                   "packet_files": [str(path) for path in paths], "review_date": "2026-10-12",
                   "objective": "Check integer discount calculation", "criteria": ["correctness"],
                   "approved_boundary": ["brief.md", "example.py"]}
        cases = []
        for phase in ("formal-plan", "implementation-review", "pre-merge"):
            context["review_kind"] = phase
            prompt = render_prompt(context).encode()
            metadata = json.loads(prompt.split(b"\n", 1)[0].removeprefix(b"Review v2 metadata: "))
            purpose = (b"Review whether this plan meets" if phase == "formal-plan"
                       else b"Review this change's correctness and completeness")
            if metadata["review_kind"] != phase or purpose not in prompt:
                raise AssertionError("Synthetic phase rendering mismatch.")
            verdict = {"schema_version": 2, **expected, "verdict": "SAFE TO MERGE",
                       "criteria_checked": ["correctness"], "findings": [],
                       "affected_surfaces_inspected": ["example.py"], "open_questions": []}
            finding = {"path": "example.py", "line": 2, "severity": "must-fix",
                       "summary": "Synthetic arithmetic finding", "trigger": "1000 cents, 20 percent",
                       "evidence": "Synthetic fixture evidence", "context_known": True,
                       "correction": "Compute the remaining price"}
            negative = verdict | {"verdict": "MERGE WITH FIXES", "findings": [finding]}

            def check(name, raw, wanted, *, expected_result=None, saved_prompt=prompt):
                result = None
                try:
                    result = admit_result(raw, context, saved_prompt)
                    outcome = "admit"
                except lib.AdmissionError as error:
                    outcome = error.code
                except ValueError as error:
                    # Only these known adapter refusals count; other errors fail the run.
                    refusals = {"Prepared prompt mismatch.": "prompt_mismatch",
                                "Packet digest mismatch.": "packet_mismatch"}
                    if str(error) not in refusals:
                        raise
                    outcome = refusals[str(error)]
                if outcome != wanted or (outcome == "admit" and result != expected_result):
                    raise AssertionError(f"Synthetic case failed: {phase}/{name}")
                case = {"review_kind": phase, "name": name, "outcome": outcome,
                        "prompt_sha256": sha256(saved_prompt), "raw_result_sha256": sha256(raw)}
                if outcome == "admit":
                    case["verdict"] = result["verdict"]
                cases.append(case)

            for name, value in (
                ("safe", verdict), ("negative-finding", negative),
                ("negative-question", verdict | {"verdict": "DO NOT MERGE", "open_questions": ["Required fact unresolved"]}),
                ("negative-minor", negative | {"findings": [finding | {"severity": "Minor"}]}),
            ):
                check(name, json.dumps(value).encode(), "admit", expected_result=value)
            for field, value in (("review_id", "stale"), ("family", "claude"),
                                 ("content_digest", "b" * 64), ("leg_name", "other-leg"),
                                 ("attempt", 2), ("route", "agy")):
                check(field.replace("_", "-"), json.dumps(verdict | {field: value}).encode(),
                      "schema_violation" if field == "route" else "binding_mismatch")
            raw = json.dumps(verdict).encode()
            negative_raw = json.dumps(negative).encode()
            for name, candidate, code in (
                ("duplicate", raw.replace(b'"attempt": 1', b'"attempt": 1, "attempt": 1'), "duplicate_member"),
                ("nested-duplicate", negative_raw.replace(b'"path": "example.py"', b'"path": "example.py", "path": "example.py"'), "duplicate_member"),
                ("invalid-utf8", b"\xff", "invalid_utf8"),
                ("fenced", b"```json\n" + raw + b"\n```", "invalid_json"),
                ("trailing", raw + b" trailing prose", "invalid_json"),
                ("overflow", raw.replace(b'"attempt": 1', b'"attempt": 1e400'), "nonfinite_number"),
            ):
                check(name, candidate, code)
            check("prompt-change", raw, "prompt_mismatch", saved_prompt=prompt + b"changed")
            original_packet = paths[1].read_bytes()
            try:
                paths[1].write_bytes(original_packet + b"\n# changed packet\n")
                check("packet-change", raw, "packet_mismatch")
            finally:
                paths[1].write_bytes(original_packet)
        return {"capture_method": "synthetic", "checks": ["render", "admit", "duplicate_member", "binding_mismatch"],
                "prompt_sha256": sha256(prompt), "cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--installed-prefix", type=Path, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("render", "admit"):
        command = commands.add_parser(name)
        command.add_argument("--context", type=Path, required=True)
        command.add_argument("--prompt", type=Path, required=True)
        if name == "admit":
            command.add_argument("--result", type=Path, required=True)
    commands.add_parser("self-test")
    args = parser.parse_args()
    try:
        wheel = args.wheel.resolve()
        if not wheel.is_file():
            parser.error("wheel must be an existing regular file")
    except (OSError, RuntimeError):  # Includes Python 3.12 resolution loops.
        parser.error("wheel must be an existing regular file")
    if not args.installed_prefix:
        # Resolve input/output paths before entering the neutral working directory.
        forwarded = ["--wheel", str(wheel), "--expected-version", args.expected_version]
        with helpers()["installed_wheel"](wheel) as (python, prefix, neutral):
            forwarded += ["--installed-prefix", str(prefix), args.command]
            for name in ("context", "prompt", "result"):
                if hasattr(args, name):
                    forwarded += ["--" + name, str(getattr(args, name).absolute())]
            completed = subprocess.run([str(python), "-I", str(Path(__file__).resolve()), *forwarded], cwd=neutral)
            return completed.returncode
    import triad_dispatch_lib as lib
    try:
        report = identity(args.installed_prefix, args.expected_version)
        report["wheel_sha256"] = sha256(wheel.read_bytes())
        if args.command == "self-test":
            report.update(synthetic_smoke())
        else:
            context_raw = args.context.read_bytes()
            context = lib.parse_json(context_raw)
            prepared = prepare_context(context)
            prompt = render_prompt(context).encode()
            report.update(context_sha256=sha256(context_raw), prompt_sha256=sha256(prompt),
                          packet_hashes=prepared["packet_hashes"], expected=context["expected"])
            if args.command == "render":
                with args.prompt.open("xb") as output:
                    output.write(prompt)
                report["rendered"] = True
            else:
                raw = args.result.read_bytes()
                report["verdict"] = admit_result(raw, context, args.prompt.read_bytes())
                report.update(admitted=True, raw_result_sha256=sha256(raw))
        print(json.dumps(report, indent=2))
        return 0
    except (ValueError, OSError, lib.ContractError) as error:
        # Input and admission errors have fixed messages; do not echo OSError paths.
        message = error.code if isinstance(error, lib.AdmissionError) else type(error).__name__
        print("Codex smoke refused: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
