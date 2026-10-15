"""Behavioral checks for the synthetic installed-feature verification harness."""
import importlib.util
import errno
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


def driver():
    path = Path(__file__).parents[1] / 'tools/four_route_smoke.py'
    assert path.is_file(), 'Installed four-route driver missing'
    spec = importlib.util.spec_from_file_location('four_route_smoke', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_synthetic_four_route_matrix():
    # Missing admission, ignored dissent/swap/failure or investigation coupling
    # must fail the harness's own assertions rather than report success.
    report = driver().synthetic_smoke()
    assert report['capture_method'] == 'synthetic'
    assert report['roster_split'] == {
        'validated_parity': True, 'inherited_block_refused': True,
    }
    assert report['cases'] == {
        'unanimous': True, 'informational-dissent': False,
        'google-sibling-swap': False, 'invoke-failure': False,
        'integrity-false': False, 'integrity-exception': False,
        'preflight-refused': True, 'bounded-callbacks': True,
        'independent-investigations': True,
    }
    assert len(report['prompt_profiles']) == 51
    assert report['investigation_count'] == 4


def test_matrix_detects_approval_fault(monkeypatch):
    import pytest
    import triad_dispatch_lib as lib
    from dataclasses import replace
    original = lib.evaluate_agreement
    def approves(*args, **kwargs):
        return replace(original(*args, **kwargs), agreed=True)
    monkeypatch.setattr('triad_dispatch_lib.dispatch.evaluate_agreement', approves)
    with pytest.raises(AssertionError):
        driver().synthetic_smoke()


def test_matrix_detects_skipped_resolved_validation(monkeypatch):
    import triad_dispatch_lib as lib
    monkeypatch.setattr(lib, 'validate_resolved', lambda roster: None)
    with pytest.raises(AssertionError, match='Inherited vendor block accepted'):
        driver().synthetic_smoke()


@pytest.mark.parametrize("ancestor", [False, True], ids=["leaf", "ancestor"])
def test_cli_cyclic_wheel_refused_before_install(ancestor, tmp_path, monkeypatch, capsys):
    module = driver()
    cycle = tmp_path / 'cycle'
    cycle.symlink_to(cycle)
    wheel = cycle / 'package.whl' if ancestor else cycle

    def forbidden_helpers():
        raise AssertionError('installation attempted for cyclic wheel')

    monkeypatch.setattr(module, 'helpers', forbidden_helpers)
    monkeypatch.setattr(sys, 'argv', ['four_route_smoke.py', '--wheel', str(wheel),
                                    '--expected-version', '0.1.0.dev3'])
    with pytest.raises(SystemExit) as caught:
        module.main()
    assert caught.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'wheel must be an existing regular file' in captured.err
    assert 'Traceback' not in captured.err


@pytest.mark.parametrize('operation', ['resolve', 'is_file'])
@pytest.mark.parametrize('error_number', [errno.EACCES, errno.EIO], ids=['access', 'io'])
def test_cli_wheel_oserror_refused(operation, error_number, tmp_path, monkeypatch, capsys):
    module = driver()
    wheel = tmp_path.resolve() / 'fixture.whl'
    wheel.write_bytes(b'fixture')
    original = getattr(Path, operation)

    def fail_wheel(path, *args, **kwargs):
        if path == wheel:
            raise OSError(error_number, 'wheel observation failed')
        return original(path, *args, **kwargs)

    def forbidden_helpers():
        raise AssertionError('installation attempted for inaccessible wheel')

    monkeypatch.setattr(Path, operation, fail_wheel)
    monkeypatch.setattr(module, 'helpers', forbidden_helpers)
    monkeypatch.setattr(sys, 'argv', ['four_route_smoke.py', '--wheel', str(wheel),
                                    '--expected-version', '0.1.0.dev3'])
    with pytest.raises(SystemExit) as caught:
        module.main()
    assert caught.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'wheel must be an existing regular file' in captured.err
    assert 'Traceback' not in captured.err


@pytest.mark.parametrize('invalid_origin', [None, 'export', 'package'])
def test_identity_loads_helper_once_per_call_and_checks_real_origins(tmp_path, invalid_origin):
    root = Path(__file__).resolve().parents[1]
    prefix = tmp_path.resolve() / 'environment'
    site = prefix / 'lib' / 'site-packages'
    shutil.copytree(root / 'src' / 'triad_dispatch_lib', site / 'triad_dispatch_lib')
    # A fresh interpreter avoids replacing the suite's imported library modules.
    code = '''
import inspect, json, pathlib, runpy, sys
prefix, site, driver, invalid_origin = sys.argv[1:]
sys.path.insert(0, site)
import triad_dispatch_lib as lib
module = runpy.run_path(driver)
identity = module['identity']
namespace = identity.__globals__
original_helpers = namespace['helpers']
original_getfile = inspect.getfile
expected = [str(pathlib.Path(original_getfile(getattr(lib, name)))) for name in lib.__all__]
expected.append(str(pathlib.Path(lib.__file__)))
outside = pathlib.Path(prefix).parent / 'outside.py'
outside.write_text('# external origin fixture\\n')
if invalid_origin == 'export':
    first = getattr(lib, lib.__all__[0])
    inspect.getfile = lambda value: str(outside) if value is first else original_getfile(value)
    expected = [str(outside)]
elif invalid_origin == 'package':
    lib.__file__ = str(outside)
    expected[-1] = str(outside)
loads, checks, refusals = [], [], []
def counted_helpers():
    loads.append(True)
    helper = original_helpers()
    verify = helper['verify_import']
    def observed_verify(path, wanted_prefix):
        checks.append(str(path))
        return verify(path, wanted_prefix)
    helper['verify_import'] = observed_verify
    return helper
namespace['helpers'] = counted_helpers
for _ in range(2):
    try:
        report = identity(pathlib.Path(prefix), namespace['version']('triad-dispatch-lib'))
        assert set(report['runtime_paths']) == set(lib.__all__)
    except ValueError as error:
        assert str(error) == 'package must load from isolated environment site-packages'
        refusals.append(True)
print(json.dumps(dict(loads=len(loads), checks=checks, expected=expected * 2,
                     refusals=len(refusals), exports=len(lib.__all__))))
'''
    completed = subprocess.run([sys.executable, '-I', '-c', code, str(prefix), str(site),
                                str(root / 'tools' / 'four_route_smoke.py'), str(invalid_origin)],
                               check=True, capture_output=True, text=True)
    observed = json.loads(completed.stdout)
    assert observed['checks'] == observed['expected']
    assert observed['exports'] == 29
    assert observed['refusals'] == (0 if invalid_origin is None else 2)
    assert observed['loads'] == 2
