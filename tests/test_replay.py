import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

from triad_dispatch_lib import AdmissionError, validate_verdict

ROOT = Path(__file__).parent / "fixtures" / "replay"
CASES = json.loads((ROOT / "cases.json").read_bytes())["cases"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["name"])
def test_replay_vectors(case):
    raw = (ROOT / case["raw"]).read_bytes()
    if case["outcome"] == "admit":
        assert validate_verdict(raw, expected=case["expected"]) == json.loads(raw)
    else:
        with pytest.raises(AdmissionError) as caught:
            validate_verdict(raw, expected=case["expected"])
        assert caught.value.code == case["outcome"]


def verifier():
    path = Path(__file__).parents[1] / "tools" / "verify_wheel.py"
    assert path.is_file(), "installed-wheel verifier is missing"
    spec = importlib.util.spec_from_file_location("verify_wheel", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_installed_probe_requires_site_packages(tmp_path):
    module = verifier()
    with pytest.raises(ValueError, match="site-packages"):
        module.verify_import(Path(__file__).resolve(), tmp_path)
    with pytest.raises(ValueError, match="site-packages"):
        module.verify_import(tmp_path / "source" / "__init__.py", tmp_path)
    module.verify_import(tmp_path / "lib/python3.12/site-packages/triad_dispatch_lib/__init__.py", tmp_path)


def test_installed_probe_replays_vectors():
    assert verifier().replay(ROOT) == [case["name"] for case in CASES]


def test_environment_interpreter_starts(tmp_path):
    python = verifier().create_environment(tmp_path / "venv")
    result = subprocess.run([str(python), "-I", "-c", "import sys; print(sys.prefix)"],
                            check=True, capture_output=True, text=True)
    assert Path(result.stdout.strip()).resolve() == (tmp_path / "venv").resolve()
