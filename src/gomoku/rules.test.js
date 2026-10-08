/*
 * The rules engine's lane: the golden replays that decide whether `rules.js` still plays
 * the game this repository promised. Every expectation here is a point sequence and the
 * outcome it must reach, so the test reads as a game rather than as a unit of code.
 *
 *   node --test src/gomoku/rules.test.js
 */
"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");

const Gomoku = require("./rules.js");

const BLACK = "black";
const WHITE = "white";
const DRAW = "draw";

/**
 * Play `points` in order, in one game, asserting that each one lands. A point that the
 * engine refuses fails here with the reason, which is what makes an accidental five in
 * the middle of a long fill visible instead of silent.
 */
function play(game, points) {
  return points.reduce((current, [row, col]) => {
    const moved = Gomoku.place(current, row, col);
    assert.equal(
      moved.ok,
      true,
      `expected (${row}, ${col}) to be playable, but the engine said ${moved.reason}`,
    );
    return moved.game;
  }, game);
}

// Each line ends in the black stone that completes it. White's four stones are spaced
// two apart on purpose: a filler that made a line of its own would end the game early.
const WIN_LINES = [
  ["horizontal", [[7, 3], [0, 0], [7, 4], [0, 2], [7, 5], [0, 4], [7, 6], [0, 6], [7, 7]]],
  ["vertical", [[3, 7], [0, 0], [4, 7], [0, 2], [5, 7], [0, 4], [6, 7], [0, 6], [7, 7]]],
  ["down-right diagonal", [[3, 3], [0, 0], [4, 4], [0, 2], [5, 5], [0, 4], [6, 6], [0, 6], [7, 7]]],
  ["up-right diagonal", [[7, 3], [0, 0], [6, 4], [0, 2], [5, 5], [0, 4], [4, 6], [0, 6], [3, 7]]],
];

for (const [name, points] of WIN_LINES) {
  test(`five in a row wins along the ${name}`, () => {
    const won = play(Gomoku.start(), points);
    assert.equal(Gomoku.winner(won), BLACK);
    assert.equal(won.turn, BLACK, "nobody moves after the winning move, so the turn stays put");
  });
}

test("the default board is 15 x 15 and black moves first", () => {
  const game = Gomoku.start();
  assert.equal(Gomoku.SIZE, 15);
  assert.equal(game.size, Gomoku.SIZE);
  assert.equal(game.board.length, 225);
  assert.equal(game.board.every((cell) => cell === null), true);
  assert.deepEqual(game.moves, []);
  assert.equal(game.turn, BLACK);
  assert.equal(Gomoku.winner(game), null);
});

test("the turns alternate while the game is unfinished", () => {
  const afterBlack = play(Gomoku.start(), [[7, 7]]);
  assert.equal(afterBlack.turn, WHITE);
  assert.equal(afterBlack.moves.length, 1);
  assert.deepEqual(afterBlack.moves[0], { row: 7, col: 7, player: BLACK });
  assert.equal(play(afterBlack, [[0, 0]]).turn, BLACK);
});

test("an overline of six wins", () => {
  // Black holds four in a row and a loose stone; the Stone at (7, 7) joins them into six.
  const won = play(Gomoku.start(), [
    [7, 3], [0, 0], [7, 4], [0, 2], [7, 5], [0, 4], [7, 6], [0, 6], [7, 8], [0, 8], [7, 7],
  ]);
  assert.equal(Gomoku.winner(won), BLACK);
});

test("a gapped four does not win", () => {
  const fourWithAGap = [
    [7, 3], [0, 0], [7, 4], [0, 2], [7, 5], [0, 4], [7, 7], [0, 6],
  ];
  const game = play(Gomoku.start(), fourWithAGap);
  assert.equal(Gomoku.winner(game), null, "four stones spanning five points are not five in a row");
  const stillOpen = play(game, [[10, 10]]);
  assert.equal(Gomoku.winner(stillOpen), null, "a move elsewhere does not close the gap either");
});

test("a stone already on the board is refused", () => {
  const game = play(Gomoku.start(), [[7, 7], [0, 0]]);
  const before = JSON.stringify(game);
  const taken = Gomoku.place(game, 7, 7);
  assert.deepEqual(taken, { ok: false, reason: "occupied" });
  assert.equal(JSON.stringify(game), before);
});

test("a point off the board is refused", () => {
  const game = Gomoku.start();
  for (const [row, col] of [[-1, 0], [15, 0], [0, 15], [1.5, 0], ["3", 0]]) {
    assert.deepEqual(
      Gomoku.place(game, row, col),
      { ok: false, reason: "out-of-range" },
      `(${row}, ${col}) is not an intersection`,
    );
  }
});

test("a move after the game is finished is refused", () => {
  const won = play(Gomoku.start(), WIN_LINES[0][1]);
  assert.equal(Gomoku.winner(won), BLACK);
  assert.deepEqual(Gomoku.place(won, 0, 1), { ok: false, reason: "finished" });
});

test("a full board with no five in it is a draw", () => {
  // A two-colouring with no run longer than two in any of the four directions: the band
  // `(row + 2 * col) % 4` advances by 1 vertically, 2 horizontally and 3 (or -1) along
  // the diagonals, so no axis can hand five stones of one colour in a row.
  const size = Gomoku.SIZE;
  const black = [];
  const white = [];
  for (let row = 0; row < size; row += 1) {
    for (let col = 0; col < size; col += 1) {
      ((row + 2 * col) % 4 < 2 ? black : white).push([row, col]);
    }
  }
  assert.equal(
    black.length - white.length,
    1,
    "an odd board can be filled alternately only when black holds exactly one more point",
  );

  let game = Gomoku.start();
  for (let i = 0; i < black.length; i += 1) {
    game = play(game, [black[i]]);
    if (i < white.length) {
      game = play(game, [white[i]]);
    }
  }
  assert.equal(game.moves.length, size * size);
  assert.equal(Gomoku.winner(game), DRAW);
});

test("place returns a new game and leaves the one it was given alone", () => {
  const before = play(Gomoku.start(), [[7, 7], [0, 0]]);
  const snapshot = JSON.stringify(before);
  const moved = Gomoku.place(before, 7, 8);

  assert.equal(moved.ok, true);
  assert.equal(JSON.stringify(before), snapshot, "the game passed in was mutated");
  assert.notEqual(moved.game, before);
  assert.notEqual(moved.game.board, before.board, "the board array is shared between the two games");
  assert.equal(before.board[7 * Gomoku.SIZE + 8], null);
  assert.equal(moved.game.board[7 * Gomoku.SIZE + 8], BLACK);
});
