from typing import List
import helpers


def part01(lines: List[str]) -> int:
    depth = 0
    horiz = 0

    for line in lines:
        inst, value = line.split()
        value = int(value)
        if inst == "up":
            depth -= value
        elif inst == "down":
            depth += value
        elif inst == "forward":
            horiz += value

    return depth * horiz


def part02(lines: List[str]) -> int:
    aim = 0
    depth = 0
    horiz = 0

    for line in lines:
        inst, value = line.split()
        value = int(value)
        if inst == "up":
            aim -= value
        elif inst == "down":
            aim += value
        elif inst == "forward":
            horiz += value
            depth += aim * value

    return depth * horiz


def run():
    lines = helpers.get_lines(r"./data/day_02.txt")

    assert part01(lines) == 1893605
    assert part02(lines) == 2120734350


if __name__ == "__main__":
    run()
