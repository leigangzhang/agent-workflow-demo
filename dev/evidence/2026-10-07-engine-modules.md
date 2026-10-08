# The engine and the suite, split by subject — verification record, 2026-10-07

## What changed

`tools/check-invariants.py` went from 1637 lines to a 95-line entry (its manual, then the engine call), and the engine became the package `tools/kitcheck/`. The suite went from one 669-line file to `harness.py` plus five subject modules holding the same fourteen classes.

## Imports resolve statically

The first version of the split left imports that only worked because Python puts directories on `sys.path`: `import kitcheck` in the suite, `from harness import …` in the modules, `from kitcheck.cli import main` in the entry. Editors cannot resolve those, and the report that opened this check named exactly that.

The fix keeps the commands identical and removes the ambiguity: the suite is a package, its modules import `tests.harness`, and the suite and the entry load the engine **by path**, the way every hyphen-named tool in `tools/` is already loaded. The probe below is the check that it stayed fixed.

```text
cross-root plain imports left in the tree: 0
```

## The shape after the split

```text
107 tools/check-invariants.py
        15 tools/kitcheck/__init__.py
       162 tools/kitcheck/capabilities.py
        47 tools/kitcheck/cli.py
       112 tools/kitcheck/core.py
       209 tools/kitcheck/mirrors.py
       122 tools/kitcheck/policies.py
       431 tools/kitcheck/records.py
       360 tools/kitcheck/registry.py
        63 tools/kitcheck/skills.py
       156 tools/kitcheck/tiers.py
         1 tests/__init__.py
        59 tests/harness.py
        77 tests/test_evidence.py
       184 tests/test_pairing.py
       126 tests/test_policies.py
       189 tests/test_records.py
        75 tests/test_tiers.py
      2495 total
```

## Two manifests and one path followed the code

- `dev/contracts/mirrors.json`: `source` → `tools/kitcheck/core.py`, where `SUPPORTED_KINDS` and its `# region: supported-kinds` markers now live.
- `dev/capabilities/registry.json`: `providers` → `tools/kitcheck/registry.py`, where the `# capability: check-engine` marker now lives.
- `DEFAULT_CONFIG` resolved to `Path(__file__).parent / "workflow.json"`, which inside the package would have meant `tools/kitcheck/workflow.json`; it now resolves to `tools/workflow.json`.

## The kit's own gates

### `python3 -m unittest discover -s tests 2>&1 | tail -2`

```text
OK
exit=0
```

### `python3 tools/check-invariants.py --self-test | tail -1`

```text
check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
exit=0
```

### `python3 tools/check-invariants.py | grep -c "^PASS"`

```text
50
exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 42 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/gen-docs.py --check`

```text
gen-docs: docs/check-catalog.md is up to date (85 lines).
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1163 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

## What did not move

Every documented command is the same string, and the verdicts are identical: 50 declared checks, 64 tests, the same fixtures producing the same failures. Like every other command in this kit, both are run from the repository root — running them from elsewhere fails the same way `tools/check-invariants.py` already did, because every path in the configuration is relative to the root.


## Second level: the record guards, split by subject

`records.py` held four subjects in 432 lines, so the four moved apart: publication (102), seals (171), and criteria (125) are modules of their own, the note-class guard stays in `records.py` (58), and `read_manifest` moved to `core` (132) because two modules read a manifest. The engine is now thirteen modules, none over 366 lines.

```text
107 tools/check-invariants.py
        19 tools/kitcheck/__init__.py
       162 tools/kitcheck/capabilities.py
        47 tools/kitcheck/cli.py
       132 tools/kitcheck/core.py
       125 tools/kitcheck/criteria.py
       209 tools/kitcheck/mirrors.py
       122 tools/kitcheck/policies.py
       102 tools/kitcheck/publication.py
        58 tools/kitcheck/records.py
       366 tools/kitcheck/registry.py
       171 tools/kitcheck/seals.py
        63 tools/kitcheck/skills.py
       156 tools/kitcheck/tiers.py
         1 tests/__init__.py
        59 tests/harness.py
        77 tests/test_evidence.py
       184 tests/test_pairing.py
       126 tests/test_policies.py
       189 tests/test_records.py
        75 tests/test_tiers.py
      2550 total
```

## The layout rules, written where a contributor looks

```text
tools/AGENTS.md    one module per subject; the module-aware four-place change
tests/AGENTS.md    new: harness + one module per subject, the corpus-test rule,
                   load-a-tool-by-path, and run-from-the-root
tools/README.md    what each module owns
docs/testing.md    the Unit row names the layout
```


## The gate that should have caught the switcher damage

Repairing links across the moved tree with a string replace hit the language switcher in 23 pairs, pointing each Chinese side at itself. The host renderer caught one of them — it governs the READMEs only — and this kit's pairing gate caught none, because it verified that a switcher exists and that its target exists, never that the target is the counterpart. The data is repaired, the gate now checks the target, and three cases in `SwitcherTargets` prove it can fail.

```text
cross-root plain imports left in the tree: 0
language switchers pointing at their own side: 0
engine modules: 13, none over 366 lines
suite modules: 7 (harness + one per subject)
```


## tools/README: the inventory became a layout

The module inventory this change first put in `tools/README.md` was a file-level list, which is the kit's own slop-checklist item — a hand-restated inventory that drifts the moment a guard moves. It is now a directory-level layout block: the five scripts, the engine package as one entry, and the two data files, with the per-module rule left where it belongs, in `tools/AGENTS.md`. The pair's fenced block is byte-identical on both sides, which is what the pairing gate compares.


## Directory-structure sections, and a README for tests

Both directories now state their own layout under a heading of its own: [tools/README.md](../../tools/README.md) and [tests/README.md](../../tests/README.md), each with a Chinese side whose descriptions are Chinese. They are tables, not fenced blocks, and that is not a style choice: the host renderer compares fenced blocks byte for byte across a pair, so a code block cannot carry Chinese annotations — a table mirrors in shape and translates in content, which is what the request actually needed.

`tests/` had no README, so one was created with its `.i18n.yaml` record, classified `public` in the publication switch, added to `pairing.hostCanonical` (the host governs it now), enumerated in `agent-inputs`, and linked from the index. The host gate's corpus grew from 1163 to 1164 pairs.

Two gates caught mistakes in the making, which is the point of having them: `guide-budget` red at 924 of 900 words, so the table was condensed to 898 rather than the ceiling raised; and the pairing gate rejected the new Chinese side for localizing a link inside a file that is now host-governed, where the authored path is the rule.


## Every file, at the granularity that fits each directory

`tools/` now carries a second section, `## The engine's modules`: thirteen rows, one per module of `kitcheck/`, each line taken from that module's own docstring. The directory table's row for the package points at that section rather than restating it, so the same fact still has one home. `tests/` needed no second section — it is flat — so its table simply gained `__init__.py`, which is what makes the modules import by name.

`guide-budget` is shared by `tools/README.md` and `docs/extending.md`, so the new table pushed the pair over it twice: the cells were condensed twice, to 1078 words, and the ceiling moved 900 → 1120 with the reason recorded in the check. That is the kit's own order — relocate, condense, then raise — and the raise is the part that had to be justified rather than assumed.
