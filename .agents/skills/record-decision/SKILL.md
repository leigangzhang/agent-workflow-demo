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

**When it stops guiding anyone**, delete it, or move it to `.agents/notes/archived/` with an `Archived:` date and never edit it again.

## Verification

- `python3 tools/check-invariants.py` — `decision-proposed` and `decision-implemented` require their sections to exist and be non-empty.
- Read the `Alternatives considered` section yourself. No check can tell whether it is honest.

## Anti-patterns

- Recording the plan instead of the decision: "we will add X" is not a decision.
- An empty or perfunctory alternatives section — it is the only part that prevents re-litigation.
- Editing a shipped record to describe a different decision.
- Keeping every record forever, so superseded facts still read as current.
