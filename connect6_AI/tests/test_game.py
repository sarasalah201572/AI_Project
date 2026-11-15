"""Tests for the ``game`` package: board, rules, state, turn and undo rules."""

import ast
import pathlib

import pytest

import game
from game import (
    BLACK,
    DIRECTIONS,
    EMPTY,
    WHITE,
    WIN_LENGTH,
    Board,
    GameState,
    check_win,
    find_winning_line,
)


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def board_with(black=(), white=(), n=9):
    board = Board(n)
    for r, c in black:
        board.place(r, c, BLACK)
    for r, c in white:
        board.place(r, c, WHITE)
    return board


def state_with(black=(), white=(), n=9, current_player=BLACK, stones_left=1):
    state = GameState(n)
    for r, c in black:
        state.board.place(r, c, BLACK)
    for r, c in white:
        state.board.place(r, c, WHITE)
    state.current_player = current_player
    state.stones_left = stones_left
    return state


def snapshot(state):
    return (
        [row[:] for row in state.board.grid],
        state.current_player,
        state.stones_left,
        state.winner,
        list(state.history),
    )


# ----------------------------------------------------------------------
# Constants and board basics
# ----------------------------------------------------------------------
def test_constants():
    assert EMPTY == 0
    assert BLACK == 1
    assert WHITE == 2
    assert WIN_LENGTH == 6
    assert len(DIRECTIONS) == 4
    assert set(DIRECTIONS) == {(0, 1), (1, 0), (1, 1), (1, -1)}


@pytest.mark.parametrize("n", [6, 9, 13, 19])
def test_variable_board_sizes_work(n):
    board = Board(n)
    assert board.n == n
    assert len(board.grid) == n
    assert all(len(row) == n for row in board.grid)
    assert board.stone_count == 0

    state = GameState(n)
    assert state.board.n == n
    assert state.n == n
    assert state.size == n


@pytest.mark.parametrize("n", [5, 0, -1])
def test_board_size_below_win_length_raises(n):
    with pytest.raises(ValueError):
        Board(n)
    with pytest.raises(ValueError):
        GameState(n)


@pytest.mark.parametrize("n", ["9", 9.5, True, None])
def test_non_integer_board_size_raises(n):
    with pytest.raises(ValueError):
        Board(n)
    with pytest.raises(ValueError):
        GameState(n)


def test_board_queries_and_mutation():
    board = Board(6)
    assert board.stone_count == 0
    assert not board.is_full()
    assert board.is_inside(0, 0)
    assert board.is_inside(5, 5)
    assert not board.is_inside(-1, 0)
    assert not board.is_inside(0, 6)
    assert board.is_empty(2, 3)

    board.place(2, 3, BLACK)
    assert board.grid[2][3] == BLACK
    assert board[2][3] == BLACK
    assert board.stone_count == 1
    assert not board.is_empty(2, 3)

    assert board.remove(2, 3) == BLACK
    assert board.is_empty(2, 3)
    assert board.stone_count == 0

    board.place(0, 0, BLACK)
    board.place(0, 1, WHITE)
    text = str(board)
    assert "X" in text
    assert "O" in text
    assert "." in text


def test_board_rejects_illegal_placements_and_removals():
    board = Board(6)
    board.place(0, 0, BLACK)

    with pytest.raises(ValueError):
        board.place(0, 0, WHITE)  # occupied
    with pytest.raises(ValueError):
        board.place(-1, 0, BLACK)  # out of bounds
    with pytest.raises(ValueError):
        board.place(0, 6, BLACK)  # out of bounds
    with pytest.raises(ValueError):
        board.place(1, 1, 3)  # invalid player
    with pytest.raises(ValueError):
        board.remove(1, 1)  # already empty
    with pytest.raises(ValueError):
        board.remove(9, 9)  # out of bounds


def test_board_copy_is_independent():
    board = Board(9)
    board.place(4, 4, BLACK)
    clone = board.copy()
    clone.place(3, 3, WHITE)

    assert board.is_empty(3, 3)
    assert not clone.is_empty(3, 3)
    assert board.stone_count == 1
    assert clone.stone_count == 2


# ----------------------------------------------------------------------
# Turn rules and legal moves
# ----------------------------------------------------------------------
def test_first_turn_is_one_stone_then_two_per_turn():
    state = GameState(9)
    assert state.current_player == BLACK
    assert state.stones_left == 1

    state.play(0, 0)  # Black's single opening stone
    assert state.current_player == WHITE
    assert state.stones_left == 2

    state.play(1, 1)  # White's first stone
    assert state.current_player == WHITE
    assert state.stones_left == 1

    state.play(1, 2)  # White's second stone
    assert state.current_player == BLACK
    assert state.stones_left == 2

    state.play(2, 1)  # Black's first stone
    assert state.current_player == BLACK
    assert state.stones_left == 1

    state.play(2, 2)  # Black's second stone
    assert state.current_player == WHITE
    assert state.stones_left == 2


