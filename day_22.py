from dataclasses import dataclass
from typing import Tuple, Dict, Optional

cuboid: Dict[Tuple[int, int, int], bool] = {}

MIN = -50
MAX = 50


def frame(nums: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    if nums[0] <= MIN and nums[1] <= MIN:
        return None
    if nums[0] >= MAX and nums[1] >= MAX:
        return None

    new_min = MIN if nums[0] < MIN else nums[0]
    new_max = MAX if nums[1] > MAX else nums[1]
    return new_min, new_max


def parse() -> None:
    with open(r"data/day_22.txt", encoding="utf-8") as file:
        for line in file.readlines():
            cmd, instr = line.strip().split()
            items = []
            for p in instr.split(","):
                stuff = tuple(int(r) for r in p[2:].split(".") if r != "")
                items.append(stuff)
            xs, ys, zs = items
            # print(cmd, xs)
            # print(cmd, ys)
            # print(cmd, zs)
            # print()
            xs = frame(items[0])
            ys = frame(items[1])
            zs = frame(items[2])
            if None in (xs, ys, zs):
                continue

            for x in range(xs[0], xs[1] + 1):
                for y in range(ys[0], ys[1] + 1):
                    for z in range(zs[0], zs[1] + 1):
                        cuboid[(x, y, z)] = cmd == "on"

    part01 = 0
    for k, v in cuboid.items():
        part01 += v
    assert part01 == 623748


def run() -> None:
    parse()


if __name__ == "__main__":
    run()
