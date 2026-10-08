#!/usr/bin/env python3
"""Run the evidence the changed surfaces require, then write down what actually happened.

This is the missing half of `change-scope.py`. That tool answers "what evidence does
this change need?" and stops there; this one executes the runnable part of that answer,
refuses to call anything green on its own, and leaves a record a reviewer can read.

Read-only with respect to the repository except for one output file: the evidence
record under `dev/evidence/`. It never fetches, never guesses a base, and never overwrites
an earlier record: a second run on the same day and branch writes `-2`, `-3`, … next to
it, because a record of what was true at a moment stops being evidence once it can be
edited. `--out` is used exactly as given.

Every evidence entry in `surfaces[].evidence` is one of two things:

  runnable  a command line that starts with a known runner (`python3 `, `pnpm `, `make `,
            `bash `, `node `, `cargo `, `go `, `dotnet `, `./`, `uv ` …). It is executed
            from the repository root and receives one of three verdicts.
  manual    anything else — a sentence describing what a person must do or judge.
            Printed under "you must still do these", never reported as passing.

A runnable command's verdict separates "the change is wrong" from "the tooling is wrong":

  PASS      it resolved and exited 0.
  FAIL      it resolved, ran, and exited non-zero. A verdict about the change.
  UNKNOWN   it could not run at all — it does not resolve at execution time, the shell
            reported 126/127, or the process could not be spawned. A tooling problem is
            not a verdict about the change, and it is never counted as a pass.

The exit code is 1 when any runnable command fails or could not run. Manual entries never
fail the run: a tool cannot judge them, and pretending otherwise is how a green record
starts lying.

Usage:
  python3 tools/run-evidence.py --base origin/main
  python3 tools/run-evidence.py --worktree-only --dry-run
  python3 tools/run-evidence.py --check          # validate the declared commands only
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NoReturn

DEFAULT_CONFIG = Path(__file__).resolve().parent / "workflow.json"

# A command is runnable when its first token is one of these. The list is deliberately a
# closed set: an unrecognised leading token is manual evidence, which keeps a typo in the
# config from silently executing the wrong thing.
RUNNER_TOKENS = {
    "python3", "python", "node", "npm", "pnpm", "yarn", "bun", "deno",
    "make", "just", "task", "go", "cargo", "dotnet", "ruby", "rake",
    "bash", "sh", "pwsh", "uv", "poetry", "mvn", "gradle",
}

# A placeholder proves nothing, so an entry containing one is never executed and never
# reported as passing — including mid-command, as in `--base <verified-base-ref>`.
PLACEHOLDER = re.compile(r"<[^>]*>")

MAX_TAIL_LINES = 12


def die(message: str, code: int = 2) -> NoReturn:
    """Print a diagnostic to stderr and exit."""
    print(f"run-evidence: {message}", file=sys.stderr)
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
    return config


def git_root() -> Path:
    """Return the working tree root, or exit when this is not a git repository."""
    result = git("rev-parse", "--show-toplevel")
    if result.returncode != 0:
        die("not a git repository")
    return Path(result.stdout.strip())


def changed_paths(base: str | None, head: str, worktree_only: bool) -> tuple[list[str], str | None]:
    """Return the changed paths and the resolved merge base."""
    paths: set[str] = set()
    merge_base: str | None = None
    if not worktree_only:
        if not base:
            die("--base is required unless --worktree-only is given")
        resolved = git("merge-base", base, head)
        if resolved.returncode != 0:
            die(
                f"cannot resolve the merge base of {base!r} and {head!r}: "
                f"{resolved.stderr.strip() or 'no output'}\n"
                "  This tool never fetches and never guesses a base. Fetch the ref first.",
            )
        merge_base = resolved.stdout.strip()
        result = git("diff", "--name-only", merge_base, head)
        if result.returncode != 0:
            die(f"git diff failed: {result.stderr.strip()}")
        paths.update(line for line in result.stdout.splitlines() if line)
    result = git("status", "--porcelain", "--untracked-files=all")
    if result.returncode != 0:
        die(f"git status failed: {result.stderr.strip()}")
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.rsplit(" -> ", 1)[1]
        paths.add(path)
    return sorted(paths), merge_base


def classify(entry: str) -> tuple[str, str]:
    """Return ('runnable' | 'manual' | 'placeholder', the entry)."""
    stripped = entry.strip()
    if PLACEHOLDER.search(stripped):
        return "placeholder", stripped
    head = stripped.split(maxsplit=1)[0] if stripped else ""
    if not head:
        return "manual", stripped
    if head.startswith("./") or head in RUNNER_TOKENS:
        return "runnable", stripped
    return "manual", stripped


def matches(path: str, patterns: list[str]) -> bool:
    """fnmatch with the repository's convention: '*' also matches '/'."""
    from fnmatch import fnmatch

    return any(fnmatch(path, pattern) for pattern in patterns)


