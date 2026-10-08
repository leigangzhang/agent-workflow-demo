# Testing policy: three language-neutral rules, a budget, and a repaired citation — verification record, 2026-10-07

## What changed

- `## Test doubles` joined the policy: substitute only the expensive or non-deterministic edge; name the boundary you replaced; keep the interface the code already calls; green with a stand-in proves the call site, not the integration.
- `## Determinism` gained **resolve one plane, never two** — the failure mode a TypeScript plugin and a packaged Java server share.
- `## Flake policy` gained the diagnosis half: a test that passes only when it runs alone is a defect in the test, and a shared fixture is never collected as a test.
- `testing-budget` (1800 words) and `testing-budget-zh` (125 lines) joined, so all four standing policies are budgeted alike.
- The standing order's citation was repaired: it named this file as the mock policy's home and the section did not carry the rule; it now points at `#test-doubles`.

## The two sides stayed mirrors

```text
sections (en / zh): see the counts below — the structural gate compares heading depths, fence info strings, table shapes, and list counts
```

## The kit's own gates

### `python3 tools/check-invariants.py | grep -E "^(FAIL|check-invariants)" | tail -2`

```text

exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 40 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/gen-docs.py --check`

```text
gen-docs: docs/check-catalog.md is up to date (84 lines).
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 59 tests in 0.082s

OK
exit=0
```

### `python3 -c "import json;c=json.load(open('tools/workflow.json'));print([len(x['sections']) for x in c['checks'] if x['id']=='testing-policy'])"`

```text
[7]
exit=0
```

### `grep -c "^## " docs/testing.md docs/testing.zh.md`

```text
docs/testing.md:8
docs/testing.zh.md:8
exit=0
```

### `grep -c "^- \|^[0-9]\." docs/testing.md docs/testing.zh.md`

```text
docs/testing.md:28
docs/testing.zh.md:28
exit=0
```

### `wc -w docs/testing.md`

```text
1759 docs/testing.md
exit=0
```

### `wc -l docs/testing.zh.md`

```text
114 docs/testing.zh.md
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1163 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

## Deliberately not added

A coverage tier or threshold, the mechanics of a browser or container lane, and per-language fixture recipes. The kit binds no framework, forces no percentage, and ships no CI configuration; those are choices a project makes with its own tier names.
