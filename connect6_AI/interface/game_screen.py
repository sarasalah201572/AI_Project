
import pygame

from game.board import create_board, make_move, check_winner
from ai.alpha_beta import find_best_move_alpha_beta


WIDTH = 800
HEIGHT = 800

BOARD_SIZES = [10, 15, 19]

BACKGROUND = (222, 184, 135)
LINE_COLOR = (70, 45, 25)
BLACK = (20, 20, 20)
WHITE = (245, 245, 245)


def choose_board_size(screen):
    font = pygame.font.SysFont(None, 48)
    button_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill(BACKGROUND)

        title = font.render("Choose Board Size", True, BLACK)
        screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 180)
        )

        buttons = []

        for i, size in enumerate(BOARD_SIZES):
            rect = pygame.Rect(
                WIDTH // 2 - 100,
                280 + i * 100,
                200,
                65
            )

            pygame.draw.rect(
                screen, LINE_COLOR, rect, border_radius=10
            )

            text = button_font.render(
                f"{size} x {size}",
                True,
                WHITE
            )

            screen.blit(
                text,
                (
                    rect.centerx - text.get_width() // 2,
                    rect.centery - text.get_height() // 2
                )
            )

            buttons.append((rect, size))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, size in buttons:
                    if rect.collidepoint(event.pos):
                        return size


def draw_board(screen, board, current_player, winner, cell_size, margin):
    screen.fill(BACKGROUND)

    size = len(board)
    font = pygame.font.SysFont(None, 32)

    if winner:
        message = f"Player {winner} Wins!"
    elif current_player == 2:
        message = "Computer is thinking..."
    else:
        message = "Your Turn"

    text = font.render(message, True, BLACK)
    screen.blit(
        text,
        (WIDTH // 2 - text.get_width() // 2, 25)
    )

    board_end = margin + (size - 1) * cell_size

    for i in range(size):
        position = margin + i * cell_size

        pygame.draw.line(
            screen, LINE_COLOR,
            (margin, position),
            (board_end, position), 2
        )

        pygame.draw.line(
            screen, LINE_COLOR,
            (position, margin),
            (position, board_end), 2
        )

    for row in range(size):
        for col in range(size):
            if board[row][col] != 0:
                x = margin + col * cell_size
                y = margin + row * cell_size

                color = BLACK if board[row][col] == 1 else WHITE

                pygame.draw.circle(
                    screen,
                    color,
                    (x, y),
                    max(3, cell_size // 2 - 2)
                )

                pygame.draw.circle(
                    screen,
                    LINE_COLOR,
                    (x, y),
                    max(3, cell_size // 2 - 2),
                    1
                )


def run_game():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect6")

    board_size = choose_board_size(screen)

    if board_size is None:
        pygame.quit()
        return

    board = create_board(board_size)

    current_player = 1
    winner = None

    margin = 100
    available_space = WIDTH - 2 * margin
    cell_size = available_space // (board_size - 1)

    running = True
    clock = pygame.time.Clock()

    ai_thinking = False
    ai_start_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and winner is None
                and current_player == 1
                and not ai_thinking
            ):
                mouse_x, mouse_y = event.pos

                col = round((mouse_x - margin) / cell_size)
                row = round((mouse_y - margin) / cell_size)

                if 0 <= row < board_size and 0 <= col < board_size:
                    x = margin + col * cell_size
                    y = margin + row * cell_size

                    if (
                        abs(mouse_x - x) <= cell_size // 2
                        and abs(mouse_y - y) <= cell_size // 2
                    ):
                        if make_move(board, row, col, current_player):
                            if check_winner(
                                board, row, col, current_player
                            ):
                                winner = current_player
                            else:
                                current_player = 2
                                ai_thinking = True
                                ai_start_time = pygame.time.get_ticks()

        if ai_thinking:
            current_time = pygame.time.get_ticks()

            if current_time - ai_start_time >= 800:
                ai_move = find_best_move_alpha_beta(
                    board,
                    ai_player=2,
                    depth=2
                )

                if ai_move is not None:
                    ai_row, ai_col = ai_move

                    make_move(board, ai_row, ai_col, 2)

                    if check_winner(board, ai_row, ai_col, 2):
                        winner = 2
                    else:
                        current_player = 1

                ai_thinking = False

        draw_board(
            screen,
            board,
            current_player,
            winner,
            cell_size,
            margin
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


