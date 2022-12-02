"""day 2 module
For example, suppose you were given the following strategy guide:

```
A Y
B X
C Z
```

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should
    choose Paper (Y). This ends in a win for you with a score of 8 (2 because
                                                                    you chose
                                                                    Paper + 6
                                                                    because you
                                                                    won).
    In the second round, your opponent will choose Paper (B), and you should
    choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a
    score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

"""


from pathlib import Path
from typing import Union


class Rock:
    def __init__(self):
        self.identity = "rock"
        self.defeats = "scissors"
        self.is_defeated_by = "paper"
        self.score = 1


class Paper:
    def __init__(self):
        self.identity = "paper"
        self.defeats = "rock"
        self.is_defeated_by = "scissors"
        self.score = 2


class Scissors:
    def __init__(self):
        self.identity = "scissors"
        self.defeats = "paper"
        self.is_defeated_by = "rock"
        self.score = 3

        self.winning_score_map = {"me": 6, "tie": 4, "opponent": 0}


class Round:
    def __init__(self, my_move_encoded: str, opponent_move_encoded: str):
        base_map = {
            "rock": Rock,
            "paper": Paper,
            "scissors": Scissors,
        }
        my_moves = {
            **base_map,
            "X": Rock,
            "Y": Paper,
            "Z": Scissors,
        }
        opponent_moves = {
            **base_map,
            "A": Rock,
            "B": Paper,
            "C": Scissors,
        }
        self.my_move: Union[Rock, Paper, Scissors] = my_moves[my_move_encoded]()
        self.opponent_move: Union[Rock, Paper, Scissors] = opponent_moves[
            opponent_move_encoded
        ]()
        self.winning_score_map = {"me": 6, "tie": 3, "opponent": 0}

    @property
    def winner(self):
        return self.who_won()

    def who_won(self):
        if self.my_move.identity == self.opponent_move.is_defeated_by:
            return "me"
        elif self.my_move.identity == self.opponent_move.identity:
            return "tie"
        else:
            return "opponent"

    def outcome_score(self):
        winning_score = self.winning_score_map[self.who_won()]
        return winning_score + self.my_move.score


class Round2:
    def __init__(self, desired_outcome_encoded: str, opponent_move_encoded: str):
        base_map = {
            "rock": Rock,
            "paper": Paper,
            "scissors": Scissors,
        }
        opponent_moves = {
            **base_map,
            "A": Rock,
            "B": Paper,
            "C": Scissors,
        }

        self.opponent_move: Union[Rock, Paper, Scissors] = opponent_moves[
            opponent_move_encoded
        ]()

        desired_winner_map = {"X": "opponent", "Y": "tie", "Z": "me"}

        if desired_outcome_encoded == "X":
            my_move = base_map[self.opponent_move.defeats]()
        elif desired_outcome_encoded == "Y":
            my_move = base_map[self.opponent_move.identity]()
        elif desired_outcome_encoded == "Z":
            my_move = base_map[self.opponent_move.is_defeated_by]()

        self.my_move: Union[Rock, Paper, Scissors] = my_move

        self.winning_score_map = {"me": 6, "tie": 3, "opponent": 0}

    @property
    def winner(self):
        return self.who_won()

    def who_won(self):
        if self.my_move.identity == self.opponent_move.is_defeated_by:
            return "me"
        elif self.my_move.identity == self.opponent_move.identity:
            return "tie"
        else:
            return "opponent"

    def outcome_score(self):
        winning_score = self.winning_score_map[self.who_won()]
        return winning_score + self.my_move.score


def who_won(my_move: str, opponent_move: str):
    """who_won.
    Takes either human-readable {rock, paper, scissors} or encrypted data
    {A,B,C,X,Y,Z} and returns the winner
    """
    my_moves = {
        "rock": Rock,
        "paper": Paper,
        "scissors": Scissors,
        "X": Rock,
        "Y": Paper,
        "Z": Scissors,
    }
    opponent_moves = {
        "rock": Rock,
        "paper": Paper,
        "scissors": Scissors,
        "A": Rock,
        "B": Paper,
        "C": Scissors,
    }
    if my_moves[my_move]().identity == opponent_moves[opponent_move]().is_defeated_by:
        return "me"
    elif my_moves[my_move]().identity == opponent_moves[opponent_move]().identity:
        return "tie"
    else:
        return "opponent"


def main():
    # data = Path("./data/day2.sample").read_text().split("\n")
    data = Path("./data/day2.data").read_text().split("\n")
    score = 0
    score2 = 0
    for round in data[:-1]:
        opponent_move, my_move = round.split(" ")
        r = Round(my_move, opponent_move)
        score += r.outcome_score()

        opponent_move, desired_outcome = round.split(" ")
        r2 = Round2(desired_outcome, opponent_move)
        score2 += r2.outcome_score()
    return score, score2


if __name__ == "__main__":
    score, score2 = main()
    print(score)
    print(score2)