def test_legal_moves_are_all_empty_cells():
    state = GameState(9)
    moves = state.legal_moves()
    assert len(moves) == 81
    assert (4, 4) in moves

    state.play(4, 4)
    moves = state.legal_moves()
    assert len(moves) == 80
    assert (4, 4) not in moves
    assert all(state.board.is_empty(r, c) for r, c in moves)


@pytest.mark.parametrize("n, centre", [(6, (3, 3)), (9, (4, 4)), (19, (9, 9))])
def test_candidate_moves_center_on_empty_board(n, centre):
    assert GameState(n).get_candidate_moves() == [centre]


def test_candidate_moves_are_near_stones_and_empty():
    state = GameState(9)
    state.play(4, 4)  # Black's first stone

    radius_one = state.get_candidate_moves(radius=1)
    expected_one = {
        (r, c) for r in range(3, 6) for c in range(3, 6)
    } - {(4, 4)}
    assert set(radius_one) == expected_one
    assert all(state.board.is_empty(r, c) for r, c in radius_one)

    radius_two = state.get_candidate_moves(radius=2)
    expected_two = {
        (r, c) for r in range(2, 7) for c in range(2, 7)
    } - {(4, 4)}
    assert set(radius_two) == expected_two

    # Add a far-away stone: candidates now include its neighbourhood too.
    state.board.place(0, 0, WHITE)
    moves = set(state.get_candidate_moves(radius=1))
    assert {(0, 1), (1, 0), (1, 1), (4, 3), (3, 4)} <= moves
    assert (8, 8) not in moves
    assert (4, 4) not in moves


def test_candidate_moves_radius_validation():
    with pytest.raises(ValueError):
        GameState(9).get_candidate_moves(radius=-1)
    with pytest.raises(ValueError):
        GameState(9).get_candidate_moves(radius=1.5)

    state = GameState(9)
    state.play(4, 4)
    assert state.get_candidate_moves(radius=0) == []


# ----------------------------------------------------------------------
# Win detection
# ----------------------------------------------------------------------
@pytest.mark.parametrize(
    "stones, probe",
    [
        ([(0, c) for c in range(6)], (0, 0)),       # top edge, horizontal
        ([(5, c) for c in range(6)], (5, 5)),       # bottom edge, horizontal
        ([(r, 0) for r in range(6)], (5, 0)),       # left edge, vertical
        ([(r, 5) for r in range(6)], (0, 5)),       # right edge, vertical
        ([(i, i) for i in range(6)], (0, 0)),       # main diagonal, corner
        ([(i, 5 - i) for i in range(6)], (0, 5)),   # anti-diagonal, corner
    ],
)
def test_win_in_all_directions_at_edges_and_corners(stones, probe):
    board = board_with(black=stones, n=6)
    assert check_win(board, *probe, BLACK)

    line = find_winning_line(board, *probe, BLACK)
    assert line is not None
    assert len(line) == 6
    assert all(board.grid[r][c] == BLACK for r, c in line)


def test_five_in_a_row_is_not_a_win():
    board = board_with(black=[(2, c) for c in range(5)], n=9)
    assert not check_win(board, 2, 4, BLACK)
    assert find_winning_line(board, 2, 4, BLACK) is None


def test_seven_or_more_in_a_row_is_a_win():
    board = board_with(black=[(2, c) for c in range(7)], n=9)
    assert check_win(board, 2, 3, BLACK)

    line = find_winning_line(board, 2, 3, BLACK)
    assert line is not None
    assert len(line) == 7


def test_check_win_only_uses_the_given_last_stone():
    board = board_with(black=[(2, c) for c in range(6)], n=9)
    assert check_win(board, 2, 0, BLACK)
    assert not check_win(board, 2, 6, BLACK)  # empty cell
    assert not check_win(board, 4, 0, BLACK)  # different row


def test_find_winning_line_returns_ordered_cells():
    board = board_with(black=[(2, c) for c in range(1, 7)], n=9)
    assert find_winning_line(board, 2, 3, BLACK) == [
        (2, c) for c in range(1, 7)
    ]

    board = board_with(
        black=[(1, 5), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)],
        n=9,
    )
    assert find_winning_line(board, 3, 3, BLACK) == [
        (1, 5),
        (2, 4),
        (3, 3),
        (4, 2),
        (5, 1),
        (6, 0),
    ]


def test_game_state_detects_win_from_real_turns():
    state = GameState(10)
    moves = [
        (2, 0),                 # Black: opening stone
        (9, 9), (9, 8),         # White
        (2, 1), (2, 2),         # Black
        (8, 9), (8, 8),         # White
        (2, 3), (2, 4),         # Black
        (7, 9), (7, 8),         # White
        (2, 5),                 # Black wins on first stone of the turn
    ]
    for r, c in moves:
        state.play(r, c)

    assert state.winner == BLACK
    assert state.is_over()


