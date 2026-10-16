import importlib.util
import errno
import json
from pathlib import Path
import subprocess
import shutil
import sys

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
        if "diagnostics" in case:
            assert caught.value.missing == case["diagnostics"]["missing"]
            assert caught.value.path == tuple(case["diagnostics"]["path"])


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


def test_installed_probe_checks_missing_diagnostic(monkeypatch):
    import triad_dispatch_lib

    real_validate = triad_dispatch_lib.validate_verdict

    def wrong_missing(raw, *, expected):
        try:
            return real_validate(raw, expected=expected)
        except AdmissionError as error:
            error.missing = "wrong-required-name"
            raise

    monkeypatch.setattr(triad_dispatch_lib, "validate_verdict", wrong_missing)
    with pytest.raises(AssertionError, match="unexpected diagnostic: missing-root"):
        verifier().replay(ROOT)


def test_probe_reports_all_verified_bundle_identities():
    data = Path(__file__).parents[1] / "src/triad_dispatch_lib/data"
    report = verifier().verify_bundles(data)
    assert set(report) == {"verdict", "roster", "prompts", "receipt"}
    assert [len(report[name]["sha256"]) for name in ("verdict", "roster", "prompts", "receipt")] == [1, 1, 6, 1]
    for manifest in report.values():
        assert set(manifest) == {"schema_version", "source_repository", "source_path",
                                 "status", "sha256", "contract_id"}
        assert len(manifest["contract_id"]) == 64


@pytest.mark.parametrize("relative", [
    "leg-verdict.schema.json", "roster-bundle/contracts/review-legs.schema.json",
    "prompt-bundle/contracts/review-kind.schema.json",
    "prompt-bundle/prompts/common-clauses.md", "prompt-bundle/prompts/leg-codex.md",
    "prompt-bundle/prompts/leg-claude.md", "prompt-bundle/prompts/leg-google.md",
    "prompt-bundle/prompts/investigation.md",
    "source-manifest.json", "roster-bundle/source-manifest.json",
    "prompt-bundle/source-manifest.json",
    "receipt-bundle/contracts/receipt-fields.json", "receipt-bundle/source-manifest.json",
])
def test_probe_refuses_corruption_in_every_bundle_resource(tmp_path, relative):
    from triad_dispatch_lib import ContractError

    data = tmp_path / "data"
    shutil.copytree(Path(__file__).parents[1] / "src/triad_dispatch_lib/data", data)
    target = data / relative
    if target.name == "source-manifest.json":
        manifest = json.loads(target.read_bytes())
        manifest["contract_id"] = "0" * 64
        target.write_text(json.dumps(manifest))
    else:
        target.write_bytes(target.read_bytes() + b"\ncorruption")
    with pytest.raises(ContractError):
        verifier().verify_bundles(data)


def test_environment_interpreter_starts(tmp_path):
    python = verifier().create_environment(tmp_path / "venv")
    result = subprocess.run([str(python), "-I", "-c", "import sys; print(sys.prefix)"],
                            check=True, capture_output=True, text=True)
    assert Path(result.stdout.strip()).resolve() == (tmp_path / "venv").resolve()


@pytest.mark.parametrize("operation", ["resolve", "is_file"])
@pytest.mark.parametrize("error_number", [errno.EACCES, errno.EIO], ids=["access", "io"])
def test_cli_wheel_oserror_refused(operation, error_number, tmp_path, monkeypatch, capsys):
    module = verifier()
    wheel = tmp_path.resolve() / "fixture.whl"
    wheel.write_bytes(b"fixture")
    original = getattr(Path, operation)

    def fail_wheel(path, *args, **kwargs):
        if path == wheel:
            raise OSError(error_number, "wheel observation failed")
        return original(path, *args, **kwargs)

    def forbidden_install(wheel):
        raise AssertionError("installation attempted for inaccessible wheel")

    monkeypatch.setattr(Path, operation, fail_wheel)
    monkeypatch.setattr(module, "installed_wheel", forbidden_install)
    monkeypatch.setattr(sys, "argv", ["verify_wheel.py", str(wheel)])
    with pytest.raises(SystemExit) as caught:
        module.main()
    assert caught.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "provide one existing wheel path" in captured.err
    assert "Traceback" not in captured.err


def test_public_help_hides_internal_probe_without_installation(monkeypatch, capsys):
    monkeypatch.setenv("PYTHON_COLORS", "0")
    monkeypatch.setenv("NO_COLOR", "1")
    module = verifier()

    def forbidden_install(wheel):
        raise AssertionError("help attempted wheel installation")

    monkeypatch.setattr(module, "installed_wheel", forbidden_install)
    monkeypatch.setattr(sys, "argv", ["verify_wheel.py", "--help"])
    with pytest.raises(SystemExit) as caught:
        module.main()
    assert caught.value.code == 0
    captured = capsys.readouterr()
    assert captured.err == ""
    assert "  wheel\n" in captured.out
    assert "--probe" not in captured.out


def test_installed_probe_exercises_minimal_adoption_apis():
    assert verifier().verify_minimal_adoption() == {
        'transport_valid': True, 'transport_schema_refused': True,
        'transport_nesting_refused': True, 'roster_diagnostics': True,
    }


@pytest.mark.parametrize('fault', ['receipt_accepts_invalid', 'receipt_wrong_code', 'roster_wrong_document',
                                 'roster_wrong_path', 'roster_wrong_missing'])
def test_installed_probe_detects_minimal_adoption_faults(monkeypatch, fault):
    import triad_dispatch_lib as lib
    if fault.startswith('receipt'):
        original = lib.validate_transport_receipt
        def wrong_receipt(doc):
            if doc == {}:
                if fault == 'receipt_accepts_invalid':
                    return None
                raise lib.ReceiptError('nesting_limit')
            return original(doc)
        monkeypatch.setattr(lib, 'validate_transport_receipt', wrong_receipt)
    else:
        original = lib.validate_resolved
        def wrong_roster(doc):
            try:
                return original(doc)
            except lib.RosterError as error:
                if fault == 'roster_wrong_document': error.document = 'override'
                if fault == 'roster_wrong_path': error.path = ('wrong',)
                if fault == 'roster_wrong_missing': error.missing = 'wrong'
                raise
        monkeypatch.setattr(lib, 'validate_resolved', wrong_roster)
    with pytest.raises(AssertionError):
        verifier().verify_minimal_adoption()
