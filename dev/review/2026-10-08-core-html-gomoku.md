# Review: the two-player Gomoku page, and the two gates it exposed (2026-10-08)

English | [中文](2026-10-08-core-html-gomoku.zh.md)

## Status

Both defects this review found are fixed in `dsh-router-preset` at commit `559558a`, and the review's own failing observations were re-run against that build: the two that reported a false pass now report the declared policy, and the one that reported an `invalid output` error now returns a valid success. The finding about this repository's brief was correct and the brief has been corrected. One finding is accepted as a limit rather than fixed; the last one — how an evidence record is named — was settled in the kit by a later session, and its **Status** below says so.

A later session wrote the fixes and this section. The review below is kept as it was written, including the observations that were true of the build it ran; where a later observation changes what a finding means, that is said in **Status** under the finding rather than by editing the finding.

## Claim

`src/gomoku/rules.js`, `src/gomoku/rules.test.js`, and `src/gomoku/index.html` deliver a two-player Gomoku page that opens from `file://` and plays to a win, and the two gate defects that delivery hit are fixed where they live: `tools/pair-docs.py` here, and the delivery gate in the shared `dsh-router-preset`.

## Evidence

This session wrote `src/gomoku/*`, so this is a same-source review and cannot supply the independence station 7 asks for. What it can do is re-run the observations the fix carries and read their outputs, which is what the entries below are. The gate entries were re-run after the web profile restart.

**The delivery gate (`~/dsh-playgroud/tools/dsh-router-preset`, live after the restart).**

- `node --test tests/delivery-gate.test.mjs` → `# tests 19`, `# pass 19`, `# fail 0`; `node scripts/patch-bootstrap.mjs --check` → `patch-bootstrap.mjs: --check: all patches applied`; `node .agent-presets/router-standard/router-bootstrap-v34.selftest.mjs` (run from `/Users/ray/dsh-playgroud/.router-preset-probe`) → `SELFTEST PASS`.
- `dev_visual_check(…, workspace=/Users/ray/Workspace/agent-workflow-demo)` on the two distinct screenshots → `Error: tool "dev_visual_check" returned invalid output: "value.proof" is not a declared property (additionalProperties: false)`, and `.dsh/visual-proof.json` is written anyway.
- `.dsh/visual-proof.json` now reads `"provider": "deepseek-official"`, `"model": "deepseek-flash"`, `"match": true`, with the two `760x880` fingerprints distinct. It no longer names the fixture provider the brief's probe left behind.
- `delivery_check(file=…/src/gomoku/index.html, url=file:///…/src/gomoku/index.html, evidence=<page reviewed + both screenshots reviewed>)` with no `workspace` → `[PASS] page-verify: 2 screenshot(s), 760x880/760x880, fingerprints distinct; visual read not required by tools/workflow.json (delivery.page.visual is not true)`, while reading the same file back prints `delivery.page.visual = True`.
- The same call with `.dsh/visual-proof.json` deleted → still `[PASS]`, carrying the same `not true` detail, so the declared layer was never consulted.
- The same call with `workspace=/Users/ray/Workspace/agent-workflow-demo` and the proof present → `[PASS] page-verify: … read by deepseek-official/deepseek-flash: 第一张截图：顶部标题「五子棋」，其下状态文字「黑方落子」…`.
- The same call with `workspace` named and the proof deleted → `[FAIL] page-verify: … tools/workflow.json requires a visual read (delivery.page.visual) but no proof is at .dsh/visual-proof.json — run dev_visual_check on these screenshots`.
- `dev_visual_check(…)` with one screenshot copied over the other → `visual-check: FAIL ❌ … 1 fingerprint(s) repeat: two claimed states are the same picture`.

**The gate re-run against the fixed build (`559558a`), from a working directory that is not the project.**

