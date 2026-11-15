from game.board import check_winner
from ai.heuristics import evaluate_board


def get_valid_moves(board):
    size = len(board)
    moves = set()

    occupied = []

    for row in range(size):
        for col in range(size):
            if board[row][col] != 0:
                occupied.append((row, col))

    if not occupied:
        center = size // 2
        return [(center, center)]

    for row, col in occupied:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):

                if dr == 0 and dc == 0:
                    continue

                new_row = row + dr
                new_col = col + dc

                if (
                    0 <= new_row < size
                    and 0 <= new_col < size
                    and board[new_row][new_col] == 0
                ):
                    moves.add((new_row, new_col))

    return sorted(moves)


def minimax(board, depth, is_maximizing, ai_player, last_move=None, stats=None):
    if stats is not None:
        stats["nodes"] += 1

    if last_move is not None:
        row, col, player = last_move

        if check_winner(board, row, col, player):
            if player == ai_player:
                return 1000000 + depth
            else:
                return -1000000 - depth

    if depth == 0:
        return evaluate_board(board, ai_player)

    valid_moves = get_valid_moves(board)

    if not valid_moves:
        return 0

    if is_maximizing:
        best_score = float("-inf")

        for row, col in valid_moves:
            board[row][col] = ai_player

            score = minimax(
                board,
                depth - 1,
                False,
                ai_player,
                (row, col, ai_player),
                stats
            )

            board[row][col] = 0

            best_score = max(best_score, score)

        return best_score

    else:
        best_score = float("inf")
        opponent = 3 - ai_player

        for row, col in valid_moves:
            board[row][col] = opponent

            score = minimax(
                board,
                depth - 1,
                True,
                ai_player,
                (row, col, opponent),
                stats
            )

            board[row][col] = 0

            best_score = min(best_score, score)

        return best_score

def find_best_move(board, ai_player, depth=2, stats=None):
    if stats is None:
        stats = {"nodes": 0}

    best_score = float("-inf")
    best_move = None

    for row, col in get_valid_moves(board):

        board[row][col] = ai_player

        score = minimax(
            board,
            depth - 1,
            False,
            ai_player,
            (row, col, ai_player),
            stats
        )

        board[row][col] = 0

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move