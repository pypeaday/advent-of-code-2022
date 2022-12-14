"""day4 module
For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

    Within the first pair of Elves, the first Elf was assigned sections 2-4
    (sections 2, 3, and 4), while the second Elf was assigned sections 6-8
    (sections 6, 7, 8). The Elves in the second pair were each assigned two
    sections. The Elves in the third pair were each assigned three sections:
        one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw; your
actual list might contain larger numbers. Visually, these pairs of section
assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

Some of the pairs have noticed that one of their assignments fully contains the
other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6.
In pairs where one assignment fully contains the other, one Elf in the pair
would be exclusively cleaning sections their partner will already be cleaning,
so these seem like the most in need of reconsideration. In this example, there
are 2 such pairs.

In how many assignment pairs does one range fully contain the other?
"""

from pathlib import Path
from typing import List


def expand_range(s: str) -> List[set]:
    """expane_range.
    s (str): entry like '2-4'
    returns (List[set]) like { 2,3,4 }
    """
    a, b = s.split("-")
    return set(range(int(a), int(b) + 1))


def read_data() -> List[str]:
    return Path("./data/day4.data").read_text().split("\n")[:-1]


def main():
    data = read_data()
    fully_contained = 0
    overlap = 0
    for assignment_pair in data:
        range1, range2 = assignment_pair.split(",")
        sec1: set
        sec2: set
        sec1, sec2 = expand_range(range1), expand_range(range2)
        if sec1.issubset(sec2) or sec2.issubset(sec1):
            fully_contained += 1

        if not sec1.isdisjoint(sec2):
            overlap += 1
    return fully_contained, overlap


if __name__ == "__main__":
    answer, answer2 = main()
    print(f"{answer=}")
    print(f"{answer2=}")
