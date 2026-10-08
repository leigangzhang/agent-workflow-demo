# Evidence record

Recorded: 2026-10-08T04:52:58Z
Scope: worktree only
Verdict: PASS — 2 passed, 0 failed, 0 could not run (of 2 runnable command(s))

## Changed paths and their surfaces

### i18n

A translated pair is two facts that must not drift. The answer key binds each section to a confirmed hash, the switcher keeps both sides reachable, and identical fenced blocks keep the code comparable. A gate proves the pair is complete and in step; only review proves it is faithful. Generated evidence records are excluded: pairing excludes them, so a change there must not ask for a pairing run.

- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.i18n.yaml`
- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.md`
- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.zh.md`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.i18n.yaml`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.md`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.zh.md`

- **PASS (exit 0)** — `python3 tools/pair-docs.py --check`

  ```
  pair-docs: 22 pair(s) in scope, all complete and in step.
  ```

- **manual** — read one changed pair end to end: the counterpart must say what the authored side says, not merely something similar

### decisions

A decision without what it beat invites re-litigation.

- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.md`
- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.zh.md`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.md`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.zh.md`

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

- **manual** — read the Alternatives considered section yourself; a gate cannot judge it

### prose

Prose states current state; links and budgets are checked mechanically. Generated evidence records are written by tools/run-evidence.py, so they are excluded here: they are not hand-authored prose, and pairing already excludes them.

- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.md`
- `.agents/notes/proposed/feature/2026-10-08-gomoku-computer-opponent.zh.md`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.md`
- `.agents/notes/proposed/feature/2026-10-08-html-gomoku-game.zh.md`

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
