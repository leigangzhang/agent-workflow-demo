# Proposal: a computer opponent for the Gomoku page

English | [中文](2026-10-08-core-computer-opponent.zh.md)

Status: proposed
Date: 2026-10-08
Class: feature

## Problem

One person at a keyboard wants a game of Gomoku. The two-player page proposed in [an HTML Gomoku game for two players at one screen](2026-10-08-core-html-gomoku.md) is not built yet, and its v1 scope settles that a second person has to be present: alone, a player makes one click and the board then waits forever. Nothing on that page chooses a move, so the shortest path from "I want a game" to "I am playing" still runs through finding someone else.

It is also the first behaviour this repository would pin as a decision rather than a rendering. The page's rules are written down once and clicked through; a chooser's output is checkable only if the same position yields the same move every time, so the acceptance criteria here have to pin a choice, not a picture.

## Proposal

The change is one module, its lane, and one mode on the page. It consumes the v1 record's delivery stage 1, the rules engine at `src/gomoku/rules.js`, and does not change it; it lands in dependency order behind that record.

- `src/gomoku/ai.js` — the move chooser. A classic script that publishes exactly one global, `GomokuAI`, and hands the same object to Node behind one guarded line, the shape `rules.js` already uses; it touches no DOM. Its whole interface is `GomokuAI.chooseMove(game)`, which returns `{ row, col }` for a legal point, or `null` when the game is finished or the board is full. It takes no options object: a difficulty setting would be an option with no consumer today. It never mutates the game it is given and never plays the point itself — the page still applies the reply through `Gomoku.place`, so the rules engine stays the only authority on legality and on who won.
- The chooser decides one ply deep. If the side to move can complete five now, it plays that point; otherwise, if the opponent could complete five on their next move, it plays the blocking point; otherwise it takes the highest-scoring empty point among the candidates within two steps of an existing stone, and the centre on an empty board. A point's score is what the runs it would extend and the runs it would break are worth in each of the four directions, and ties go to the lowest row, then the lowest column. The terminal tests run through `Gomoku.place` on a copy of the game rather than counting a line here, so the win rule keeps one implementation; the counting exists only to rank the points that do not end the game. The chooser reads no clock and no random source, so the same position yields the same point, which is what lets its lane assert exact moves.
- `src/gomoku/ai.test.js` — the golden replays, run by Node's built-in runner, in the lane shape the v1 record declares for `rules.test.js`. No `package.json`, and no dependency to install.
- `src/gomoku/index.html` — one mode control with two modes. In vs-computer mode the human plays black and moves first, and each human move is answered by exactly one reply, computed and applied inside the same click handler: there is no thinking state, no timer, and no second step for the player to trigger. The status line and the final message name 你 and 电脑 in this mode, and 黑方 and 白方 in the other. Changing the mode empties the board and starts a fresh game, and so does the reset button. The two-player path keeps the behaviour the v1 record pins.
- `tools/workflow.json` — the `tests` and `source` evidence lists gain `node --test src/gomoku/ai.test.js` beside the v1 lane. Listing both commands is the whole fix for the warning the v1 record already carries, that one concrete command on `source` becomes a false green at the second module: the surface is a flat list of commands, so a change to either module runs both lanes.
- `README.md`, `README.zh.md`, and their consistency record — the v1 record adds the page's bullet there; if that bullet describes two players only, this change corrects the wording on both sides and re-records the pair.
- [The v1 record](2026-10-08-core-html-gomoku.md) — its `## Alternatives considered` entry for an AI opponent gains a relative link to this record on both sides, so a reader of either is not left with the other's earlier scope.

Two defaults are settled for v1 and cheap to reverse: the human is black and moves first, and the opponent has one level. Both are revisit conditions in `## Risks`.

## Alternatives considered

**A random legal move.** Rejected: it never blocks a four, so a player who lines up five on the fourth move wins, and the mode would be a demonstration rather than an opponent. It would cost the least, which is exactly why it is worth naming — the cheap version is not worth a mode.

**A minimax search with alpha-beta pruning.** Rejected for v1: a 15×15 board with no candidate restriction branches past what one click can afford, and a search budgeted by time would make the move depend on the machine's speed, so the golden replays would stop pinning anything and the determinism rules in [testing.md](../../../../docs/testing.md) would be broken by the design rather than by a test. A depth-limited search over the same candidate set is the shape a stronger level takes; it is deferred, and it needs a new record because it changes the acceptance criteria.

**An external engine or a library.** Rejected: it adds an install step and a dependency to a page whose shortest path is a double-click on a file, a cost the v1 record already refused once when it ruled out `type="module"` and a server. A vendored search would also carry a second board model and a second win rule to keep in step.

