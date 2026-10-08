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

- `src/gomoku/ai.js` — the opponent. A classic script that publishes exactly one global, `GomokuAI`, and hands the same object to Node behind one guarded line, the shape `rules.js` already uses; it touches no DOM. It publishes two functions. `GomokuAI.chooseMove(game)` returns `{ row, col }` for the point the side to move should play, or `null` when the game is finished or the board is full. `GomokuAI.replyPoint(game, mode)` is the page's turn decision, and it is a plain function over the state so that the decision, not the rendering, is what a test can run: `null` in `two-player` mode, `null` once the game is finished, and otherwise the point `chooseMove` returns for the state the page has just placed. Neither function takes an options object — a difficulty setting would be an option with no consumer today — neither mutates the game it is given, and neither plays the point: the page applies every move through `Gomoku.place`, so the rules engine stays the only authority on legality and on who won.
- The chooser decides one ply deep over one candidate list, read in one fixed order: the empty points within two steps of an existing stone, and the centre alone on an empty board, ordered by lowest row first and then lowest column. If the side to move can complete five now, it plays the first candidate that does; otherwise, if the opponent could complete five on their next move, it plays the first candidate that stops that; otherwise it plays the highest-scoring candidate, where a point's score is what the runs it would extend and the runs it would break are worth in each of the four directions, and a tie goes to the earlier candidate in that order. The terminal tests run through `Gomoku.place` on a copy of the game rather than counting a line here, so the win rule keeps one implementation; the counting exists only to rank the points that do not end the game. The chooser reads no clock and no random source, so the same position yields the same point, which is what lets its lane assert exact moves.

The chooser's specified output is the table below. Coordinates are 0-based `(row, col)`, counted from the top-left corner. The weights behind a score are the implementation's; the rows are not — a chooser that moves one of these points is a different chooser. The last two rows are the tie-break: each leaves two points that complete five, so nothing but the order decides between them. In the fifth row the two points share row 7 and the lower column wins; in the sixth they share column 7 and the lower row wins.

| Position | Point to play |
|---|---|
| Black: (7,7); white: (7,3) (7,4) (7,5) (7,6); white to move | (7,2) |
| Black: (7,3) (7,4) (7,5) (7,6); white: (7,2); white to move | (7,7) |
| Black: (7,3) (7,4) (7,6) (7,7); white: (10,10); white to move | (7,5) |
| No stones; either side to move | (7,7) |
| Black: (0,0); white: (7,3) (7,4) (7,5) (7,6); white to move | (7,2) |
| Black: (0,0); white: (3,7) (4,7) (5,7) (6,7); white to move | (2,7) |

- `src/gomoku/ai.test.js` — the lane, run by Node's built-in runner in the shape the v1 record declares for `rules.test.js`: it replays the table above and asserts the turn decision. No `package.json`, and no dependency to install.
- `src/gomoku/index.html` — one mode control with two modes, and no decision of its own. The page keeps the mode and the game, calls `GomokuAI.replyPoint(game, mode)` after every human move, and applies the point it returns through `Gomoku.place`; the reply is computed and applied inside the same click handler, so there is no thinking state, no timer, and no second step for the player to trigger. The status line and the final message name 你 and 电脑 in this mode, and 黑方 and 白方 in the other. Changing the mode empties the board and starts a fresh game, and so does the reset button. The two-player path keeps the behaviour the v1 record pins.
- `tools/workflow.json` — the `tests` and `source` evidence lists gain `node --test src/gomoku/ai.test.js` beside the v1 lane. Listing both commands is the whole fix for the warning the v1 record already carries, that one concrete command on `source` becomes a false green at the second module: the surface is a flat list of commands, so a change to either module runs both lanes.
- `README.md`, `README.zh.md`, and their consistency record — the v1 record adds the page's bullet there; if that bullet describes two players only, this change corrects the wording on both sides and re-records the pair.
- [The v1 record](2026-10-08-core-html-gomoku.md) — its `## Alternatives considered` entry for an AI opponent gains a relative link to this record on both sides, so a reader of either is not left with the other's earlier scope.

Two defaults are settled for v1 and cheap to reverse: the human is black and moves first, and the opponent has one level. Both are revisit conditions in `## Risks`.

## Alternatives considered

**A random legal move.** Rejected: it never blocks a four, so a player who lines up five on the fourth move wins, and the mode would be a demonstration rather than an opponent. It would cost the least, which is exactly why it is worth naming — the cheap version is not worth a mode.

**A minimax search with alpha-beta pruning.** Rejected for v1: a 15×15 board with no candidate restriction branches past what one click can afford, and a search budgeted by time would make the move depend on the machine's speed, so the golden replays would stop pinning anything and the determinism rules in [testing.md](../../../../docs/testing.md) would be broken by the design rather than by a test. A depth-limited search over the same candidate set is the shape a stronger level takes; it is deferred, and it needs a new record because it changes the acceptance criteria.

**An external engine or a library.** Rejected: it adds an install step and a dependency to a page whose shortest path is a double-click on a file, a cost the v1 record already refused once when it ruled out `type="module"` and a server. A vendored search would also carry a second board model and a second win rule to keep in step.

**The heuristic inline in `index.html`.** Rejected: the chooser would then be reachable only through a browser, so its lane would need a browser driver — the same reason the v1 record split the rules out of the page.

**Leaving the turn decision in the click handler, and marking the page observation `unpinned`.** Rejected: it is the smaller change, and it leaves the one decision the page makes — reply once, or not at all — with no evidence when a plain function over the same state can carry it. The rendering that remains is out of a command's reach here either way, and [A3] says so.

