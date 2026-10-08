# Index columns, surface scope, study corrections, and a placement proposal — verification record, 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **The index answers two more questions.** [docs/README.md](../../docs/README.md) and its Chinese side gained `Tier` and `Gate` columns, so a reader can see which copy set a home ships in and which checks bite there, without opening the lifecycle map.
2. **A changed surface can exclude paths.** `change-scope.py` gained the optional `exclude` key, `prose` and `i18n` exclude `evidence/*`, and the generated catalog prints the resulting scope (`*.md` (except `evidence/*`)) so it stops projecting a wider scope than the tool applies.
3. **Two study-document claims about the host were corrected.** `study/engineering/dsh-docs.md` no longer says the host compares a mirror against `begin`/`end` markers in source (the host uses the TypeScript parser; the markers are this kit's mechanism) and no longer calls `capability-registry` a host artifact (it is this kit's check).
4. **The placement question is filed, not silently answered.** [.agents/notes/proposed/process/2026-10-07-source-derived-co-location.md](../../.agents/notes/implemented/process/2026-10-07-source-derived-co-location.md) proposes deciding the two source-derived artifacts' placement, with three outcomes and traceable acceptance criteria.

## The guard was watched going red

The exclusion was neutered in `surfaces_for` (one line removed) and the suite was re-run before restoring:

```text
python3 -m unittest tests.test_kit_contract.SurfaceExclude  → FAILED (failures=1): the excluded path was claimed again
```

## The kit's own gates

### `python3 tools/check-invariants.py --self-test | tail -2`

```text
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
gen-docs: docs/check-catalog.md is up to date (82 lines).
exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 37 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 54 tests in 0.078s

OK
exit=0
```

### `python3 -m unittest tests.test_kit_contract.SurfaceExclude 2>&1 | tail -2`

```text
OK
exit=0
```

## Structural checks the kit gate deliberately does not make

```text
relative links across the kit: 614, broken: 0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1162 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

The host gate is untouched by these changes: the two study-document corrections are outside its corpus, and the kit-side edits re-recorded their pairs.

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
