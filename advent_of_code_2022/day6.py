"""day6

The device will send your subroutine a datastream buffer (your puzzle input);
your subroutine needs to identify the first position where the four most
recently received characters were all different. Specifically, it needs to
report the number of characters from the beginning of the buffer to the end of
the first such four-character marker.

For example, suppose you receive the following datastream buffer:

mjqjpqmgbljsphdztnvjfqwrcgsmlb

After the first three characters (mjq) have been received, there haven't been
enough characters received yet to find the marker. The first time a marker
could occur is after the fourth character is received, making the most recent
four characters mjqj. Because j is repeated, this isn't a marker.

The first time a marker appears is after the seventh character arrives. Once it
does, the last four characters received are jpqm, which are all different. In
this case, your subroutine should report the value 7, because the first
start-of-packet marker is complete after 7 characters have been processed.

Here are a few more examples:

    bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
    nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
    nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
    zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11

"""

from pathlib import Path
from typing import Tuple

from more_itertools import windowed


def is_marker(s: Tuple[str]):
    """is_marker.

    Returns whether s contains a marker

    Args:
        s: Description of s.
    """
    return len(set(s)) == len(s)


def get_marker(s: str, n: int = 4):
    # pad s since I assume I have the whole data buffer in memory
    # needs to be such that it doesn't
    s = "1" * n + s
    for j, win in enumerate(windowed(s, n)):
        if j < n:
            continue
        if is_marker(win):
            return j


def read_data():
    return Path("./data/day6.data").read_text()


def main():
    s = read_data()
    marker = get_marker(s)
    print(f"{marker=}")
