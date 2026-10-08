# Lowercase policy-document names — verification record, 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What changed

Four policy documents lost their uppercase names: `DOCS.md` → `documentation.md`, `TESTING.md` → `testing.md`, `I18N.md` → `i18n.md`, `EVOLUTION.md` → `evolution.md`, each with its Chinese side and its i18n record. Uppercase is now reserved for the five names something looks up by name (`README.md`, `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, `TEMPLATE.md`), and the rule is stated inside the document standard, beside the kind table.

## Layout after the rename

```text
docs/*.md: README.md check-catalog.md documentation.md evolution.md extending.md glossary.md i18n.md plain-language.md testing.md
files still carrying an old uppercase policy name: 2
relative links across the kit: 643, broken: 0
```

## Reference sweep

```text
12 files renamed (four documents x English, Chinese, i18n record)
29 files carried links that were recomputed, not hand-edited (38 links)
95 files carried a label, a path mention, or a configuration pattern
```

## History is left alone

The frozen run records under `dev/evidence/` still quote the old names inside their pasted gate output, and the rename deliberately did not touch them: they are verbatim history and are excluded from every pattern, so rewriting them would forge a record.

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
pair-docs: 39 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 59 tests in 0.088s

OK
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1163 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

## A side discovery: the study tree's links into the kit

Sweeping outward found that the research and integration pages under `study/` (outside the kit, and outside every gate this kit runs) held roughly thirty links into the kit that resolved to nothing. Most were broken **before** this rename — they omitted the `docs/` or `dev/` segment — and the rest stopped resolving when the process records moved under `dev/`. They were repaired by resolving each link against the file it meant to name.

```text
study/ docs pointing into the kit: 157 links, 0 broken (before: 30 broken)
```

The kit's own gates cannot see that tree: `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files, which is also why `run-evidence.py --base` cannot scope this work.

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
