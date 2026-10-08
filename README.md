# agent-workflow-demo

English | [中文](README.zh.md)

A copy-in workflow kit: the eleven-station lifecycle, executable gates, and bilingual document pairs. This repository runs it at the **minimum** tier, so release, evolution, retirement, rejected records, and postmortems are declared absent instead of installed.

## Where to go

- What each station produces, and which gate decides it: [dev/README.md](dev/README.md)
- How a document is written, budgeted, and published: [docs/README.md](docs/README.md)
- The standing rules an agent loads, and the only command list: [AGENTS.md](AGENTS.md)

## Run the gates

```sh
python3 tools/check-invariants.py --self-test   # the checks can fail
python3 tools/check-invariants.py               # the conventions hold
python3 tools/pair-docs.py --check              # every pair is in step
python3 tools/gen-docs.py --check               # the generated page is current
python3 tools/run-evidence.py --check           # every declared command resolves
python3 -m unittest discover -s tests           # the kit's own contract tests
```
