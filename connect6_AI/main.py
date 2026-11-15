"""Entry point: start the pygame GUI, or the terminal demo if pygame is absent."""

if __name__ == "__main__":
    try:
        from interface.game_screen import run_game
    except ImportError as exc:
        print(f"Pygame GUI unavailable ({exc}). Starting the terminal demo instead.")
        print()
        from game.cli import main as run_game

    run_game()
