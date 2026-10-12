import hashlib
import importlib
import importlib.util
from importlib.resources import files
import json
import socket

import pytest

from triad_dispatch_lib import ContractError


def contracts():
    assert importlib.util.find_spec("triad_dispatch_lib.contracts"), "contract loader is missing"
    return importlib.import_module("triad_dispatch_lib.contracts")


def test_manifest_and_digest():
    module = contracts()
    root = files("triad_dispatch_lib").joinpath("data")
    manifest = json.loads(root.joinpath("source-manifest.json").read_bytes())
    assert manifest["source_commit"] == "fcd96a15d18f3131c1f0111bdb10c3faceae34f8"
    assert manifest["sha256"]["leg-verdict.schema.json"] == hashlib.sha256(root.joinpath("leg-verdict.schema.json").read_bytes()).hexdigest()
    schema = module.load_contract()
    schema["required"].clear()
    assert module.load_contract()["required"]


@pytest.mark.parametrize("fault", ["missing", "manifest_json", "commit", "extra", "digest", "schema_json", "schema_type", "dialect", "invalid_schema"])
def test_broken_contract(tmp_path, monkeypatch, fault):
    module = contracts()
    source = files("triad_dispatch_lib").joinpath("data")
    root = tmp_path / "data"
    root.mkdir()
    raw = source.joinpath("leg-verdict.schema.json").read_bytes()
    manifest = json.loads(source.joinpath("source-manifest.json").read_bytes())
    if fault == "missing":
        monkeypatch.setattr(module, "files", lambda _: tmp_path)
        with pytest.raises(ContractError):
            module.load_contract()
        return
    if fault == "commit":
        manifest["source_commit"] = "0" * 40
    elif fault == "extra":
        manifest["extra"] = "unexpected"
    elif fault == "digest":
        raw += b" "
    elif fault in ("schema_json", "schema_type", "dialect", "invalid_schema"):
        raw = {"schema_json": b"{", "schema_type": b"[]", "dialect": b'{}',
               "invalid_schema": b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":123}'}[fault]
        manifest["sha256"]["leg-verdict.schema.json"] = hashlib.sha256(raw).hexdigest()
    root.joinpath("leg-verdict.schema.json").write_bytes(raw)
    root.joinpath("source-manifest.json").write_text("{" if fault == "manifest_json" else json.dumps(manifest))
    monkeypatch.setattr(module, "files", lambda _: tmp_path)
    with pytest.raises(ContractError):
        module.load_contract()


@pytest.mark.parametrize("ref", ["https://example.invalid/schema.json", "file:///tmp/triad-never-read.json"])
def test_external_ref_is_offline(monkeypatch, ref):
    assert importlib.util.find_spec("triad_dispatch_lib.verdict"), "verdict module is missing"
    module = importlib.import_module("triad_dispatch_lib.verdict")
    monkeypatch.setattr(module, "load_contract", lambda: {"$ref": ref})
    def forbidden(*args, **kwargs):
        pytest.fail("schema admission attempted network retrieval")
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    with pytest.raises(ContractError):
        module.validate_verdict("{}", expected={})


def test_roster_contract_fresh_and_pinned():
    module = contracts()
    assert callable(getattr(module, 'load_roster_contract', None)), 'roster contract missing'
    schema = module.load_roster_contract()
    assert schema['$defs']['resolvedRoster']['required'] == ['schema', 'legs']
    schema['$defs'].clear()
    assert module.load_roster_contract()['$defs']


@pytest.mark.parametrize('fault', ['missing', 'digest', 'manifest', 'invalid_schema'])
def test_broken_roster_contract(tmp_path, monkeypatch, fault):
    import shutil
    module = contracts()
    source = files('triad_dispatch_lib').joinpath('data/roster-bundle')
    root = tmp_path / 'data/roster-bundle'
    shutil.copytree(str(source), root)
    target = root / 'contracts/review-legs.schema.json'
    if fault == 'missing':
        target.unlink()
    elif fault == 'digest':
        target.write_text('changed')
    elif fault == 'manifest':
        (root / 'source-manifest.json').write_text('{}')
    else:
        raw = b'{"$schema":"https://json-schema.org/draft/2020-12/schema","type":123}'
        target.write_bytes(raw)
        manifest = json.loads((root / 'source-manifest.json').read_text())
        manifest['sha256']['contracts/review-legs.schema.json'] = hashlib.sha256(raw).hexdigest()
        (root / 'source-manifest.json').write_text(json.dumps(manifest))
    monkeypatch.setattr(module, 'files', lambda _: tmp_path)
    with pytest.raises(ContractError):
        module.load_roster_contract()
