from __future__ import annotations

from collections import deque
from typing import List, Optional, Union, Tuple, Iterator, Dict, Any, Set


def monad() -> Iterator[List[int]]:
    start = 11_111_111_111_111
    # end = 29_989_297_949_530
    end = 99_999_999_999_999
    for number in range(end, start - 1, -1):
        s = str(number)
        if "0" in s:
            continue
        # the following is commented out -- but when starting to understand the need to reduce
        # the combinations, my first attempt was to create fewer monads... which was still too
        # many.

        # if s[5] not in "12":
        #     continue
        # if s[6] not in "23456789":
        #     continue
        # if s[8] not in "3456789":
        #     continue
        # if s[10] not in "8967":
        #     continue
        # if s[11] not in "12345":
        #     continue
        # if s[12] not in "1":
        #     continue
        # if s[13] not in "89":
        #     continue

        yield [int(n) for n in s]


class Alu:
    """The ALU is a four-dimensional processing unit."""

    DIVS = [1, 1, 1, 1, 1, 26, 26, 1, 26, 1, 26, 26, 26, 26]
    ADDA = [14, 14, 14, 12, 15, -12, -12, 12, -7, 13, -8, -5, -10, -7]
    ADDB = [14, 2, 1, 13, 5, 5, 5, 9, 3, 13, 2, 1, 11, 8]
    registers = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }

    CACHE: Dict[Tuple[int, int, int, int, int], int] = {}

    def __init__(self, instructions: List[Tuple[str, str, Union[str, int]]]) -> None:
        self.number: deque[int] = deque([])
        self.instructions = instructions

    def run(self, number: List[int]) -> Tuple[List[int], int]:
        total = 0
        for num, d, aa, ab in zip(number, self.DIVS, self.ADDA, self.ADDB):
            total = self.func2(total, num, d, aa, ab)

        # total = self.original_unoptimized(number)

        return number, total

    def original_unoptimized(self, number: int) -> int:
        # original ...
        self.number = deque(number)
        self.clear_registers()
        for instruction in instructions:
            self.op(*instruction)
        if self.registers["z"] == 0:
            print("Winner!", number)
        else:
            print(self.registers["z"])
        return self.registers["z"]

    def clear_registers(self) -> None:
        self.registers["w"] = 0
        self.registers["x"] = 0
        self.registers["y"] = 0
        self.registers["z"] = 0

    def op(self, arg0: str, arg1: str, arg2: Optional[Union[str, int]] = None) -> None:
        # print(arg0, arg1, arg2)
        if arg0 == "inp":
            """Read an input value and write it to variable a."""
            self.registers[arg1] = self.number.popleft()

        if arg0 == "add":
            """Add the value of a to the value of b, then store the result in variable a."""
            b = self.registers[arg2] if arg2 in self.registers.keys() else int(arg2)
            self.registers[arg1] += b

        if arg0 == "mul":
            """Multiply the value of a by the value of b, then store the result in variable a."""
            b = arg2 if isinstance(arg2, int) else self.registers[arg2]
            self.registers[arg1] *= b

        if arg0 == "div":
            """
            Divide the value of a by the value of b, truncate the result to an integer,
            then store the result in variable a. (Here, "truncate" means to round the value
            toward zero.)
            """
            b = arg2 if isinstance(arg2, int) else self.registers[arg2]
            self.registers[arg1] //= b

        if arg0 == "mod":
            """
            Divide the value of a by the value of b, then store the remainder in variable a.
            (This is also called the modulo operation.)
            """
            b = arg2 if isinstance(arg2, int) else self.registers[arg2]
            self.registers[arg1] %= b

        if arg0 == "eql":
            """
            If the value of a and b are equal, then store the value 1 in variable a.
            Otherwise, store the value 0 in variable a.
            """
            b = arg2 if isinstance(arg2, int) else self.registers[arg2]
            a = self.registers[arg1]
            self.registers[arg1] = int(a == b)

    def func2(self, total: int, num: int, division: int, add_a: int, add_b: int) -> int:
        if (total, num, division, add_a, add_b) in self.CACHE:
            return self.CACHE[(total, num, division, add_a, add_b)]

        total = self.forward(total, num, division, add_a, add_b)

        self.CACHE[(total, num, division, add_a, add_b)] = total
        return total

    # - - - - - - - -- - - - - - - - - - -
    # After several optimization steps -- it still wasn't enough -- so creating a forward/backward
    # functions to figure out what possible numbers could be used to derive a known answer.
    #
    # Since we must have zero in the register before starting, we find out what all digits 1-9 will generate for z
    # This in turn provides the next step 9 * 9 combinations and so on.
    # This reveals that seven of the slots that have a reduced number of options and even fewer that can make it
    # all the way through to all 14 slots using this technique.
    #
    # By examining items that can reach the 14th position, must mean that those combinations are valid.  Collecting
    # them all and sorting and taking the min/max of those numbers reveals the answer for this puzzle.

    @staticmethod
    def forward(total: int, num: int, division: int, add_a: int, add_b: int) -> int:
        x_val = (total % 26) + add_a

        if division == 26:
            total //= division

        if x_val != num:
            total = 26 * total + num + add_b

        return total

    @staticmethod
    def backward(
        total: int, num: int, division: int, add_a: int, add_b: int
    ) -> List[int]:
        zs = []
        x = total - num - add_b
        if x % 26 == 0:
            zs.append(x // 26 * division)
        if 0 <= num - add_a < 26:
            z0 = total * division
            zs.append(num - add_a + z0)

        return zs


def parse() -> List[Tuple[str, str, str | int]]:
    result = []
    with open("./data/day_24.txt", "r", encoding="utf-8") as handle:
        for line in handle.readlines():
            items = line.split()
            if len(items) == 2:
                result.append((items[0], items[1]))
            if len(items) == 3:
                a, b, c = items[0], items[1], items[2]
                c = int(c) if c.isdigit() else c
                result.append((a, b, c))
    return result


class Node:
    def __init__(
        self, state: Tuple[int, int, int], parent: Optional[Node] = None
    ) -> None:
        self.state = state
        self.parent = parent


def lock_pick(start: int, d: int, aa: int, ab: int) -> List[Tuple[int, int]]:
    results = []
    for index in range(9, 0, -1):
        f = Alu.forward(start, index, d, aa, ab)
        goods = Alu.backward(f, index, d, aa, ab)
        for g in goods:
            if g == start:
                results.append((f, index))
    return results


def run() -> None:
    # Collect all possible combinations
    # This is much reduced from the 9 ** 14
    # Seven of the numbers are limited in some way
    # the BFS also reduces the possible end points so some things may end early.
    levels: Dict[int, Set[Node]] = {}
    stack = deque([Node((0, 0, 0))])
    while stack:
        node = stack.popleft()  # bfs
        current, level, num = node.state
        results = lock_pick(current, Alu.DIVS[level], Alu.ADDA[level], Alu.ADDB[level])
        if len(results) == 1:
            if level not in levels:
                levels[level] = set()
            for r in results:
                levels[level].add(Node((r[0], level + 1, r[1]), parent=node))

        for (item, num) in results:
            if level < 13:
                stack.append(Node((item, level + 1, num), parent=node))

    visited = set()
    for r in levels[13]:
        final = []
        while r.parent is not None:
            final.append(r.state[2])
            r = r.parent
        final_s = int("".join(reversed([str(s) for s in final])))
        if final_s not in visited:
            visited.add(final_s)
    assert max(visited) == 29989297949519
    assert min(visited) == 19518121316118


# def _used_this_to_figure_out_assembly():
#     instructions = parse()
#     m = monad()
#
#     from time import time
#
#     t1 = time()
#     for _ in range(1):
#         a = Alu(instructions)
#         num, result = a.run(next(m))
#         if result == 0:
#             print("Winner!:", "".join(str(r) for r in num))
#         print(num)
#     t2 = time() - t1
#     print(t2)


if __name__ == "__main__":
    run()