def test_win_on_first_stone_of_two_stone_turn_ends_game_immediately():
    state = state_with(
        white=[(2, c) for c in range(5)],
        current_player=WHITE,
        stones_left=2,
    )
    state.play(2, 5)

    assert state.winner == WHITE
    assert state.is_over()
    assert state.current_player == WHITE
    assert state.stones_left == 2  # turn did not continue

    with pytest.raises(ValueError):
        state.play(3, 3)


def test_win_on_second_stone_of_two_stone_turn_ends_game():
    state = state_with(
        white=[(2, c) for c in range(4)],
        current_player=WHITE,
        stones_left=2,
    )

    state.play(2, 4)
    assert state.winner is None
    assert state.stones_left == 1

    state.play(2, 5)
    assert state.winner == WHITE
    assert state.is_over()


# ----------------------------------------------------------------------
# Illegal moves
# ----------------------------------------------------------------------
def test_occupied_move_raises_and_leaves_state_unchanged():
    state = GameState(9)
    state.play(4, 4)
    before = snapshot(state)

    with pytest.raises(ValueError):
        state.play(4, 4)

    assert snapshot(state) == before


@pytest.mark.parametrize(
    "r, c",
    [(-1, 0), (0, -1), (9, 0), (0, 9), (1.5, 2), ("a", 1), (None, 2)],
)
def test_out_of_bounds_or_non_integer_move_raises_and_leaves_state_unchanged(r, c):
    state = GameState(9)
    before = snapshot(state)

    with pytest.raises(ValueError):
        state.play(r, c)

    assert snapshot(state) == before


def test_move_after_game_over_raises_and_leaves_state_unchanged():
    state = state_with(
        black=[(2, c) for c in range(5)],
        current_player=BLACK,
        stones_left=2,
    )
    state.play(2, 5)
    assert state.winner == BLACK

    before = snapshot(state)
    with pytest.raises(ValueError):
        state.play(3, 3)
    assert snapshot(state) == before


# ----------------------------------------------------------------------
# Undo
# ----------------------------------------------------------------------
def test_undo_restores_one_move_exactly():
    state = GameState(9)
    state.play(0, 0)
    state.play(1, 1)

    before = snapshot(state)
    state.play(1, 2)
    state.undo()

    assert snapshot(state) == before
    assert state.board.is_empty(1, 2)


def test_multiple_undos_return_to_initial_state():
    state = GameState(9)
    moves = [(0, 0), (1, 1), (1, 2), (2, 1), (2, 2)]
    for r, c in moves:
        state.play(r, c)

    for _ in moves:
        state.undo()

    assert state.current_player == BLACK
    assert state.stones_left == 1
    assert state.winner is None
    assert state.history == []
    assert state.board.stone_count == 0
    assert all(cell == EMPTY for row in state.board.grid for cell in row)


def test_undo_after_winning_move_restores_winner_and_turn():
    state = state_with(
        black=[(2, c) for c in range(5)],
        current_player=BLACK,
        stones_left=2,
    )
    before = snapshot(state)

    state.play(2, 5)
    assert state.winner == BLACK

    state.undo()
    assert snapshot(state) == before
    assert not state.is_over()
    assert state.board.is_empty(2, 5)


def test_undo_after_win_on_first_stone_of_turn_restores_two_stones_left():
    state = state_with(
        white=[(2, c) for c in range(5)],
        current_player=WHITE,
        stones_left=2,
    )
    before = snapshot(state)

    state.play(2, 5)
    assert state.winner == WHITE

    state.undo()
    assert snapshot(state) == before
    assert state.stones_left == 2


def test_undo_with_no_history_raises():
    with pytest.raises(IndexError):
        GameState(9).undo()


# ----------------------------------------------------------------------
# Draw
# ----------------------------------------------------------------------
def test_full_board_with_no_winner_is_a_draw():
    state = GameState(6)

    # This 4-periodic pattern has no run of 6 in any direction.
    for r in range(6):
        for c in range(6):
            player = BLACK if ((r + 2 * c) % 4) < 2 else WHITE
            state.board.place(r, c, player)

    assert state.board.is_full()
    assert state.board.stone_count == 36
    assert state.winner is None
    assert state.is_over()

    for r in range(6):
        for c in range(6):
            assert not check_win(state.board, r, c, state.board.grid[r][c])

    with pytest.raises(ValueError):
        state.play(0, 0)


# ----------------------------------------------------------------------
# Copy / package isolation
# ----------------------------------------------------------------------
def test_game_state_copy_is_independent():
    state = GameState(9)
    state.play(4, 4)

    clone = state.copy()
    clone.play(3, 3)

    assert state.board.is_empty(3, 3)
    assert not clone.board.is_empty(3, 3)
    assert len(state.history) == 1
    assert len(clone.history) == 2


def test_game_package_does_not_import_ai_or_interface():
    package_dir = pathlib.Path(game.__file__).parent
    forbidden = {"ai", "interface"}

    for path in package_dir.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] not in forbidden, (
                        f"{path.name} imports {alias.name}"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0 and node.module:
                    assert node.module.split(".")[0] not in forbidden, (
                        f"{path.name} imports {node.module}"
                    )
