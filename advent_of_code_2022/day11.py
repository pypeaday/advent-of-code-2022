"""day 11"""

from pathlib import Path
from typing import Dict, List

from rich import print_json


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
        self.items = self.__format_items(items)
        self.operation_desc = self.__format_operation(operation)
        self.test_desc = self.__format_test(test)
        self.throw_if_true = self.__format_boolean_result(true_result)
        self.throw_if_false = self.__format_boolean_result(false_result)

    def __repr__(self):
        print_json(data={k: v for k, v in self.__dict__.items()})
        return f"Monkey # {self.idx}"

    def __format_boolean_result(self, cond: str):
        s, t = cond.split(" throw to monkey ")
        return int(t)

    def __format_items(self, items: str):
        """
        ex: items: "Starting items: 79, 98"
            return [79,98]
        """
        s, t = items.split(": ")
        return [int(x) for x in t.split(", ")]

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
        ...

    def operation(self, item: int):
        return eval(self.operation_desc, {"new": item})

    def test(self, item: int):
        return eval(self.test_desc, {"new": item}) == 0


def get_data():
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
