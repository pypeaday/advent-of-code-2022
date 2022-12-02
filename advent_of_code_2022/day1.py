"""day 1 module."""

"""

For example, suppose the Elves finish writing their items' Calories and end up
with the following list:

```
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

This list represents the Calories of the food carried by five Elves:

    The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total
    of 6000 Calories. The second Elf is carrying one food item with 4000
    Calories. The third Elf is carrying food with 5000 and 6000 Calories, a
    total of 11000 Calories. The fourth Elf is carrying food with 7000, 8000,
    and 9000 Calories, a total of 24000 Calories. The fifth Elf is carrying one
    food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know which Elf
to ask: they'd like to know how many Calories are being carried by the Elf
carrying the most Calories. In the example above, this is 24000 (carried by the
                                                                 fourth Elf).
"""


from pathlib import Path
from typing import List, Tuple


def read_data() -> List[List[int]]:
    data = Path("./data/day1.data").read_text().split("\n\n")
    return [[int(x) for x in s.split("\n") if x] for s in data]


def sum_elves(data: List[List[int]]) -> List[int]:
    return [sum(s) for s in data]


def find_elf_carrying_most_calories(data: List[int]) -> Tuple[int, int]:
    return data.index(max(data)), max(data)


def index_data(data: List[int]) -> List[Tuple[int, List[int]]]:
    return [(j, s) for s in data]


def find_elf_carrying_most_calories2(data: Tuple[int, List[int]]) -> Tuple[int, int]:
    sums = [(t[0], sum(t[1])) for t in data]
    # sort by the sums
    sorted_sums = sorted(sums, key=lambda x: x[1])
    return sorted_sums[-1]


def find_n_heaviest_elves(data: List[int], n: int = 1):
    elves: List[Tuple[int, int]] = []
    for j in range(n):
        elves.append((idx_of_max, max_value))  # ???


def main():
    data = read_data()
    sums = sum_elves(data)
    idx, most_calories = find_elf_carrying_most_calories(sums)

    print(
        f"Most calories carried by elf is elf number {idx} with {most_calories} calories carried"
    )


if __name__ == "__main__":
    main()
