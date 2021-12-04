from typing import List

import helpers


def get_rates(lines: List[str]) -> [int, int]:
    final = [0] * len(lines[0])
    for line in lines:
        for index, item in enumerate(line):
            final[index] += item == "1"

    g = ["1" if f > len(lines) // 2 else "0" for f in final]
    e = ["0" if f > len(lines) // 2 else "1" for f in final]
    return int("".join(g), 2), int("".join(e), 2)


def part01(lines) -> int:
    gamma_rate, epsilon_rate = get_rates(lines)
    return gamma_rate * epsilon_rate


def get_generator_rating(lines, index):
    nums = [line[index] == "1" for line in lines]
    bit = "0" if sum(nums) < len(lines) // 2 else "1"
    return [line for line in lines if line[index] == bit]


def get_scrubbing_rating(lines, index):
    nums = [line[index] == "0" for line in lines]
    bit = "1" if sum(nums) > len(lines) // 2 else "0"
    return [line for line in lines if line[index] == bit]


def part02(lines) -> int:
    x = _reduce_func(get_generator_rating, lines[:])
    y = _reduce_func(get_scrubbing_rating, lines[:])
    return x * y


def _reduce_func(func, lines):
    for index in range(len(lines[0])):
        lines = func(lines, index)
        if len(lines) == 1:
            return int(lines[0], 2)

    raise RuntimeError


def run():
    lines = helpers.get_lines(r"./data/day_03.txt")
    assert part01(lines) == 3633500
    assert part02(lines) == 4550283


if __name__ == "__main__":
    run()
