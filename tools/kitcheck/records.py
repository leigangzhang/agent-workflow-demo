"""The note-class guard: a record's folder, its `Class:` line, and the closed set must agree."""

from __future__ import annotations

from .core import die

import hashlib
import json
import re

from .core import iter_files

RECORD_PATH = re.compile(r"^notes/(?P<lifecycle>[^/]+)/(?P<klass>[^/]+)/(?P<file>[^/]+)$")


def check_note_class(root: Path, check: dict) -> list[str]:
    """Reject a record whose path class is outside the closed set or disagrees with its Class line.

    A lifecycle's `TEMPLATE.md` is a matched subject only: the skeleton keeps the corpus
    non-empty before the first record exists, and a skeleton is not a record to classify.
    """
    classes = check.get("classes")
    if not isinstance(classes, list) or not classes:
        die(f"check {check['id']!r}: 'classes' must be a non-empty list")
    lifecycles = check.get("lifecycles", ["proposed", "implemented", "rejected"])
    if not isinstance(lifecycles, list) or not lifecycles:
        die(f"check {check['id']!r}: 'lifecycles' must be a non-empty list when present")
    violations: list[str] = []
    for relative, text in iter_files(root, check["patterns"]):
        if relative.rsplit("/", 1)[-1].startswith("TEMPLATE"):
            continue
        match = RECORD_PATH.match(relative)
        if match is None:
            violations.append(f"{relative}: a record lives at notes/<lifecycle>/<class>/<file>")
            continue
        lifecycle, klass = match.group("lifecycle"), match.group("klass")
        if lifecycle not in lifecycles:
            violations.append(f"{relative}: unknown lifecycle {lifecycle!r}; expected one of {', '.join(lifecycles)}")
        if klass not in classes:
            violations.append(f"{relative}: unknown class {klass!r}; the closed set is {', '.join(classes)}")
            continue
        declared = next((line for line in text.splitlines() if line.startswith("Class:")), None)
        if declared is None:
            violations.append(f"{relative}: no 'Class:' line, so the path class {klass!r} is unconfirmed")
        elif declared.split(":", 1)[1].strip() != klass:
            violations.append(
                f"{relative}: Class line {declared.split(':', 1)[1].strip()!r} disagrees with the path class {klass!r}"
            )
    return violations


SELF_TEST_CASES = (
    (
        "note-class",
        {
            "id": "self-note-class",
            "kind": "note-class",
            "patterns": ["notes/*/*/*.md"],
            "classes": ["feature", "bug-fix", "simplification", "architecture", "process", "testing"],
        },
        {"notes/implemented/architecture/decision.md": "Status: implemented\nClass: process\n\n## Problem\nx\n"},
        {"notes/implemented/architecture/decision.md": "Status: implemented\nClass: architecture\n\n## Problem\nx\n"},
    ),
)
