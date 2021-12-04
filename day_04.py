import itertools
from typing import Dict, List, Set, Tuple

import helpers


class Board:
    def __init__(self) -> None:
        self.rows = []
        self.cols = [[], [], [], [], []]

    def bingo(self, nums):
        for line in itertools.chain(self.rows, self.cols):
            if all(c in nums for c in line):
                return True
        return False

    def unmarked_value(self, nums: Set[int]) -> int:
        total = 0
        for row in self.rows:
            total += sum(r for r in row if r not in nums)

        return total

    def populate_cols(self):
        for r in self.rows:
            for index, c in enumerate(r):
                self.cols[index].append(c)

    def __str__(self):
        msg = ""
        for r in self.rows:
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
            b = Board()
            for i in range(5):
                b.rows.append([int(i) for i in next(lines).split()])
            b.populate_cols()
            boards.append(b)
    except StopIteration:
        pass
    return header, boards


def simulate_win_order(numbers: List[int], boards: List[Board]) -> Dict[Board, int]:
    winners = dict()  # ordered

    nums = set()
    for spin in numbers:
        for board in boards:
            nums.add(spin)
            if board not in winners:
                if board.bingo(nums):
                    unmarked = board.unmarked_value(nums)
                    winners[board] = unmarked * spin

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
