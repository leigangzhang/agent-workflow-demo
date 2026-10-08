# Evidence record

Recorded: 2026-10-08T07:23:03Z
Scope: origin/main (merge base bfeb6e8361b8)
Verdict: PASS — 2 passed, 0 failed, 0 could not run (of 2 runnable command(s))

## Changed paths and their surfaces

### evidence

An evidence record is written by tools/run-evidence.py rather than by hand, and it is the artifact station 6 leaves behind. It needs an owner like any other path: without this surface, the record the tool has just written is an unowned path and change-scope --strict refuses the very change that produced it.

- `dev/evidence/2026-10-08-i18n-decisions-prose-2.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-2.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-3.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-4.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose.md`

- **PASS (exit 0)** — `python3 tools/check-invariants.py`

  ```
  PASS evidence-record
  PASS notes-readme-budget
  PASS notes-readme-budget-zh
  PASS glossary-sections
  PASS plain-language-sections
  PASS reference-budget
  PASS reference-budget-zh
  PASS term-headings-ascii
  PASS banned-spellings
  PASS testing-budget
  PASS testing-budget-zh
  PASS tier-manifest
  ```

- **manual** — read the record: the command it ran, that command's three-state result, and every entry run-evidence could not execute

### prose

Prose states current state; links and budgets are checked mechanically. Generated evidence records are written by tools/run-evidence.py, so they are excluded here: they are not hand-authored prose, and pairing already excludes them.

- `dev/evidence/2026-10-08-i18n-decisions-prose-2.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-2.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-3.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-4.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose.md`

- **PASS (exit 0)** — `python3 tools/check-invariants.py`

  ```
  PASS evidence-record
  PASS notes-readme-budget
  PASS notes-readme-budget-zh
  PASS glossary-sections
  PASS plain-language-sections
  PASS reference-budget
  PASS reference-budget-zh
  PASS term-headings-ascii
  PASS banned-spellings
  PASS testing-budget
  PASS testing-budget-zh
  PASS tier-manifest
  ```

- **UNFILLED** — `<your Markdown link/lint check>` (a placeholder is not evidence)

### i18n

A translated pair is two facts that must not drift. The answer key binds each section to a confirmed hash, the switcher keeps both sides reachable, and identical fenced blocks keep the code comparable. A gate proves the pair is complete and in step; only review proves it is faithful. Generated evidence records are excluded: pairing excludes them, so a change there must not ask for a pairing run.

- `dev/evidence/2026-10-08-i18n-decisions-prose-2.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-2.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-3.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more-4.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose-and-more.md`
- `dev/evidence/2026-10-08-i18n-decisions-prose.md`

- **PASS (exit 0)** — `python3 tools/pair-docs.py --check`

  ```
  pair-docs: 22 pair(s) in scope, all complete and in step.
  ```

- **manual** — read one changed pair end to end: the counterpart must say what the authored side says, not merely something similar
