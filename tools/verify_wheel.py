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
        else:
            if case["outcome"] != "admit" or result != json.loads(raw):
                raise AssertionError(f"unexpected admission: {case['name']}")
        passed.append(case["name"])
    if not passed:
        raise AssertionError("replay corpus must not be empty")
    return passed


def probe(root: Path, prefix: Path) -> dict:
    import triad_dispatch_lib

    verify_import(Path(triad_dispatch_lib.__file__), prefix)
    passed = replay(root)
    data = files("triad_dispatch_lib").joinpath("data")
    manifest = json.loads(data.joinpath("source-manifest.json").read_bytes())
    schema_hash = hashlib.sha256(data.joinpath("leg-verdict.schema.json").read_bytes()).hexdigest()
    if schema_hash != manifest["sha256"]["leg-verdict.schema.json"]:
        raise AssertionError("installed schema digest mismatch")
    return {
        "package_path": triad_dispatch_lib.__file__,
        "version": version("triad-dispatch-lib"), "python": platform.python_version(),
        "platform": platform.platform(), "machine": platform.machine(),
        "source_commit": manifest["source_commit"], "schema_sha256": schema_hash,
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
    parser.add_argument("--probe", nargs=2, type=Path, metavar=("FIXTURES", "PREFIX"))
    args = parser.parse_args()
    if args.probe:
        print(json.dumps(probe(*args.probe), indent=2))
        return
    if args.wheel is None or not args.wheel.is_file():
        parser.error("provide one existing wheel path")
    wheel = args.wheel.resolve()
    script = Path(__file__).resolve()
    fixtures = script.parents[1] / "tests" / "fixtures" / "replay"
    with installed_wheel(wheel) as (python, prefix, neutral):
        result = subprocess.run([str(python), "-I", str(script), "--probe",
                                 str(fixtures), str(prefix)], cwd=neutral,
                                check=True, capture_output=True, text=True)
        report = json.loads(result.stdout)
        report["wheel_sha256"] = hashlib.sha256(wheel.read_bytes()).hexdigest()
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
