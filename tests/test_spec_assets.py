"""Exercise bundle integrity and offline generation against real temporary trees."""
import errno
import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import runpy
import shutil

import pytest

from triad_dispatch_lib import ContractError
from triad_dispatch_lib.contracts import load_verified_bundle

REPO = Path(__file__).resolve().parents[1]
MAPPING = {
    'leg-verdict.schema.json': 'contracts/leg-verdict.schema.json',
    'roster-bundle/contracts/review-legs.schema.json': 'contracts/review-legs.schema.json',
    'prompt-bundle/contracts/review-kind.schema.json': 'contracts/review-kind.schema.json',
    **{f'prompt-bundle/prompts/{name}.md': f'prompts/{name}.md' for name in
       ('common-clauses', 'leg-codex', 'leg-claude', 'leg-google', 'investigation')},
}


def manifest(digests):
    serialized = json.dumps(digests, sort_keys=True, separators=(',', ':'), ensure_ascii=True)
    return {'schema_version': 1, 'source_repository': 'https://github.com/codefoundry-io/triad-dispatch-lib',
            'source_path': 'spec', 'status': 'candidate', 'sha256': digests,
            'contract_id': hashlib.sha256(b'triad-dispatch-lib:bundle:v1\n' + serialized.encode()).hexdigest()}


def test_identity_serialization():
    assert importlib.util.find_spec('triad_dispatch_lib.bundle_manifest'), 'bundle identity implementation missing'
    identity = importlib.import_module('triad_dispatch_lib.bundle_manifest').contract_id
    digests = {'z': '0' * 64, 'é': '1' * 64}
    expected = hashlib.sha256(b'triad-dispatch-lib:bundle:v1\n' +
                              ('{"z":"' + '0' * 64 + '","\\u00e9":"' + '1' * 64 + '"}').encode()).hexdigest()
    assert identity(digests) == expected
    assert identity(dict(reversed(list(digests.items())))) == expected


@pytest.mark.parametrize('fault', [None, 'bool', 'unknown_version', 'missing', 'extra', 'repository',
                                   'path', 'status', 'digest_type', 'digest_upper', 'digest_short',
                                   'id', 'payload', 'names', 'duplicate', 'nonfinite'])
def test_manifest_integrity(tmp_path, fault):
    raw = b'canonical\r\n\x00'
    data = manifest({'asset': hashlib.sha256(raw).hexdigest()})
    if fault == 'bool': data['schema_version'] = True
    elif fault == 'unknown_version': data['schema_version'] = 2
    elif fault == 'missing': del data['status']
    elif fault == 'extra': data['extra'] = 1
    elif fault == 'repository': data['source_repository'] = 'old'
    elif fault == 'path': data['source_path'] = '../spec'
    elif fault == 'status': data['status'] = 'released'
    elif fault == 'digest_type': data['sha256']['asset'] = 123
    elif fault == 'digest_upper': data['sha256']['asset'] = 'A' * 64
    elif fault == 'digest_short': data['sha256']['asset'] = 'a'
    elif fault == 'id': data['contract_id'] = '0' * 64
    elif fault == 'payload': raw += b'changed'
    elif fault == 'names': data['sha256']['extra'] = '0' * 64
    encoded = json.dumps(data)
    if fault == 'duplicate': encoded = encoded[:-1] + ',"status":"candidate"}'
    elif fault == 'nonfinite': encoded = encoded.replace('"schema_version": 1', '"schema_version": NaN')
    (tmp_path / 'asset').write_bytes(raw)
    (tmp_path / 'source-manifest.json').write_text(encoded)
    if fault is None:
        assert load_verified_bundle(tmp_path, ('asset',)) == {'asset': raw}
    else:
        with pytest.raises(ContractError): load_verified_bundle(tmp_path, ('asset',))


@pytest.fixture
def generated(tmp_path):
    assert (REPO / 'tools/sync_spec_assets.py').is_file(), 'asset generator missing'
    sync = runpy.run_path(str(REPO / 'tools/sync_spec_assets.py'))['sync_assets']
    for index, source in enumerate(MAPPING.values()):
        target = tmp_path / 'spec' / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(f'asset-{index}\r\n'.encode() + b'\x00\xff')
    return tmp_path, sync


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file()}


def test_generation_preserves_bytes_and_is_deterministic(generated):
    root, sync = generated
    sync(root, write=True)
    first = snapshot(root)
    for target, source in MAPPING.items():
        assert (root / 'src/triad_dispatch_lib/data' / target).read_bytes() == (root / 'spec' / source).read_bytes()
    sync(root, write=True)
    assert snapshot(root) == first
    sync(root, write=False)
    assert snapshot(root) == first
    for bundle, names in [('', ('leg-verdict.schema.json',)),
                          ('roster-bundle', ('contracts/review-legs.schema.json',)),
                          ('prompt-bundle', tuple(p.removeprefix('prompt-bundle/') for p in MAPPING if p.startswith('prompt-bundle/')))]:
        assert load_verified_bundle(root / 'src/triad_dispatch_lib/data' / bundle, names)


