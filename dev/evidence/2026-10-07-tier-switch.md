# Tier switch — verification record, 2026-10-07

Verdict: MANUAL — every command below was run by hand in this checkout and its output pasted verbatim, because run-evidence could not see this tree at the time.

## What landed

`tools/tiers.json` is the only tier switch: an ordered `tiers` ladder, `ladder` increments, a `stages` catalogue that names the paths each stage owns, a top-level default, and per-lifecycle overrides. `check-invariants.py` resolves it, skips the checks that own nothing but an absent stage's paths (withholding the empty-corpus rule), and runs the new `tier-manifest` check.

## The end-to-end control, on a real copy of the kit

Two runs on one copied tree. In both, `incident` was declared in the switch and `dev/postmortem/` was deleted first.

```text
A: `incident` declared `none`  → exit 0, 50 checks pass, 0 postmortem failures
B: same tree, switch reverted to `long-lived` → exit 1, exactly three failures:
   FAIL postmortem-record     no file matched ['dev/postmortem/*.md']: a check with no subject cannot fail
   FAIL postmortem-guardrail  no file matched ['dev/postmortem/*.md']: a check with no subject cannot fail
   FAIL tier-manifest         stage 'incident' is installed, but 'dev/postmortem/*.md' matches no file
```

B is the negative control for A: the green in A comes from the switch's declared absence rather than from checks quietly passing.

## Follow-up: the prose the switch replaced

The switch made two instructions wrong at once, and both are deleted. `dev/README.md`'s paragraph of eight "no directory → comment out these checks" mappings and the root `README.md`'s matching sentence now say one thing: declare the stage `none` in the switch. One instruction replaces nine, and it is the one the gate reads. Two records that stated the old rule as current state were corrected in place.

Two modelling gaps surfaced while doing it, and both are closed:

- `no-time-based-test-sync` matches tests wherever they live, so a single `tests/` path could not cover it. `home` is the set of paths a stage owns, and `tests` is a stage of its own; an installed stage must own a file somewhere across those paths, an absent one must own none of them.
- A fragment on a host-governed pair must be identical on both sides. The root README's link into the map carried `#adoption-tiers` while the Chinese side carried none, because that heading is translated there; both sides now link the page without the fragment.

## Corpus

```text
stages declared: 15 · tiers: 3 · lifecycles declared: 1
hand-mapping instructions left in the corpus (outside historical records): 0
relative links across the kit: 672, broken: 0
```

## The kit's own gates, and the control's two runs

### `python3 tools/check-invariants.py --self-test | tail -1`

```text
check-invariants: self-test PASSED — every check rejects an invalid fixture and accepts a valid one, a check with no subject is rejected, and every registration direction is covered
exit=0
```

### `python3 tools/check-invariants.py | grep -E "^(FAIL|check-invariants)" | tail -2`

```text

exit=0
```

### `python3 tools/pair-docs.py --check`

```text
pair-docs: 41 pair(s) in scope, all complete and in step.
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

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 64 tests in 0.092s

OK
exit=0
```

### `grep -c "^PASS" /tmp/a.txt`

```text
50
exit=0
```

### `grep -c "^FAIL" /tmp/b.txt`

```text
3
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1163 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```
