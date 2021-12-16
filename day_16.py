import collections
from enum import Enum
from typing import Callable
import math

import helpers


class LengthType(Enum):
    FIFTEEN_BIT = 0
    ELEVEN_BIT = 1


class Packet:
    hex_to_bin = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }

    def __init__(self):
        self.m = None
        self.p = 0
        self.versions = []
        self.q = True
        self.stack = collections.defaultdict(list)

    def load(self, line):
        self.p = 0
        self.m = ''.join([self.hex_to_bin[c] for c in line])
        self.versions.clear()
        self.stack.clear()

        if not self.q:
            print('Memory:', self.m)

    def step(self, stack_id=0):
        if self.p > len(self.m):
            raise MemoryError("Pointer ran past program length.")

        self._get_version()
        id_ = self._get_id()

        current_func = None
        if id_ == 4:
            self._process_id4(stack_id)
        else:
            if id_ == 0:
                current_func = sum
            elif id_ == 1:
                current_func = math.prod
            elif id_ == 2:
                current_func = min
            elif id_ == 3:
                current_func = max
            elif id_ == 5:
                current_func = lambda gt: int(gt[0] > gt[1])
            elif id_ == 6:
                current_func = lambda lt: int(lt[0] < lt[1])
            elif id_ == 7:
                current_func = lambda eq: int(eq[0] == eq[1])

            length_type_id = self._get_length_type()

            # 15-bit number
            if length_type_id == LengthType.FIFTEEN_BIT:
                num = self.m[self.p: self.p + 15]
                self.p += 15

                read_mem = self.p + (int(num, 2))
                stack_id += 1
                while self.p < read_mem:
                    self.step(stack_id)

            # 11 bit number
            elif length_type_id == LengthType.ELEVEN_BIT:
                num = self.m[self.p: self.p + 11]
                self.p += 11
                stack_id += 1
                for _ in range(int(num, 2)):
                    self.step(stack_id)

        if current_func is not None:
            self._calculate(current_func, stack_id)
            pop = self.stack[stack_id].pop()
            stack_id -= 1
            self.stack[stack_id].append(pop)

    def _calculate(self, current_func: Callable, stack_id: int):
        if not self.q:
            print(current_func, self.stack[stack_id], '=')
        self.stack[stack_id] = [current_func(self.stack[stack_id])]

    def _get_length_type(self) -> LengthType:
        # this is op code domain -- any id that is not 4
        v = int(self.m[self.p], 2)
        self.p += 1
        return LengthType.FIFTEEN_BIT if v == 0 else LengthType.ELEVEN_BIT

    def _process_id4(self, stack_id: int):
        """
        Loop through the packets' data until instructed to stop.
        :param stack_id: The current level of the memory stack to operate on.
        :return: a literal base 10 value of the binary numbers collected.
        """

        if not self.q:
            print(">>OpCode4 - Processing a literal value")
        cmd = int(self.m[self.p], 2)

        self.p += 1
        num = ''
        while cmd != 0:
            num += self.m[self.p:self.p + 4]
            self.p += 4
            cmd = int(self.m[self.p], 2)
            self.p += 1
        num += self.m[self.p:self.p + 4]
        self.p += 4
        self.stack[stack_id].append(int(num, 2))

    def _get_id(self) -> int:
        """Return opcode id for the packet."""
        id_ = int(self.m[self.p:self.p + 3], 2)
        self.p += 3
        return id_

    def _get_version(self) -> int:
        """Return version of the packet."""
        version = int(self.m[self.p:self.p + 3], 2)
        self.versions.append(version)
        self.p += 3
        return version


def run():
    tests()
    lines = helpers.get_lines(r'./data/day_16.txt')
    packet = Packet()
    packet.load(lines[0])
    packet.step()
    assert sum(packet.versions) == 1007
    assert packet.stack[0][0] == 834151779165


def tests():
    lines = helpers.get_lines(r'./data/day_16_test.txt')
    expect = [2021]
    packet = Packet()
    packet.load(lines[0])
    packet.step()
    assert packet.stack[0] == [2021], f"Expected {expect}, but received {packet.stack}"

    packet.load(lines[1])
    packet.step()
    assert packet.stack[0] == [1], f"Expected [1], but received {packet.stack[0]}"

    packet.load(lines[2])
    packet.step()
    assert packet.stack[0] == [3]

    packet.load(lines[3])
    packet.step()
    assert sum(packet.versions) == 16

    packet.load(lines[4])
    packet.step()
    assert sum(packet.versions) == 12

    packet.load(lines[5])
    packet.step()
    assert sum(packet.versions) == 23

    packet.load(lines[6])
    packet.step()
    assert sum(packet.versions) == 31

    packet.load(lines[7])
    packet.step()
    assert packet.stack[0] == [3]

    packet.load(lines[8])
    packet.step()
    assert packet.stack[0] == [54]

    packet.load(lines[9])
    packet.step()
    assert packet.stack[0] == [7]

    packet.load(lines[10])
    packet.step()
    assert packet.stack[0] == [9]

    packet.load(lines[11])
    packet.step()
    assert packet.stack[0] == [1]

    packet.load(lines[12])
    packet.step()
    assert packet.stack[0] == [0]

    packet.load(lines[13])
    packet.step()
    assert packet.stack[0] == [0]

    packet.load(lines[14])
    packet.step()
    assert packet.stack[0] == [1], f"Expected [1], received {packet.stack[0]}"


if __name__ == "__main__":
    run()