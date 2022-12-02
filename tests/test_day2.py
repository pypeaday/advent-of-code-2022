import pytest

from advent_of_code_2022 import day2


@pytest.mark.parametrize(
    "my_move,opponent_move,winner",
    [
        ("rock", "paper", "opponent"),
        ("paper", "scissors", "opponent"),
        ("scissors", "rock", "opponent"),
        ("rock", "scissors", "me"),
        ("paper", "rock", "me"),
        ("scissors", "paper", "me"),
        ("scissors", "scissors", "tie"),
        ("X", "B", "opponent"),
        ("Y", "C", "opponent"),
        ("Z", "A", "opponent"),
        ("X", "C", "me"),
        ("Y", "A", "me"),
        ("Z", "B", "me"),
        ("Z", "C", "tie"),
    ],
)
def test_who_won(my_move: str, opponent_move: str, winner: str):
    assert day2.who_won(my_move, opponent_move) == winner


@pytest.mark.parametrize(
    "my_move,opponent_move,winner,score",
    [
        ("rock", "paper", "opponent", 1),
        ("paper", "scissors", "opponent", 2),
        ("scissors", "rock", "opponent", 3),
        ("rock", "scissors", "me", 7),
        ("paper", "rock", "me", 8),
        ("scissors", "paper", "me", 9),
        ("scissors", "scissors", "tie", 6),
        ("X", "B", "opponent", 1),
        ("Y", "C", "opponent", 2),
        ("Z", "A", "opponent", 3),
        ("X", "C", "me", 7),
        ("Y", "A", "me", 8),
        ("Z", "B", "me", 9),
        ("Z", "C", "tie", 6),
    ],
)
def test_who_won_round(my_move: str, opponent_move: str, winner: str, score: int):
    assert day2.Round(my_move, opponent_move).winner == winner
    assert day2.Round(my_move, opponent_move).outcome_score() == score
