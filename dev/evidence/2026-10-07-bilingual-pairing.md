# Pairing, layout and heading-language verification record — 2026-10-07

Every command below was run in this checkout and its output is pasted verbatim. The kit's `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **Layout**: five standing documents moved from the kit root into `docs/` with their `.zh.md` counterpart and `.i18n.yaml` record (15 files); `README` and `AGENTS.md` stay at the root.
2. **Heading language**: the Chinese side now translates its headings and table headers. Before: 168/168 headings and 21 table headers were English. After: 172/174 headings and all table headers are Chinese, and the two that remain are placeholder titles that are identifiers (`# Capability: `<key>``, `# Release <version>（<date>）`).
3. **Checks accept both spellings**: a `sections` entry may list the accepted spellings of one section, so `required-sections` and `criteria-traced` cover translated pages. 16 checks declare the Chinese spelling; `docs-policy`, `i18n-policy`, `evolution-policy`, and `testing-policy` now scan both sides.
4. **Fragments resolve per side**: `pair-docs.py --check` resolves every fragment with GitHub's slug rule. It found two links that were already broken before this change — the emoji cross-cutting headings slug to `#--documentation-cross-cutting` / `#--文档横切十一站`, not `#-documentation-cross-cutting` / `#-文档横切十一站`.

## `python3 tools/check-invariants.py --self-test`

```text
check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
exit=0
```

The two probes that prove the new rule in both directions:

```text
PASS required-sections-localized: a declared translated spelling satisfied its section
PASS required-sections-missing-alias: a section absent in every spelling was rejected (notes/decision.md: missing section '## Alternatives considered' or '## 曾考虑的替代方案')
```

## `python3 tools/check-invariants.py`, `gen-docs.py --check`, `pair-docs.py --check`

```text
real scan exit=0
gen-docs: docs/check-catalog.md is up to date (69 lines).
pair-docs: 25 pair(s) in scope, all complete and in step.
exit=0
```

## `python3 -m unittest discover -s tests` and `python3 tools/run-evidence.py --check`

```text
Ran 42 tests — OK
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

## Checks the kit gate deliberately does not make

Structural signature (heading depths, table shape, list kinds and counts), relative-link resolution, fragment resolution, and the archive seal:

```text
pairs=25 structural_mismatches=0
zh_headings=172/174 in Chinese
relative_links=374 broken=0
fragments=40 all resolve (enforced by pair-docs.py --check)
archive_sealed=9 digest_mismatches=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts` (from the repository root)

```text
verify-translation-pairing: 1160 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

Both host-governed records are byte-identical to the host renderer, including after the heading translation:

```text
MATCH  study/agent-workflow-kit/README.i18n.yaml with the host renderer
MATCH  study/agent-workflow-kit/docs/README.i18n.yaml with the host renderer
```

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
