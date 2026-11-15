from ai.minimax import find_best_move
from ai.alpha_beta import find_best_move_alpha_beta


board = [[0] * 10 for _ in range(10)]

board[5][4] = 1
board[5][5] = 2
board[4][5] = 1
board[6][4] = 2


minimax_stats = {"nodes": 0}
alpha_beta_stats = {"nodes": 0}


minimax_move = find_best_move(
board, 2, depth=4, stats=minimax_stats)

alpha_beta_move = find_best_move_alpha_beta(
board, 2, depth=4, stats=alpha_beta_stats)


print("Minimax:")
print("Best move:", minimax_move)
print("Visited nodes:", minimax_stats["nodes"])

print("\nAlpha-Beta:")
print("Best move:", alpha_beta_move)
print("Visited nodes:", alpha_beta_stats["nodes"])