
from board import create_board, make_move, is_valid_move, check_winner


def test_create_board():
    board = create_board(10)

    assert len(board) == 10
    assert all(len(row) == 10 for row in board)


def test_valid_move():
    board = create_board(5)

    assert is_valid_move(board, 2, 3)


def test_invalid_move():
    board = create_board(5)

    assert not is_valid_move(board, 8, 2)


def test_occupied_cell():
    board = create_board(5)

    make_move(board, 2, 2, 1)

    assert not is_valid_move(board, 2, 2)


def test_make_move():
    board = create_board(5)

    result = make_move(board, 1, 2, 2)

    assert result is True
    assert board[1][2] == 2


def test_horizontal_win():
    board = create_board(10)

    for col in range(6):
        make_move(board, 2, col, 1)

    assert check_winner(board, 2, 5, 1)


def test_five_stones_not_win():
    board = create_board(10)

    for col in range(5):
        make_move(board, 2, col, 1)

    assert not check_winner(board, 2, 4, 1)