**A second page for the mode (`vs-computer.html`).** Rejected: it duplicates the board rendering, the strings map, and the lock-out behaviour, and the copies would drift at the first UI change. One board with a mode control keeps one renderer.

**A random tie-break among equal-scoring points.** Rejected: it makes the same position produce different moves, so the lane cannot assert a move, a player cannot reproduce a game, and a reported bug becomes unreproducible. Variety, if it is ever wanted, belongs in an opening book fed by a seeded source, not in the tie-break.

**A pluggable opponent interface with a capability registry entry.** Rejected: there is one provider and one consumer, and this kit refuses to split preemptively for a hypothetical second implementation. The registry also discovers its markers in `tools/*.py`, so an entry for a JavaScript module would be registered and undiscoverable, and `capability-registry` would reject the pair.

**Letting the chooser decide the win itself.** Rejected: two implementations of one win rule are two facts, and the v1 record already refused that trade when it rejected a Python rewrite of the win check. The chooser asks `Gomoku.place` instead.

## Acceptance criteria

- [A1] `tests` — `node --test src/gomoku/ai.test.js` builds every row of the position table in `## Proposal` from that row's coordinates and turn, and asserts the point the row names, so the golden expectations are transcribed from this record instead of written by whoever implements the chooser. The same lane asserts the properties a table cannot show: a repeated call on one position returns the same point, the call leaves its input game unchanged, and every point returned is a legal intersection. A chooser that moves any row's point turns the lane red.
- [A2] `tests` — the same lane covers the page's turn decision that `## Proposal` puts in `GomokuAI.replyPoint(game, mode)`: on an unfinished game in `vs-computer` mode it returns exactly one legal point, in `two-player` mode it returns `null`, and after a win or a draw it returns `null`. The page has no other way to decide whether to reply; what it then does with the answer is [A3]'s subject.
- [A3] `source` — `unpinned`: from `file://`, with no server and no network request, `src/gomoku/index.html` shows the board, the 你/电脑 strings in this mode, keyboard-reachable intersections, a mode change that empties the board, and the point [A2] returns applied exactly once per human move. The reason it is unpinned: this repository runs no browser driver — the v1 record refused Playwright and a served page — so the observation is manual, and a manual entry is never counted as verified.
- [A4] `i18n` — `python3 tools/pair-docs.py --check` reports this record's three siblings complete and in step, keeps the v1 pair level after its cross-link edit, and resolves the links between the two records.
- [A5] `workflow` — `tools/workflow.json` declares `node --test src/gomoku/ai.test.js` as runnable evidence on the `tests` and `source` surfaces beside the v1 lane, so `python3 tools/run-evidence.py --check` resolves both and a run records PASS or FAIL instead of a manual entry.
- [A6] `decisions` — reading both records shows the dependency from either side: the v1 record's AI alternative links to this record, and this record's `## Problem` links to the v1 record.

## Risks

- One ply is the whole opponent: it wins a five and blocks a five, and it ranks points by what they build, but it does not search a combination, so a player who creates two threats in one move wins. Revisit when a stronger opponent is asked for; that is a new record, because it changes the table and [A2].
- The opponent has one level, and `chooseMove` takes no options, because a single level has no consumer for one. Revisit when a second level is asked for: the option arrives with the level that consumes it.
- The human is always black. Revisit when someone asks to play second: the mode control grows a second dimension, the board has to apply the opening reply, and the chooser's empty-board centre becomes reachable from the page.
- There is no take-back. Revisit with a record of its own: in this mode one undo has to remove two stones, or the player would take back a stone and the reply that answered it separately.
- The reply is computed inside the click handler, which holds only while one reply costs less than a frame. A stronger chooser has to move to a deferred path with an explicit locked state, and [A3]'s observation changes with it.
- Determinism is a constraint on the chooser, not a property it happens to have: no clock and no random source. An opening that varied would have to arrive through a seeded source passed in at the call site, or the golden replays stop pinning anything.
- Load order is now a dependency: the page must load `rules.js` before `ai.js`, and `ai.test.js` requires both. A page that loads the chooser alone throws when the first reply is computed.
- The `source` surface now runs both lanes for any source change, and a third module makes that a false green again: the list then has to split or become a per-module map.
- The chooser is not a registered capability: one provider, one consumer, and the registry discovers its markers only in `tools/*.py`. A second opponent implementation makes the seam real, and the discovery pattern has to grow with it.
- The interface this record consumes belongs to a record that has not landed: v1 is `proposed` too. If the rules engine lands with a different contract — another return shape for `place`, another argument, another index base — the lines in `## Proposal` that cite it are corrected in the same change. No gate goes red on that drift: `agent-input-links` resolves links and `decision-proposed` checks sections, and neither reads an identifier.
- Stage 2's visual and interaction half ([A3]) has exactly one evidence slot, the `source` surface, and that slot still holds the repository's placeholder — the entry the v1 record promises to replace. Until it holds a real command, or the observation is accepted as permanently manual, whether stage 2 is finished cannot be decided.

## Delivery stages

1. The chooser, the turn decision, and their lane — `src/gomoku/ai.js` (`chooseMove` and `replyPoint`), `src/gomoku/ai.test.js`, and the two evidence commands in `tools/workflow.json`; this lands and is tested with no page at all, as soon as the v1 rules engine exists.
2. The mode on the page — `src/gomoku/index.html` and the manual observation that [A3] records as `unpinned`.
