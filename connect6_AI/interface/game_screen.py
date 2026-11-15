
import pygame

from game.board import create_board, make_move, check_winner


WIDTH = 800
HEIGHT = 800

BOARD_SIZE = 19
CELL_SIZE = 36
MARGIN = 76

BACKGROUND = (222, 184, 135)
LINE_COLOR = (70, 45, 25)
BLACK = (20, 20, 20)
WHITE = (245, 245, 245)


def draw_board(screen, board, current_player, winner):
    screen.fill(BACKGROUND)

    font = pygame.font.SysFont(None, 32)

    if winner:
        message = f"Player {winner} Wins!"
    else:
        message = f"Player {current_player}'s Turn"

    text = font.render(message, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 25))

    for i in range(BOARD_SIZE):
        position = MARGIN + i * CELL_SIZE

        pygame.draw.line(
            screen, LINE_COLOR,
            (MARGIN, position),
            (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, position), 2
        )

        pygame.draw.line(
            screen, LINE_COLOR,
            (position, MARGIN),
            (position, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE), 2
        )


    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):

            if board[row][col] != 0:

                x = MARGIN + col * CELL_SIZE
                y = MARGIN + row * CELL_SIZE

                color = BLACK if board[row][col] == 1 else WHITE

                pygame.draw.circle(
                    screen,
                    color,
                    (x, y),
                    CELL_SIZE // 2 - 2
                )

                pygame.draw.circle(
                    screen,
                    LINE_COLOR,
                    (x, y),
                    CELL_SIZE // 2 - 2,
                    1
                )


def run_game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect6")

    board = create_board(BOARD_SIZE)

    current_player = 1
    winner = None

    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and winner is None
            ):

                mouse_x, mouse_y = event.pos

                col = round((mouse_x - MARGIN) / CELL_SIZE)
                row = round((mouse_y - MARGIN) / CELL_SIZE)

                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:

                    x = MARGIN + col * CELL_SIZE
                    y = MARGIN + row * CELL_SIZE

                    if (
                        abs(mouse_x - x) <= CELL_SIZE // 2
                        and abs(mouse_y - y) <= CELL_SIZE // 2
                    ):

                        if make_move(board, row, col, current_player):

                            if check_winner(
                                board, row, col, current_player
                            ):
                                winner = current_player
                            else:
                                current_player = 3 - current_player

        draw_board(screen, board, current_player, winner)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

