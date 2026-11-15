"""Board representation for Connect-6.

The :class:`Board` class is the canonical board API.  The module also keeps
the small functional helpers that the existing interface/tests use
(``create_board``, ``make_move``, ``is_valid_move``, ``check_winner`` and
``display_board``) so old callers keep working.

Coordinates are 0-indexed ``(row, column)`` pairs, with ``(0, 0)`` at the
top-left.
"""

from .constants import BLACK, EMPTY, SYMBOLS, WHITE, WIN_LENGTH
from .rules import check_win, find_winning_line


class Board:
    """A square Connect-6 board.

    Parameters
    ----------
    n:
        Board side length.  It must be at least :data:`WIN_LENGTH` (6).
    """

    def __init__(self, n: int = 19):
        if isinstance(n, bool) or not isinstance(n, int):
            raise ValueError("Board size must be an integer")
        if n < WIN_LENGTH:
            raise ValueError(f"Board size must be at least {WIN_LENGTH}")

        self.n = n
        self.grid = [[EMPTY] * n for _ in range(n)]
        self.stone_count = 0

    # ------------------------------------------------------------------
    # Basic queries
    # ------------------------------------------------------------------
    def is_inside(self, r: int, c: int) -> bool:
        """Return ``True`` when ``(r, c)`` is a valid board coordinate."""
        return (
            isinstance(r, int)
            and isinstance(c, int)
            and 0 <= r < self.n
            and 0 <= c < self.n
        )

    def is_empty(self, r: int, c: int) -> bool:
        """Return ``True`` when ``(r, c)`` is inside the board and empty."""
        return self.is_inside(r, c) and self.grid[r][c] == EMPTY

    def is_full(self) -> bool:
        """Return ``True`` when every cell is occupied."""
        return self.stone_count >= self.n * self.n

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def place(self, r: int, c: int, player: int) -> None:
        """Place ``player`` at ``(r, c)``.

        Raises :class:`ValueError` for an invalid player, an out-of-bounds
        coordinate, or an occupied cell.
        """
        if player not in (BLACK, WHITE):
            raise ValueError(f"Invalid player: {player!r}")
        if not self.is_inside(r, c):
            raise ValueError(f"Move ({r}, {c}) is outside the board")
        if self.grid[r][c] != EMPTY:
            raise ValueError(f"Cell ({r}, {c}) is already occupied")

        self.grid[r][c] = player
        self.stone_count += 1

    def remove(self, r: int, c: int) -> int:
        """Remove and return the stone at ``(r, c)``.

        Raises :class:`ValueError` when the coordinate is invalid or the cell
        is already empty.
        """
        if not self.is_inside(r, c):
            raise ValueError(f"Cell ({r}, {c}) is outside the board")
        if self.grid[r][c] == EMPTY:
            raise ValueError(f"Cell ({r}, {c}) is already empty")

        player = self.grid[r][c]
        self.grid[r][c] = EMPTY
        self.stone_count -= 1
        return player

    def copy(self) -> "Board":
        """Return an independent copy of this board."""
        clone = Board.__new__(Board)
        clone.n = self.n
        clone.grid = [row[:] for row in self.grid]
        clone.stone_count = self.stone_count
        return clone

    # ------------------------------------------------------------------
    # Convenience / compatibility helpers
    # ------------------------------------------------------------------
    def __getitem__(self, index):
        """Allow ``board[row][column]`` access, like a nested list."""
        return self.grid[index]

    def __len__(self) -> int:
        """Board side length (so a Board can be used like a grid)."""
        return self.n

    def __iter__(self):
        """Iterate over rows (so ``for row in board`` works)."""
        return iter(self.grid)

    def __str__(self) -> str:
        return "\n".join(
            " ".join(SYMBOLS[cell] for cell in row) for row in self.grid
        )

    def __repr__(self) -> str:
        return f"Board(n={self.n}, stones={self.stone_count})"


# ----------------------------------------------------------------------
# Functional compatibility API
# ----------------------------------------------------------------------
def create_board(size: int = 19) -> Board:
    """Create a board (legacy helper; returns a :class:`Board`)."""
    return Board(size)


def display_board(board) -> None:
    """Print a board in the terminal."""
    if isinstance(board, Board):
        print(board)
        return

    print(
        "\n".join(
            " ".join(SYMBOLS.get(cell, str(cell)) for cell in row)
            for row in board
        )
    )


def is_valid_move(board, row: int, col: int) -> bool:
    """Return ``True`` when a stone can be placed at ``(row, col)``."""
    if isinstance(board, Board):
        return board.is_inside(row, col) and board.is_empty(row, col)

    size = len(board)
    return (
        isinstance(row, int)
        and isinstance(col, int)
        and 0 <= row < size
        and 0 <= col < size
        and board[row][col] == EMPTY
    )


def make_move(board, row: int, col: int, player: int) -> bool:
    """Place a stone and return whether the move was successful.

    This is the boolean-returning legacy helper.  New code should normally
    use :meth:`Board.place` or :meth:`game.game_state.GameState.play`, which
    raise :class:`ValueError` on illegal moves.
    """
    if player not in (BLACK, WHITE):
        return False
    if not is_valid_move(board, row, col):
        return False

    if isinstance(board, Board):
        board.place(row, col, player)
    else:
        board[row][col] = player
    return True


def check_winner(board, row: int, col: int, player: int, target: int = WIN_LENGTH) -> bool:
    """Legacy alias for :func:`game.rules.check_win`."""
    return check_win(board, row, col, player, target=target)
