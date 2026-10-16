"""Controls for the root-only structural gate, using tiny real packages."""

import importlib.util
import json
from pathlib import Path
import subprocess

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


@pytest.mark.parametrize("decorator, receiver", [("", "instance"), ("", "instance, /"),
                                                (" @classmethod\n", "instance")])
def test_implicit_constructor_receiver_rename_passes(tmp_path, decorator, receiver):
    old = f"__all__=['Error']\nclass Error(ValueError):\n{decorator} def __init__(self, code): self.code = code"
    new = old.replace("self, code", f"{receiver}, code").replace("self.code", "instance.code")
    assert compare(tmp_path, old, new) == []


@pytest.mark.parametrize("signature", ["instance, extra=1", "instance, extra, code=1",
                                       "instance, code, extra=2"])
def test_real_constructor_arguments_remain_protected(tmp_path, signature):
    old = "__all__=['Record']\nclass Record:\n def __init__(self, code, extra=1): pass"
    new = f"__all__=['Record']\nclass Record:\n def __init__({signature}): pass"
    assert compare(tmp_path, old, new)


def test_static_constructor_first_argument_is_public(tmp_path):
    old = "__all__=['Record']\nclass Record:\n @staticmethod\n def __init__(code, extra=1): pass"
    assert compare(tmp_path, old, old.replace("code, extra=1", "extra=1"))


def test_regular_function_first_argument_is_public(tmp_path):
    old = "__all__=['api']\ndef api(self, code): pass"
    assert compare(tmp_path, old, old.replace("self, code", "code"))


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


def test_missing_metadata_refuses(tmp_path):
    with pytest.raises((ValueError, RuntimeError), match="baseline|Git"):
        checker().check_repository(tmp_path)


def metadata(tmp_path, commit):
    document = {"floor": {"commit": commit}, "baseline": {"commit": commit},
                "floor_exports": ["api"]}
    (tmp_path / "api-compatibility.json").write_text(json.dumps(document))


def test_missing_baseline_commit_refuses(tmp_path):
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    metadata(tmp_path, "0" * 40)
    with pytest.raises(ValueError, match="cannot resolve compatibility baseline/source/Git") as caught:
        checker().check_repository(tmp_path)
    assert isinstance(caught.value.__cause__, subprocess.CalledProcessError)
    assert caught.value.__cause__.cmd[1] == "rev-parse"


def test_baseline_requires_full_commit_identity(tmp_path):
    metadata(tmp_path, "main")
    with pytest.raises(ValueError, match="full immutable commit IDs"):
        checker().check_repository(tmp_path)


def test_candidate_cwd_cannot_replace_baseline(tmp_path, monkeypatch):
    (tmp_path / "new").mkdir()
    monkeypatch.chdir(tmp_path / "new")
    assert compare(tmp_path, "__all__=['api']\ndef api(a=1): pass",
                   "__all__=['api']\ndef api(a=2): pass")


def test_wrong_loaded_root_origin_refuses(tmp_path, monkeypatch):
    root = tmp_path / "sample"
    root.mkdir()
    (root / "__init__.py").write_text("__all__=['api']\ndef api(): pass")
    module = checker()
    wrong = module.griffe.Module("sample", filepath=tmp_path / "elsewhere.py")
    monkeypatch.setattr(module.griffe, "load", lambda *args, **kwargs: wrong)
    with pytest.raises(ValueError, match="loaded root origin mismatch"):
        module.root_exports(tmp_path, "sample")


@pytest.mark.parametrize("signature, breaks", [("a=1, b=2", False), ("a=3, b=2", True),
    ("a=1, b=2, *, required", True), ("b=2, a=1", True)])
def test_old_private_target_still_compares_public_shape(tmp_path, signature, breaks):
    alias = "from .helpers import _implementation as api\n__all__=['api']"
    assert bool(compare(tmp_path, alias, alias,
                        old_helpers="def _implementation(a=1, b=2): pass",
                        new_helpers=f"def _implementation({signature}): pass")) is breaks


