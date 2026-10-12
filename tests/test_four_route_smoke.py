"""Behavioral checks for the synthetic installed-feature verification harness."""
import importlib.util
from pathlib import Path


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
