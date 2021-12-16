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

    def get_grid(self):
        cells = dict()
        for y in range(self.y_len * self.mult):
            y_bonus = y // self.y_len
            for x in range(self.x_len * self.mult):
                x_bonus = x // self.x_len
                val = self.cells[(x % self.y_len, y % self.y_len)] + y_bonus + x_bonus
                if val > 9:
                    val %= 9
                cells[(x, y)] = val
        return cells

    def update_multi(self, num: int):
        self.mult = num

    def end_pos(self) -> Tuple[int, int]:
        return (self.x_len * self.mult) - 1, (self.y_len * self.mult) - 1


@dataclass(order=True)
class Node:
    state: Tuple[int, int]
    parent: "Node" = field(default=None)


def search(lut: LUT, pos: Tuple[int, int], end_pos: Tuple[int, int]) -> int:
    visited = set()
    pq = PriorityQueue()
    pq.put((0, Node(pos)))
    while pq:
        risk, node = pq.get()
        if node.state == end_pos:
            return risk, node
        n = neighbours(lut, node.state)
        for (node_risk, node_state) in n:
            if node_state not in visited:
                visited.add(node_state)
                pq.put((risk + node_risk, Node(node_state, node)))


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
    risk, node = search(lut, (0, 0), lut.end_pos())
    assert risk == 462

    # _ Part02
    lut.update_multi(5)
    risk, node = search(lut, (0, 0), lut.end_pos())
    assert risk == 2846


if __name__ == "__main__":
    run()
