#!/usr/bin/env python3
"""Report which declared surface a branch's changes touch, and the evidence each surface requires.

Read-only: never fetches, never writes, never guesses a base ref.

Patterns use fnmatch semantics, in which `*` also matches `/`:
  "*.md"          every Markdown file at any depth
  "notes/*.md"    Markdown under notes/ at any depth
  "AGENTS.md"     exactly the root file

A surface may also declare `exclude`, whose patterns remove a path the include patterns
would otherwise claim. No glob can express negation, so an exclusion needs its own key:
  "exclude": ["dev/evidence/*"]   generated run records stay out of the prose surfaces

Exit codes:
  0  report produced
  1  --strict was given and some changed path matches no declared surface
  2  usage or environment error (not a git repository, unresolvable base, bad config)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path
from typing import NoReturn

DEFAULT_CONFIG = Path(__file__).resolve().parent / "workflow.json"


def die(message: str, code: int = 2) -> NoReturn:
    """Print a diagnostic to stderr and exit."""
    print(f"change-scope: {message}", file=sys.stderr)
    raise SystemExit(code)


def git(*args: str) -> subprocess.CompletedProcess[str]:
    """Run git with the given arguments and capture its output."""
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        die("git is not on PATH")


def load_config(path: Path) -> dict:
    """Read and minimally validate the surface map."""
    if not path.is_file():
        die(f"config not found: {path}")
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        die(f"cannot read config {path}: {exc}")
    if not isinstance(config, dict):
        die(f"config must be a JSON object: {path}")
    surfaces = config.get("surfaces")
    if not isinstance(surfaces, list) or not surfaces:
        die(f"config needs a non-empty 'surfaces' list: {path}")
    for surface in surfaces:
        if not isinstance(surface, dict) or not surface.get("name") or not surface.get("patterns"):
            die(f"every surface needs a non-empty 'name' and 'patterns': {path}")
        exclude = surface.get("exclude")
        if exclude is not None and (not isinstance(exclude, list) or not all(isinstance(item, str) and item for item in exclude)):
            die(f"surface {surface['name']!r}: 'exclude' must be a list of non-empty patterns when present: {path}")
    return config


def resolve_merge_base(base: str, head: str) -> str:
    """Return the merge base, refusing to guess when it does not exist locally."""
    result = git("merge-base", base, head)
    if result.returncode != 0:
        detail = result.stderr.strip() or "no output"
        die(
            f"cannot resolve the merge base of {base!r} and {head!r}: {detail}\n"
            "  This tool never fetches and never guesses a base. Fetch the ref first, or pass\n"
            "  the exact ref your change is based on, for example --base origin/main."
        )
    return result.stdout.strip()


def committed_changes(merge_base: str, head: str) -> list[tuple[str, str]]:
    """Return (status, path) for every path that differs between the base and the head."""
    result = git("diff", "--name-status", "--find-renames", merge_base, head)
    if result.returncode != 0:
        die(f"git diff failed: {result.stderr.strip()}")
    changes: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        # A rename prints "R100<TAB>old<TAB>new"; the new path is the one that matters.
        changes.append((fields[0], fields[-1]))
    return changes


def worktree_changes() -> list[tuple[str, str]]:
    """Return (status, path) for staged, unstaged, and untracked paths."""
    # --untracked-files=all lists each new file instead of collapsing a new
    # directory into one "dir/" entry, so a declared pattern can match it.
    result = git("status", "--porcelain", "--untracked-files=all")
    if result.returncode != 0:
        die(f"git status failed: {result.stderr.strip()}")
    changes: list[tuple[str, str]] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        status = line[:2].strip() or "??"
        path = line[3:].strip()
        if " -> " in path:  # a worktree rename prints "old -> new"
            path = path.rsplit(" -> ", 1)[1]
        changes.append((status, path))
    return changes


def surfaces_for(path: str, surfaces: list[dict]) -> list[dict]:
    """Return every declared surface that claims this path: a pattern matches, no exclude does."""
    return [
        surface for surface in surfaces
        if any(fnmatch(path, pattern) for pattern in surface["patterns"])
        and not any(fnmatch(path, pattern) for pattern in surface.get("exclude", []))
    ]


def build_report(base: str | None, head: str, worktree_only: bool, surfaces: list[dict]) -> dict:
    """Collect the changed paths, their surfaces, and the evidence those surfaces require."""
    entries: dict[str, dict] = {}
    merge_base = None

    def record(origin: str, status: str, path: str) -> None:
        entry = entries.setdefault(path, {"path": path, "origins": [], "statuses": []})
        if origin not in entry["origins"]:
            entry["origins"].append(origin)
        if status not in entry["statuses"]:
            entry["statuses"].append(status)

    if not worktree_only:
        merge_base = resolve_merge_base(base or "", head)
        for status, path in committed_changes(merge_base, head):
            record("committed", status, path)
    for status, path in worktree_changes():
        record("worktree", status, path)

    files: list[dict] = []
    unmatched: list[str] = []
    for entry in sorted(entries.values(), key=lambda item: item["path"]):
        matched = surfaces_for(entry["path"], surfaces)
        entry["surfaces"] = [surface["name"] for surface in matched]
        files.append(entry)
        if not matched:
            unmatched.append(entry["path"])

    used: list[dict] = []
    for surface in surfaces:
        paths = [entry["path"] for entry in files if surface["name"] in entry["surfaces"]]
        if paths:
            used.append({
                "name": surface["name"],
                "why": surface.get("why", ""),
                "evidence": surface.get("evidence", []),
                "paths": paths,
            })

    return {
        "base": base,
        "head": head,
        "mergeBase": merge_base,
        "files": files,
        "surfaces": used,
        "unmatched": unmatched,
    }


def print_report(report: dict) -> None:
    """Print the human-readable report."""
    count = len(report["files"])
    if report["mergeBase"]:
        scope = f"against {report['base']} (merge base {report['mergeBase'][:12]})"
    else:
        scope = "in the worktree only"
    print(f"change-scope: {count} changed path(s) {scope}")
    print()

    print("## Changed paths")
    for entry in report["files"]:
        names = ", ".join(entry["surfaces"]) or "NO SURFACE"
        print(f"  {entry['statuses'][0]:>3}  {entry['path']}  [{names}]")
    print()

    if report["surfaces"]:
        print("## Evidence this change requires")
        for surface in report["surfaces"]:
            print(f"  {surface['name']}: {surface['why']}")
            for command in surface["evidence"]:
                print(f"      $ {command}")
        print()

    if report["unmatched"]:
        print("## No declared surface — decide and declare one")
        for path in report["unmatched"]:
            print(f"  {path}")
        print()
        print("  Add a row to the 'surfaces' list in the config, or drop the change.")
    else:
        print("## Every changed path matches a declared surface.")


def main(argv: list[str] | None = None) -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        prog="change-scope",
        description="Report the changed surface of a branch and the evidence it requires.",
    )
    parser.add_argument("--base", help="exact base ref to compare against (required unless --worktree-only)")
    parser.add_argument("--head", default="HEAD", help="head ref to compare (default: HEAD)")
    parser.add_argument("--worktree-only", action="store_true", help="report only staged, unstaged, and untracked paths")
    parser.add_argument("--strict", action="store_true", help="exit 1 when a changed path matches no declared surface")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="surface map (default: tools/workflow.json)")
    args = parser.parse_args(argv)

    if not args.base and not args.worktree_only:
        parser.error("--base is required (or pass --worktree-only); this tool never guesses a base ref")

    inside = git("rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        die("not inside a git working tree")

    config = load_config(args.config)
    report = build_report(args.base, args.head, args.worktree_only, config["surfaces"])

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)

    return 1 if args.strict and report["unmatched"] else 0


if __name__ == "__main__":
    sys.exit(main())
