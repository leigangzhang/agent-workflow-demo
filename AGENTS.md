# AGENTS.md

Standing orders for anyone — human or agent — changing this repository. Every rule is one to three lines and links the file that owns the detail. This file is in context on every task, so it is a **budget**: if a rule needs a paragraph, it belongs in the linked document, not here.

## Read first

- Read [dev/README.md](dev/README.md) and [docs/README.md](docs/README.md) before changing anything: they map the lifecycle's stations and every home in this repository.
- Read [testing.md](docs/testing.md) before writing or changing a test, a fixture, a helper, or a CI lane. It owns the tiers, the evidence map, the determinism rules, and the flake policy.
- Read [documentation.md](docs/documentation.md) before writing, restructuring, or publishing documentation. It owns the kinds, the placement table, the tutorial/reference split, the budgets, and the publication switch.
- Read [glossary.md](docs/glossary.md) before naming a concept, a check, or a document kind: it owns what each word means here and which spelling to use.
- Read [i18n.md](docs/i18n.md) before writing or editing any paired document. It owns which files pair, what stays untranslated, and how the two sides stay in step.
- Read [evolution.md](docs/evolution.md) before changing a surface that has already been consumed, or retiring a record. It owns which record a change gets, the three version states, and the archive seal.
- Prefer the owning document over this file: this file states the rule, the linked file states the contract.

## Working rules

