import itertools
from typing import Dict, List, Set, Tuple

import helpers


class Board:
    def __init__(self, rows: List[List[int]]) -> None:
        self._rows = rows
        self._cols = helpers.rotate_matrix_right(rows)

    def bingo(self, nums: Set[int]) -> bool:
        """Check if the numbers passed in resulted in a win."""
        for line in itertools.chain(self._rows, self._cols):
            if all(c in nums for c in line):
                return True
        return False

    def unmarked_value(self, nums: Set[int]) -> int:
        total = 0
        for row in self._rows:
            total += sum(r for r in row if r not in nums)

        return total

    def __str__(self) -> str:
        msg = ""
        for r in self._rows:
            msg += "".join(str(r))
        return msg


def parse_info(lines: List[str]) -> Tuple[List[int], List[Board]]:
    lines = iter(lines)

    # Order matters for both header and boards
    header = [int(i) for i in next(lines).split(",")]
    boards = []

    try:
        while True:
            next(lines)  # skip the blank line
            rows = []
            for i in range(5):
                rows.append([int(i) for i in next(lines).split()])
            boards.append(Board(rows))
    except StopIteration:
        pass
    return header, boards


def simulate_win_order(numbers: List[int], boards: List[Board]) -> Dict[Board, int]:
    winners = dict()  # ordered

    nums = set()
    for number in numbers:
        for board in boards:
            nums.add(number)
            if board not in winners:
                if board.bingo(nums):
                    unmarked = board.unmarked_value(nums)
                    winners[board] = unmarked * number

    return winners


def run() -> None:
    lines = helpers.get_lines(r"./data/day_04.txt")
    numbers, boards = parse_info(lines)
    winners = simulate_win_order(numbers, boards)

    vals = list(winners.values())
    assert vals[0] == 14093
    assert vals[-1] == 17388


if __name__ == "__main__":
    run()
