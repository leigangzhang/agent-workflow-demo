"""Helpers every check shares: configuration, file iteration, line and word counts."""

from __future__ import annotations

from fnmatch import fnmatch

import os

from pathlib import Path
from typing import Iterator
from typing import NoReturn
import json
import sys

DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "workflow.json"  # tools/workflow.json, beside the package


MAX_FILE_BYTES = 2 * 1024 * 1024


SKIP_DIRECTORIES = {
    ".git", ".hg", ".svn", ".venv", "venv", "__pycache__", "node_modules",
    "dist", "build", "target", ".next", ".cache", ".mypy_cache", ".pytest_cache",
    "vendor", "coverage",
}

# capability: check-engine — the declared check kinds are this capability's interface.
# region: supported-kinds
SUPPORTED_KINDS = ("tier-manifest", "budget", "required-sections", "source-mirror", "capability-registry", "criteria-traced", "forbidden-regex", "note-class", "skill-trigger", "publish-manifest", "sealed-manifest")
# endregion: supported-kinds


def die(message: str, code: int = 2) -> NoReturn:
    """Print a diagnostic to stderr and exit."""
    print(f"check-invariants: {message}", file=sys.stderr)
    raise SystemExit(code)


def load_config(path: Path) -> dict:
    """Read and validate the check declarations."""
    if not path.is_file():
        die(f"config not found: {path}")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read config {path}: {exc}")
    if not isinstance(config, dict):
        die(f"config must be a JSON object: {path}")
    checks = config.get("checks")
    if not isinstance(checks, list) or not checks:
        die(f"config needs a non-empty 'checks' list: {path}")
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            die(f"check #{index} is not a JSON object: {path}")
        if not check.get("id"):
            die(f"check #{index} has no 'id': {path}")
        if check.get("kind") not in SUPPORTED_KINDS:
            die(f"check {check['id']!r} has unsupported kind {check.get('kind')!r}; supported: {', '.join(SUPPORTED_KINDS)}")
        if not check.get("patterns"):
            die(f"check {check['id']!r} needs a non-empty 'patterns' list: {path}")
    return config


def iter_files(root: Path, patterns: list[str]) -> Iterator[tuple[str, str]]:
    """Yield (repository-relative path, text) for every text file matching one pattern."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in SKIP_DIRECTORIES)
        for filename in sorted(filenames):
            path = Path(dirpath) / filename
            relative = path.relative_to(root).as_posix()
            if not any(fnmatch(relative, pattern) for pattern in patterns):
                continue
            if path.is_symlink():
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            yield relative, text


def section_body(text: str, section: str) -> list[str]:
    """Return the lines between `section` and the next '## ' heading."""
    body: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line == section
            continue
        if inside:
            body.append(line)
    return body


def count_lines(text: str) -> int:
    """Count physical lines, treating a missing trailing newline as a line."""
    if text == "":
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def count_words(text: str) -> int:
    """Count whitespace-separated tokens, the same unit as `wc -w`.

    The unit undercounts prose written without word-separating spaces, so a
    Chinese standing document stays on a line budget; see docs/documentation.md.
    """
    return len(text.split())


def read_manifest(root: Path, check: dict, key: str) -> dict:
    """Read a check's manifest and require `key` to be a non-empty list."""
    manifest_rel = check.get("manifest")
    if not isinstance(manifest_rel, str) or manifest_rel == "":
        die(f"check {check['id']!r}: 'manifest' must be a non-empty string")
    manifest_path = root / manifest_rel
    if not manifest_path.is_file():
        die(f"check {check['id']!r}: manifest not found: {manifest_rel}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"check {check['id']!r}: cannot read manifest {manifest_rel}: {exc}")
    if not isinstance(manifest, dict):
        die(f"check {check['id']!r}: manifest {manifest_rel} must be a JSON object")
    values = manifest.get(key)
    if not isinstance(values, list) or not values:
        die(f"check {check['id']!r}: manifest {manifest_rel} needs a non-empty {key!r} list")
    return manifest
