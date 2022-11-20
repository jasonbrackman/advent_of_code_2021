import itertools
from typing import Dict, List, Optional


class QuantumDie:
    def __init__(self):
        self.val1 = 1
        self.val2 = 2
        self.val3 = 3


class Die:
    def __init__(self) -> None:
        self._val = 0
        self._rolled = 0

    def roll(self) -> int:
        self._rolled += 1
        self._val += 1
        if self._val > 100:
            self._val = 1
        return self._val

    def count(self) -> int:
        return self._rolled


class Player:
    def __init__(self, name: str, pos: int) -> None:
        self._score: int = 0
        self._pos: int = pos
        self._mod: int = 10
        self._name = name
        self._winner = False

    def pos(self) -> int:
        return self._pos

    def move(self, val: int) -> None:
        self._pos = (self._pos + val) % self._mod
        self._score += self._pos if self._pos != 0 else 10
        if self._score >= 1000:
            self._winner = True

    def score(self) -> int:
        return self._score

    def pprint(self) -> None:
        print(f'Player {self.name()} is in position {self.pos()} with a score of {self.score()}')

    def is_winner(self) -> bool:
        return self._winner

    def name(self) -> str:
        return self._name


def roll_three_times(dd: Die) -> int:
    x: int = dd.roll()
    y: int = dd.roll()
    z: int = dd.roll()
    return sum((x, y, z))


def part01():
    p1 = Player('1', 10)
    p2 = Player('2', 6)
    dd = Die()

    for _ in range(10_000):

        p1.move(roll_three_times(dd))
        # print(f'Player {p1.name()} has a score {p1.score()} with a roll count of {dd.count()}')
        if p1.is_winner():
            final = p1.score() if p1.score() < p2.score() else p2.score()
            return final * dd.count()

        p2.move(roll_three_times(dd))
        # print(f'Player {p2.name()} has a score {p2.score()} with a roll count of {dd.count()}')
        if p2.is_winner():
            final = p1.score() if p1.score() < p2.score() else p2.score()
            return final * dd.count()


def part02():
    # q1 = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    # items = set()
    # for item in itertools.product(*q1):
    #     items.add(sum(item))
    return {3, 4, 5, 6, 7, 8, 9}


def run():
    assert part01() == 900099


if __name__ == "__main__":
    run()
    # part02()