- `node --test tests/delivery-gate.test.mjs` → `# tests 23`, `# pass 23`, `# fail 0`; `node scripts/patch-bootstrap.mjs --check` → `patch-bootstrap.mjs: --check: all patches applied`; `node scripts/gen.mjs --check` → `gen.mjs: cordis.patch.yml is up to date`.
- `delivery_check(file=…/src/gomoku/index.html, url=file:///…, evidence=<page reviewed + both screenshots reviewed>)` with **no** `workspace`, run with `cwd=/private/tmp`, and the proof present → `[PASS] page-verify: 2 screenshot(s), 760x880/760x880, fingerprints distinct; read by deepseek-official/deepseek-flash: Screenshot 1: title 「五子棋」, status line 「黑方落子」, a 15×15 grid board with no stones…` — the declared layer is reached and the proof is audited without the caller naming anything.
- The same call with `.dsh/visual-proof.json` renamed away first → `[FAIL] page-verify: … tools/workflow.json requires a visual read (delivery.page.visual) but no proof is at .dsh/visual-proof.json — run dev_visual_check on these screenshots`. The proof is restored afterwards, and `.dsh/` holds no leftover.
- `dev_visual_check` returning successfully now validates against the schema the tool declares: the lane's `a successful dev_visual_check return validates against the schema the tool declares` passes the declared shape and reds on a return carrying one undeclared property.
- Four mutations were watched red and restored in that lane: the ancestor walk, the workspace fallback chain, the declared `proof` property, and the proof-equality check.

**The `pair-docs` fix (this repository).**

- `python3 tools/pair-docs.py --write .agents/notes/implemented/feature/2026-10-08-core-html-gomoku.md` → `pair-docs: wrote .agents/notes/implemented/feature/2026-10-08-core-html-gomoku.i18n.yaml`, exit 0. The same command was refused as `not an in-scope pair` before the fix.
- `python3 -m unittest tests.test_pairing.ANamedPathKeepsItsOwnPrefix -v` → `Ran 5 tests in 0.059s`, `OK`.
- Reverse control run by this session: with `select_anchors` mutated back to `item.lstrip("./")`, the same suite reports `FAILED (errors=2)` and the named write exits 1 with `pair-docs: agents/notes/implemented/feature/2026-10-08-core-html-gomoku.md is not an in-scope pair (see pairing in tools/workflow.json)`. Restoring the file returns `OK`.

**The delivered page and engine.**

- `node --test src/gomoku/rules.test.js` → `# tests 13`, `# pass 13`, `# fail 0`.
- `node -e '<five lines played along row 14, column 14, row 0, and the two corner diagonals>'` → `"winner":"black"` for all five, `moves: 9` each, so the run walk handles the board boundary.
- `node --test src/gomoku/rules.test.js` with `isPoint`'s column bound mutated to `col <= size` → `# pass 12`, `# fail 1`: the out-of-range case goes red, so the bound is pinned rather than assumed.
- `git status --porcelain` and `git diff --stat` → 17 tracked paths changed, `125 insertions(+), 178 deletions(-)`, plus the untracked `src/`, the two `dev/evidence/*.png`, and the new record triplet.
- `python3 tools/change-scope.py --base origin/main --strict` → `Every changed path matches a declared surface.`
- `python3 tools/check-invariants.py --self-test` → `self-test PASSED`; `python3 tools/check-invariants.py` → exit 0; `python3 tools/pair-docs.py --check` → `24 pair(s) in scope, all complete and in step`; `python3 tools/gen-docs.py --check` → `up to date (88 lines)`; `python3 -m unittest discover -s tests` → `Ran 76 tests`, `OK (skipped=2)`.
- The deletion this brief names: `git ls-files dev/evidence/` lists no `2026-10-08-i18n-decisions-prose-and-more-5.md`, `git status --porcelain` carries no deletion for it, and the only committed `-5` in history is `dev/evidence/2026-10-08-main-5.md`, which `0533bde` renamed to `…-i18n-decisions-prose-and-more-4.md` — a path that is still tracked.
- Teardown: the loopback server started for the smoke was stopped; `curl` against its port now fails and no listener is left behind.

## Findings

