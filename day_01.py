import sys
from typing import List

import helpers


def part01(data: List[int]) -> int:
    count = 0
    start = (
        sys.maxsize
    )  # first item can't be higher than anything else so let's go as high as possible.
    for item in data:
        if item > start:
            count += 1
        start = item

    return count


def part02(data: List[int]) -> int:
    items = [sum((x, y, z)) for x, y, z in zip(data, data[1:], data[2:])]
    return part01(items)


def run():
    items = helpers.get_ints(r"./data/day_01.txt")

    assert part01(items) == 1688
    assert part02(items) == 1728


if __name__ == "__main__":
    run()
