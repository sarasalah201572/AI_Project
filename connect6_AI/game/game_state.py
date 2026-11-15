from board import create_board, make_move, check_winner


class GameState:

    def __init__(self, size=19):
        self.board = create_board(size)
        self.game_over = False
        self.winner = None
        self.last_move = None


    def play_move(self, row, col, player):

        if self.game_over :
            return False

        success = make_move(self.board, row, col, player)

        if not success:
            return False

        self.last_move = (row, col)

        if check_winner(self.board, row, col, player):
            self.game_over = True
            self.winner = player

        return True