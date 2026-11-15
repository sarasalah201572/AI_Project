
from ai.heuristics import evaluate_board, evaluate_window


def test_empty_window():
    window = [0, 0, 0, 0, 0, 0]

    assert evaluate_window(window, 1) == 0


def test_opponent_blocks_window():
    window = [1, 1, 2, 1, 0, 0]

    assert evaluate_window(window, 1) == 0


def test_one_stone_gets_score():
    window = [1, 0, 0, 0, 0, 0]

    assert evaluate_window(window, 1) == 1


def test_more_stones_get_higher_score():
    window_three = [1, 1, 1, 0, 0, 0]
    window_four = [1, 1, 1, 1, 0, 0]

    assert evaluate_window(window_four, 1) > evaluate_window(window_three, 1)


def test_six_stones_get_highest_score():
    window = [1, 1, 1, 1, 1, 1]

    assert evaluate_window(window, 1) == 1000000


def test_consecutive_stones_get_run_bonus():
    consecutive = [1, 1, 1, 1, 0, 0]
    broken = [1, 0, 1, 0, 1, 1]

    assert evaluate_window(consecutive, 1) > evaluate_window(broken, 1)


def test_broken_pattern_gets_bonus():
    broken = [1, 1, 0, 1, 1, 0]
    without_broken_pattern = [1, 1, 0, 0, 1, 1]

    assert evaluate_window(broken, 1) > evaluate_window(
        without_broken_pattern, 1
    )


def test_player_two_evaluation():
    window = [2, 2, 2, 0, 0, 0]

    assert evaluate_window(window, 2) > 0



def test_empty_board():
    board = [[0] * 10 for _ in range(10)]

    assert evaluate_board(board, 1) == 0


def test_player_advantage():
    board = [[0] * 10 for _ in range(10)]
    board[2][2:5] = [1, 1, 1]

    assert evaluate_board(board, 1) > 0


def test_opponent_advantage():
    board = [[0] * 10 for _ in range(10)]
    board[2][2:5] = [2, 2, 2]

    assert evaluate_board(board, 1) < 0


def test_six_stones_win_score():
    board = [[0] * 10 for _ in range(10)]
    board[2][2:8] = [1, 1, 1, 1, 1, 1]

    assert evaluate_board(board, 1) > 0
    assert evaluate_board(board, 1) > evaluate_board(board, 2)


def test_vertical_evaluation():
    board = [[0] * 10 for _ in range(10)]

    for row in range(2, 5):
        board[row][3] = 1

    assert evaluate_board(board, 1) > 0


def test_diagonal_evaluation():
    board = [[0] * 10 for _ in range(10)]

    for i in range(3):
        board[2 + i][2 + i] = 1

    assert evaluate_board(board, 1) > 0


def test_reverse_diagonal_evaluation():
    board = [[0] * 10 for _ in range(10)]

    for i in range(3):
        board[2 + i][5 - i] = 1

    assert evaluate_board(board, 1) > 0


def test_dangerous_opponent_pattern():
    board = [[0] * 10 for _ in range(10)]
    board[2][2:6] = [2, 2, 2, 2]

    assert evaluate_board(board, 1) < 0


def test_evaluation_symmetry():
    board = [[0] * 10 for _ in range(10)]

    board[2][2:5] = [1, 1, 1]
    board[4][3:6] = [2, 2, 2]

    assert evaluate_board(board, 1) == -evaluate_board(board, 2)


def test_broken_pattern_on_board():
    board = [[0] * 10 for _ in range(10)]
    board[2][1:6] = [1, 1, 0, 1, 1]

    assert evaluate_board(board, 1) > 0
