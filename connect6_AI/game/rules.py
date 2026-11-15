"""Win detection for Connect-6.

Both functions accept a :class:`game.board.Board` or a plain nested list
(``board[row][col]``) so they can also be used by the heuristic code that
works directly on grids.
"""

from .constants import BLACK, DIRECTIONS, WHITE, WIN_LENGTH


def _grid(board):
    """Return the underlying nested-list grid for a Board or raw grid."""
    return board.grid if hasattr(board, "grid") else board


def _size(board) -> int:
    """Return the board side length for a Board or raw grid."""
    return board.n if hasattr(board, "n") else len(_grid(board))


def find_winning_line(board, r: int, c: int, player: int, target: int = WIN_LENGTH):
    """Return the winning line through ``(r, c)``, or ``None``.

    Only the four axes through the last placed stone are inspected, so this
    is O(1) with respect to the board size.  The returned list contains every
    consecutive stone on the winning axis (so a run of 7 returns 7 cells),
    ordered from one end of the line to the other.
    """
    if player not in (BLACK, WHITE) or target < 1:
        return None

    grid = _grid(board)
    n = _size(board)

    if not (isinstance(r, int) and isinstance(c, int)):
        return None
    if not (0 <= r < n and 0 <= c < n):
        return None
    if grid[r][c] != player:
        return None

    for dr, dc in DIRECTIONS:
        line = [(r, c)]

        for sign in (1, -1):
            rr = r + dr * sign
            cc = c + dc * sign
            while 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == player:
                line.append((rr, cc))
                rr += dr * sign
                cc += dc * sign

        if len(line) >= target:
            # Sort along the direction vector.  This works for all four
            # directions, including the anti-diagonal (1, -1).
            line.sort(key=lambda cell: cell[0] * dr + cell[1] * dc)
            return line

    return None


def check_win(board, r: int, c: int, player: int, target: int = WIN_LENGTH) -> bool:
    """Return ``True`` when the stone at ``(r, c)`` completes a line."""
    return find_winning_line(board, r, c, player, target=target) is not None
