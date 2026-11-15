from ai.minimax import find_best_move


def test_ai_takes_winning_move():
    board = [[0] * 10 for _ in range(10)]

    board[5][2:7] = [2, 2, 2, 2, 2]

    move = find_best_move(board, ai_player=2, depth=2)

    assert move in [(5, 1), (5, 7)]


def test_ai_blocks_opponent_winning_move():
    board = [[0] * 10 for _ in range(10)]

    board[5][1:6] = [2, 1, 1, 1, 1]

    move = find_best_move(board, ai_player=2, depth=2)

    assert move == (5, 6)


def test_ai_does_not_change_board():
    board = [[0] * 10 for _ in range(10)]

    board[5][3] = 1
    board[5][4] = 2

    original_board = [row[:] for row in board]

    find_best_move(board, ai_player=2, depth=2)

    assert board == original_board


def test_ai_prioritizes_winning_move():
    board = [[0] * 10 for _ in range(10)]

    board[2][2:7] = [2, 2, 2, 2, 2]
    board[6][2:7] = [1, 1, 1, 1, 1]

    move = find_best_move(board, ai_player=2, depth=2)

    assert move in [(2, 1), (2, 7)]