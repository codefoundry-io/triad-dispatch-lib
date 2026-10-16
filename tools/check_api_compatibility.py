"""Compare the declared Git baseline with candidate package-root contracts.

Static, source-only gate. Consumer tests cover selected behavior separately.
"""

import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

import griffe


def root_exports(source: Path, package: str, *, allow_empty=False):
    if not (source / package / "__init__.py").is_file():
        raise ValueError(f"cannot resolve source package: {source / package}")
    module = griffe.load(package, search_paths=[source], allow_inspection=False,
                         resolve_aliases=True, resolve_external=False)
    exports = module.exports
    if exports is None or (not exports and not allow_empty) or any(not isinstance(name, str) for name in exports):
        raise ValueError(f"cannot resolve nonempty explicit root exports: {source}")
    try:
        return {name: (module[name].final_target if module[name].is_alias else module[name])
                for name in exports}
    except (KeyError, griffe.AliasResolutionError) as error:
        raise ValueError(f"cannot resolve root export in {source}: {error}") from error


def callable_surface(obj):
    # Project only callable shape: no annotations or recursive member traversal.
    public_parameters = list(obj.parameters)
    if obj.is_class and public_parameters:
        initializer = obj.all_members["__init__"]
        if ("staticmethod" not in initializer.labels
                and public_parameters[0].kind in (griffe.ParameterKind.positional_only,
                                                  griffe.ParameterKind.positional_or_keyword)):
            public_parameters = public_parameters[1:]
    parameters = griffe.Parameters(*(griffe.Parameter(
        p.name, kind=p.kind, default=p.default) for p in public_parameters))
    return griffe.Function(obj.name, parameters=parameters)


def compare_exports(old, new):
    errors = []
    for name, before in old.items():
        if name not in new:
            errors.append(f"{name}: root export removed")
            continue
        after = new[name]
        if before.kind != after.kind:
            errors.append(f"{name}: kind changed from {before.kind} to {after.kind}")
            continue
        if before.is_function and ("async" in before.labels) != ("async" in after.labels):
            errors.append(f"{name}: sync/async function kind changed")
        if before.is_class:
            # Exception inheritance is a documented root contract. Normalize root
            # aliases so moving their implementation module remains compatible.
            def bases(obj, exports):
                paths = {target.path: public for public, target in exports.items()}
                return {paths.get(getattr(base, "canonical_path", str(base)), str(base))
                        for base in obj.bases}
            if not bases(before, old).issubset(bases(after, new)):
                errors.append(f"{name}: declared base inheritance removed or changed")
        if before.is_function or before.is_class:
            left, right = callable_surface(before), callable_surface(after)
            old_surface = griffe.Module("contract", filepath=Path("baseline.py"))
            new_surface = griffe.Module("contract", filepath=Path("candidate.py"))
            old_surface.set_member("call", left)
            new_surface.set_member("call", right)
            for breakage in griffe.find_breaking_changes(old_surface, new_surface):
                errors.append(f"{name}: {breakage.explain()}")
            # Keep named arguments explicit even if variadics could swallow them.
            for parameter in left.parameters:
                if parameter.name not in right.parameters:
                    errors.append(f"{name}({parameter.name}): existing argument removed")
    return errors


def compare_sources(baseline: Path, candidate: Path, *, package="triad_dispatch_lib"):
    return compare_exports(root_exports(baseline, package), root_exports(candidate, package, allow_empty=True))


def check_repository(repo: Path):
    try:
        metadata = json.loads((repo / "api-compatibility.json").read_text())
        commits = [metadata["floor"]["commit"], metadata["baseline"]["commit"]]
        if not metadata["floor_exports"] or any(not isinstance(name, str) for name in metadata["floor_exports"]):
            raise ValueError("baseline requires nonempty protected floor exports")
        if any(not re.fullmatch(r"[0-9a-f]{40}", commit) for commit in commits):
            raise ValueError("baseline and floor require full immutable commit IDs")
        for commit in commits:
            resolved = subprocess.run(["git", "rev-parse", "--verify", f"{commit}^{{commit}}"],
                                      cwd=repo, check=True, capture_output=True, text=True)
            if resolved.stdout.strip() != commit:
                raise ValueError("baseline commit does not resolve exactly")
        archive = subprocess.run(["git", "archive", commits[1], "src"], cwd=repo,
                                 check=True, capture_output=True).stdout
        with tempfile.TemporaryDirectory(prefix="triad-api-baseline-") as temp:
            root = Path(temp)
            with tarfile.open(fileobj=io.BytesIO(archive)) as source:
                source.extractall(root, filter="data")
            old = root_exports(root / "src", "triad_dispatch_lib")
            if not set(metadata["floor_exports"]).issubset(old):
                raise ValueError("baseline lost protected floor exports")
            return compare_exports(old, root_exports(repo / "src", "triad_dispatch_lib"))
    except (OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        raise ValueError(f"cannot resolve compatibility baseline/source/Git: {error}") from error


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = check_repository(args.repo)
    except Exception as error:
        print(f"API compatibility check failed: {error}", file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Declared public API baseline is structurally compatible.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
