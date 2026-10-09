# Evidence record

Recorded: 2026-10-09T12:37:48Z
Scope: origin/main (merge base b7bc69470f5a)
Verdict: PASS — 4 passed, 0 failed, 0 could not run (of 4 runnable command(s))

## Changed paths and their surfaces

### i18n

A translated pair is two facts that must not drift. The answer key binds each section to a confirmed hash, the switcher keeps both sides reachable, and identical fenced blocks keep the code comparable. A gate proves the pair is complete and in step; only review proves it is faithful. Generated evidence records are excluded: pairing excludes them, so a change there must not ask for a pairing run.

- `.agents/notes/README.i18n.yaml`
- `.agents/notes/README.md`
- `.agents/notes/README.zh.md`
- `.agents/skills/record-decision/SKILL.md`
- `AGENTS.md`
- `docs/check-catalog.md`

- **PASS (exit 0)** — `python3 tools/pair-docs.py --check`

  ```
  pair-docs: 24 pair(s) in scope, all complete and in step.
  ```

- **manual** — read one changed pair end to end: the counterpart must say what the authored side says, not merely something similar

### decisions

A decision without what it beat invites re-litigation.

- `.agents/notes/README.md`
- `.agents/notes/README.zh.md`

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

- `.agents/notes/README.md`
- `.agents/notes/README.zh.md`
- `.agents/skills/record-decision/SKILL.md`
- `AGENTS.md`
- `docs/check-catalog.md`

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

### agent-inputs

Anything an agent reads is an input to a model request, so it has to be enumerable and its edits reviewed as behaviour. A skill whose description stops naming when it loads has been silently deleted from the agent's reach.

- `.agents/notes/README.md`
- `.agents/skills/record-decision/SKILL.md`
- `AGENTS.md`
- `docs/check-catalog.md`

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

- **manual** — re-read what the agent actually sees: the description, the section order, the examples. A renamed section or a reworded trigger is a changed input, not an edit.

### workflow

A guard is only real if a violation makes it red; a skill is only real if its description names when it fires. `.gitignore` is here because it is repository configuration like the rest of this list, and without a pattern that matches it a change to it is an unowned path — the one file every project has and no surface claimed.

- `.agents/skills/record-decision/SKILL.md`
- `tools/workflow.json`

- **PASS (exit 0)** — `python3 tools/check-invariants.py --self-test`

  ```
  PASS budget-words: a file over its word ceiling was rejected (NOTE.md: 40 words, budget is 10)
  PASS publish-stale-public: a public entry with no file behind it was rejected (docs/publish.json: public pattern 'docs/gone.md' matches no file — a published promise with nothing behind it is a broken link)
  PASS publish-public-glob: a public entry that publishes a whole directory was rejected (docs/publish.json public[0] 'docs/*.md': publication is a per-file promise — name the file, do not publish a directory)
  PASS publish-ambiguous: one file matched by both classes was rejected (docs/a.md: matches 2 declared patterns ('docs/a.md' (public), 'docs/*.md' (internal)) — a file has exactly one class)
  PASS publish-no-reason: an internal entry with no reason was rejected (docs/publish.json internal[0] 'docs/b.md': missing 'reason' — say why this file stays in the repository)
  PASS seal-unsealed-file: an archive file nobody sealed was rejected (archive/b.md: is in the archive but carries no seal — register it in archive/manifest.json; an archive is append-only, so nothing lands here unsealed)
  PASS seal-missing-file: a seal whose file no longer exists was rejected (archive/manifest.json sealed[0]: sealed file not found: archive/gone.md)
  PASS seal-drifted-file: a sealed file edited after sealing was rejected (archive/manifest.json sealed[0]: archive/a.md changed after it was sealed — recorded 8a6656423503…, found bc9f4a85d8f8…; an archived record is frozen: restore its bytes, or retire it and write a new record)
  PASS seal-header-mismatch: a seal whose date disagrees with the record it seals was rejected (archive/manifest.json sealed[0]: archive/a.md carries no 'Archived: 2026-02-02' line — the seal and the record it seals must name the same date)
  PASS seal-outside-patterns: a seal outside the scanned corpus was rejected (archive/manifest.json sealed[0]: .agents/notes/x.md matches none of ['archive/*'], so its seal is never verified)
  PASS seal-empty-archive: an archive with nothing sealed is accepted, and the unsealed-file probe keeps the guard live
  check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
  ```

- **manual** — read each skill's description: it must name when the skill loads, not what it contains

### context-rules

Always-loaded rules are a budget; they must stay short and well-formed.

- `AGENTS.md`

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


### docs

Documentation has one home per fact and a declared kind; a page whose kind or owner changed is a behaviour change for every reader and every agent that loads it. A claim you did not re-run is not a fact.

- `docs/check-catalog.md`

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

- **manual** — read the changed page as its reader: does it still say what a reader can do, and does its kind still match its content

### generated-docs

A generated page is a projection of its source. Hand-patching it creates a second fact that the next regeneration deletes, and a generator edit without a regeneration leaves the committed page stale.

- `docs/check-catalog.md`

- **PASS (exit 0)** — `python3 tools/gen-docs.py --check`

  ```
  gen-docs: docs/check-catalog.md is up to date (88 lines).
  ```

- **manual** — confirm the page was produced by the generator, never patched by hand
