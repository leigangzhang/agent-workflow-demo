# Decision records

English | [中文](README.zh.md)

One kind of design document lives here. A **decision record** keeps a decision or a proposal that shapes this kit — the *why*, what it beat, and what it cost: the parts the templates and the gates cannot carry. This file defines where records live, when to write one, and the in-file format.

## Layout and naming

Every record has two axes, both encoded in its **path** — `{lifecycle}/{class}/yyyy-mm-dd-topic-title.md`, under `.agents/notes/`:

- **Lifecycle** (the top-level folder) is the record's status; a record moves between folders as that status changes:
  - **`proposed/`** — designed but not built, or only partly; gate `decision-proposed`.
  - **`implemented/`** — the decision shipped, and **kept current with what shipped**: a later path, name, or default change updates the record in the same change — facts only, never the decision; gates `decision-implemented`, `no-proposal-era-headings`.
  - **`rejected/`** — considered and declined; keep it only while its rationale prevents a tempting mistake, otherwise delete the triplet; gate `decision-rejected`.
- **Class** (the nested folder) is the *kind* of decision, from the closed set in the next section; gate `note-class`.

The date in the filename is when the topic was **first proposed**. Records cross-reference each other with relative Markdown links, never bare prose: a link survives a move, and `pair-docs.py --check` resolves its fragment.

Templates live one level up, at `.agents/notes/<lifecycle>/TEMPLATE.md`: the skeleton is keyed by the lifecycle, not the class, and each one keeps its checks from matching no file — an empty corpus is void, not passing.

The tree is the inventory: browse its class folders, or start from the index in [docs/README.md](../../docs/README.md). Do not add a centralized index page for it — a second list is a second fact.

## Classification

Each record belongs to one path-encoded class from the closed set declared in the `note-class` check in [workflow.json](../../tools/workflow.json), which rejects a folder outside the set, an unknown lifecycle, a missing `Class:` line, and a `Class:` line that disagrees with its folder. Adding a class means updating that list and this table together.

| Class | What it covers |
|---|---|
| `feature` | A new user- or model-facing capability. |
| `bug-fix` | Corrects a defect, or closes a gap an incident record surfaced. |
| `simplification` | Removes behaviour or surface area without adding a capability. |
| `architecture` | A structural decision about what this kit ships — how its parts relate, what its vocabulary is. |
| `process` | Tooling, policy, or workflow around the artefact: gates, records, publication, documentation rules. |
| `testing` | Test infrastructure and strategy. |

The `architecture` / `process` line: architecture is about the artefact itself; process is the surrounding machinery and the rules that govern it. `refactor` is deliberately absent — its only discriminator, "does observable behaviour change?", is already `simplification`'s.

## Modules

A record's topic title opens with the **subject** the decision belongs to: the domain it is about, never the folder it is filed in or where the code it describes sits. A record is a sub-record of one subject, and moving the code does not move it between subjects. Gate `note-class` rejects a title whose first token is not in the table below.

The class set above is closed and adopted. This one is open and this project's own: a subject is named once and reused, it grows when a decision belongs to a domain nothing here names yet, and a new project starts with its first entry.

| Module | What it covers |
|---|---|
| `init` | This project's start: the tier it runs, and the records it began with. |
| `core` | The product's core feature: the Gomoku rules, the computer opponent, and the page that shows them. |

**How the list is kept.** Look the subject up before you name a file, by the words a reader would search for — a near match is a match. Reuse it whenever the decision lives in a domain an entry already names; a list that grows with every record is a list nobody reads. Add a row only when nothing here is where the decision belongs, in the same change as the record that needs it, and name a **domain, not a topic** — `sandbox`, not `new-sandbox-flag`. Never rename an entry a record already uses, because records are addressed by their paths: a subject that splits gains a second row, and the first leaves when the last record that used it is gone. In reverse, an entry no record reaches a file through is a name the next reader will reuse by mistake.
## Archiving and deletion

Delete an implemented record that only describes a mechanical or local change — its English, Chinese, and sidecar files together, with every inbound link repaired. A small bug fix, a new capability, or a substantive decision does not qualify merely because its implementation is small.

Seal a record into `.agents/notes/archived/{class}/yyyy-mm-dd-topic-title.md` when the decision is complete, its rationale is unlikely to guide future work, and it still owns history. Keep it active while its alternatives, an ownership boundary, a negative guarantee, or a reintroduction condition still guides anyone. Never archive a proposal: reject it. A rejected record lives only while it prevents a plausible mistake.