def build_plan(config: dict, paths: list[str]) -> tuple[list[dict], list[str]]:
    """Return (used surfaces with their evidence, unmatched paths)."""
    surfaces = config["surfaces"]
    used: list[dict] = []
    unmatched: list[str] = []
    for path in paths:
        hits = [surface for surface in surfaces if matches(path, surface["patterns"])]
        if not hits:
            unmatched.append(path)
        for surface in hits:
            if surface["name"] not in {item["name"] for item in used}:
                used.append({
                    "name": surface["name"],
                    "why": surface.get("why", ""),
                    "paths": [],
                    "evidence": [classify(entry) for entry in surface.get("evidence", [])],
                })
            entry = next(item for item in used if item["name"] == surface["name"])
            if path not in entry["paths"]:
                entry["paths"].append(path)
    return used, unmatched


def plan_for_all(config: dict) -> list[dict]:
    """Return every declared surface with its evidence, for `--check`."""
    return [
        {
            "name": surface["name"],
            "why": surface.get("why", ""),
            "paths": [],
            "evidence": [classify(entry) for entry in surface.get("evidence", [])],
        }
        for surface in config["surfaces"]
    ]


def looks_like_command(entry: str) -> bool:
    """Return True when an entry reads as a command line but does not start with a runner.

    A typo must not silently downgrade a command to "manual evidence": the record would
    then read as if a person had judged it. Flags, shell operators, and script
    extensions are strong enough signals to demand an explicit runner token or an
    explicit rewording.
    """
    if PLACEHOLDER.search(entry):
        return False
    if any(token in entry for token in (" --", " && ", " || ", " | ")):
        return True
    head = entry.split(maxsplit=1)[0] if entry.strip() else ""
    return head.endswith((".py", ".sh", ".mjs", ".cjs", ".ts", ".js", ".rb", ".go"))


def validate_commands(plan: list[dict]) -> list[str]:
    """Return a violation for every runnable command whose entry point does not resolve."""
    violations: list[str] = []
    for surface in plan:
        for kind, entry in surface["evidence"]:
            if kind == "manual" and looks_like_command(entry):
                violations.append(
                    f"{surface['name']}: {entry!r} reads as a command but does not start with a known runner"
                    f" — start it with one of {sorted(RUNNER_TOKENS)} or reword it as manual evidence",
                )
                continue
            if kind != "runnable":
                continue
            head = entry.split(maxsplit=1)[0]
            if head.startswith("./"):
                target = Path(head)
                if not target.exists():
                    violations.append(f"{surface['name']}: {entry!r} — {head} does not exist")
                continue
            if shutil.which(head) is None:
                violations.append(f"{surface['name']}: {entry!r} — {head!r} is not on PATH")
    return violations


def tail(text: str) -> str:
    """Return the last few non-empty lines, for the record."""
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[-MAX_TAIL_LINES:])


# A shell reports 126 for "found but not executable" and 127 for "not found". Neither is
# a statement about the change under test.
UNRUNNABLE_EXIT_CODES = frozenset({126, 127})


def resolves(root: Path, entry: str) -> bool:
    """Return True when a runnable entry's command resolves from the repository root."""
    head = entry.split(maxsplit=1)[0]
    if head.startswith("./"):
        return (root / head).exists()
    return shutil.which(head) is not None


def verdict_for(completed: subprocess.CompletedProcess[str] | None, reason: str | None) -> tuple[str, str | None]:
    """Return (verdict, detail) for one attempted command.

    UNKNOWN stays distinct from FAIL on purpose: a tool that never ran has said nothing
    about the change, and recording it as a failure teaches the reader to distrust the
    record exactly as much as recording it as a pass would.
    """
    if completed is None:
        return "UNKNOWN", reason or "the command was not attempted"
    if completed.returncode in UNRUNNABLE_EXIT_CODES:
        return "UNKNOWN", f"the shell could not run it (exit {completed.returncode})"
    if completed.returncode == 0:
        return "PASS", None
    return "FAIL", None


LONG_LIVED_BRANCHES = ("main", "master", "detached", "")