- **Blocker** — a project's declared visual policy is silently skipped when `delivery_check` is called without `workspace`. Location: `router-bootstrap-v34.mjs:457-475`, where `readDeliveryPolicy` reads `<root>/tools/workflow.json`, with the root supplied by `workspaceOf` (`:430-443`), which falls back to the session header's `cwd`. Impact: for a project whose file says `delivery.page.visual: true`, the gate prints the opposite, passes `page-verify` on the universal layer alone, and never audits the proof — so a page can be delivered with no visual read at all, and the sentence it prints as the reason is false. Evidence: the two no-`workspace` PASS calls above, one of them with the proof deleted, beside `delivery.page.visual = True` read back from the file; naming `workspace` moves the same call into the declared layer, which then fails without the proof and passes with it.
  **Status — fixed**, `559558a`. Resolution is now explicit `workspace` → the session header's `cwd` → the project root found by walking up from the deliverable itself, and `workspaceOf` ends at that root so relative screenshot targets resolve too. The proof writer and the proof reader share one anchor. Re-run with no `workspace` and an unrelated `cwd`: the declared layer is reached (see Evidence). The reviewer's diagnosis was right about the symptom and narrower than the cause: the reader tried only the deliverable's immediate parent, so it never reached the repository root, and the `cwd` fallback it named was the second-order hazard rather than the mechanism.
- **Suggestion** — `dev_visual_check` cannot return a success under a declared policy. Location: `router-bootstrap-v34.mjs:1243-1245` declares an output schema of `{ ok, lines }` with `additionalProperties: false`, while the success return at `:681` is `{ ok: true, proof, lines }`. Impact: every successful call reaches the agent as `Error: … invalid output`, so an agent that reads the error as a failed check re-runs it or reports a false negative, and the tool's own PASS lines are never rendered. Evidence: the same error on two successive successful calls, while the proof file's contents advanced anyway.
  **Status — fixed**, `559558a`. `proof` is declared in the output schema of both registrations, and the lane now validates a successful return against the schema the tool declares. The reviewer's reading of the impact was exact: a tool that succeeds while the host reports a schema error costs the agent a retry and hides its own PASS lines.
- **Suggestion** — the visual audit trusts fingerprints and the `match` flag, never who produced them. Location: `verifyDeclaredVisual` (`:535-560`) and the proof file it audits. Impact: the policy asks for an independent model read and the gate cannot tell one from a stand-in, and because the proof lives in a gitignored directory no check in this repository can see it. Evidence: the proof's own `provider`/`model` fields, which this session watched change from `fixture` to `deepseek-official` with no gate outcome tied to either.
  **Status — accepted as a limit, not fixed.** Verifying who produced a proof needs an issuing authority this gate does not have, and adding one would turn a delivery check into an identity system. The limit is now stated where the gate is documented (`dsh-router-preset/delivery-gate.NOTES.md`), and the proof's `provider`/`model` fields stay readable for whoever audits it. The part of the finding that said the fingerprint requirement is too weak was the reason the requirement exists: the reference to `fixture` in the earlier proof is exactly what the equality check is meant to make visible, and it does not by itself make a wrong read a passing one.
- **Suggestion** — the brief's deletion premise is not this worktree's fact. Location: `dev/evidence/`. Impact: a reviewer told to handle "the deletion of `…-more-5.md`" looks for a tracked-path deletion that git does not have, and may record a change that is not there. Evidence: `git ls-files dev/evidence/` has no such path, `git status --porcelain` has no ` D` for it, and the only committed `-5` was renamed away by `0533bde`.
  **Status — confirmed, and the brief was corrected** rather than the finding. The premise came from a session log line (`rm -f …`) read without checking git, and the reviewer's three checks were the right ones. The `AGENTS.md` rule the fix added still governs committed paths; this file was never one.
