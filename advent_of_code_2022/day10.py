"""day10"""

import logging
from importlib import reload
from pathlib import Path
from typing import Dict, List, Optional, Tuple

reload(logging)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

CRT_WIDTH = 40  # pixels


def get_instructions() -> List[Tuple[str, Optional[int]]]:
    data = Path("./data/day10.data").read_text().split("\n")[:-1]
    # data = Path("./data/day10.sample2").read_text().split("\n")[:-1]
    # data = Path("./data/day10.sample").read_text().split("\n")[:-1]

    instructions = []

    for line in data:
        if line == "noop":
            instructions.append((line, None))
        else:
            v = int(line.split(" ")[-1])
            instructions.append(("addx", v))

    return instructions


def calculate_signal_strenth(
    value_map: Dict[int, Tuple[int, int]], cycles: Tuple[int]
) -> int:
    signal_strengths: int = 0
    for cycle in cycles:
        x = value_map[cycle][0]
        signal_strengths += cycle * x
    return signal_strengths


def main():
    instructions = get_instructions()
    cycle = 0
    start_x = 1
    end_x = 1
    cycle_x_value_map: Dict[int, Tuple[int, int]] = {}
    cycles_to_calculate: Tuple[int] = (20, 60, 100, 140, 180, 220)

    # will chunk it later to avoid modulo and roll-over
    crt: List[str] = []

    for instruction in instructions:
        # iterate cycle either way
        cycle += 1
        crt_idx = (cycle - 1) % CRT_WIDTH
        logger.debug(f"Starting {cycle=} with {start_x=}")
        logger.debug(f"{instruction=}")

        function, value = instruction
        logger.debug(f"{function=}, {value=}")

        if start_x in (crt_idx - 1, crt_idx, crt_idx + 1):
            character = "#"
        else:
            character = "."
        crt.append(character)

        # basically do a noop for one cycle either way
        end_x = start_x
        cycle_x_value_map[cycle] = (start_x, end_x)
        logger.debug(
            f"updated cycle_x_value_map for {cycle=} with {start_x=} and {end_x=}"
        )
        logger.debug(f"Ending {cycle=} with {end_x=}")
        if function == "addx":
            cycle += 1
            crt_idx = (cycle - 1) % CRT_WIDTH
            logger.debug(f"Starting {cycle=} with {start_x=}")

            if start_x in (crt_idx - 1, crt_idx, crt_idx + 1):
                character = "#"
            else:
                character = "."
            crt.append(character)

            end_x = start_x + value
            cycle_x_value_map[cycle] = (start_x, end_x)
            logger.debug(f"Ending {cycle=} with {end_x=}")

        # reset start_x to ending value for start of next cycle
        logger.debug(f"setting start_x to {end_x}\n")
        start_x = end_x

    return calculate_signal_strenth(cycle_x_value_map, cycles_to_calculate), crt


if __name__ == "__main__":
    answer, crt = main()
    print(f"{answer=}")
    from more_itertools import chunked

    for chunk in chunked(crt, 40):
        print("".join(chunk))
