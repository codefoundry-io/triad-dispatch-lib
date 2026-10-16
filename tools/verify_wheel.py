"""Install a wheel outside the checkout and replay the shared raw corpus."""

import argparse
from contextlib import contextmanager
import hashlib
from importlib.metadata import version
from importlib.resources import files
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import tomllib
import venv


def verify_import(module_path: Path, expected_prefix: Path) -> None:
    path = module_path.resolve()
    prefix = expected_prefix.resolve()
    if not path.is_relative_to(prefix) or "site-packages" not in path.relative_to(prefix).parts:
        raise ValueError("package must load from isolated environment site-packages")


def replay(root: Path) -> list[str]:
    from triad_dispatch_lib import AdmissionError, validate_verdict

    cases = json.loads((root / "cases.json").read_bytes())["cases"]
    passed = []
    for case in cases:
        raw = (root / case["raw"]).read_bytes()
        try:
            result = validate_verdict(raw, expected=case["expected"])
        except AdmissionError as error:
            if error.code != case["outcome"]:
                raise AssertionError(f"unexpected rejection: {case['name']}") from None
            diagnostics = case.get("diagnostics")
            if diagnostics is not None and (
                error.missing != diagnostics["missing"]
                or error.path != tuple(diagnostics["path"])
            ):
                raise AssertionError(f"unexpected diagnostic: {case['name']}") from None
        else:
            if case["outcome"] != "admit" or result != json.loads(raw):
                raise AssertionError(f"unexpected admission: {case['name']}")
        passed.append(case["name"])
    if not passed:
        raise AssertionError("replay corpus must not be empty")
    return passed


def verify_bundles(data) -> dict:
    """Verify all runtime payloads and report their complete bundle provenance."""
    from triad_dispatch_lib.contracts import load_verified_bundle
    from triad_dispatch_lib.json_input import parse_json

    bundles = {
        "verdict": (data, ("leg-verdict.schema.json",)),
        "roster": (data.joinpath("roster-bundle"), ("contracts/review-legs.schema.json",)),
        "receipt": (data.joinpath("receipt-bundle"), ("contracts/receipt-fields.json",)),
        "prompts": (data.joinpath("prompt-bundle"), (
            "contracts/review-kind.schema.json", "prompts/common-clauses.md",
            "prompts/leg-codex.md", "prompts/leg-claude.md", "prompts/leg-google.md",
            "prompts/investigation.md")),
    }
    report = {}
    for name, (bundle, payloads) in bundles.items():
        load_verified_bundle(bundle, payloads)
        report[name] = parse_json(bundle.joinpath("source-manifest.json").read_bytes())
    return report


def verify_minimal_adoption() -> dict:
    """Exercise installed APIs and fixed refusals, beyond checking exports."""
    import triad_dispatch_lib as lib
    from triad_dispatch_lib import receipt

    doc = dict(schema_version=2.0, stdin_delivery="complete", route="codex",
               binary="codex", cli_version="opaque future build", attempt=1.0)
    saved = dict(doc)
    assert lib.validate_transport_receipt(doc) is None and doc == saved
    try:
        lib.validate_transport_receipt({})
    except lib.ReceiptError as error:
        assert error.code == "schema_violation"
        assert str(error) == "Transport receipt violates the canonical schema."
    else:
        raise AssertionError("Invalid transport accepted")

    # Synthetic local schema fault tests the installed recursion refusal path.
    loader = receipt._load_receipt_contract
    try:
        receipt._load_receipt_contract = lambda: {
            "$defs": {"loop": {"$ref": "#/$defs/loop"}}, "$ref": "#/$defs/loop",
        }
        try:
            lib.validate_transport_receipt(doc)
        except lib.ReceiptError as error:
            assert error.code == "nesting_limit"
            assert str(error) == "Transport receipt nesting exceeds the validation limit."
        else:
            raise AssertionError("Recursive transport contract accepted")
    finally:
        receipt._load_receipt_contract = loader

    try:
        lib.validate_resolved({})
    except lib.RosterError as error:
        assert error.code == "schema_violation"
        assert str(error) == "Roster violates the canonical schema."
        assert (error.document, error.path, error.missing) == ("resolved", ("required",), "schema")
    else:
        raise AssertionError("Invalid resolved roster accepted")
    return dict(transport_valid=True, transport_schema_refused=True,
                transport_nesting_refused=True, roster_diagnostics=True)


def probe(root: Path, prefix: Path) -> dict:
    import triad_dispatch_lib

    verify_import(Path(triad_dispatch_lib.__file__), prefix)
    passed = replay(root)
    data = files("triad_dispatch_lib").joinpath("data")
    bundles = verify_bundles(data)
    return {
        "package_path": triad_dispatch_lib.__file__,
        "version": version("triad-dispatch-lib"), "python": platform.python_version(),
        "platform": platform.platform(), "machine": platform.machine(),
        "bundles": bundles,
        "minimal_adoption": verify_minimal_adoption(),
        "dependencies": {name: version(name) for name in ("jsonschema", "referencing", "rpds-py", "attrs")},
        "replay_passed": passed,
    }


def create_environment(prefix: Path) -> Path:
    # Copying a standalone macOS interpreter breaks its relative dylib lookup.
    venv.EnvBuilder(with_pip=True, symlinks=True).create(prefix)
    return prefix / "bin" / "python"


@contextmanager
def installed_wheel(wheel: Path):
    """Supply a fresh installed interpreter to repository verification tools."""
    with tempfile.TemporaryDirectory(prefix="triad-wheel-") as temp:
        neutral = Path(temp).resolve()
        prefix = neutral / "venv"
        python = create_environment(prefix)
        subprocess.run([str(python), "-I", "-m", "pip", "--isolated", "--disable-pip-version-check", "install",
                        "--only-binary=:all:", str(wheel.resolve())], cwd=neutral,
                       check=True, stdout=sys.stderr)
        yield python, prefix, neutral


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path, nargs="?")
    parser.add_argument("--probe", nargs=2, type=Path, metavar=("FIXTURES", "PREFIX"), help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.probe:
        print(json.dumps(probe(*args.probe), indent=2))
        return
    if args.wheel is None:
        parser.error("provide one existing wheel path")
    try:
        if not args.wheel.is_file():
            parser.error("provide one existing wheel path")
        wheel = args.wheel.resolve()
    except (OSError, RuntimeError):  # Includes Python 3.12 resolution loops.
        parser.error("provide one existing wheel path")
    script = Path(__file__).resolve()
    fixtures = script.parents[1] / "tests" / "fixtures" / "replay"
    consumers = script.parents[1] / "tests" / "test_public_api_consumers.py"
    expected_version = tomllib.loads((script.parents[1] / "pyproject.toml").read_text())["project"]["version"]
    with installed_wheel(wheel) as (python, prefix, neutral):
        subprocess.run([str(python), "-I", str(consumers), "--installed-prefix", str(prefix),
                        "--expected-version", expected_version], cwd=neutral, check=True)
        result = subprocess.run([str(python), "-I", str(script), "--probe",
                                 str(fixtures), str(prefix)], cwd=neutral,
                                check=True, capture_output=True, text=True)
        report = json.loads(result.stdout)
        report["public_api_consumers"] = {"passed": True, "expected_version": expected_version}
        report["wheel_sha256"] = hashlib.sha256(wheel.read_bytes()).hexdigest()
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