- **A decision earns a record only when its decision sentence is a constraint no other home already states.** Write `## Decision` as one sentence another change can be checked against; if it can only be written as "we did X", write no record. Copy [.agents/notes/proposed/TEMPLATE.md](.agents/notes/proposed/TEMPLATE.md) to `.agents/notes/proposed/<class>/<yyyy-mm-dd>-<module>-<slug>.md` in the same change; when it ships, move it to `.agents/notes/implemented/` and rewrite its skeleton. The two questions and the session file live in [.agents/notes/README.md](.agents/notes/README.md#when-to-write-one).
- **Close a change by saying two things out loud**: whether any settled decision is still unfrozen, and whether this delivery unit has its one evidence record. Freeze with `/record-decision`.
- **Write down what you rejected.** `Alternatives considered` is mandatory and may not be empty: a decision recorded without what it beat invites re-litigation ([rules](.agents/notes/AGENTS.md)).
- **Design before build.** A non-trivial capability starts as a [proposal](.agents/notes/proposed/TEMPLATE.md) that names the interface and the acceptance criteria; implementation follows. Review holds the order; no check can.
- **One role alone is not a capability.** A `seam` needs a definition, a provider, and a consumer. Anything registered under another kind says in its `note` why it is not one ([shape](dev/capabilities/TEMPLATE.md)).
- **Don't split preemptively.** Keep the roles in one file or package until a second provider or consumer actually appears; "we may need it later" is not a reason ([shape](dev/capabilities/TEMPLATE.md)).
- **Every capability names a current consumer.** An abstraction, option, or compatibility path with no consumer is rejected, not parked ([shape](dev/capabilities/TEMPLATE.md)).
- **A rejected record lives only while it prevents a mistake.** Once the verdict stops anyone re-proposing the same thing, delete the record ([.agents/notes/rejected/TEMPLATE.md](.agents/notes/rejected/TEMPLATE.md)).
- **A convention that cannot fail is not a convention.** Wire every rule you care about into an executable check declared in [tools/workflow.json](tools/workflow.json); prose alone does not bind anyone.
- **Match evidence to the changed surface.** Run `python3 tools/change-scope.py --base <verified-base-ref>` and run the checks it names ([skill](.agents/skills/pick-evidence/SKILL.md)). There is no universal local baseline.
- **Say what is not verified.** Name the entries that did not run, and the claims nothing can falsify, beside the verified ones ([rules](.agents/notes/AGENTS.md)).
- **Verify the world, not the self-report.** An assertion re-runs the command or re-reads the file from outside the writer ([skill](.agents/skills/apply-distrust/SKILL.md)). Never accept "the output says it worked".
- **Distrust the green signal by default; spend it where a signal can lie.** A report, a coverage number, a refreshed snapshot, a green gate, or a missing error is not evidence on its own — name what would go red instead. Do not defend typed same-process values, consumer-less surfaces, or uncovered dead code "just in case"; the reverse list and the eight delivery questions live in [.agents/skills/apply-distrust/SKILL.md](.agents/skills/apply-distrust/SKILL.md).
- **Mock only the expensive or non-deterministic edge** — model, network, clock, randomness ([policy](docs/testing.md#test-doubles)). Keep everything downstream real.
- **Prose states current state.** History lives in commits, decision records, and incident notes — never in comments, READMEs, or prompts ([rules](docs/documentation.md#the-slop-checklist)).
- **Write to the human in their own words.** In anything a person reads — a reply, a PR description, a release note, a post-mortem summary, a commit message — expand a compressed term on first use or replace it ([plain-language.md](docs/plain-language.md)); the glossary is the agent's vocabulary, not the reader's.
- **One home per fact.** If a sentence exists in two places, delete one copy and link the other.
- **Name the lifecycle stage.** Every artifact belongs to one stage of [dev/README.md](dev/README.md). A record filed under the wrong stage is checked against the wrong skeleton.
- **Contracts point at their source; they never restate it.** An interface lives in a file a compiler can compare, and prose links to it. A copy of an interface is a second fact, and two facts drift.
- **Every document is classified once.** [docs/publish.json](docs/publish.json) is the only publication switch: a Markdown file classified neither `public` nor `internal` is red, and a `public` entry with no file behind it is red. A page that exists is not a page that ships.
- **Verify a release from outside.** Release evidence includes installing and running the artifact in a clean directory outside this repository. In-repo runs are masked by caches and leftover build output.
- **Retire, do not accumulate.** A record that no longer guides anyone is deleted, or moved to `.agents/notes/archived/` with an `Archived:` date, sealed in [.agents/notes/archived/manifest.json](.agents/notes/archived/manifest.json), and never edited again; gate `archive-seal` catches an unsealed drop, an edited record, and a date that disagrees with the seal. Old prose returns as fact in the next reader's context.
- **Used artifacts are append-only.** Once a format, schema, or published interface has been consumed, add a versioned successor. Never move, overwrite, or delete a committed generation ([policy](docs/evolution.md)).
- **A skill is loaded by its description.** Write the trigger ("use when …"), never a summary of the skill's own contents. A skill whose trigger is not obvious is an article nobody opens; gate `skill-trigger` rejects a description that is a summary instead of a trigger.

## Closing the gate

The rules above say how to produce evidence. These say what to do when the gate that judges it is wrong — the failure mode is not a bad artifact but a session that cannot end.

- **A flag you must pass to get through a gate is a gate defect, not a route.** `requireSmoke: false`, `--no-verify`, an entry deleted from a manifest: when the gate's own contract says it cannot be bypassed, bypassing it silently is a false delivery. Report the defect with the exact call and let a person decide — do not report the work green.
- **A check that cannot pass is not a check to satisfy.** When every other gate is green, the artifact is real, and one check stays red under every evidence shape you can honestly produce, stop producing shapes. Name it as a defect of the check, with what you tried, and treat it as a real finding instead of a blocker you may ignore.
- **Bound the retries on a single gate.** Two failed shapes of the same evidence is the signal to re-examine the gate itself; a third identical attempt is not diligence. Keep the rest of the work moving and report the dead end.
- **Never end a silent turn.** A turn that finishes with a gate still red must carry, in its final message, what is red and what you did about it. Reasoning that reaches that conclusion is not a report.
- **A shared gate owns the mechanism, the project owns the policy.** A preset, plugin, or shared tool that every project runs may enforce only what holds for every project; whether a page needs a screenshot, and how strong that evidence must be, is declared by the project itself (this repository's `tools/workflow.json`). A shared default that reaches every project is a decision no project asked for.

## Commands

```sh
# no install step yet: this repository is standard-library Python only
# the gate commands below, in order, are the full local check
python3 tools/check-invariants.py --self-test               # prove the checks can fail
python3 tools/check-invariants.py                           # run the executable conventions
python3 tools/gen-docs.py --check                           # the generated page is still a current projection
python3 tools/pair-docs.py --check                          # every bilingual pair is complete and in step
python3 tools/change-scope.py --base origin/main            # what changed, and what evidence it needs
python3 tools/run-evidence.py --check                       # every declared evidence command resolves
python3 tools/run-evidence.py --base origin/main            # run that evidence and write the record
python3 -m unittest discover -s tests                       # the kit's own contract tests
```
