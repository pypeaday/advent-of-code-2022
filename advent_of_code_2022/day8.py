"""day8"""

import logging
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")
logger.setLevel("INFO")


def get_data() -> List[List[int]]:
    data = Path("./data/day8.data").read_text().split("\n")[:-1]
    # data = Path("./data/day8.sample").read_text().split("\n")[:-1]
    return data


def check_visibility_from_left(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    if all([tree_height > data[row_id][k] for k in range(0, col_id)]):
        return True
    return False


def check_visibility_from_right(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    if all(
        [tree_height > data[row_id][k] for k in range(col_id + 1, len(data[row_id]))]
    ):
        return True
    return False


def check_visibility_from_top(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    if all([tree_height > data[k][col_id] for k in range(0, row_id)]):
        return True
    return False


def check_visibility_from_bottom(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    if all([tree_height > data[k][col_id] for k in range(row_id + 1, len(data))]):
        return True
    return False


def check_visibility_to_left(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    trees = [data[row_id][k] for k in range(0, col_id)]
    score = 0
    for tree in trees[::-1]:
        if tree < tree_height:
            score += 1
            continue
        elif tree >= tree_height:
            score += 1
            return score
    return score


def check_visibility_to_right(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    trees = [data[row_id][k] for k in range(col_id + 1, len(data[row_id]))]
    score = 0
    for tree in trees:
        if tree < tree_height:
            score += 1
            continue
        elif tree >= tree_height:
            score += 1
            return score
    return score


def check_visibility_to_top(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    trees = [data[k][col_id] for k in range(0, row_id)]
    score = 0
    for tree in trees[::-1]:
        if tree < tree_height:
            score += 1
            continue
        elif tree >= tree_height:
            score += 1
            return score
    return score


def check_visibility_to_bottom(data: List[List[int]], row_id: int, col_id: int):
    tree_height = data[row_id][col_id]
    trees = [data[k][col_id] for k in range(row_id + 1, len(data))]
    score = 0
    for tree in trees:
        if tree < tree_height:
            score += 1
            continue
        elif tree >= tree_height:
            score += 1
            return score
    return score


def calculate_scenic_score(data: List[List[int]], row_id: int, col_id: int):
    scores = [
        check_visibility_to_top(data, row_id, col_id),
        check_visibility_to_left(data, row_id, col_id),
        check_visibility_to_bottom(data, row_id, col_id),
        check_visibility_to_right(data, row_id, col_id),
    ]
    return reduce(mul, scores, 1)


def main():
    data = get_data()
    # all outter trees are automatically visible
    trees_visible = 4 * (len(data) - 1)
    logger.debug(f"Trees visible around perimiter is {trees_visible}")
    tree_ids_visible: List[Tuple[int, int]] = []
    tree_ids_not_visible: List[Tuple[int, int]] = []
    scores: List[int] = []
    for row_id, row in enumerate(data):
        for col_id, _ in enumerate(row):
            idx = (row_id, col_id)
            col = [data[k][col_id] for k in range(len(data))]
            if (
                row_id == 0
                or row_id + 1 == len(data)
                or col_id == 0
                or col_id + 1 == len(col)
            ):
                logger.debug(f"EDGE: {row_id=} and {col_id=}")
                continue
            if check_visibility_from_left(data, row_id, col_id):
                logger.debug(f"INNER: {row_id=} and {col_id=}")
                if idx not in tree_ids_visible:
                    trees_visible += 1
                    tree_ids_visible.append(idx)
            elif check_visibility_from_right(data, row_id, col_id):
                logger.debug(f"INNER: {row_id=} and {col_id=}")
                if idx not in tree_ids_visible:
                    trees_visible += 1
                    tree_ids_visible.append(idx)
            elif check_visibility_from_top(data, row_id, col_id):
                logger.debug(f"INNER: {row_id=} and {col_id=}")
                if idx not in tree_ids_visible:
                    trees_visible += 1
                    tree_ids_visible.append(idx)
            elif check_visibility_from_bottom(data, row_id, col_id):
                logger.debug(f"INNER: {row_id=} and {col_id=}")
                if idx not in tree_ids_visible:
                    trees_visible += 1
                    tree_ids_visible.append(idx)
            else:
                logger.debug(f"INVISIBLE INNER: {row_id=} and {col_id=}")
            tree_ids_not_visible.append(idx)

            score = calculate_scenic_score(data, row_id, col_id)
            logger.debug(f"{idx=} has score of {score=}")
            scores.append(score)
    logger.info(f"{trees_visible=}")
    logger.debug(f"{tree_ids_visible=}")
    logger.debug(f"{tree_ids_not_visible=}")
    logger.info(f"{max(scores)=}")
    # logger.debug(f"{scores=}")
