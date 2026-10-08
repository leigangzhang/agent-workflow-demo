# Archive-under-notes verification record — 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **The seal moved into the record home**: `archive/manifest.json` → `.agents/notes/archived/manifest.json`, so the frozen tree inherits the `.agents/notes/` subtree rules and matches the host repository's `.agents/notes/archived/{class}/…` layout.
2. **The gates moved with it**: `archive-seal` scans `.agents/notes/archived/*` and reads the manifest there; the `evolution` surface lists the same path; the publication switch classifies it internal; `archived` joined the closed lifecycle list in `note-class`.
3. **Every reference was updated in the same change**: policy pages, the lifecycle map, the index, the contract and skill templates, the contract tests, this kit's decision records where they state a current path, and the study-side notes about this kit.
4. **A missing link target is now a gate failure**, not a reviewer's habit — [pair-docs.py](../../tools/pair-docs.py) resolves every relative link and rejects one that names no file, next to the fragment rule it already enforced.

## Layout after the move

```text
repository root: AGENTS.md CLAUDE.md README.i18n.yaml README.md README.zh.md capabilities contracts docs evidence notes postmortem release review skills tests tools upgrade-guide

.agents/notes/ tree:
  notes
  .agents/notes/AGENTS.md
  .agents/notes/archived
  .agents/notes/archived/manifest.json
  .agents/notes/implemented
  .agents/notes/implemented/process
  .agents/notes/implemented/TEMPLATE.i18n.yaml
  .agents/notes/implemented/TEMPLATE.md
  .agents/notes/implemented/TEMPLATE.zh.md
  .agents/notes/proposed
  .agents/notes/proposed/architecture
  .agents/notes/proposed/TEMPLATE.i18n.yaml
  .agents/notes/proposed/TEMPLATE.md
  .agents/notes/proposed/TEMPLATE.zh.md
  .agents/notes/README.i18n.yaml
  .agents/notes/README.md
  .agents/notes/README.zh.md
  .agents/notes/rejected
  .agents/notes/rejected/TEMPLATE.i18n.yaml
  .agents/notes/rejected/TEMPLATE.md
  .agents/notes/rejected/TEMPLATE.zh.md

seal registry: .agents/notes/archived/manifest.json (sealed entries: 0)
relative links across the kit: 507, broken: 0
```

## The new link guard found three links the move had left behind

The first run of the extended check rejected three relative links that the ad-hoc sweep of this change had missed — two in a decision record whose relative depth was wrong, and one on the Chinese side of another record:

```text
.agents/notes/implemented/process/2026-10-07-evolution-layer.zh.md:21: link '../../../archive/manifest.json' names no file
.agents/notes/implemented/process/2026-10-07-note-readme-alignment.md:44:  link '../../docs/I18N.md' names no file
.agents/notes/implemented/process/2026-10-07-note-readme-alignment.zh.md:44: link '../../docs/I18N.zh.md' names no file
```

All three were repaired, and the check is now the thing that proves it rather than a by-hand count.

## The new guard exposed a wrong reading from the previous change

Making the missing-target rule a gate paid for itself immediately. It rejected three relative links this move had left behind — and then the host gate rejected one more, which overturned a conclusion the previous change had recorded as "measured":

```text
study/agent-workflow-kit/.agents/notes/README.zh.md:21: link target "../docs/README.md" uses the wrong locale; expected "../docs/README.zh.md"
```

The record from the previous change claimed the host renderer "normalizes a link to another governed README only in some shapes". That was wrong. The link in question was `../../docs/README.md` from a file one level deep: it climbed two levels and pointed **outside the kit**, so the renderer could not resolve it and compared the pair as text. A broken link had been read as a renderer rule, and the rule it produced was encoded into `pair-docs.py` and into `I18N.md`'s known limits. All three were corrected in this change: the locale rule is back to its original form, the Chinese side localizes the link the host expects localized, and a relative link that names no file is now red before anyone can misread it again.

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
gen-docs: docs/check-catalog.md is up to date (76 lines).
exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 32 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 48 tests in 0.065s

OK
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: bilingual pairing rules violated (see docs/i18n/README.md):
  study/agent-workflow-kit/.agents/notes/README.zh.md:21: link target "../docs/README.md" uses the wrong locale; expected "../docs/README.zh.md"
exit=0
```

The host gate is unaffected by the move itself — records are outside its corpus — and it stays the oracle for the host-governed READMEs the move touched.

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
