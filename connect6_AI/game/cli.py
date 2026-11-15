"""Small two-human terminal demo for Connect-6.

Run from the directory that contains ``main.py``::

    python -m game.cli

Coordinates are 0-indexed: the top-left cell is ``0 0``.
"""

from .constants import BLACK, PLAYER_NAMES, SYMBOLS, WHITE, WIN_LENGTH
from .game_state import GameState


def _read_line(prompt: str):
    """Read a line, returning ``None`` on end-of-input (Ctrl-D)."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return None


def _prompt_board_size(default: int):
    while True:
        raw = _read_line(f"Board size (at least {WIN_LENGTH}) [{default}]: ")
        if raw is None:
            return None

        raw = raw.strip()
        if not raw:
            return default

        try:
            n = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        try:
            return GameState(n).board.n
        except ValueError as exc:
            print(exc)


def _print_board(board) -> None:
    width = len(str(board.n - 1))
    header = " " * (width + 1) + " ".join(
        f"{c:>{width}}" for c in range(board.n)
    )
    print(header)

    for r in range(board.n):
        cells = " ".join(
            f"{SYMBOLS[board.grid[r][c]]:>{width}}" for c in range(board.n)
        )
        print(f"{r:>{width}} {cells}")


def _describe_player(player: int) -> str:
    symbol = SYMBOLS[player]
    return f"{PLAYER_NAMES[player]} ({symbol})"


def _parse_coordinates(raw: str):
    parts = raw.replace(",", " ").split()
    if len(parts) != 2:
        raise ValueError("enter exactly two integers, for example: 9 9")

    try:
        r, c = (int(part) for part in parts)
    except ValueError:
        raise ValueError("coordinates must be whole numbers") from None

    return r, c


def main() -> None:
    print("Connect-6 terminal demo")
    print("Place six stones in a row. Black starts with 1 stone, then 2 per turn.")
    print("Commands: 'undo' removes the last stone, 'quit' exits.\n")

    default_size = GameState().board.n
    board_size = _prompt_board_size(default_size)
    if board_size is None:
        print("Goodbye.")
        return
    game = GameState(board_size)

    while not game.is_over():
        _print_board(game.board)
        print(
            f"{_describe_player(game.current_player)} to move: "
            f"place {game.stones_left} stone(s)."
        )

        raw = _read_line("Enter 'row col' (0-indexed), 'undo', or 'quit': ")
        if raw is None:
            print("Goodbye.")
            return
        raw = raw.strip()
        if not raw:
            continue

        command = raw.lower()
        if command in {"q", "quit", "exit"}:
            print("Goodbye.")
            return

        if command in {"u", "undo"}:
            try:
                game.undo()
            except IndexError:
                print("There are no moves to undo.")
            else:
                print("Last stone removed.")
            continue

        try:
            r, c = _parse_coordinates(raw)
            game.play(r, c)
        except ValueError as exc:
            print(f"Illegal move: {exc}")
            continue

    _print_board(game.board)
    if game.winner is None:
        print("Draw - the board is full and nobody connected six.")
    else:
        print(f"{_describe_player(game.winner)} wins!")


if __name__ == "__main__":
    main()
