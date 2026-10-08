---
name: record-decision
description: Use when starting any non-trivial change, so its motivation, the alternatives it beat, and its cost survive the session that produced them — and use again when a shipped decision proves wrong.
---

# Record a decision

Every round of rework has the same cause: the reason a thing is the way it is lives only in the session that produced it. A decision record is where that reason survives.

## When to use

- A change is non-trivial: it changes behaviour, a contract, a format, a default, or a workflow.
- A previously recorded decision is being reversed.

**Exempt:** mechanical edits, renames, formatting, and local presentation tweaks that change no contract.

## How

**Before the work — copy the proposal template.**

```sh
cp .agents/notes/proposed/TEMPLATE.md .agents/notes/proposed/<yyyy-mm-dd>-<slug>.md
```

Fill all five sections. Two of them are mandatory, and they are the ones people skip:

- **`## Alternatives considered`** may not be empty. A decision recorded without what it beat invites re-litigation. Alternatives are **recorded, never invented**: if something was genuinely never on the table, say so and say why.
- **`## Acceptance criteria`** must be translatable into an assertion or a command. If you cannot picture the check, it is a wish, not a criterion.

**When it ships — move it and rewrite the skeleton.**

```sh
# .agents/notes/proposed/<file>.md  →  .agents/notes/implemented/<file>.md, then:
#   ## Proposal                      → ## Decision   (present tense)
#   ## Acceptance criteria + ## Risks → ## Consequences
```

Moving the file without rewriting it fails the check. That is deliberate: the rewrite is the work the move always owed.

**Afterwards — keep the facts current, never the decision.**

When a path, symbol, or default changes, update the record in place. When the **decision** changes, write a new record and cross-link it. Do not append "update: later we changed it to…" — that hands the next reader two contradicting facts.

**Before you name the file — look the module up, and reuse before you add.**

The topic title opens with the module the decision lives in, and that module must be declared in `areas` in [tools/workflow.json](../../../tools/workflow.json), or the gate rejects the record. The list is this project's, it is open, it grows with its records, and it starts with one entry.

1. **Look it up first**, by the name the code, the package, or the directory uses, and by the words a reader would search for. A near match is a match: `docs` covers a decision about a policy page, and inventing a second name for the same place is how a list stops being usable.
2. **Reuse whenever the decision lives where an existing module points.** Most records reuse; a list that grows with every record is a list nobody reads.
3. **Add one only when nothing in the list is where the decision lives.** Adding is one line in `areas`, in the same change as the record that needs it, and the new name is a **place, not a topic**: `sandbox`, not `new-sandbox-flag`. The lookup is what keeps the count of places from tracking the count of decisions.
4. **Never rename a module a record already uses.** Records are addressed by their paths, so a name that moves under them is a broken link. A module that splits or is renamed gains a second entry; the first is retired only when the last record that used it is gone.

**Retiring an entry is the same judgement in reverse.** When no record cites a module any more, delete it from `areas` in the same change that removed the last one. An entry no reader can reach a file through is a name they will reuse by mistake.

**When it stops guiding anyone**, delete it, or move it to `.agents/notes/archived/` with an `Archived:` date and never edit it again.

## Verification

- `python3 tools/check-invariants.py` — `decision-proposed` and `decision-implemented` require their sections to exist and be non-empty, and `note-class` rejects a record dated on or after `areasSince` whose topic title opens with a module that `areas` does not declare.
- Read the `Alternatives considered` section yourself. No check can tell whether it is honest.
- Read `areas` against the records: no check can tell a reused module from a new name for the same place.

## Anti-patterns

- Recording the plan instead of the decision: "we will add X" is not a decision.
- An empty or perfunctory alternatives section — it is the only part that prevents re-litigation.
- Editing a shipped record to describe a different decision.
- Keeping every record forever, so superseded facts still read as current.
- A module invented per record, so the list becomes a second title.
