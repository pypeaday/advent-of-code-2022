"""day 11"""


import json
import logging
from functools import reduce
from pathlib import Path
from typing import Dict, List, Optional

from tqdm import tqdm

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("WARNING")


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def adjust_worry_level(self, modulo: int = 3):
        self.worry_level = self.worry_level // modulo

    def __repr__(self):
        return f"Item: {self.__dict__}"

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class Monkey:
    def __init__(
        self,
        idx: int,
        items: List[int],
        operation: str,
        test: str,
        true_result: str,
        false_result: str,
    ):
        """
        ex: items: "Starting items: 79, 98"
            operation: "Operation: new = old * 19"
            test: "Test: divisible by 23"
            true_result: "If true: throw to monkey 2"
            false_result: "If false: throw to monkey 3"
        """

    def __init__(self, idx, items, operation, test, true_result, false_result):
        self.idx = idx
        self.items: List[Item] = self.__format_items(items)
        self.operation_desc = self.__format_operation(operation)
        self.test_desc = self.__format_test(test)
        self.throw_if_true = self.__format_boolean_result(true_result)
        self.throw_if_false = self.__format_boolean_result(false_result)
        self.inspect_count = 0

    def __repr__(self):
        return f"{self.__dict__}"

    def __str__(self):
        return f"Monkey {self.idx}"

    def __format_boolean_result(self, cond: str):
        s, t = cond.split(" throw to monkey ")
        return int(t)

    def __format_items(self, items: str):
        """
        ex: items: "Starting items: 79, 98"
            return [79,98]
        """
        s, t = items.split(": ")
        return [Item(int(x)) for x in t.split(", ")]

    def __format_operation(self, operation: str):
        """
        ex: operation = "Operation: new = old * 19"
            return "old * 19"
        """
        return operation.split(" = ")[1]

    def __format_test(self, test: str):
        """
        ex: test = "Test: divisible by 23"
            return "new % 23"
        """
        self.divisor = int(test.split(" ")[-1])
        return f"new % {self.divisor}"

    def operation(self, item: Item):
        self.inspect_count += 1
        v = eval(self.operation_desc, {"old": item.worry_level})
        item.worry_level = v

    def test(self, item: Item):
        return eval(self.test_desc, {"new": item.worry_level}) == 0


def get_data():
    raw = Path("./data/day11.data").read_text().split("\n\n")
    raw = Path("./data/day11.sample").read_text().split("\n\n")
    monkey_map: Dict[int, Monkey] = {}
    for _data in raw:
        data = _data.split("\n")
        # Monkey 0: --> Monkey 0 --> [Monkey, "0"] --> int("0")
        monkey_id = int(data[0].replace(":", "").split(" ")[1])
        items = data[1].strip()
        operation = data[2].strip()
        test = data[3].strip()
        true_result = data[4].strip()
        false_result = data[5].strip()
        monkey_map[monkey_id] = Monkey(
            idx=monkey_id,
            items=items,
            operation=operation,
            test=test,
            true_result=true_result,
            false_result=false_result,
        )

    return monkey_map


def do_round(
    monkey_map: Dict[int, Monkey], manage_worry: Optional[int] = 3
) -> Dict[int, Monkey]:
    for k, monkey in monkey_map.items():
        logger.debug(f"{monkey}")
        # Monkey inspects item
        # items = copy.deepcopy(monkey.items)
        num_items = list(range(len(monkey.items)))
        for _ in num_items:
            # pop left-most item from item list for current monkey and append
            # it to target monkey's items after operations
            item = monkey.items.pop(0)
            logger.debug(
                f"monkey inspects an item with worry level of {item.worry_level}"
            )
            # Worry level is affected by operation
            monkey.operation(item)
            logger.debug(
                f"worry level is affected by {monkey.operation_desc} and results in {item.worry_level}"
            )
            # Worry level of item is divided by 3 by default
            if manage_worry:
                item.adjust_worry_level(manage_worry)
                logger.debug(
                    f"monkey gets bored with item - worry level divided by 3 to {item.worry_level}"
                )
            target_monkey = (
                monkey.throw_if_true if monkey.test(item) else monkey.throw_if_false
            )
            logger.debug(
                f"item with worry level {item.worry_level} thrown to monkey {target_monkey}"
            )
            monkey_map[target_monkey].items.append(item)
    return monkey_map


def main(n_rounds: int = 20, be_smart: bool = False):
    m = get_data()

    if be_smart:
        levels = [monkey.divisor for monkey in m.values()]
        manage_worry = reduce(lambda x, y: x * y, levels)
    else:
        manage_worry = 3
    for j in tqdm(range(n_rounds)):
        m = do_round(m, manage_worry)
        if j == 0 or (j + 1) % 1000 == 0:
            logger.warning(f"\n=== After round {j+1} ===")
            for monkey in m.values():
                logger.warning(
                    f"Monkey {monkey.idx} inspected items {monkey.inspect_count} times"
                )

    active_monkeys = sorted(m.values(), key=lambda x: x.inspect_count)
    most_active = active_monkeys[-2:]

    monkey_business = most_active[0].inspect_count * most_active[1].inspect_count
    # breakpoint()
    return monkey_business


if __name__ == "__main__":
    ans = main(20)
    print(f"part 1 answer: {ans}")

    ans2 = main(10_000, True)
    print(f"part 2 answer: {ans2}")
