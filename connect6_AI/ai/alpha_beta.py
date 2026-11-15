from game.board import check_winner
from ai.heuristics import evaluate_board
from ai.minimax import get_valid_moves

def alpha_beta(
    board,
    depth,
    alpha,
    beta,
    is_maximizing,
    ai_player,
    last_move=None,
    stats=None
):
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

            score = alpha_beta(
                board,
                depth - 1,
                alpha,
                beta,
                False,
                ai_player,
                (row, col, ai_player),
                stats
            )

            board[row][col] = 0

            best_score = max(best_score, score)

            alpha = max(alpha, best_score)

            if alpha >= beta:
                break

        return best_score
    else:
        best_score = float("inf")

        opponent = 3 - ai_player

        for row, col in valid_moves:
            board[row][col] = opponent

            score = alpha_beta(
                board,
                depth - 1,
                alpha,
                beta,
                True,
                ai_player,
                (row, col, opponent),
                stats
            )

            board[row][col] = 0

            best_score = min(best_score, score)

            beta = min(beta, best_score)

            if alpha >= beta:
                break

        return best_score



def find_best_move_alpha_beta(board, ai_player, depth=2, stats=None):
    if stats is None:
        stats = {"nodes": 0}
    best_score = float("-inf")
    best_move = None

    alpha = float("-inf")
    beta = float("inf")

    for row, col in get_valid_moves(board):

        board[row][col] = ai_player

        score = alpha_beta(
            board,
            depth - 1,
            alpha,
            beta,
            False,
            ai_player,
            (row, col, ai_player),
            stats
        )

        board[row][col] = 0

        if score > best_score:
            best_score = score
            best_move = (row, col)

        alpha = max(alpha, best_score)

    return best_move