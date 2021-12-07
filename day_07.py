import sys
from typing import Callable, List

import helpers


def get_cost(n: int) -> float:
    return n * (n + 1) / 2


def run() -> None:
    lines = helpers.get_lines(r"./data/day_07.txt")
    nums = sorted([int(i) for i in lines[0].split(",")])

    assert fuel_cost(nums, cost_func=lambda x: x) == 355521
    assert fuel_cost(nums, cost_func=get_cost) == 100148777


def fuel_cost(nums: List[int], cost_func: Callable) -> int:
    total = sys.maxsize
    for index in range(nums[0], nums[-1] + 1):
        temp = sum(
            cost_func(n - index) if n > index else cost_func(index - n) for n in nums
        )
        if temp < total:
            total = temp
    return int(total)


if __name__ == "__main__":
    run()