def record_slug(branch: str, surfaces: list[str]) -> str:
    """Name a record for what it covered, in the reader's words rather than the tool's.

    A reader browsing `dev/evidence/` has the file name and little else. The branch answers
    that where it says something — a working branch is named for its work — and on a branch
    that outlives the work it does not: every record there would be `<date>-main`, told apart
    by a counter nobody can read anything from. The surfaces a run covers are the project's
    own names for the parts it touched, so the record is named for those instead.
    """
    clean = re.sub(r"[^A-Za-z0-9._-]+", "-", branch).strip("-")
    if clean not in LONG_LIVED_BRANCHES:
        return clean
    if not surfaces:
        return "worktree"
    return "-".join(surfaces[:3]) + ("-and-more" if len(surfaces) > 3 else "")


def slug_for(root: Path, plan: list[dict]) -> str:
    """Return a filesystem-safe name for the record this run writes."""
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    return re.sub(r"[^A-Za-z0-9._-]+", "-", record_slug(branch, [surface["name"] for surface in plan])) or "evidence"


def unique_record_path(base: Path, stamp: str) -> Path:
    """Return the name this run stamps its record with, or a same-second successor.

    An evidence record is a claim about a moment: rewriting it after the fact is
    forging the record. Two rules name one, and the reader is meant to read the whole
    name: `record_slug` says what the run covered, and this one stamps *when* it ran, so
    a name is never an ordinal over a name that a rename or a deletion can move. The
    `-<n>` successor survives for the one collision a stamp cannot separate — two runs
    inside the same second — and takes the first free number only there.
    """
    candidate = base.with_name(f"{base.stem}-{stamp}{base.suffix}")
    if not candidate.exists():
        return candidate
    for number in range(2, 1000):
        successor = base.with_name(f"{base.stem}-{stamp}-{number}{base.suffix}")
        if not successor.exists():
            return successor
    die(f"cannot find a free evidence record name next to {base}")


