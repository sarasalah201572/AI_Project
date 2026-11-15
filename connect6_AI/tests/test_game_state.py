"""Compatibility tests for the public GameState API."""

from game import BLACK, GameState


def test_new_game_defaults():
    game = GameState(10)

    assert not game.is_over()
    assert game.game_over is False
    assert game.winner is None
    assert game.current_player == BLACK
    assert game.stones_left == 1
    assert game.board.stone_count == 0


def test_winner_detection_from_legal_turns():
    game = GameState(10)

    # Black wins horizontally.  Every move follows the 1/2-stone turn rule.
    moves = [
        (2, 0),
        (9, 9), (9, 8),
        (2, 1), (2, 2),
        (8, 9), (8, 8),
        (2, 3), (2, 4),
        (7, 9), (7, 8),
        (2, 5),
    ]
    for r, c in moves:
        game.play(r, c)

    assert game.is_over()
    assert game.winner == BLACK


def test_cannot_play_after_game_over():
    game = GameState(10)

    for r, c in [
        (2, 0),
        (9, 9), (9, 8),
        (2, 1), (2, 2),
        (8, 9), (8, 8),
        (2, 3), (2, 4),
        (7, 9), (7, 8),
        (2, 5),
    ]:
        game.play(r, c)

    try:
        game.play(3, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("playing after game over must raise ValueError")
