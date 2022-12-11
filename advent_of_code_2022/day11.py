"""day 11"""


import copy
import json
import logging
from pathlib import Path
from typing import Dict, List

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def adjust_worry_level(self):
        self.worry_level = self.worry_level // 3

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
        return f"new % {test.split(' ')[-1]}"

    def operation(self, item: Item):
        self.inspect_count += 1
        v = eval(self.operation_desc, {"old": item.worry_level})
        item.worry_level = v

    def test(self, item: Item):
        return eval(self.test_desc, {"new": item.worry_level}) == 0


def get_data():
    raw = Path("./data/day11.data").read_text().split("\n\n")
    # raw = Path("./data/day11.sample").read_text().split("\n\n")
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


def do_round(monkey_map: Dict[int, Monkey]) -> Dict[int, Monkey]:
    for k, monkey in monkey_map.items():
        logger.debug(f"{monkey}")
        # Monkey inspects item
        items = copy.deepcopy(monkey.items)
        for _item in items:
            # pop left-most item from item list for current monkey and append
            # it to target monkey's items after operations
            item = monkey.items.pop(0)
            # mutating monkey.items list while iterating I think messes up the loop
            logger.debug(
                f"monkey inspects an item with worry level of {item.worry_level}"
            )
            # Worry level is affected by operation
            monkey.operation(item)
            logger.debug(
                f"worry level is affected by {monkey.operation_desc} and results in {item.worry_level}"
            )
            # Worry level of item is divided by 3
            item.adjust_worry_level()
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


def main():
    m = get_data()
    for _ in range(20):
        m = do_round(m)

    active_monkeys = sorted(m.values(), key=lambda x: x.inspect_count)
    most_active = active_monkeys[-2:]

    monkey_business = most_active[0].inspect_count * most_active[1].inspect_count
    return monkey_business