**The heuristic inline in `index.html`.** Rejected: the chooser would then be reachable only through a browser, so its lane would need a browser driver — the same reason the v1 record split the rules out of the page.

**A second page for the mode (`vs-computer.html`).** Rejected: it duplicates the board rendering, the strings map, and the lock-out behaviour, and the copies would drift at the first UI change. One board with a mode control keeps one renderer.

**A random tie-break among equal-scoring points.** Rejected: it makes the same position produce different moves, so the lane cannot assert a move, a player cannot reproduce a game, and a reported bug becomes unreproducible. Variety, if it is ever wanted, belongs in an opening book fed by a seeded source, not in the tie-break.

**A pluggable opponent interface with a capability registry entry.** Rejected: there is one provider and one consumer, and this kit refuses to split preemptively for a hypothetical second implementation. The registry also discovers its markers in `tools/*.py`, so an entry for a JavaScript module would be registered and undiscoverable, and `capability-registry` would reject the pair.

**Letting the chooser decide the win itself.** Rejected: two implementations of one win rule are two facts, and the v1 record already refused that trade when it rejected a Python rewrite of the win check. The chooser asks `Gomoku.place` instead.

## Acceptance criteria

- [A1] `tests` — `node --test src/gomoku/ai.test.js` covers playing the point that completes five, blocking the opponent's four, returning `null` on a finished game and on a full board, never returning an occupied point or one off the board, returning the same point for the same position across repeated calls, leaving the input game unchanged, the centre on an empty board, and a point within one step of a lone centre stone. Deleting any one of those turns the lane red.
- [A2] `source` — `src/gomoku/index.html` opened from `file://`, with no server and no network request, switches to vs-computer mode; one click on an empty intersection adds one black stone and exactly one white reply on an empty intersection, with no further click; the status line and the final message name 你 and 电脑; switching the mode mid-game empties the board; a reset starts a fresh game with the human to move; after the computer completes five, further clicks change nothing; and switching back to two players still works.
- [A3] `i18n` — `python3 tools/pair-docs.py --check` reports this record's three siblings complete and in step, keeps the v1 pair level after its cross-link edit, and resolves the links between the two records.
- [A4] `workflow` — `tools/workflow.json` declares `node --test src/gomoku/ai.test.js` as runnable evidence on the `tests` and `source` surfaces beside the v1 lane, so `python3 tools/run-evidence.py --check` resolves both and a run records PASS or FAIL instead of a manual entry.
- [A5] `decisions` — reading both records shows the dependency from either side: the v1 record's AI alternative links to this record, and this record's `## Problem` links to the v1 record.

## Risks

- One ply is the whole opponent: it wins a five and blocks a five, and it ranks points by what they build, but it does not search a combination, so a player who creates two threats in one move wins. Revisit when a stronger opponent is asked for; that is a new record, because it changes [A1] and [A2].
- The opponent has one level, and `chooseMove` takes no options, because a single level has no consumer for one. Revisit when a second level is asked for: the option arrives with the level that consumes it.
- The human is always black. Revisit when someone asks to play second: the mode control grows a second dimension, the board has to apply the opening reply, and the chooser's empty-board centre becomes reachable from the page.
- There is no take-back. Revisit with a record of its own: in this mode one undo has to remove two stones, or the player would take back a stone and the reply that answered it separately.
- The reply is computed inside the click handler, which holds only while one reply costs less than a frame. A stronger chooser has to move to a deferred path with an explicit locked state, and [A2]'s observation changes with it.
- Determinism is a constraint on the chooser, not a property it happens to have: no clock and no random source. An opening that varied would have to arrive through a seeded source passed in at the call site, or the golden replays stop pinning anything.
- Load order is now a dependency: the page must load `rules.js` before `ai.js`, and `ai.test.js` requires both. A page that loads the chooser alone throws when the first reply is computed.
- The `source` surface now runs both lanes for any source change, and a third module makes that a false green again: the list then has to split or become a per-module map.
- The chooser is not a registered capability: one provider, one consumer, and the registry discovers its markers only in `tools/*.py`. A second opponent implementation makes the seam real, and the discovery pattern has to grow with it.

## Delivery stages

1. The chooser and its lane — `src/gomoku/ai.js`, `src/gomoku/ai.test.js`, and the two evidence commands in `tools/workflow.json`; this lands and is tested with no page at all, as soon as the v1 rules engine exists.
2. The mode on the page — `src/gomoku/index.html` and the browser observation that closes [A2].
