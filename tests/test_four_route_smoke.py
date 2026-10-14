"""Behavioral checks for the synthetic installed-feature verification harness."""
import importlib.util
from pathlib import Path
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
