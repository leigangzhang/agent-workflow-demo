# Decision: install the workflow kit at the minimum tier

English | [中文](2026-10-08-init-minimum-tier-install.zh.md)

Status: implemented
Date: 2026-10-08
Class: process

## Problem

This repository is a demonstration project: it exists to run the kit's lifecycle on a project that has no code yet, and to be the place where the first feature is proposed, decided, verified, and reviewed. It needs a discipline a human and an agent can both act on from the first commit.

Installing every station would mean carrying the homes and gates of release, evolution, retirement, rejected records, and incidents before any of them has a subject. The kit's own rule is that a check matching no file is an empty shell, so a stage the switch calls installed whose home is empty is red by design. The tree would either fail or force placeholder files that mean nothing.

## Decision

`tools/tiers.json` carries `default: minimum`, and an explicit `none` for the seven stations this repository does not run: implementation, integration, release, evolution, retirement, rejection, and incident. The homes of those stations — `dev/release`, `dev/upgrade-guide`, `dev/postmortem`, `.agents/notes/archived`, `.agents/notes/rejected` — are absent from the tree, so the switch and the tree agree in both directions.

Nine stages are installed: intent, proposal, decision, contract, capabilities, verification, review, documentation, and tests. `dev/contracts` and `dev/capabilities` stay, because the check engine's own definition, providers, and consumers live there, and the minimum tier is where that engine runs.

The kit's own decision records were deleted on installation; `.agents/notes/` keeps only each lifecycle's `TEMPLATE.md`, its `README.md`, and its `AGENTS.md`. `README.md`, `README.zh.md`, and `README.i18n.yaml` are this repository's own, because the kit's copy list deliberately omits a root README.

`AGENTS.md` is this repository's own too: its read-first entry is the kit's own two maps, it states that there is no install step yet, and the two rules that pointed at removed homes now stand without the links.

## Alternatives considered

**Install the delivery tier.** Rejected: it adds release and evolution, and this repository has published nothing and has no consumed surface to evolve. A tier is a statement about what the project does; adding one before there is a release record to write is a placeholder.

**Install the long-lived tier.** Rejected for the same reason one step further: contracts, integration, retirement, rejected records, and incidents would each need a subject this repository does not have.

**Copy the kit without pruning, and without declaring any tier.** Rejected: a stage declared installed whose home is empty is red by design, and leaving the directories in place with nothing to check is the hollow guard the kit refuses.

**Copy the kit's decision records along with it.** Rejected: the kit's decisions are the kit's history, and a reader here would take them for this repository's decisions.

## Consequences

The repository starts with the stations whose artifacts a project without code can actually produce: a proposal, a decision, a contract, a test, a review, and the documentation that carries them. Moving up a tier later is a change to `tools/tiers.json` plus the change that creates that station's first artifact; nothing decided here has to be undone.

The cost is that the lifecycle map in `dev/README.md` and the policy in `docs/evolution.md` describe stations this repository does not run. That is deliberate — a reader needs to know what the ladder holds — and the guards that read the tree now read the switch, so a link into an absent station's home is silent rather than red.

Revisit this when the repository has a published surface, which is delivery, or several rounds of evolution with more than one contributor, which is long-lived.

## Testing

- [A1] `tier-manifest` fails when the switch and the tree disagree in either direction, so a station declared `none` whose home holds a file, or an installed station whose home is empty, is red.
- [A2] `agent-input-links` resolves every relative link in the files an agent loads here, which is `AGENTS.md`, the twelve skills, and the record templates.
- [A3] `i18n` — `pair-docs --check` keeps `README.md`, `README.zh.md`, and `README.i18n.yaml` complete and in step.
- [A4] `tests` — `unittest` runs the kit's contract suite in this repository, and the two tests whose stage the switch declares absent report as skipped rather than as errors.
- [A5] `note-class` holds this record to the class its folder encodes.
