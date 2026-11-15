"""Mutable Connect-6 game state and turn handling."""

from .board import Board
from .constants import BLACK, EMPTY, WHITE
from .rules import check_win


class GameState:
    """Complete state of one Connect-6 game.

    Turn rules
    ----------
    Black places 1 stone on the first turn.  Every later turn consists of 2
    stones for the player whose turn it is.  A win ends the game immediately,
    even when it happens on the first stone of a two-stone turn.
    """

    def __init__(self, n: int = 19):
        self.board = Board(n)
        self.current_player = BLACK
        self.stones_left = 1
        self.winner = None
        self.history = []

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    @property
    def n(self) -> int:
        """Board side length."""
        return self.board.n

    @property
    def size(self) -> int:
        """Alias for :attr:`n`."""
        return self.board.n

    @property
    def game_over(self) -> bool:
        """Alias for :meth:`is_over`."""
        return self.is_over()

    @property
    def last_move(self):
        """The most recently placed ``(row, column)``, or ``None``."""
        if not self.history:
            return None
        return (self.history[-1][0], self.history[-1][1])

    def is_over(self) -> bool:
        """Return ``True`` after a win or when the board is full."""
        return self.winner is not None or self.board.is_full()

    def legal_moves(self):
        """Return every empty cell as a list of ``(row, column)`` pairs."""
        n = self.board.n
        return [
            (r, c)
            for r in range(n)
            for c in range(n)
            if self.board.grid[r][c] == EMPTY
        ]

    def get_candidate_moves(self, radius: int = 2):
        """Return empty cells within ``radius`` of any existing stone.

        Distance is Chebyshev distance (a square neighbourhood), which is the
        usual choice for board-game move generation.  On an empty board the
        single centre cell is returned.
        """
        if isinstance(radius, bool) or not isinstance(radius, int) or radius < 0:
            raise ValueError("radius must be a non-negative integer")

        n = self.board.n
        if self.board.stone_count == 0:
            return [(n // 2, n // 2)]

        grid = self.board.grid
        candidates = set()

        for r in range(n):
            for c in range(n):
                if grid[r][c] == EMPTY:
                    continue

                row_start = max(0, r - radius)
                row_end = min(n, r + radius + 1)
                col_start = max(0, c - radius)
                col_end = min(n, c + radius + 1)

                for rr in range(row_start, row_end):
                    for cc in range(col_start, col_end):
                        if grid[rr][cc] == EMPTY:
                            candidates.add((rr, cc))

        return sorted(candidates)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def play(self, r: int, c: int) -> None:
        """Place the current player's stone at ``(r, c)``.

        Raises :class:`ValueError` if the game is over, the coordinate is out
        of bounds, or the cell is occupied.  A failed move leaves the state
        completely unchanged.
        """
        if self.is_over():
            raise ValueError("Game is already over")
        if not self.board.is_inside(r, c):
            raise ValueError(f"Move ({r}, {c}) is outside the board")
        if not self.board.is_empty(r, c):
            raise ValueError(f"Cell ({r}, {c}) is already occupied")

        player = self.current_player
        snapshot = (r, c, player, self.stones_left, self.winner)

        # The move has been validated, so place it and record the snapshot.
        self.board.place(r, c, player)
        self.history.append(snapshot)

        if check_win(self.board, r, c, player):
            self.winner = player
            return

        self.stones_left -= 1
        if self.stones_left == 0:
            self.current_player = WHITE if player == BLACK else BLACK
            self.stones_left = 2

    def undo(self) -> None:
        """Undo the most recent stone and restore the complete previous state.

        Raises :class:`IndexError` when there is nothing to undo.
        """
        if not self.history:
            raise IndexError("No moves to undo")

        r, c, player, stones_left, winner = self.history.pop()
        self.board.remove(r, c)
        self.current_player = player
        self.stones_left = stones_left
        self.winner = winner

    def play_move(self, r: int, c: int, player=None) -> bool:
        """Boolean-returning compatibility wrapper around :meth:`play`.

        If ``player`` is supplied it must match the current player.  New code
        should call :meth:`play`, which raises on illegal moves.
        """
        if player is not None and player != self.current_player:
            return False
        try:
            self.play(r, c)
        except ValueError:
            return False
        return True

    def copy(self) -> "GameState":
        """Return an independent copy of this game state."""
        clone = GameState.__new__(GameState)
        clone.board = self.board.copy()
        clone.current_player = self.current_player
        clone.stones_left = self.stones_left
        clone.winner = self.winner
        clone.history = list(self.history)
        return clone

    def __str__(self) -> str:
        return str(self.board)

    def __repr__(self) -> str:
        return (
            f"GameState(n={self.n}, current_player={self.current_player}, "
            f"stones_left={self.stones_left}, winner={self.winner})"
        )
