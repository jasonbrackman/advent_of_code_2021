from typing import Iterator
import helpers


def part01(data: Iterator[int]) -> int:
    """
    From an interator, calculate the total number of adjacent
    numbers that result in a < b.
    :param data: An iterator of integers
    :return: The total number of pairs that are True
    """

    return sum(a < b for a, b in helpers.window(data, 2))


def part02(data: Iterator[int]) -> int:
    items = (sum(xyz) for xyz in helpers.window(data, 3))
    return part01(items)


def run() -> None:
    items = helpers.get_ints(r"./data/day_01.txt")
    assert part01(items) == 1688
    assert part02(items) == 1728


if __name__ == "__main__":
    helpers.time_it(run)
