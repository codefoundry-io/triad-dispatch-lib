"""Transport shape only: immutable input, canonical semantics and offline assets."""
import copy
import importlib
import json
import socket
from pathlib import Path

import pytest
import triad_dispatch_lib as lib


def transport(**changes):
    return dict(schema_version=2, stdin_delivery='complete', route='codex',
                binary='codex', cli_version='opaque build text', attempt=1, **changes)


def api():
    assert callable(getattr(lib, 'validate_transport_receipt', None)), 'receipt API missing'
    assert hasattr(lib, 'ReceiptError'), 'receipt error missing'
    return lib.validate_transport_receipt


@pytest.mark.parametrize('route', ['codex', 'claude', 'agy', 'gemini', 'native'])
def test_valid_transport_no_mutation(route):
    doc = transport()
    doc['route'] = route
    if route == 'native':
        doc.update(binary=None, cli_version=None, stdin_delivery='unexposed')
    saved = copy.deepcopy(doc)
    assert api()(doc) is None
    assert doc == saved


@pytest.mark.parametrize('field', ['schema_version', 'stdin_delivery', 'route', 'binary', 'cli_version', 'attempt'])
def test_required_members(field):
    doc = transport()
    del doc[field]
    assert_refusal(doc)


def assert_refusal(doc):
    validate = api()
    with pytest.raises(lib.ReceiptError) as caught:
        validate(doc)
    assert caught.value.code == 'schema_violation'
    assert str(caught.value) == 'Transport receipt violates the canonical schema.'


@pytest.mark.parametrize('change', [
    {'schema_version': True}, {'schema_version': 1}, {'attempt': True}, {'attempt': 0},
    {'attempt': 1.5}, {'stdin_delivery': 'unknown-private'}, {'route': 'unknown-private'},
    {'binary': 42}, {'binary': '  '}, {'cli_version': ''}, {'cli_version': []},
    {'private-key': 'private-value'}, {'route': 'native', 'binary': 'native'},
    {'route': 'native', 'binary': None, 'cli_version': 'native'},
    {'route': 'native', 'binary': None, 'cli_version': None, 'stdin_delivery': 'complete'},
    {'route': 'native', 'binary': None, 'cli_version': None, 'stdin_delivery': 'failed'},
    {'route': 'native', 'binary': None, 'cli_version': None, 'stdin_delivery': 'not-started'},
])
def test_schema_refusals(change):
    assert_refusal({**transport(), **change})


@pytest.mark.parametrize('doc', [None, [], 1, 'private', {'transport': transport()}])
def test_wrong_types_and_whole_envelope_refused(doc):
    assert_refusal(doc)


@pytest.mark.parametrize('delivery', ['not-used', 'not-started', 'complete', 'failed', 'unexposed'])
def test_non_native_delivery_and_unobserved_versions_are_allowed(delivery):
    assert api()({**transport(), 'binary': None, 'cli_version': None,
                  'stdin_delivery': delivery}) is None


def test_integral_float_and_opaque_version_preserve_schema_semantics():
    doc = {**transport(), 'schema_version': 2.0, 'attempt': 1.0,
           'cli_version': ' future prerelease / account-specific build '}
    assert api()(doc) is None


def receipt_module():
    api()
    return importlib.import_module('triad_dispatch_lib.receipt')


@pytest.mark.parametrize('reference', ['https://example.invalid/remote.json', '#/$defs/absent'])
def test_unresolved_references_do_not_retrieve(monkeypatch, reference):
    module = receipt_module()
    schema = {'$ref': reference}
    monkeypatch.setattr(module, '_load_receipt_contract', lambda: schema)
    monkeypatch.setattr(socket.socket, 'connect', lambda *args: pytest.fail('network retrieval'))
    with pytest.raises(lib.ContractError):
        api()(transport())


def test_recursive_validation_has_fixed_nesting_refusal(monkeypatch):
    module = receipt_module()
    schema = {'$defs': {'loop': {'$ref': '#/$defs/loop'}}, '$ref': '#/$defs/loop'}
    monkeypatch.setattr(module, '_load_receipt_contract', lambda: schema)
    with pytest.raises(lib.ReceiptError) as caught:
        api()(transport())
    assert caught.value.code == 'nesting_limit'
    assert str(caught.value) == 'Transport receipt nesting exceeds the validation limit.'


@pytest.mark.parametrize('fault', ['missing', 'corrupt', 'identity', 'dialect', 'schema'])
def test_broken_receipt_bundle_is_contract_failure(tmp_path, monkeypatch, fault):
    api()
    contracts = importlib.import_module('triad_dispatch_lib.contracts')
    from triad_dispatch_lib.bundle_manifest import make_manifest
    import hashlib
    schema = json.loads((Path(__file__).parents[1] / 'spec/contracts/receipt-fields.json').read_bytes())
    if fault == 'identity': schema['$id'] = 'https://example.invalid/wrong'
    if fault == 'dialect': schema['$schema'] = 'https://json-schema.org/draft-07/schema'
    if fault == 'schema': schema['type'] = 'bad-type'
    name = 'contracts/receipt-fields.json'
    root = tmp_path / 'data/receipt-bundle'
    (root / 'contracts').mkdir(parents=True)
    raw = json.dumps(schema).encode()
    (root / name).write_bytes(raw)
    (root / 'source-manifest.json').write_text(json.dumps(make_manifest({name: hashlib.sha256(raw).hexdigest()})))
    if fault == 'missing': (root / name).unlink()
    if fault == 'corrupt': (root / name).write_bytes(raw + b' ')
    monkeypatch.setattr(contracts, 'files', lambda package: tmp_path)
    with pytest.raises(lib.ContractError):
        api()(transport())


def test_receipt_public_exports_and_private_loader():
    api()
    assert len(lib.__all__) == 32
    assert lib.__all__.count('ReceiptError') == lib.__all__.count('validate_transport_receipt') == 1
    assert not hasattr(lib, '_load_receipt_contract')
