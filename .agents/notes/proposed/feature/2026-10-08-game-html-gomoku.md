# Proposal: an HTML Gomoku game for two players at one screen

English | [中文](2026-10-08-game-html-gomoku.zh.md)

Status: proposed
Date: 2026-10-08
Class: feature

## Problem

Two people sitting at one machine want a game of Gomoku. The shortest path today is a web search and a page full of ads, or a program whose install step takes longer than the game itself; nothing in this repository plays at all.

That costs more than one game. This repository exists to run the lifecycle on a project that has no code yet, and the minimum-tier decision closed by promising that its first feature would be proposed, decided, verified, and reviewed here. Every station after the proposal — contract, verification, review — has only ever been exercised on documents, never on a program whose behaviour a browser shows a person. Until a real module lands, "the checks work" is a claim about Markdown.

## Proposal

The feature is one page plus one module, both dependency-free, plus the test lane that proves the module.

- `src/gomoku/rules.js` — the rules engine. A classic script that publishes exactly one global, `Gomoku`, and hands the same object to Node behind a single guarded line (`if (typeof module !== "undefined") module.exports = Gomoku;`). It touches no DOM and defines no other global. Its whole interface is `Gomoku.SIZE` (15), `Gomoku.start(size)`, `Gomoku.place(game, row, col)`, and `Gomoku.winner(game)`. A game is a plain object, `{ size, board, turn, winner, moves }`, and `place` returns a new one: `{ ok: true, game }` or `{ ok: false, reason }` with `reason` one of `out-of-range`, `occupied`, `finished`. Win detection reads only the four lines through the move just played.
- `src/gomoku/index.html` — the page. A classic `<script src="rules.js">`, a 15×15 grid of real `<button>` intersections, a status line, and a reset button. Every user-visible string comes from one `STRINGS` map. Clicking an intersection plays that point; clicking a taken one changes nothing; after a win or a draw the board stops taking moves until it is reset.
- `src/gomoku/rules.test.js` — the golden replays, run by Node's built-in runner. Node already ships on the machines this repository is developed on, and the page needs a JavaScript runtime in the browser anyway, so this lane's cost is declaring it rather than installing it. No `package.json`, no dependency to install.
- `tools/workflow.json` — the `source` surface's evidence entry is today the placeholder `<the narrowest owning test for the changed module>`. This change replaces it with the real command, `node --test src/gomoku/rules.test.js`, and adds that same command to the `tests` surface, so the JavaScript lane is declared where `change-scope.py` and `run-evidence.py` already read.
- `README.md`, `README.zh.md`, `README.i18n.yaml` — one bullet under `## Where to go` pointing at the page, with the pair re-recorded.

The ruleset is the common one: 15×15, black first, five or more in a row horizontally, vertically, or diagonally; an overline of six or more wins; a full board with no five is a draw. The intersection is a button rather than a canvas pixel, so the page is keyboard-reachable and a test addresses elements instead of coordinates.

Open question, settled for v1 and cheap to reverse: the page's strings are Chinese only, because the person who asked writes Chinese. One map keeps an English side a later one-line change.

## Alternatives considered

**One self-contained `index.html` with the rules inlined.** Rejected: the win rule would then be reachable only through a browser, so the unit tier would need a browser driver and an install step. A separate classic script keeps the rule testable by a plain JavaScript runtime.

**ES modules, served by `python3 -m http.server`.** Rejected: a browser refuses `type="module"` imports over `file://`, because the page's origin is `null`. The module graph would cost a server and a terminal command before anyone can play, and double-clicking the file is the shortest path from "I have the page" to "I am playing".

**Playwright or headless Chrome as the only lane.** Rejected one tier up for the same reason: it adds an install step this repository has deliberately never had, and it spends a browser on a pure function that a plain runtime already runs.

**Reimplement the win rule in Python and test that.** Rejected: two implementations of one rule are two facts, and they drift. The golden replays must exercise the JavaScript that ships.

**Canvas rendering with pixel hit-testing.** Rejected: it trades addressable elements for coordinate arithmetic in the page and in every test, and it drops keyboard access.

**An AI opponent, or a Renju ruleset with forbidden moves.** Rejected for v1: the requester asked for two players at one screen, and forbidden-move rules change the win check and would need their own acceptance criteria. Revisit when a second player asks. The opponent half is now proposed in [a computer opponent for the Gomoku page](2026-10-08-game-computer-opponent.md); the forbidden-move half is unchanged.

## Acceptance criteria

- [A1] `tests` — `node --test src/gomoku/rules.test.js` covers all four win directions, an overline, a gapped four that must not win, a move on an occupied intersection, a move out of range, a move after the game ended, a full board that draws a game, and that `place` leaves its input state unchanged; deleting any one win direction turns the lane red.
- [A2] `source` — `src/gomoku/index.html` opened from `file://`, with no server and no network request, shows a 15×15 board; a scripted sequence of real intersection clicks ends in the visible win message; a click on an occupied intersection leaves the board unchanged; a reset empties it.
- [A3] `i18n` — `python3 tools/pair-docs.py --check` reports this record's three siblings complete and in step, and keeps `README.md`, `README.zh.md`, and `README.i18n.yaml` level once the game's link is added to both sides.
- [A4] `workflow` — `tools/workflow.json` declares `node --test src/gomoku/rules.test.js` as runnable evidence on the `tests` and `source` surfaces, so `python3 tools/run-evidence.py --check` resolves it and a run records PASS or FAIL instead of a manual entry.

## Risks

- This repository's kit is standard-library Python; Node becomes a second runtime here. The kit's rule is about installed dependencies, and the page needs a JavaScript runtime in the browser regardless, but the boundary does move: where Node is missing, `run-evidence.py` reports UNKNOWN — a tooling problem — and a reader must not take that for a pass. Revisit if a contributor without Node is a real case; the fallback is a browser observation marked unverified, which is weaker and has to be labelled as such.
- Replacing the shared `source` evidence placeholder with one concrete command is true only while this repository has one source module. A second module makes that command a false green; at that point it must become a per-module map, or the surface has to split.
- Freestyle "five or more in a row" is a decision a Renju player would call wrong on an overline. Revisit when someone asks for forbidden moves: that is a new record, not an edit to this one.
- The page lands at `src/gomoku/`, which no surface pattern named before; `source` matches `src/*` today, so nothing new has to be declared. If the game moves, its evidence has to move with it, or the lane quietly stops running.

## Delivery stages

1. Rules engine and its lane — `src/gomoku/rules.js`, `src/gomoku/rules.test.js`, and the evidence entry in `tools/workflow.json`; this lands and is tested with no page at all.
2. Page and entry point — `src/gomoku/index.html`, the link in both READMEs, and the browser observation that closes [A2].
