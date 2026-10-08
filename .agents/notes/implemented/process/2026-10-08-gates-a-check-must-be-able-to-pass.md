# Decision: gates — a check must be able to pass

English | [中文](2026-10-08-gates-a-check-must-be-able-to-pass.zh.md)

Status: implemented
Date: 2026-10-08
Class: process

## Problem

A live session built a two-player Gomoku page and finished with every gate this kit ships green, and one gate outside it red in a way no evidence could fix. That session's `delivery_check` grew a `page-verify` check that pushed `pass: false` whenever a page was delivered with a URL — no branch anywhere in it could return true. The tool's own description said the page path could not be bypassed; the only call that passed was one carrying `requireSmoke: false`, which the same description called a bypass. A model that follows the contract therefore cannot deliver a page, and a model that wants a green gate must take the route the contract forbids.

Three more failures in that session share one cause: a gate or a rule that reads as decisive does not decide. The gate's evidence reader called `statSync` on whatever `target` held, so a `page` item whose target was the URL it came from was reported missing, and two runs of the same relative path disagreed only because the host process's working directory had moved. `tools/pair-docs.py` selected its named anchors with `lstrip("./")`, which is a character set, not a prefix: every record this kit tells a reader to write lives under `.agents/`, so the exact `--write <path>` line the tool's own sidecar prints was rejected as "not an in-scope pair". And the session's own rules never said what to do when a check cannot pass, so the agent re-tried one dead check for twenty-eight steps and ended its turn with no message at all.

## Decision

A check that cannot pass is a gate defect, and this kit now says so in three places.

**`tools/pair-docs.py` keeps the dot that names a hidden directory.** Anchor selection moved into `select_anchors(anchors, corpus)`, which strips the leading `./` of a command-line path and nothing else. `.agents/notes/implemented/TEMPLATE.md` — the path printed in the sidecar beside it — is now the path the recorder accepts.

**`AGENTS.md` carries a `## Closing the gate` section.** Six rules, each the size of one incident: a flag you must pass to get through a gate is a gate defect rather than a route; a check that cannot pass is not a check to satisfy; two failed evidence shapes bound the retries on one gate; a turn that ends with a gate red must carry that fact in its final message; an acceptance criterion whose check cannot go red is a wish; and a deletion of a committed path is a change like any other, so it claims a surface and its inbound links are repaired in the same change.

**The delivery gate in the `dsh-router-preset` bundle decides instead of failing, and it decides in two layers because that bundle is shared.** `page-verify` is no longer a hardcoded false. The universal layer decodes every reviewed screenshot target with `delivery-gate.mjs` — the host's `sharp`, or a self-contained PNG reader when the host has none — refuses a frame that is flat, and refuses two claimed states that share one 8x8 luminance fingerprint. The project layer runs only when the project declares it: a `delivery.page.visual` entry in its own `tools/workflow.json` makes the gate require a reviewed local screenshot and the proof `dev_visual_check` writes, whose fingerprints must be exactly the screenshots under the gate; that tool asks the host's image-capable route, through `delivery-vision.mjs`, to read the screenshots against the render facts the agent recorded in the `page` evidence. A project that declares nothing is never asked for a screenshot, and the check says so. Evidence targets resolve against the session workspace rather than the host process's working directory, and a URL is never handed to `statSync`. A deployment deliberately without a vision route passes `visionSkip: true`, which is reported in the check's own detail rather than hidden. The same rule now stands in `AGENTS.md`: a shared gate owns the mechanism, the project owns the policy.

## Alternatives considered

**Delete `page-verify` and let the evidence check carry the page.** Rejected: the evidence check accepts a photographed anything. The session that found the dead check had also attached one PNG of a page-like screen; removing the check would have converted an undeliverable page into an unverified one, which is the failure this kit exists to prevent.

**Make `requireSmoke: false` the documented route for pages.** Rejected: it is the same bypass, renamed into policy. A contract that says "cannot be bypassed" and then documents a bypass teaches the reader that its own words are decoration, and the next gate inherits the licence.

**Render the page inside the gate and compare it with the screenshot.** Rejected for now: it is the strongest evidence, and it is also a browser dependency, a platform matrix, and a second source of the page's appearance inside a plugin that runs in a host process. The vision route gives an independent observer without owning a renderer; when a deployment needs to prove that a *served* page is reachable, that belongs in the project's own evidence lane, where it can name its own browser.

**Let a check report UNKNOWN instead of red when the gate cannot decide.** Rejected: this kit counts a command's result in three states, and `run-evidence` never reports a manual entry as passing. A gate that answers "unknown" for the one question it exists to answer is a gate nobody has to satisfy; `page-verify` refuses, in the same three states, and says which of decode, fingerprint, or route was missing.

## Consequences

The visible defect is gone: a page deliverable with a URL can now pass, and only by supplying a screenshot that decodes, is not flat, is not a duplicate of another claimed state, and whose content an independent model recognises. The cost is a model call on every page delivery, and one verdict the gate does not own: a vision route that answers "no" fails a page a person might accept. That is deliberate — the gate reports what the model said, so a wrong verdict is a reviewable sentence rather than a silent pass.

The kit cannot enforce the delivery gate. `delivery_check` lives in the router preset bundle, not in `tools/`; this record fixes it where it lives and records why, so the next reader does not look for it here. `lstrip` was a real defect in a real tool and now has a test that fails without the fix.

The six rules are prose, and prose alone does not bind: none of them is wired into a check, because the failure they describe is a session's decision, not a tree's state. The one mechanical part — a deletion having an owner — is already `change-scope`'s job; what was missing was the rule that says a deletion is a change at all.

Revisit this when a project ships a page on a host with no image-capable route, when a vision verdict disagrees with a human review twice in a row, or when a second gate grows an unsatisfiable branch: that is the signal to make "every check has a passing fixture" executable rather than remembered.

## Testing

- [A1] `tests` — `python3 -m unittest discover -s tests -v` runs `tests/test_pairing.py::ANamedPathKeepsItsOwnPrefix`, which pins the anchor rule in five cases and drives the recorder end to end through the real parser. The lane was watched red with `lstrip("./")` restored: `test_a_hidden_directory_keeps_its_dot` and the end-to-end case both failed before the fix and pass after it.
- [A2] `workflow` — `python3 tools/check-invariants.py --self-test` still proves every registered check rejects an invalid fixture, and `python3 tools/pair-docs.py --check` reports every pair complete and in step after the tool change.
- [A3] `context-rules` — `python3 tools/check-invariants.py` reads the standing rules for their headings and their links, so `## Closing the gate` has to stay well formed and keep the vocabulary links its sibling rules carry.
- [A4] `workflow` — the delivery gate's own behaviour is **unpinned** here: it lives in the `dsh-router-preset` bundle, not in this repository's `tools/`, so no check in this tree can go red for it. Its lane is `node --test tests/delivery-gate.test.mjs` in that bundle, covering the flat-frame refusal, the repeated-fingerprint refusal, a confirmed verdict, a denied verdict, a dying route, a URL-only page item, a document with no URL, workspace-relative targets, route selection, and verdict parsing; three mutations were watched red and restored (the flat floor, the fingerprint, the deny branch). A reader of this record must take that result from the bundle's own evidence, not from here.