- **Suggestion** — evidence records carry a `-N` successor suffix and are also renamed for the surfaces they cover, so the numbers no longer form one sequence. Location: `tools/run-evidence.py`'s `unique_record_path` against the naming rule. Impact: a committed `main-5.md` became `…-more-4.md` while an unrelated `…-more-5.md` existed untracked at the same time, and that suffix has since been taken again by a fresh run — which is how a reader comes to mistake a successor for a tracked deletion. Evidence: the rename in `0533bde`, the untracked `-6` this session wrote earlier, and the reused `-5` it wrote last.
  **Status — fixed in the kit** (`agent-workflow-kit`), in the record `2026-10-08-gates-a-run-names-its-record.md` that this finding asked for: the name carries the surfaces the run covered and the run's own UTC time, and the first-free `-<n>` survives only for two runs inside one second, so a deletion can no longer hand a name to a different claim. `tools/run-evidence.py` and `tests/test_evidence.py` are synced here byte for byte, and with the old rule restored both new cases fail.

No defect was found in the delivered engine or page under the classes that need a running system: the four edges and the two corner diagonals all win, the column bound fails a mutation, the draw and purity cases pass, and the smoke's server was torn down. Once the declared layer is reached, the vision route recognises the shipped page in both states.

## Follow-up

- **Became a rule** — `AGENTS.md` `## Closing the gate`, which this fix adds in seven rules: a flag that gets a red gate through is a gate defect, a check that cannot pass is not a check to satisfy, two failed shapes bound the retries, a turn ending red must say so, a criterion whose check cannot go red is a wish, a deletion of a committed path is a change, and a shared gate owns the mechanism while the project owns the policy. The reasoning and the rejected routes are in [the record that carries them](../../.agents/notes/implemented/process/2026-10-08-gates-a-check-must-be-able-to-pass.md).
- **Became a check, upstream** — the universal layer and the three-state decision are pinned by `tests/delivery-gate.test.mjs` in `dsh-router-preset`, which this review re-ran. It is not a check in this repository's `tools/workflow.json`, because the gate lives in the shared bundle and its project-level half reads `delivery.page.visual` from this file.
- **Became a check, here** — `tools/pair-docs.py`'s `select_anchors` and `tests/test_pairing.py`'s `ANamedPathKeepsItsOwnPrefix`, which this review watched fail under the pre-fix mutation and pass without it.
- **Became a check, upstream** — the workspace fallback, done in `559558a`: `the policy is found from the deliverable path, not from the host working directory`, `a declared project still requires the proof when no workspace is named`, and `the proof dev_visual_check writes is the proof the gate finds without a workspace`. The proposed negative is the second of those three.
- **Became a check, upstream** — the `dev_visual_check` output schema, done in `559558a`: `proof` is declared, and `a successful dev_visual_check return validates against the schema the tool declares` both passes the declared shape and reds on an extra property.
- **Deliberately nothing** — the deletion itself and the numbering collision. The `-5` record was never committed, so it claims no surface and has no inbound link to repair; the new rule binds committed paths, and a manifest over `dev/evidence/` would cost more than it catches for run output nobody reads.
- **Deliberately nothing** — an edge-win case in `src/gomoku/rules.test.js`. The boundary is already pinned by the out-of-range case, which the `col <= size` mutation reds, and both walk directions are covered by the existing four axes, so a new case could not be made to fail for a regression the lane misses.

## Deliberate risks

- The page's visual half now has a real gate, and since `559558a` it is reached without the caller naming anything; the default call audits the proof. What remains is that the proof lives outside the repository, so no check here can see it (next risk).
- The visual proof lives in a gitignored directory, so the promise is auditable in-session and invisible to every check that reads the repository.
- `source` carries one concrete command (`node --test src/gomoku/rules.test.js`); a second source module makes it a false green, as the implemented record's `## Consequences` says.
- This review is same-source on `src/gomoku/*`. The observations above were re-run by hand, but the rendering judgement is still one pair of eyes; a second reader on the two screenshots is the missing half.
- The page's strings are Chinese only, and its ruleset is freestyle: an overline of six wins, which a Renju player would call wrong.
- `delivery_check` used to pass vacuously when `workspace` was not named; after `559558a` that path reaches the declared layer and fails without a proof, which the re-run in Evidence shows. The old behaviour is kept in this record as the finding it was, not as a description of the build.
