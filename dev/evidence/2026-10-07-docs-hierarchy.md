# Documentation-hierarchy verification record — 2026-10-07

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **One home per level**: the root README shrank from 322 lines to 85 and now only installs and routes; `AGENTS.md` is the only command list; `CLAUDE.md` symlinks `AGENTS.md`.
2. **Each home states its own rules**: new paired pages `tools/README.md`, `notes/README.md`, `docs/extending.md`, and subtree rule files `notes/AGENTS.md` and `tools/AGENTS.md`.
3. **One file listing**: `docs/README.md` routes every question and carries the only "home → what it owns" table.
4. **Limits with their owner**: the twenty gate limits moved out of the README into the tools page, `DOCS.md`, `TESTING.md`, and `EVOLUTION.md`; `I18N.md` already owned its own.
5. **No unsealed drop**: `archive/AGENTS.md` was written and removed once `archive-seal` proved that nothing lands under `archive/` unsealed.

## The kit's own gates

### `python3 tools/check-invariants.py --self-test`

```text
PASS budget: the invalid fixture was rejected (AGENTS.md: 4 lines, budget is 2), the valid one was accepted
PASS required-sections: the invalid fixture was rejected (notes/decision.md: section '## Alternatives considered' has an empty body (needs 1 non-blank line(s))), the valid one was accepted
PASS forbidden-regex: the invalid fixture was rejected (leak.txt:1: matches forbidden pattern 'BEGIN-FAKE-SECRET'), the valid one was accepted
PASS source-mirror: the invalid fixture was rejected (contracts/mirrors.json mirrors[0]: contracts/a.md does not match src/a.py between markers — first difference at line 1: doc 'keep = 1' != source 'keep = 2'), the valid one was accepted
PASS capability-registry: the invalid fixture was rejected (capabilities/registry.json capabilities[0] engine: a seam needs at least one provider), the valid one was accepted
PASS criteria-traced: the invalid fixture was rejected (notes/implemented/TEMPLATE.md: criterion A1 names no declared check or surface — cite one of ['budget', 'source'] in backticks), the valid one was accepted
PASS skill-trigger: the invalid fixture was rejected (skills/a/SKILL.md: description must open with when the skill loads ('Use when' / 'Use before' / 'Use after' / 'Use during'), not a summary: 'Summarizes the testing policy.'), the valid one was accepted
PASS publish-manifest: the invalid fixture was rejected (docs/b.md: matches no declared pattern — classify it public or internal in docs/publish.json), the valid one was accepted
PASS sealed-manifest: the invalid fixture was rejected (archive/manifest.json sealed[0]: archive/a.md changed after it was sealed — recorded 000000000000…, found 8a6656423503…; an archived record is frozen: restore its bytes, or retire it and write a new record), the valid one was accepted
PASS kind-coverage: all 9 kinds have a runner and a negative-control case
PASS empty-corpus: a check matching no file was rejected (no file matched ['AGENTS.md']: a check with no subject cannot fail)
PASS required-sections-localized: a declared translated spelling satisfied its section
PASS required-sections-missing-alias: a section absent in every spelling was rejected (notes/decision.md: missing section '## Alternatives considered' or '## 曾考虑的替代方案')
PASS source-mirror-markers: a missing source region marker was rejected (contracts/mirrors.json mirrors[0]: begin marker '# begin: a' matches 0 line(s) in src/a.py)
PASS source-mirror-orphan: an unregistered block was rejected (contracts/a.md: 1 block(s) with info 'text mirror' have no mirror entry in contracts/mirrors.json — register the block or remove it)
PASS capability-registry-discovery: an unclassified capability was rejected ('unregistered' is declared by a marker but missing from capabilities/registry.json — classify it)
PASS criteria-no-id: an untraced criterion was rejected (notes/implemented/TEMPLATE.md: criterion in '## Testing' has no id: '- the feature works as intended.')
PASS criteria-unknown-owner: a criterion naming an undeclared owner was rejected (notes/implemented/TEMPLATE.md: criterion A1 names no declared check or surface — cite one of ['budget', 'source'] in backticks)
PASS criteria-empty-section: a section with no criterion bullets was rejected (notes/implemented/TEMPLATE.md: '## Testing' carries no criterion bullets to trace)
PASS budget-words: a file over its word ceiling was rejected (NOTE.md: 40 words, budget is 10)
PASS publish-stale-public: a public entry with no file behind it was rejected (docs/publish.json: public pattern 'docs/gone.md' matches no file — a published promise with nothing behind it is a broken link)
PASS publish-public-glob: a public entry that publishes a whole directory was rejected (docs/publish.json public[0] 'docs/*.md': publication is a per-file promise — name the file, do not publish a directory)
PASS publish-ambiguous: one file matched by both classes was rejected (docs/a.md: matches 2 declared patterns ('docs/a.md' (public), 'docs/*.md' (internal)) — a file has exactly one class)
PASS publish-no-reason: an internal entry with no reason was rejected (docs/publish.json internal[0] 'docs/b.md': missing 'reason' — say why this file stays in the repository)
PASS seal-unsealed-file: an archive file nobody sealed was rejected (archive/b.md: is in the archive but carries no seal — register it in archive/manifest.json; an archive is append-only, so nothing lands here unsealed)
PASS seal-missing-file: a seal whose file no longer exists was rejected (archive/manifest.json sealed[0]: sealed file not found: archive/gone.md)
PASS seal-drifted-file: a sealed file edited after sealing was rejected (archive/manifest.json sealed[0]: archive/a.md changed after it was sealed — recorded 8a6656423503…, found bc9f4a85d8f8…; an archived record is frozen: restore its bytes, or retire it and write a new record)
PASS seal-header-mismatch: a seal whose date disagrees with the record it seals was rejected (archive/manifest.json sealed[0]: archive/a.md carries no 'Archived: 2026-02-02' line — the seal and the record it seals must name the same date)
PASS seal-outside-patterns: a seal outside the scanned corpus was rejected (archive/manifest.json sealed[0]: notes/x.md matches none of ['archive/*'], so its seal is never verified)
PASS seal-empty-archive: an archive with nothing sealed is accepted, and the unsealed-file probe keeps the guard live
check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
exit=0
```

### `python3 tools/check-invariants.py`

```text

exit=0
```

### `python3 tools/gen-docs.py --check`

```text
gen-docs: docs/check-catalog.md is up to date (73 lines).
exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 29 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 42 tests in 0.051s

OK
exit=0
```

## Structural checks the kit gate deliberately does not make

Heading depths, table shape, list kinds and counts, relative-link resolution, fragment resolution, and the Chinese-side heading census:

```text
pairs=29 structural_mismatches=0
zh_headings=187/189 in Chinese (the two exceptions are placeholder titles: `# Capability: `<key>`` and `# Release <version>（<date>）`)
relative_links=489 broken=0
fragments=every fragment resolves (enforced by pair-docs.py --check)
archive_sealed=0 (nothing has been retired yet; the empty-seal behaviour is covered by --self-test)
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1162 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

The host corpus grew from 1160 to 1162 pairs in this change: a `README.md` outside a dot-directory is discovered by the host's pairing manifest, so the kit's two new home READMEs (`notes/README.md`, `tools/README.md`) are now host-governed. Both render byte-identically through the host renderer, which is why they were added to the kit's `pairing.hostCanonical` list in the same change.

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
