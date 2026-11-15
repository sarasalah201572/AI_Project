
def evaluate_window(window, player):
    opponent = 3 - player

    if opponent in window:
        return 0

    count = window.count(player)

    if count == 0:
        return 0

    scores = {
        1: 1,
        2: 10,
        3: 100,
        4: 1000,
        5: 10000,
        6: 1000000
    }

    score = scores[count]

    longest_run = 0
    current_run = 0

    for cell in window:
        if cell == player:
            current_run += 1
            longest_run = max(longest_run, current_run)
        else:
            current_run = 0

    run_bonus = {
        1: 0,
        2: 2,
        3: 20,
        4: 200,
        5: 2000,
        6: 0
    }

    score += run_bonus[longest_run]

    if count >= 3:
        for i in range(len(window) - 2):
            if (
                window[i] == player
                and window[i + 1] == 0
                and window[i + 2] == player
            ):
                score += 15

    return score


def evaluate_board(board, player):
    size = len(board)
    opponent = 3 - player

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    total_score = 0

    for row in range(size):
        for col in range(size):

            for dr, dc in directions:

                end_row = row + 5 * dr
                end_col = col + 5 * dc

                if not (
                    0 <= end_row < size
                    and 0 <= end_col < size
                ):
                    continue

                window = []

                for i in range(6):
                    r = row + i * dr
                    c = col + i * dc
                    window.append(board[r][c])

                total_score += evaluate_window(window, player)
                total_score -= evaluate_window(window, opponent)

    return total_score



