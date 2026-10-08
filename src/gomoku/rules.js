/*
 * The Gomoku rules engine: the one authority on legality and on who won.
 *
 * A classic script, not an ES module, because a browser refuses `type="module"` imports
 * over `file://` — the page's origin is `null` — and this page has to be openable by
 * double-clicking it. The tail of this file hands the same object to Node for its lane,
 * and publishes it as a single browser global otherwise.
 *
 * Vocabulary of a game object, `{ size, board, turn, winner, moves }`:
 *   board   `size * size` cells, row-major, each `null`, `"black"`, or `"white"`
 *   turn    `"black"` or `"white"` — the side to move; once a game is finished it is the
 *           side that moved last, because nobody moves next
 *   winner  `null` while the game is unfinished, else `"black"`, `"white"`, or `"draw"`
 *   moves   the stones in play order, each `{ row, col, player }`
 *
 * `place` is the only thing that decides an outcome. It checks the four lines through the
 * point just played, so a move costs the length of those lines and not the board.
 */
(function (global) {
  "use strict";

  var SIZE = 15;
  var BLACK = "black";
  var WHITE = "white";
  var DRAW = "draw";
  var RUN = 5;

  // The four axes a line can run along. `[1, -1]` walks down-left, which covers the
  // up-right direction in the same pass.
  var AXES = [
    [0, 1],
    [1, 0],
    [1, 1],
    [1, -1],
  ];

  function isPoint(size, row, col) {
    return (
      Number.isInteger(row) &&
      Number.isInteger(col) &&
      row >= 0 &&
      row < size &&
      col >= 0 &&
      col < size
    );
  }

  function other(player) {
    return player === BLACK ? WHITE : BLACK;
  }

  function runThrough(board, size, row, col, player, dr, dc) {
    var run = 1;
    var r;
    var c;
    for (r = row + dr, c = col + dc; isPoint(size, r, c) && board[r * size + c] === player; r += dr, c += dc) {
      run += 1;
    }
    for (r = row - dr, c = col - dc; isPoint(size, r, c) && board[r * size + c] === player; r -= dr, c -= dc) {
      run += 1;
    }
    return run;
  }

  function completesFive(board, size, row, col, player) {
    for (var i = 0; i < AXES.length; i += 1) {
      if (runThrough(board, size, row, col, player, AXES[i][0], AXES[i][1]) >= RUN) {
        return true;
      }
    }
    return false;
  }

  function start(size) {
    var width = size === undefined ? SIZE : size;
    return {
      size: width,
      board: new Array(width * width).fill(null),
      turn: BLACK,
      winner: null,
      moves: [],
    };
  }

  function place(game, row, col) {
    if (game.winner !== null) {
      return { ok: false, reason: "finished" };
    }
    if (!isPoint(game.size, row, col)) {
      return { ok: false, reason: "out-of-range" };
    }
    var at = row * game.size + col;
    if (game.board[at] !== null) {
      return { ok: false, reason: "occupied" };
    }

    var player = game.turn;
    var board = game.board.slice();
    var moves = game.moves.concat([{ row: row, col: col, player: player }]);
    board[at] = player;

    var outcome = null;
    if (completesFive(board, game.size, row, col, player)) {
      outcome = player;
    } else if (moves.length === game.size * game.size) {
      outcome = DRAW;
    }

    return {
      ok: true,
      game: {
        size: game.size,
        board: board,
        turn: outcome === null ? other(player) : player,
        winner: outcome,
        moves: moves,
      },
    };
  }

  function winner(game) {
    return game.winner;
  }

  var Gomoku = {
    SIZE: SIZE,
    start: start,
    place: place,
    winner: winner,
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = Gomoku;
  } else {
    global.Gomoku = Gomoku;
  }
})(typeof globalThis !== "undefined" ? globalThis : this);
