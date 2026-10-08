"""The command line: load the configuration, run every declared check, report, and exit."""

from __future__ import annotations

from pathlib import Path
import argparse

from .core import DEFAULT_CONFIG, die, load_config
from .registry import run_checks, self_test

def main(argv: list[str] | None = None) -> int:
    """Entry point."""
    parser = argparse.ArgumentParser(
        prog="check-invariants",
        description="Run the executable conventions declared in the workflow config.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("root", nargs="?", default=".", help="tree to scan (default: the current directory)")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="check declarations (default: tools/workflow.json)")
    parser.add_argument("--self-test", action="store_true", help="prove each check kind can fail, using throwaway fixtures")
    parser.add_argument("--list", action="store_true", help="list the declared checks and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    config = load_config(args.config)

    if args.list:
        for check in config["checks"]:
            print(f"  {check['id']}  ({check['kind']})  {check.get('why', '')}")
        return 0

    root = Path(args.root).resolve()
    if not root.is_dir():
        die(f"not a directory: {root}")

    failed = False
    for check_id, violations in run_checks(root, config["checks"]):
        if violations:
            failed = True
            print(f"FAIL {check_id}")
            for violation in violations:
                print(f"  {violation}")
        else:
            print(f"PASS {check_id}")
    return 1 if failed else 0
