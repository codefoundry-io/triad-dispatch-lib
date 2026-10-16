"""Controls for the root-only structural gate, using tiny real packages."""

import importlib.util
from pathlib import Path

import pytest


def checker():
    path = Path(__file__).parents[1] / "tools/check_api_compatibility.py"
    assert path.is_file(), "structural compatibility checker is missing"
    spec = importlib.util.spec_from_file_location("api_checker", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare(tmp_path, old, new, *, old_helpers="", new_helpers=""):
    roots = []
    for label, source, helpers in (("old", old, old_helpers), ("new", new, new_helpers)):
        root = tmp_path / label / "sample"
        root.mkdir(parents=True)
        (root / "__init__.py").write_text(source)
        (root / "helpers.py").write_text(helpers)
        roots.append(root.parent)
    return checker().compare_sources(*roots, package="sample")


@pytest.mark.parametrize("new", [
    "__all__ = []\ndef api(a, b=1): pass",
    "__all__ = ['api']\ndef api(a, b): pass",
    "__all__ = ['api']\ndef api(a, b=2): pass",
    "__all__ = ['api']\ndef api(b=1, a=0): pass",
    "__all__ = ['api']\ndef api(a, *, b=1): pass",
    "__all__ = ['api']\ndef api(a): pass",
    "__all__ = ['api']\ndef api(*args, **kwargs): pass",
    "__all__ = ['api']\nasync def api(a, b=1): pass",
    "__all__ = ['api']\napi = 3",
    "__all__ = ['api']\ndef api(a, b=1, *, required): pass",
])
def test_function_breaks_are_contextual(tmp_path, new):
    errors = compare(tmp_path, "__all__ = ['api']\ndef api(a, b=1): pass", new)
    assert errors and any("api" in error for error in errors)


def test_constructor_order_breaks(tmp_path):
    old = "from dataclasses import dataclass\n__all__=['Record']\n@dataclass(frozen=True)\nclass Record:\n a: str\n b: int\n"
    assert compare(tmp_path, old, old.replace(" a: str\n b: int", " b: int\n a: str"))


def test_exception_base_breaks(tmp_path):
    old = "__all__=['Refusal']\nclass Refusal(ValueError): pass"
    assert compare(tmp_path, old, old.replace("ValueError", "RuntimeError"))


def test_additive_and_private_changes_pass(tmp_path):
    old = "__all__=['api']\ndef api(a, b=1): pass\ndef helper(x): pass"
    new = "__all__=['api', 'extra']\ndef api(a, b=1, *, option=None): pass\ndef extra(): pass\ndef helper(): pass"
    assert compare(tmp_path, old, new) == []


@pytest.mark.parametrize("signature", ["a", "a, /", "*, a"])
def test_safe_argument_widening_passes(tmp_path, signature):
    old = f"__all__=['api']\ndef api({signature}): pass"
    assert compare(tmp_path, old, "__all__=['api']\ndef api(a=None): pass") == []


def test_internal_move_and_helper_change_pass(tmp_path):
    assert compare(tmp_path, "__all__=['api']\ndef api(a): pass", 
                   "from .helpers import api\n__all__=['api']",
                   new_helpers="def api(a): pass\ndef helper(): pass") == []


@pytest.mark.parametrize("default, breaks", [(1, False), (2, True)])
def test_private_target_alias_keeps_root_contract(tmp_path, default, breaks):
    errors = compare(tmp_path, "__all__=['api']\ndef api(a=1): pass",
                     "from .helpers import _implementation as api\n__all__=['api']",
                     new_helpers=f"def _implementation(a={default}): pass")
    assert bool(errors) is breaks


@pytest.mark.parametrize("source", ["", "__all__=[]", "__all__=['missing']"])
def test_unresolvable_baseline_refuses(tmp_path, source):
    with pytest.raises(ValueError, match="export|resolve"):
        compare(tmp_path, source, "__all__=['api']\ndef api(): pass")


def test_missing_baseline_commit_refuses(tmp_path):
    with pytest.raises((ValueError, RuntimeError), match="baseline|Git"):
        checker().check_repository(tmp_path)
