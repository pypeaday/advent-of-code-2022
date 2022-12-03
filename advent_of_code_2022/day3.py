"""day3 module
For example, suppose you have the following list of contents from six rucksacks:

vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw

    The first rucksack contains the items vJrwpWtwJgWrhcsFMMfFFhFp, which means
    its first compartment contains the items vJrwpWtwJgWr, while the second
    compartment contains the items hcsFMMfFFhFp. The only item type that
    appears in both compartments is lowercase p.
    The second rucksack's compartments contain jqHRNqRjqzjGDLGL and
    rsFMfFZSrLrFZsSL. The only item type that appears in both compartments is
    uppercase L.
    The third rucksack's compartments contain PmmdzqPrV and vPwwTWBwg; the only
    common item type is uppercase P.
    The fourth rucksack's compartments only share item type v.
    The fifth rucksack's compartments only share item type t.
    The sixth rucksack's compartments only share item type s.

To help prioritize item rearrangement, every item type can be converted to a priority:

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.

In the above example, the priority of the item type that appears in both
compartments of each rucksack is 16 (p), 38 (L), 42 (P), 22 (v), 20 (t), and 19
(s); the sum of these is 157.

"""

import string
from functools import reduce
from pathlib import Path
from typing import List

from more_itertools import chunked

VALUES = {letter: value + 1 for value, letter in enumerate(string.ascii_lowercase)}
VALUES.update(
    {letter: value + 27 for value, letter in enumerate(string.ascii_uppercase)}
)


def read_data() -> List[List[str]]:
    return Path("./data/day3.data").read_text().split("\n")[:-1]


def split_rucksack(data: List[str]) -> List[List[str]]:
    return data[: len(data) // 2], data[len(data) // 2 :]


def get_groups_of_n_elves(data: List[List[str]], n: int) -> List[str]:
    for chunk in chunked(data, n):
        yield chunk


def find_common_item(*args) -> str:
    return list(reduce((lambda x, y: x.intersection(y)), [set(a) for a in args]))[0]


def main1():
    data = read_data()
    priority_sum = 0
    for rucksack in data:
        comp1, comp2 = split_rucksack(rucksack)
        v = find_common_item(comp1, comp2)
        # print(f"common item is {v}")
        priority_sum += VALUES[v]
    return priority_sum


def main2():
    data = read_data()
    priority_sum = 0
    group: List[str]
    for group in get_groups_of_n_elves(data, n=3):
        v = find_common_item(*group)
        # print(f"common item is {v}")
        priority_sum += VALUES[v]
    return priority_sum


if __name__ == "__main__":
    s = main1()
    print(f"Answer: {s}")
    s2 = main2()
    print(f"Answer: {s2}")