@pytest.mark.parametrize('fault', ['missing', 'changed', 'extra', 'empty_directory'])
def test_check_never_writes_on_drift(generated, fault):
    root, sync = generated
    sync(root, write=True)
    data = root / 'src/triad_dispatch_lib/data'
    target = data / 'leg-verdict.schema.json'
    if fault == 'missing': target.unlink()
    elif fault == 'changed': target.write_bytes(b'changed')
    elif fault == 'extra': (data / 'unowned').write_bytes(b'keep')
    else: (data / 'unowned').mkdir()
    before = snapshot(root)
    with pytest.raises(ValueError): sync(root, write=False)
    assert snapshot(root) == before
    if fault in ('extra', 'empty_directory'):
        with pytest.raises(ValueError): sync(root, write=True)
        assert snapshot(root) == before


@pytest.mark.parametrize('location', ['source_file', 'source_directory', 'output_file', 'output_directory', 'output_parent', 'source_root'])
@pytest.mark.parametrize('write', [True, False])
def test_symlinks_refused_without_touching_outside(generated, location, write):
    root, sync = generated
    sync(root, write=True)
    outside = root / 'outside'
    outside.mkdir()
    (outside / 'sentinel').write_bytes(b'outside bytes')
    paths = {'source_file': root / 'spec/contracts/leg-verdict.schema.json',
             'source_directory': root / 'spec/contracts', 'source_root': root / 'spec',
             'output_file': root / 'src/triad_dispatch_lib/data/leg-verdict.schema.json',
             'output_directory': root / 'src/triad_dispatch_lib/data/prompt-bundle',
             'output_parent': root / 'src'}
    target = paths[location]
    if target.is_dir(): shutil.rmtree(target)
    else: target.unlink()
    target.symlink_to(outside if location.endswith(('directory', 'parent', 'root')) else outside / 'sentinel')
    before = snapshot(outside)
    with pytest.raises(ValueError): sync(root, write=write)
    assert snapshot(outside) == before


@pytest.mark.parametrize('location', ['source_file', 'output_file'])
@pytest.mark.parametrize('write', [True, False])
@pytest.mark.parametrize('error_number', [errno.EIO, errno.EACCES])
def test_symlink_status_errors_refuse_before_writes(generated, monkeypatch, location, write, error_number):
    root, sync = generated
    sync(root, write=True)
    data = root / 'src/triad_dispatch_lib/data'
    target = ((root / 'spec/contracts/leg-verdict.schema.json') if location == 'source_file'
              else data / 'leg-verdict.schema.json')
    sentinel = root / 'outside-sentinel'
    sentinel.write_bytes(b'preserve outside bytes')
    target.unlink()
    target.symlink_to(sentinel)
    before = snapshot(data)
    original_stat, original_lstat = os.stat, os.lstat

    def stat(path, *args, **kwargs):
        if os.fspath(path) == str(target) and not kwargs.get('follow_symlinks', True):
            raise OSError(error_number, 'injected link-status error')
        return original_stat(path, *args, **kwargs)

    def lstat(path, *args, **kwargs):
        if os.fspath(path) == str(target):
            raise OSError(error_number, 'injected link-status error')
        return original_lstat(path, *args, **kwargs)

    with monkeypatch.context() as patch:
        patch.setattr(os, 'stat', stat)
        patch.setattr(os, 'lstat', lstat)
        with pytest.raises(OSError) as error:
            sync(root, write=write)
        assert error.value.errno == error_number
    assert sentinel.read_bytes() == b'preserve outside bytes'
    assert snapshot(data) == before


def test_missing_canonical_input_does_not_partially_write(generated):
    root, sync = generated
    sync(root, write=True)
    data = root / 'src/triad_dispatch_lib/data'
    (root / 'spec/contracts/leg-verdict.schema.json').write_bytes(b'new bytes')
    (root / 'spec/prompts/investigation.md').unlink()
    before = snapshot(data)
    with pytest.raises(OSError): sync(root, write=True)
    assert snapshot(data) == before


def test_packaged_schema_ids_remain_in_original_namespace():
    from triad_dispatch_lib.contracts import load_contract, load_roster_contract
    namespace = 'https://github.com/codefoundry-io/triad-dispatch-spec/contracts/'
    assert load_contract()['$id'] == namespace + 'leg-verdict.schema.json'
    assert load_roster_contract()['$id'] == namespace + 'review-legs.schema.json'
    root = REPO / 'src/triad_dispatch_lib/data/prompt-bundle'
    name = 'contracts/review-kind.schema.json'
    assert json.loads(load_verified_bundle(root, tuple(p.removeprefix('prompt-bundle/') for p in MAPPING
                                                    if p.startswith('prompt-bundle/')))[name])['$id'] == namespace + 'review-kind.schema.json'
