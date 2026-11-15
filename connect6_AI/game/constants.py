"""Shared constants for the Connect-6 game package.

Coordinates are 0-indexed ``(row, column)`` pairs with ``(0, 0)`` at the
top-left of the board.
"""

EMPTY = 0
BLACK = 1
WHITE = 2

#: Number of stones that must be connected to win.
WIN_LENGTH = 6

#: The four axes on which a win can happen: horizontal, vertical and the two
#: diagonals.  Each entry is ``(row_delta, column_delta)``.
DIRECTIONS = [
    (0, 1),
    (1, 0),
    (1, 1),
    (1, -1),
]

PLAYER_NAMES = {
    BLACK: "Black",
    WHITE: "White",
}

SYMBOLS = {
    EMPTY: ".",
    BLACK: "X",
    WHITE: "O",
}
