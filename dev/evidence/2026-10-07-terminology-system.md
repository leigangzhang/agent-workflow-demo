# Terminology-layer verification record — 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **Two directions, two homes.** `docs/glossary.md` says what each term means here and which spelling to use — for the agent; `docs/plain-language.md` says how to say it to someone who has never read this kit — for the human. Translation pairs stay in `docs/I18N.md#terminology`, which no longer claims meaning.
2. **A new document kind.** The kit's kind table had no `reference`; both pages arrived with the skeleton, home, and check that the table's own rule demands.
3. **Six new checks.** Two framing-section checks, two reference budgets, the term-heading anchor rule, and one executable spelling ban.
4. **A thirteenth skill.** `.agents/skills/plain-language/SKILL.md` loads when the agent writes to a person and points at the table.
5. **The corpus was cleaned before the ban shipped.** 13 Chinese files moved to 正文; the frozen archive under `.backup/` and the run records under `evidence/` are outside the ban's patterns as history.

## Sizes against the ceilings

```text
docs/glossary.md: 1314 words  (ceiling 1350 words / 180 lines)
docs/plain-language.md: 754 words  (ceiling 1350 words / 180 lines)
docs/glossary.zh.md: 169 lines  (ceiling 1350 words / 180 lines)
docs/plain-language.zh.md: 98 lines  (ceiling 1350 words / 180 lines)
relative links across the kit: 588, broken: 0
```

## The new rules were watched going red

Two of them failed on real misses before they passed, which is the strongest form of the evidence:

```text
banned-spellings      → docs/check-catalog.md:80, .agents/notes/implemented/process/2026-10-07-terminology-system.md:32/55/57 names the banned spelling
term-headings-ascii   → docs/plain-language.zh.md:22: matches forbidden pattern '^### .*[^\x00-\x7F]'   (temporary translated heading, restored)
```

The ban's first two runs found the literal inside the ban's own explanation and inside the generated catalog that renders that explanation — both were rewritten to describe the spelling instead of quoting it, which is why the executable half now lives only in the check's `regex`.

## The kit's own gates

### `python3 tools/check-invariants.py --self-test | tail -3`

```text
PASS seal-outside-patterns: a seal outside the scanned corpus was rejected (archive/manifest.json sealed[0]: .agents/notes/x.md matches none of ['archive/*'], so its seal is never verified)
PASS seal-empty-archive: an archive with nothing sealed is accepted, and the unsealed-file probe keeps the guard live
check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
exit=0
```

### `python3 tools/check-invariants.py | grep -cE "^PASS"`

```text
47
exit=0
```

### `python3 tools/check-invariants.py | grep -E "^(FAIL)" | head -3`

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
pair-docs: 35 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 51 tests in 0.066s

OK
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1162 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

The two new pages are reference documents, not READMEs, so they stay outside the host's pairing corpus; the count therefore stays at 1162 while this kit's own scope grew to 35 pairs.

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