def write_record(root: Path, out: Path, plan: list[dict], unmatched: list[str], results: list[dict], merge_base: str | None, base: str | None) -> None:
    """Write the evidence record a reviewer reads."""
    out.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    passed = [item for item in results if item["verdict"] == "PASS"]
    failed = [item for item in results if item["verdict"] == "FAIL"]
    unknown = [item for item in results if item["verdict"] == "UNKNOWN"]
    verdict = "PASS" if not failed and not unknown else "FAIL"
    lines = [
        "# Evidence record",
        "",
        f"Recorded: {stamp}",
        f"Scope: {'worktree only' if merge_base is None else f'{base} (merge base {merge_base[:12]})'}",
        f"Verdict: {verdict} — {len(passed)} passed, {len(failed)} failed, "
        f"{len(unknown)} could not run (of {len(results)} runnable command(s))",
        "",
        "## Changed paths and their surfaces",
        "",
    ]
    for surface in plan:
        lines.append(f"### {surface['name']}")
        lines.append("")
        lines.append(surface["why"])
        lines.append("")
        for path in surface["paths"]:
            lines.append(f"- `{path}`")
        lines.append("")
        for kind, entry in surface["evidence"]:
            if kind == "runnable":
                outcome = next((item for item in results if item["command"] == entry), None)
                if outcome is None:
                    code = "not run"
                elif outcome["exit"] is None:
                    code = f"{outcome['verdict']} — {outcome['detail']}"
                else:
                    code = f"{outcome['verdict']} (exit {outcome['exit']})"
                lines.append(f"- **{code}** — `{entry}`")
                if outcome and outcome["output"]:
                    lines.extend(["", "  ```", *[f"  {line}" for line in outcome["output"].splitlines()], "  ```", ""])
            elif kind == "placeholder":
                lines.append(f"- **UNFILLED** — `{entry}` (a placeholder is not evidence)")
            else:
                lines.append(f"- **manual** — {entry}")
        lines.append("")
    if unmatched:
        lines.extend(["## Paths with no declared surface", ""])
        lines.extend(f"- `{path}`" for path in unmatched)
        lines.append("")
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        prog="run-evidence",
        description="Run the evidence the changed surfaces require and record the result.",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="surface map (default: tools/workflow.json)")
    parser.add_argument("--base", help="verified base ref (required unless --worktree-only)")
    parser.add_argument("--head", default="HEAD", help="head ref (default: HEAD)")
    parser.add_argument("--worktree-only", action="store_true", help="ignore committed changes and inspect the worktree")
    parser.add_argument("--dry-run", action="store_true", help="print the plan without running anything")
    parser.add_argument("--check", action="store_true", help="validate that declared commands resolve, then exit")
    parser.add_argument("--out", type=Path, help="evidence record path (default: dev/evidence/<date>-<branch>.md)")
    args = parser.parse_args(argv)

    root = git_root()
    config = load_config(args.config if args.config.is_absolute() else (root / args.config))

    if args.check:
        violations = validate_commands(plan_for_all(config))
        for violation in violations:
            print(f"FAIL {violation}")
        if violations:
            return 1
        print(f"run-evidence: every declared runnable command resolves ({len(config['surfaces'])} surface(s))")
        return 0

    paths, merge_base = changed_paths(args.base, args.head, args.worktree_only)
    plan, unmatched = build_plan(config, paths)

    violations = validate_commands(plan)
    if violations:
        for violation in violations:
            print(f"FAIL {violation}", file=sys.stderr)
        return 1

    # One execution per distinct command: the policy forbids repeating a check whose
    # inputs have not changed, and several surfaces routinely share one command.
    runnable: list[tuple[str, str]] = []
    seen: dict[str, int] = {}
    for surface in plan:
        for kind, entry in surface["evidence"]:
            if kind != "runnable":
                continue
            if entry in seen:
                index = seen[entry]
                name, surfaces = runnable[index]
                runnable[index] = (name, f"{surfaces}, {surface['name']}")
                continue
            seen[entry] = len(runnable)
            runnable.append((entry, surface["name"]))
    print(
        f"run-evidence: {len(paths)} changed path(s), {len(plan)} surface(s), "
        f"{len(runnable)} distinct runnable command(s)",
    )
    print()
    for surface in plan:
        print(f"  {surface['name']}: {surface['why']}")
        for kind, entry in surface["evidence"]:
            marker = {"runnable": "$", "manual": "?", "placeholder": "!"}[kind]
            print(f"      {marker} {entry}")
    print()
    if unmatched:
        print("## No declared surface — decide and declare one")
        for path in unmatched:
            print(f"  {path}")
        print()

    if args.dry_run:
        print("run-evidence: dry run — nothing executed, no record written")
        return 0

    results: list[dict] = []
    for command, surfaces in runnable:
        print(f"--- [{surfaces}] {command}")
        completed = None
        reason = None
        if not resolves(root, command):
            reason = "the command does not resolve at execution time"
        else:
            try:
                completed = subprocess.run(command, shell=True, cwd=root, capture_output=True, text=True)
            except OSError as exc:
                reason = f"could not spawn it: {exc}"
        combined = "" if completed is None else (completed.stdout or "") + (completed.stderr or "")
        if combined.strip():
            print(combined.rstrip())
        verdict, detail = verdict_for(completed, reason)
        results.append({
            "surface": surfaces,
            "command": command,
            "exit": None if completed is None else completed.returncode,
            "verdict": verdict,
            "detail": detail,
            "output": tail(combined),
        })
        if verdict != "PASS":
            print(f"--- [{surfaces}] {verdict}{'' if detail is None else f': {detail}'}")

    now = datetime.now(timezone.utc)
    out = args.out or unique_record_path(
        root / "dev" / "evidence" / f"{now.strftime('%Y-%m-%d')}-{slug_for(root, plan)}.md",
        now.strftime("%H%M%SZ"),
    )
    write_record(root, out, plan, unmatched, results, merge_base, args.base)

    manual = [(surface["name"], entry) for surface in plan for kind, entry in surface["evidence"] if kind in ("manual", "placeholder")]
    passed = [item for item in results if item["verdict"] == "PASS"]
    failed = [item for item in results if item["verdict"] == "FAIL"]
    unknown = [item for item in results if item["verdict"] == "UNKNOWN"]
    print()
    print(f"run-evidence: record written to {out.relative_to(root) if out.is_relative_to(root) else out}")
    if manual:
        print("run-evidence: you must still do these yourself, and paste the result:")
        for name, entry in manual:
            print(f"  [{name}] {entry}")
    if failed or unknown:
        reasons = []
        if failed:
            reasons.append(f"{len(failed)} command(s) failed")
        if unknown:
            reasons.append(f"{len(unknown)} command(s) could not run")
        print(f"run-evidence: {', '.join(reasons)} — this change is not verified")
        return 1
    print(f"run-evidence: {len(passed)} command(s) exited 0. That is not a verdict on the manual entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
