# Git state corrected, and the co-location question decided — verification record, 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

## Two things this record covers

1. **A false claim was corrected.** Nine evidence records said `study/` was git-ignored by its host repository. It is not: the host's `.gitignore` line is `# study/`, commented out, and `git ls-files study` returns `0` — the tree is **untracked**, not ignored. The effect those records described is real (the git-based tools cannot enumerate the files individually), so only the reason was wrong. Each record now states it correctly and carries a `Corrected 2026-10-07` note that preserves the misreading, including where it came from: [tools/README.md](../../tools/README.md) says a path under *an* ignored tree does not appear at all, which is the general rule, not a statement about this tree.
2. **The co-location question is closed by a decision.** [dev/contracts/kinds.md](../../dev/contracts/kinds.md) and [dev/capabilities/registry.json](../../dev/capabilities/registry.json) stay where they are, and the placement table in [docs/documentation.md](../../docs/documentation.md) gained two rows stating where a source-derived interface and a capability's roles live. The grounds are in the record: the paste is the registered `definition` of the `check-engine` seam, and the registry carries roles that no marker carries.

## Layout after the decision

```text
files moved: 0 — both artifacts keep their homes, their checks, and their records
.agents/notes/proposed/process/: removed when it became empty; the proposal shipped to .agents/notes/implemented/process/
relative links across the kit: 647, broken: 0
```

## The kit's own gates, and the git facts that were misread

### `python3 tools/check-invariants.py | grep -E "^(FAIL|check-invariants)" | tail -2`

```text

exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 39 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/gen-docs.py --check`

```text
gen-docs: docs/check-catalog.md is up to date (82 lines).
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 59 tests in 0.081s

OK
exit=0
```

### `grep -c "^# .*study/" /Users/ray/Workspace/deepseek-harness/.gitignore || true`

```text
1
exit=0
```

### `sed -n "50p" /Users/ray/Workspace/deepseek-harness/.gitignore`

```text
# study/
exit=0
```

### `git -C /Users/ray/Workspace/deepseek-harness ls-files study | wc -l | tr -d " "`

```text
0
exit=0
```

### `git -C /Users/ray/Workspace/deepseek-harness status --porcelain study`

```text
?? study/
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1163 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```
