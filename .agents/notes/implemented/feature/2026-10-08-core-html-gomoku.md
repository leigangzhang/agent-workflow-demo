# Decision: an HTML Gomoku game for two players at one screen

English | [中文](2026-10-08-core-html-gomoku.zh.md)

Status: implemented
Date: 2026-10-08
Class: feature

## Problem

Two people sitting at one machine want a game of Gomoku. The shortest path is a web search and a page full of ads, or a program whose install step takes longer than the game itself.

That cost more than one game. This repository exists to run the lifecycle on a project that has no code yet, and its minimum-tier decision closed by promising that the first feature would be proposed, decided, verified, and reviewed here. Every station after the proposal — contract, verification, review — had only ever been exercised on documents, never on a program whose behaviour a browser shows a person. Until a real module landed, "the checks work" was a claim about Markdown.

## Decision

The game ships as one page and one module, both dependency-free, plus the lane that proves the module.

- `src/gomoku/rules.js` — the rules engine. A classic script that sets `window.Gomoku` in a browser and `module.exports` in Node, and touches no DOM. Its interface is `Gomoku.SIZE` (15), `Gomoku.start(size)`, `Gomoku.place(game, row, col)`, and `Gomoku.winner(game)`. A game is `{ size, board, turn, winner, moves }`: `board` holds `size * size` row-major cells, each `null`, `"black"`, or `"white"`; `turn` is the side to move, and the side that moved last once the game is finished; `winner` is `null`, `"black"`, `"white"`, or `"draw"`; `moves` lists the stones in play order. `place` returns a new game and never mutates the one it was given, refusing a move with `{ ok: false, reason }` where `reason` is `out-of-range`, `occupied`, or `finished`. It decides the outcome from the four axes through the point just played, so a move costs the length of those lines and not the board. Black moves first; five or more in a row wins, an overline of six or more included; a full board with no five is a draw.
- `src/gomoku/index.html` — the page. A classic `<script src="rules.js">`, 15 rows of 15 `<button>` intersections under `role="grid"`, a status line, and a reset button. Every user-visible string comes from one `STRINGS` map, Chinese only. A click is offered to `Gomoku.place` and a refusal is simply not rendered, so the page holds no rule of its own: legality, the turn, and the outcome all come from the engine, and the two-player turn never moves itself.
- `src/gomoku/rules.test.js` — the golden replays, run by Node's built-in runner as `node --test src/gomoku/rules.test.js`. No `package.json` and no dependency to install.
- `tools/workflow.json` — the `tests` and `source` surfaces both declare `node --test src/gomoku/rules.test.js` as runnable evidence. The placeholder the `source` surface carried is gone.
- `README.md`, `README.zh.md`, `README.i18n.yaml` — one bullet under `## Where to go` points at the page, on both sides, with the pair re-recorded.

The page opens from `file://`: no server, no network request, and no build step stand between having the file and playing.

## Alternatives considered

**One self-contained `index.html` with the rules inlined.** Rejected: the win rule would then be reachable only through a browser, so the unit tier would need a browser driver and an install step. A separate classic script keeps the rule testable by a plain JavaScript runtime, and that is what the lane now does.

**ES modules, served by `python3 -m http.server`.** Rejected: a browser refuses `type="module"` imports over `file://`, because the page's origin is `null`. The module graph would cost a server and a terminal command before anyone can play, and double-clicking the file is the shortest path from "I have the page" to "I am playing".

**Playwright or headless Chrome as the repository's lane.** Rejected: it adds an install step this repository has deliberately never had, and it spends a browser on a pure function that a plain runtime already runs. The consequence is stated rather than hidden: the page's own behaviour is observed by hand, and `## Testing` marks it `unpinned`.

**Reimplement the win rule in Python and test that.** Rejected: two implementations of one rule are two facts, and they drift. The golden replays exercise the JavaScript that ships.

**Canvas rendering with pixel hit-testing.** Rejected: it trades addressable elements for coordinate arithmetic in the page and in every test, and it drops keyboard access. The shipped buttons are reachable by keyboard, and a click is what a test addresses.

**An AI opponent, or a Renju ruleset with forbidden moves.** Rejected for this record: the requester asked for two players at one screen, and forbidden-move rules change the win check and would need their own acceptance criteria. The opponent half is now proposed in [a computer opponent for the Gomoku page](../../proposed/feature/2026-10-08-core-computer-opponent.md); the forbidden-move half is unchanged.

## Consequences

The repository has a playable artefact and its first lane where a program's behaviour can go red. The engine is testable without a browser, the page carries no rule of its own, and a reader who has the directory has the game.

- Node is a second runtime here, and the repository's kit is standard-library Python. The page needs a JavaScript runtime in the browser regardless, but the boundary does move: where Node is missing, `run-evidence.py` reports UNKNOWN — a tooling problem — and a reader must not take that for a pass. The fallback is a browser observation marked unverified, which is weaker.
- The `source` surface carries one concrete command, which is true only while this repository has one source module. A second module makes that command a false green; at that point it must become a per-module map, or the surface has to split.
- Freestyle "five or more in a row" is a decision a Renju player would call wrong on an overline. Overturning it is a new record, not an edit to this one.
- The page's strings are Chinese only, because the person who asked writes Chinese. One map keeps an English side a later one-line change.
- The DOM half of this record is not pinned by a command: the `source` lane runs the engine, not the page. What a browser does with the engine is observed by hand, and a hand observation is never counted as verified by `run-evidence.py`.
- The page lands at `src/gomoku/`, which no surface pattern named before; `source` matches `src/*`, so nothing new had to be declared. If the game moves, its evidence has to move with it, or the lane quietly stops running.

Revisit this when a second module makes the `source` lane a false green, when Node cannot be assumed on a contributor's machine, when someone asks for forbidden moves or for a second player's strings, or when stage 2 of [the opponent record](../../proposed/feature/2026-10-08-core-computer-opponent.md) turns the page's behaviour into something the repository must run rather than observe.

## Testing

- [A1] `tests` — `node --test src/gomoku/rules.test.js` replays the four win directions, an overline, a gapped four that must not win, a stone already on the board, a point off the board, a move after the game is finished, a full board that draws, and the purity of `place`. Each win direction is its own case, so deleting one from the engine turns exactly that case red, and a run records PASS.
- [A2] `source` — the page's own behaviour is `unpinned`: the lane on this surface runs `node --test src/gomoku/rules.test.js`, which never reaches the DOM, and this repository runs no browser driver. The observation that stands in for it was made by hand on the real page from `file://`: 225 intersections in 15 rows, black's five clicks end in the visible win message, a click on an occupied intersection leaves the board unchanged, a click after the win is refused, reset empties the board, a focused intersection plays with Enter, and the page makes no network request. Two screenshots of that run are kept beside the evidence records, at `dev/evidence/2026-10-08-core-html-gomoku-headless.png` and `dev/evidence/2026-10-08-core-html-gomoku-win.png`. It is a manual entry, and `run-evidence.py` never reports it as passing.
- [A3] `i18n` — `python3 tools/pair-docs.py --check` reports this record's three siblings complete and in step, and keeps `README.md`, `README.zh.md`, and `README.i18n.yaml` level with the game's link on both sides.
- [A4] `workflow` — `tools/workflow.json` declares `node --test src/gomoku/rules.test.js` on the `tests` and `source` surfaces, so `python3 tools/change-scope.py --base origin/main` names both surfaces for a `src/gomoku/` change and `python3 tools/run-evidence.py --base origin/main` runs the lane and records PASS instead of a manual entry.
