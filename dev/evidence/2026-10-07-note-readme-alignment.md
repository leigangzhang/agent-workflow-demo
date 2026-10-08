# Record-README alignment verification record — 2026-10-07

Every command below was run in this checkout and its output is pasted verbatim. `run-evidence.py --base` cannot see this tree — `study/` is untracked in its host repository — git reports one `?? study/` entry, and its `.gitignore` line for the tree is commented out — so the git-based tools see the directory, not the files — so this record carries the run instead of a generated `evidence/<date>-<branch>.md`.

## What this record covers

1. **Section parity with the host**: the record README carries the host Agent Note README's headings, in the host's order, in both languages — with one kit-specific trailing section (`## Where to look`) and the kit's own title (`# Decision records`).
2. **The rules the host states are stated here**: layout and naming, classification, archiving and deletion, when to write one, and the file format (header block, body skeleton, the alternatives mandate, moving between lifecycles, Chinese counterparts).
3. **A wrong reading of the host gate was found and corrected later.** The gate went red on this pair's `docs/README` link and the first fix used the authored path; the real cause was that the link climbed two levels out of `notes/` and pointed outside the kit, so the host compared it as text. The follow-up change made `pair-docs.py --check` reject a relative link that names no file, and the link follows the locale again.
4. **Budgets followed the content**: the record README got its own ceiling; `guide-budget` now covers only the tools reference and the extension tutorial.

## Section parity measured, not asserted

```text
host en headings (fenced examples excluded): 11; kit en headings: 12
shared with the host (en): 10/12
  ## Layout and naming
  ## Classification
  ## Archiving and deletion
  ## When to write one
  ## The file format
  ### The header block
  ### The body skeleton
  ### Alternatives considered — mandatory
  ### Moving between lifecycles
  ### Chinese counterparts
kit-only (en): ['# Decision records', '## Where to look']

shared with the host (zh): 10/12
  ## 布局与命名
  ## 分类
  ## 归档与删除
  ## 何时需要写一份
  ## 文件格式
  ### 头部块
  ### 正文骨架
  ### 曾考虑的替代方案——必需
  ### 在生命周期之间移动
  ### 中文对侧文件
kit-only (zh): ['# 决策记录', '## 去哪看']
```

## The kit's own gates

### `python3 tools/check-invariants.py --self-test | tail -3`

```text
PASS seal-outside-patterns: a seal outside the scanned corpus was rejected (archive/manifest.json sealed[0]: notes/x.md matches none of ['archive/*'], so its seal is never verified)
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
pair-docs: 31 pair(s) in scope, all complete and in step.
exit=0
```

### `python3 tools/run-evidence.py --check`

```text
run-evidence: every declared runnable command resolves (18 surface(s))
exit=0
```

### `python3 -m unittest discover -s tests 2>&1 | tail -3`

```text
Ran 46 tests in 0.064s

OK
exit=0
```

## Host repository: `npx tsx scripts/verify-translation-pairing.ts`

```text
verify-translation-pairing: 1162 pair(s) checked across all in-scope documentation, all consistent.
exit=0
```

This gate went red on the pair, and the reading recorded here at the time — "the renderer does not normalize that link shape" — was wrong. The link was `../../docs/README.md` from a file one level deep, so it resolved outside the kit, and an unresolvable target is compared as text. The probe below shows what the renderer did with the broken path; the follow-up change replaced the inference with a guard that rejects any relative link naming no file:

```text
study/agent-workflow-kit/notes/README.md    link #1  "../../docs/README.md"       (raw, not normalized)
study/agent-workflow-kit/docs/README.zh.md  link #1  dsh-translation-target:...   (resolvable target, so the localized path is normalized — the shape was never the problem)
```

> **Corrected 2026-10-07.** This paragraph said `study/` was git-ignored. The host's `.gitignore` line for the tree (`# study/`) was commented out on 2026-10-07, after this record was written, so the wording no longer matches the file; the tree is untracked and stays untracked by choice, which leaves this record's effect unchanged — `run-evidence.py --base` still cannot enumerate these files. The earlier blame in this note (that the claim came from misreading [tools/README.md](../../tools/README.md)) was wrong and is withdrawn: the ignore rule was active when the sentence was written.
