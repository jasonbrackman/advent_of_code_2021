import sys

import helpers


def get_cost(n):
    return n * (n + 1) / 2


def run():
    lines = helpers.get_lines(r"./data/day_07.txt")
    nums = sorted([int(i) for i in lines[0].split(",")])

    assert fuel_cost(nums) == 355521
    assert fuel_cost(nums, cost_func=get_cost) == 100148777


def fuel_cost(nums, cost_func=lambda x: x):
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