Archiving moves the complete triplet, keeps `Status: implemented`, and inserts the same `Archived: <yyyy-mm-dd>` line in both language files. Gate `archive-seal` binds a sealed file's text to its digest, archive date, and reason in [manifest.json](archived/manifest.json), so an unregistered drop, a missing file, an edited byte, and a disagreeing date are all red. Once sealed, a record is frozen: never edited, reformatted, translated, or moved. The delete-versus-merge-versus-seal call belongs to the selector in [evolution.md](../../docs/evolution.md), not to word count, age, or a quota.

A fully superseded record may be consolidated into the one that now owns the decision and deleted, provided the owner keeps every unique rationale, alternative, consequence, and named gap, and every inbound link is repaired. Partial supersession does not qualify: keep both cross-linked and keep the facts that are still current.

## When to write one

Write or update a record in the same change as the work, and only for lasting rationale that code, tests, and the standing documents do not already explain ([rule](../../AGENTS.md)). Substantial future work starts in `proposed/`; a decision already made starts in `implemented/`. Updating the record that already owns the decision satisfies the rule — do not create a duplicate.

Mechanical and local edits are exempt. A record is never edited into a *different* decision: write a new one and cross-link it, unless the old one qualifies for consolidation above. Correcting an `implemented/` record to match what shipped is required, not forbidden.

## The file format

Every active record follows one in-file format, enforced by `decision-proposed`, `decision-implemented`, `no-proposal-era-headings`, `criteria-traced`, and `note-class`. The literal skeletons are the templates: one copy of the format, not two.

### The header block

The first lines of every record are these, in this order:

| Line | Value |
|---|---|
| `# Proposal: <title>` or `# Decision: <title>` | The lifecycle's own prefix: a proposal keeps `Proposal`, a moved record carries `Decision` |
| `Status: <status>` | `proposed`, `implemented`, or `rejected — <why, in one line>`; it must agree with the folder |
| `Date: <yyyy-mm-dd>` | The first-proposed date, and the same date the filename carries |
| `Class: <class>` | The path class, verbatim; `note-class` cross-checks it against the folder |

The status carries no dates and no parentheticals beyond the rejection reason: the filename holds the date, and the record holds everything else.

### The body skeleton

Every record opens with `## Problem` — the motivation, written to stand without the solution. Recurring sections use these names and nothing else; a bespoke section (a gate's contract, a table shape) sits between the required ones.

- `proposed/`: `## Problem` · `## Proposal` · `## Alternatives considered` · `## Acceptance criteria` · `## Risks`.
- `implemented/`: `## Problem` · `## Decision` · `## Alternatives considered` · `## Consequences` · `## Testing`.
- `rejected/`: the proposal as frozen; the verdict lives on the `Status:` line.

`## Proposal` may speak in the future tense — plans and open questions belong there while the work is unbuilt. `## Decision` states shipped reality in the present tense. `## Testing` keeps each criterion's id alive, and `## Consequences` records what the trade-off cost as well as what it bought.

### Alternatives considered — mandatory

Every record carries `## Alternatives considered`, and it may not be empty: each genuine alternative with why it lost, one bold-led paragraph each. A decision recorded without what it beat invites re-litigation. The requirement is gated in both languages, so a translated record cannot quietly drop it.

### Moving between lifecycles

Moving a record means updating the `Status:` line and re-satisfying the target folder's skeleton in the same change. `proposed/` → `implemented/` rewrites `## Proposal` into a present-tense `## Decision`, folds `## Acceptance criteria` and `## Risks` into `## Consequences` (or a present-tense `## Testing` for what now pins the behaviour), and keeps every criterion id — the id tells a reader which check proves which criterion. `proposed/` → `rejected/` adds the reason to the status line and freezes the body. Gate `no-proposal-era-headings` rejects a moved record still carrying `## Proposal`, `## Plan`, `## Migration plan`, or `## Acceptance criteria`.

### Chinese counterparts

A `.zh.md` counterpart mirrors its English sibling section for section, with a `.i18n.yaml` record beside the pair ([i18n.md](../../docs/i18n.md)). The machine-checked header tokens — `# Proposal: `, `# Decision: `, `Status:`, `Date:`, `Class:` — stay in English verbatim; only headings and prose are translated.

## Where to look

- How to write one: the skeletons in [.agents/notes/proposed/TEMPLATE.md](proposed/TEMPLATE.md) and [.agents/notes/implemented/TEMPLATE.md](implemented/TEMPLATE.md).
- How a goal becomes one or more records: the trigger in [.agents/skills/shape-intent/SKILL.md](../skills/shape-intent/SKILL.md).
- Which record a change needs: the selector in [evolution.md](../../docs/evolution.md).
- What each section must contain: the document kinds in [documentation.md](../../docs/documentation.md).
- Every record this kit has made: this tree, newest first by file name.
