def create_board(size=19):
    board = []

    for row in range(size):
        new_row = [0] * size
        board.append(new_row)
    return board

def display_board(board):
    for row in board:
        print(" ".join(str(cell) for cell in row))


def is_valid_move(board, row, col):
    size=len(board)

    if row < 0 or row >= size:
        return False
    if col < 0 or col >= size:
        return False
    if board[row][col] != 0:
        return False
    return True

def make_move(board, row, col, player):
    if player not in (1, 2):
        return False
    if not is_valid_move(board, row, col):
        return False
    
    board[row][col]= player

    return True


def check_winner(board, row, col, player, target=6):
    directions= [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    size= len(board)

    for dr, dc in directions:
        count = 1
        for sign in (1, -1):
            r = row + sign * dr
            c = col + sign * dc

            while (
                0 <= r < size
                and 0 <= c < size 
                and board[r][c] == player
            ):
                count += 1
                r += sign * dr
                c += sign * dc


        if count >= target:
            return True
    return False