@pytest.mark.parametrize("base, breaks", [("ValueError", False), ("RuntimeError", True)])
def test_builtin_base_alias_uses_identity(tmp_path, base, breaks):
    old = "__all__=['Error']\nclass Error(ValueError): pass"
    new = f"from builtins import {base} as BuiltinBase\n__all__=['Error']\nclass Error(BuiltinBase): pass"
    assert bool(compare(tmp_path, old, new)) is breaks


@pytest.mark.parametrize("base, breaks", [("ValueError", False), ("RuntimeError", True)])
def test_private_intermediate_preserves_external_ancestry(tmp_path, base, breaks):
    old = "__all__=['Error']\nclass Error(ValueError): pass"
    new = f"__all__=['Error']\nclass _Internal({base}): pass\nclass Error(_Internal): pass"
    assert bool(compare(tmp_path, old, new)) is breaks


def test_private_intermediate_rename_passes(tmp_path):
    old = "__all__=['Error']\nclass _Internal(ValueError): pass\nclass Error(_Internal): pass"
    assert compare(tmp_path, old, old.replace("_Internal", "_Renamed")) == []


def test_exported_base_ancestry_loss_refuses(tmp_path):
    old = "__all__=['Base', 'Error']\nclass Base(ValueError): pass\nclass Error(Base): pass"
    assert compare(tmp_path, old, old.replace("Error(Base)", "Error(ValueError)"))


@pytest.mark.parametrize("exports", ["['Base','Error','Alias']", "['Alias','Base','Error']"])
def test_additive_exported_base_alias_passes(tmp_path, exports):
    old = "from .helpers import Base\n__all__=['Base','Error']\nclass Error(Base): pass"
    new = f"from .helpers import Base, Base as Alias\n__all__={exports}\nclass Error(Base): pass"
    assert compare(tmp_path, old, new, old_helpers="class Base(ValueError): pass",
                   new_helpers="class Base(ValueError): pass") == []


def test_exported_base_alias_order_does_not_change_identity(tmp_path):
    old = "from .helpers import Base, Base as Alias\n__all__=['Base','Alias','Error']\nclass Error(Base): pass"
    new = old.replace("['Base','Alias','Error']", "['Alias','Base','Error']")
    assert compare(tmp_path, old, new, old_helpers="class Base(ValueError): pass",
                   new_helpers="class Base(ValueError): pass") == []


@pytest.mark.parametrize("from_source_cwd", [False, True])
@pytest.mark.parametrize("candidate, breaks", [
    ("__all__=['api']\ndef api(a, b=1): pass", False),
    ("__all__=['api']\ndef api(b=1): pass", True),
    ("__all__=['api','extra']\ndef api(a, b=1, *, option=None): pass\ndef extra(): pass", False),
])
def test_repository_archive_compares_real_baseline(tmp_path, monkeypatch, from_source_cwd, candidate, breaks):
    source = tmp_path / "src" / "triad_dispatch_lib"
    source.mkdir(parents=True)
    initializer = source / "__init__.py"
    initializer.write_text("__all__=['api']\ndef api(a, b=1): pass")
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    subprocess.run(["git", "add", "src"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "user.name=API Test", "-c", "user.email=test@example.invalid",
                    "commit", "--quiet", "-m", "Synthetic baseline"], cwd=tmp_path, check=True)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tmp_path, text=True).strip()
    metadata(tmp_path, commit)
    initializer.write_text(candidate)
    monkeypatch.chdir(tmp_path / "src" if from_source_cwd else tmp_path)
    errors = checker().check_repository(tmp_path)
    assert bool(errors) is breaks
    if breaks:
        assert any("api" in error and "a" in error for error in errors)


def test_resolved_baseline_identity_mismatch_refuses(tmp_path, monkeypatch):
    metadata(tmp_path, "0" * 40)
    module = checker()
    # Boundary fake: Git claims successful resolution to a different full ID.
    monkeypatch.setattr(module.subprocess, "run", lambda *args, **kwargs:
                        subprocess.CompletedProcess(args[0], 0, stdout="1" * 40 + "\n"))
    with pytest.raises(ValueError, match="baseline commit does not resolve exactly"):
        module.check_repository(tmp_path)
