"""Connect-6 rules and state package.

This package is intentionally independent of ``ai`` and ``interface``.  It
exposes the public API used by the rest of the project::

    from game import GameState, Board, check_win, find_winning_line
"""

from .constants import (
    BLACK,
    DIRECTIONS,
    EMPTY,
    PLAYER_NAMES,
    SYMBOLS,
    WHITE,
    WIN_LENGTH,
)
from .board import (
    Board,
    check_winner,
    create_board,
    display_board,
    is_valid_move,
    make_move,
)
from .rules import check_win, find_winning_line
from .game_state import GameState

__all__ = [
    "EMPTY",
    "BLACK",
    "WHITE",
    "WIN_LENGTH",
    "DIRECTIONS",
    "PLAYER_NAMES",
    "SYMBOLS",
    "Board",
    "GameState",
    "check_win",
    "find_winning_line",
    # Legacy functional API
    "create_board",
    "display_board",
    "is_valid_move",
    "make_move",
    "check_winner",
]
