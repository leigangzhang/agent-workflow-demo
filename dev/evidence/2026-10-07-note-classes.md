# Note-class verification record — 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **A second axis**: records live at `.agents/notes/<lifecycle>/<class>/<yyyy-mm-dd>-<slug>.md`, classed by the host repository's closed set — `feature`, `bug-fix`, `simplification`, `architecture`, `process`, `testing`.
2. **A gate for it**: a tenth check kind, `note-class`, rejects a folder outside the set, an unknown lifecycle, a missing `Class:` line, and a `Class:` line that disagrees with its folder.
3. **The existing records were classified and moved**, and every relative link inside them was repaired for the extra level: eight records into `.agents/notes/implemented/process/`, the version-state proposal into `.agents/notes/proposed/architecture/`, and six `Class:` lines rewritten from the retired `docs` class.
4. **The rules moved with them**: `.agents/notes/README.md` gained a `## Classes` section, `.agents/notes/AGENTS.md` a class rule, and the path shape gained its second axis in `AGENTS.md`, `docs/LIFECYCLE.md`, `docs/README.md`, and `docs/extending.md`.

## The kit's own gates

### `python3 tools/check-invariants.py --self-test | tail -3`

```text
PASS seal-outside-patterns: a seal outside the scanned corpus was rejected (archive/manifest.json sealed[0]: .agents/notes/x.md matches none of ['archive/*'], so its seal is never verified)
PASS seal-empty-archive: an archive with nothing sealed is accepted, and the unsealed-file probe keeps the guard live
check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
exit=0
```

### `python3 tools/check-invariants.py | grep -E "^(FAIL|check-invariants)" | tail -2`

```text

exit=0
```

### `python3 tools/gen-docs.py --check`

```text
gen-docs: docs/check-catalog.md is up to date (74 lines).
exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 30 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 46 tests in 0.058s

OK
exit=0
```

## The guard was watched going red

`check_note_class` was temporarily neutered (`return []` as its first statement); both guards failed before it was restored:

```text
python3 -m unittest discover -s tests         → Ran 46 tests, FAILED (failures=3)
python3 tools/check-invariants.py --self-test → FAIL note-class: an invalid fixture was accepted, so this check cannot fail
```

## Structural checks the kit gate deliberately does not make

```text
pairs=30 structural_mismatches=0
relative_links=503 broken=0
records per class: {"architecture": 1, "process": 9}
fragments=every fragment resolves (enforced by pair-docs.py --check)
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1162 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

The host gate is unaffected by the move: it scans README artifacts, and records are outside its corpus.

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
