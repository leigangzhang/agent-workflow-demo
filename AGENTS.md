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

- **Every non-trivial change gets a decision record.** Copy [notes/proposed/TEMPLATE.md](notes/proposed/TEMPLATE.md) to `notes/proposed/<class>/<yyyy-mm-dd>-<slug>.md` in the same change; when it ships, move it to `notes/implemented/` and rewrite its skeleton. Mechanical or local edits are exempt.
- **Write down what you rejected.** `Alternatives considered` is mandatory and may not be empty: a decision recorded without what it beat invites re-litigation ([rules](notes/AGENTS.md)).
- **Facts may be corrected in place; decisions may not.** When code moves or a default changes, update the record. When the decision reverses, write a new record and cross-link it ([rules](notes/AGENTS.md)).
- **Design before build.** A non-trivial capability starts as a [proposal](notes/proposed/TEMPLATE.md) that names the interface and the acceptance criteria; implementation follows. Review holds the order; no check can.
- **Every acceptance criterion names what would go red.** A criterion carries a stable id and cites a declared check or surface; a criterion you cannot picture a check for is a wish. The id survives the move into `## Testing` ([skill](skills/define-acceptance/SKILL.md), gate `criteria-traced`).
- **One role alone is not a capability.** A `seam` needs a definition, a provider, and a consumer. Anything registered under another kind says in its `note` why it is not one ([shape](dev/capabilities/TEMPLATE.md)).
- **Don't split preemptively.** Keep the roles in one file or package until a second provider or consumer actually appears; "we may need it later" is not a reason ([shape](dev/capabilities/TEMPLATE.md)).
- **Every capability names a current consumer.** An abstraction, option, or compatibility path with no consumer is rejected, not parked ([shape](dev/capabilities/TEMPLATE.md)).
- **A rejected record lives only while it prevents a mistake.** Once the verdict stops anyone re-proposing the same thing, delete the record.
- **A convention that cannot fail is not a convention.** Wire every rule you care about into an executable check declared in [tools/workflow.json](tools/workflow.json); prose alone does not bind anyone.
- **Prove a new guard.** After adding or changing a check, run `python3 tools/check-invariants.py --self-test` ([policy](docs/testing.md#prove-a-new-guard)). A check that no fixture can make red is noise, not a guard.
- **Run the evidence, do not retype it.** Before saying the work is done, run `python3 tools/run-evidence.py --base origin/main` and link the record it writes under `dev/evidence/`. Entries it cannot execute are manual: do them, or mark them unverified. A command it never ran is not evidence ([semantics](tools/README.md)).
- **A test earns its place by failing.** Watch a new test or guard go red for the regression it pins before trusting it green. Flake is a defect, never noise: do not fix it with a longer timeout, a retry, a sleep, a serial suite, or a weaker assertion — retry only at a real external boundary ([policy](docs/testing.md#flake-policy)).
- **Match evidence to the changed surface.** Run `python3 tools/change-scope.py --base origin/main` and run the checks it names ([skill](skills/pick-evidence/SKILL.md)). There is no universal local baseline.
- **Verify the world, not the self-report.** An assertion re-runs the command or re-reads the file from outside the writer ([skill](skills/apply-distrust/SKILL.md)). Never accept "the output says it worked".
- **Distrust the green signal by default; spend it where a signal can lie.** A report, a coverage number, a refreshed snapshot, a green gate, or a missing error is not evidence on its own — name what would go red instead. Do not defend typed same-process values, consumer-less surfaces, or uncovered dead code "just in case"; the reverse list and the eight delivery questions live in [skills/apply-distrust/SKILL.md](skills/apply-distrust/SKILL.md).
- **Mock only the expensive or non-deterministic edge** — model, network, clock, randomness ([policy](docs/testing.md#test-doubles)). Keep everything downstream real.
- **Prose states current state.** History lives in commits, decision records, and incident notes — never in comments, READMEs, or prompts ([rules](docs/documentation.md#the-slop-checklist)).
- **Write to the human in their own words.** In anything a person reads — a reply, a PR description, a release note, a post-mortem summary, a commit message — expand a compressed term on first use or replace it ([plain-language.md](docs/plain-language.md)); the glossary is the agent's vocabulary, not the reader's.
- **One home per fact.** If a sentence exists in two places, delete one copy and link the other.
- **Name the lifecycle stage.** Every artifact belongs to one stage of [dev/README.md](dev/README.md). A record filed under the wrong stage is checked against the wrong skeleton.
- **Contracts point at their source; they never restate it.** An interface lives in a file a compiler can compare, and prose links to it. A copy of an interface is a second fact, and two facts drift.
- **Generated pages are edited through their generator.** Change the generator or its source, re-run it, and let its `--check` command prove the committed page is current — never patch the page, and never treat a regenerated page as the owner of the fact.
- **Every document is classified once.** [docs/publish.json](docs/publish.json) is the only publication switch: a Markdown file classified neither `public` nor `internal` is red, and a `public` entry with no file behind it is red. A page that exists is not a page that ships.
- **Verify a release from outside.** Release evidence includes installing and running the artifact in a clean directory outside this repository. In-repo runs are masked by caches and leftover build output.
- **Retire, do not accumulate.** A record that no longer guides anyone is deleted, or moved to `notes/archived/` with an `Archived:` date and sealed in that archive's manifest, and never edited again; gate `archive-seal` catches an unsealed drop, an edited record, and a date that disagrees with the seal. Old prose returns as fact in the next reader's context.
- **Used artifacts are append-only.** Once a format, schema, or published interface has been consumed, add a versioned successor. Never move, overwrite, or delete a committed generation ([policy](docs/evolution.md)).
- **A skill is loaded by its description.** Write the trigger ("use when …"), never a summary of the skill's own contents. A skill whose trigger is not obvious is an article nobody opens; gate `skill-trigger` rejects a description that is a summary instead of a trigger.
- **Keep changes independent.** One concern per commit. Do not mix a refactor with a behaviour change.

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
