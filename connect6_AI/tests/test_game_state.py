
from game_state import GameState


def test_new_game():
    game = GameState(10)

    assert game.game_over is False
    assert game.winner is None


def test_winner_detection():
    game = GameState(10)

    for col in range(6):
        game.play_move(2, col, 1)

    assert game.game_over is True
    assert game.winner == 1


def test_cannot_play_after_game_over():
    game = GameState(10)

    for col in range(6):
        game.play_move(2, col, 1)

    result = game.play_move(3, 3, 2)

    assert result is False

