# AGENTS.md — decision records

Decision records are this kit's RFCs: they keep the rationale, the rejected alternatives, the consequences, and the required verification. Follow the [documentation standard](../docs/documentation.md) and the [record rules](README.md).

**A record moves; it is not renamed.** Moving a proposal into `implemented/` rewrites the skeleton (`## Proposal` becomes `## Decision`; acceptance criteria and risks fold into `## Consequences`) and keeps every criterion id; a record that still carries proposal-era headings fails `decision-implemented`.

**A record's class is path-encoded.** It lives at `notes/<lifecycle>/<class>/<yyyy-mm-dd>-<slug>.md`, with the class taken from the closed set in [workflow.json](../tools/workflow.json); gate `note-class` rejects a folder outside the set and a `Class:` line that disagrees with its folder. Pick the class by the decision, not by the files it touches ([meanings](README.md#classification)).

**Facts may be corrected in place; the decision may not.** Paths, defaults, and mechanisms are updated in the change that alters them. Reversing a decision means writing a new record and cross-linking it.

**A record that no longer guides anyone is retired, not accumulated.** Delete a mechanical one, reject an obsolete proposal, or seal an implemented record into `notes/archived/` with an `Archived:` date; the selector lives in [evolution.md](../docs/evolution.md).

**Both sides move together.** A record is a bilingual pair, so an edit to one side lands with the matching edit to the other and a re-recorded sidecar ([i18n.md](../docs/i18n.md)).
