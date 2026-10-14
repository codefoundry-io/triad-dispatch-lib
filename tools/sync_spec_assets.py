"""Generate runtime resources from canonical local bytes, without Git or network."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import sys

# Also works directly from a source archive before the library is installed.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from triad_dispatch_lib.bundle_manifest import make_manifest

BUNDLES = {
    "": {"leg-verdict.schema.json": "contracts/leg-verdict.schema.json"},
    "roster-bundle": {"contracts/review-legs.schema.json": "contracts/review-legs.schema.json"},
    "prompt-bundle": {
        "contracts/review-kind.schema.json": "contracts/review-kind.schema.json",
        **{f"prompts/{name}.md": f"prompts/{name}.md" for name in
           ("common-clauses", "leg-codex", "leg-claude", "leg-google", "investigation")},
    },
}


def refuse_symlinks(path: Path) -> None:
    for component in (path, *path.parents):
        try:
            mode = component.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise ValueError(f"Symlink refused: {component}")


def sync_assets(repo: Path, *, write: bool) -> None:
    """Validate the entire owned output tree before writing any resource."""
    source = repo / "spec"
    data = repo / "src/triad_dispatch_lib/data"
    refuse_symlinks(source)
    refuse_symlinks(data)
    if not source.is_dir():
        raise ValueError("Missing canonical specification tree")
    for path in source.rglob("*"):
        refuse_symlinks(path)
    expected = {}
    for bundle, mapping in BUNDLES.items():
        digests = {}
        for name, canonical in mapping.items():
            path = source / canonical
            refuse_symlinks(path)
            raw = path.read_bytes()
            expected[Path(bundle) / name] = raw
            digests[name] = hashlib.sha256(raw).hexdigest()
        expected[Path(bundle) / "source-manifest.json"] = (
            json.dumps(make_manifest(digests), indent=2, sort_keys=True) + "\n").encode("utf-8")
    directories = {parent for path in expected for parent in path.parents if parent != Path('.')}
    if data.exists():
        if not data.is_dir():
            raise ValueError("Generated resource root is not a directory")
        for path in data.rglob("*"):
            refuse_symlinks(path)
            relative = path.relative_to(data)
            if not ((path.is_file() and relative in expected)
                    or (path.is_dir() and relative in directories)):
                raise ValueError(f"Unexpected generated path: {relative}")
    for relative in directories:
        path = data / relative
        if path.exists() and not path.is_dir():
            raise ValueError(f"Generated directory occupied: {relative}")
    for relative in expected:
        path = data / relative
        if path.exists() and not path.is_file():
            raise ValueError(f"Generated file occupied: {relative}")
    if not write:
        for relative, raw in expected.items():
            path = data / relative
            if not path.is_file() or path.read_bytes() != raw:
                raise ValueError(f"Generated resource drift: {relative}")
        return
    for relative, raw in expected.items():
        path = data / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        sync_assets(Path(__file__).resolve().parents[1], write=args.write)
    except (OSError, ValueError) as error:
        print(f"Spec asset synchronization failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
