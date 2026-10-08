# Decision: record the kit's own changes, and delete the kit's records at copy time

English | [中文](2026-10-07-kit-records-and-copy-cleanup.zh.md)

Status: implemented
Date: 2026-10-07
Class: process

## Problem

The kit tells every adopter to write a decision record for a non-trivial change, and its own `.agents/notes/implemented/` had already accumulated four layer records. But the install instructions copied `.agents/notes/` verbatim, so those records travelled into every adopter's repository as if they were the adopter's own history. The two goals looked mutually exclusive: record the kit's decisions and ship noise, or keep the rationale outside the kit and let `record-decision` / `decision-implemented` / `criteria-traced` hold nothing. An earlier integration step chose the second, which is why the integration/release layer shipped once without a record.

## Decision

The kit records its own non-trivial changes under `.agents/notes/`, exactly as it asks adopters to. The kit's own records are the **named** files (`.agents/notes/*/<yyyy-mm-dd>-<slug>.md`); `TEMPLATE.md` in each directory is the skeleton that ships. The install section of `README.md` gains one cleanup step: after copying the kit in, delete the named records and keep the templates.

```sh
find .agents/notes -mindepth 3 -type f \( -name '*.md' -o -name '*.zh.md' -o -name '*.i18n.yaml' \) ! -name 'TEMPLATE.*' -delete
```

The cleanup is safe because every `.agents/notes/` directory keeps its `TEMPLATE.md`, so the `decision-*` and `criteria-traced` checks still match a file and cannot go vacuously red. `2026-10-07-integration-release-layer.md` is the first record written under this policy; the four earlier layer records predate it.

## Alternatives considered

**Keep the kit's rationale outside the kit (the previous practice).** It lost: a record the kit does not own is not indexed by its `.agents/notes/`, not checked by `decision-implemented` or `criteria-traced`, and not read by whoever next edits the file the decision governs. It was defensible only while copying was the only thing that moved records; once the copy step deletes them, the tradeoff disappears.

**Move the kit's own records outside the copy set, for example to `notes-kit/`.** It lost: it splits one convention into "the template everyone uses" and "the private shelf", so the kit's own records stop exercising the checks adopters rely on, and the install set grows a second exclusion rule. Keeping them in `.agents/notes/` with one explicit delete step keeps one convention and one shape.

**Ship every record and document that adopters may delete them.** It lost: an unread record is not neutral — old prose returns as fact. A record describing the kit's own history reads as the adopter's history unless it is removed, so removal is a required step, not a suggestion.

**Add a `Scope: kit` header field so records identify themselves.** It lost: the templates ship, and adding the field to the template would tell every adopter's record to declare itself kit-internal. The `TEMPLATE.md`-versus-named-file split already separates the two sets and is decidable from the path alone.

## Consequences

- The kit now records its own decisions like any adopter, and `criteria-traced` can hold its criteria. Installation removes them, so a copied kit still starts with only the templates.
- `find .agents/notes -mindepth 3 -type f \( -name '*.md' -o -name '*.zh.md' -o -name '*.i18n.yaml' \) ! -name 'TEMPLATE.*' -delete` becomes part of installation. Skipping it leaves the kit's history in a downstream repository, where it reads as that repository's decisions.
- The rule is one sentence: **named records are the kit's; `TEMPLATE.md` is the skeleton that ships.** A fact that must travel with the kit belongs in a shipped document (`dev/README.md`, `documentation.md`, `evolution.md`), not in `.agents/notes/`.
- No gate can check the deletion: nothing knows what a downstream copy removed. `README.md` states the step, and the responsibility is the copier's.

## Testing

- [A1] `decision-proposed`, `decision-implemented`, and `decision-rejected` each still match a `TEMPLATE.md` after the named records are deleted, so the cleanup cannot create an empty corpus.
- [A2] `criteria-traced` accepts `.agents/notes/implemented/TEMPLATE.md` and `.agents/notes/proposed/TEMPLATE.md` with the named records absent, because each template's bullets already name declared checks.
- [A3] `publish-manifest` classifies every `.agents/notes/**` file as `internal` through the `.agents/notes/*` pattern, so adding and removing records needs no manifest change.
- [A4] `agent-inputs` lists `README.md`, so the install instructions are reviewed as a model-visible input; the delete step itself is a human action no check can verify.
