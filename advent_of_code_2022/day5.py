"""day5
```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

In this example, there are three stacks of crates. Stack 1 contains two crates:
    crate Z is on the bottom, and crate N is on top. Stack 2 contains three
    crates; from bottom to top, they are crates M, C, and D. Finally, stack 3
    contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a
quantity of crates is moved from one stack to a different stack. In the first
step of the above rearrangement procedure, one crate is moved from stack 2 to
stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

In the second step, three crates are moved from stack 1 to stack 3. Crates are
moved one at a time, so the first crate to be moved (D) ends up below the
second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are
moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in
this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3,
so you should combine these together and give the Elves the message CMZ.
"""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List

STACK_WIDTH = 4  # number of spaces in ascii diagram per stack of crates


def read_data():
    crates, instructions = Path("./data/day5.sample").read_text().split("\n\n")
    return crates, instructions


def format_raw_crates(crates: str) -> Dict[int, List[str]]:
    """format_raw_crates.
    input:
            [D]
            [N] [C]
            [Z] [M] [P]
             1   2   3
    output:
        defaultdict(
            <class 'list'>,
                {
                    1: ['Z', 'N', ' '],
                    2: ['M', 'C', 'D'],
                    3: ['P', ' ', ' ']
                 }
        )
    """
    stacks: Dict[int, List[str]] = defaultdict(list)
    # j is the height of the crate
    for j, row in enumerate(crates.split("\n")[::-1]):
        if j < 1:
            continue
        # TODO: get number of stacks
        stack_ids: List[int] = [1, 2, 3]
        for stack_id in stack_ids:
            row_index = 1 + (STACK_WIDTH * (stack_id - 1))
            stacks[stack_id].append(row[row_index])

    return stacks
