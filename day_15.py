from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple

import helpers


@dataclass
class LUT:
    mult: int = field(default=1)
    y_len: int = field(init=False)
    x_len: int = field(init=False)
    cells: dict = field(init=False)

    def load(self, lines: List[str]) -> "LUT":
        # _ y_len
        self.y_len = len(lines)

        # _ x_len
        self.x_len = len(lines[0])

        # _ update cells
        cells = dict()
        for y in range(self.y_len):
            for x in range(self.x_len):
                cells[(x, y)] = int(lines[y][x])
        self.cells = cells

        return self

    def update_multi(self, num: int):
        self.mult = num

    def end_pos(self) -> Tuple[int, int]:
        return (self.x_len * self.mult) - 1, (self.y_len * self.mult) - 1


def search(lut: LUT, pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    visited = set()
    pq = PriorityQueue()
    pq.put((0, pos))
    while pq:
        risk, state = pq.get()
        if state == end_pos:
            return risk
        n = neighbours(lut, state)
        for (node_risk, node_state) in n:
            if node_state not in visited:
                visited.add(node_state)
                pq.put((risk + node_risk, node_state))


def neighbours(lut: LUT, pos: Tuple[int, int]) -> List[Tuple[int, Tuple[int, int]]]:
    found = []

    x, y = pos
    x_bonus = x // lut.x_len
    y_bonus = y // lut.y_len

    for yy in (y + 1, y + -1):
        if 0 <= yy < lut.mult * lut.y_len:
            yy_bonus = yy // lut.y_len
            bonus = yy_bonus + x_bonus
            val = lut.cells[(x % lut.y_len, yy % lut.y_len)] + bonus
            if val > 9:
                val %= 9
            found.append((val, (x, yy)))

    for xx in (x + 1, x + -1):
        if 0 <= xx < lut.mult * lut.x_len:
            xx_bonus = xx // lut.x_len
            bonus = xx_bonus + y_bonus
            val = lut.cells[(xx % lut.x_len, y % lut.x_len)] + bonus
            if val > 9:
                val %= 9

            found.append((val, (xx, y)))

    return found


def run() -> None:
    lines = helpers.get_lines(r"./data/day_15.txt")

    lut = LUT().load(lines)

    # _ Part01
    assert search(lut, (0, 0), lut.end_pos()) == 462

    # _ Part02
    lut.update_multi(5)
    assert search(lut, (0, 0), lut.end_pos()) == 2846


if __name__ == "__main__":
    run()
