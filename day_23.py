"""
Amber (A)  - 1 energy per step,
Bronze (B) - 10 energy,
Copper (C) - 100 energy,
Desert (D) - 1000 energy

walls = #
open = .

RULES:
Amphipods will never stop on the space immediately outside any room.
--> They can move into that space so long as they immediately continue moving.
--> This refers to the four open spaces in the hallway that are directly above an amphipod starting position.

Amphipods will never move from the hallway into a room unless that room is their destination
--> and that room contains no amphipods which do not also have that room as their own destination.
--> If an amphipod's starting room is not its destination room, it can stay in that room until it leaves the room.
--> For example, an Amber amphipod will not move from the hallway into the right three rooms,
--> and will only move into the leftmost room if that room is empty or if it only contains other Amber amphipods.

Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into a room.
--> Once any amphipod starts moving, any other amphipods currently in the hallway are locked in place
--> and will not move again until they can move fully into a room.

- I want to ensure the hallways have same items adjacent to each other
- I want to know the cheapest solution
"""

import sys
from functools import cache
from typing import Dict, Tuple, Optional, List, Set

from helpers import lines_raw


class Burrow:
    HALL = {
        "H": ((1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)),
    }

    ROOMS = {
        "A": ((2, 3), (3, 3)),
        "B": ((2, 5), (3, 5)),
        "C": ((2, 7), (3, 7)),
        "D": ((2, 9), (3, 9)),
    }

    ENERGY_LUT = {
        "A": 1,
        "B": 10,
        "C": 100,
        "D": 1000,
    }

    def __init__(self):
        self._raw: List[List[str]] = []
        self._pods: Dict[Tuple[int, int], str] = {}
        self.cost = 0

    def __hash__(self):
        return hash(tuple(self._pods.items()))

    def __str__(self) -> str:
        raw = self._raw
        for k, v in self._pods.items():
            i, j = k
            if v is None:
                raw[i][j] = "."
            else:
                raw[i][j] = v
        s = ""
        for r in raw:
            s += "".join(r)
            s += "\n"
        return s

    def set_data(self, data):
        self.cost = 0
        self._pods.clear()
        self._raw.clear()

        self._raw = [list(d) for d in data]
        for row in range(len(data)):
            for col in range(len(data[row])):
                icon = data[row][col]
                if icon in (" ", '#'):
                    pass
                else:
                    self._pods[(row, col)] = icon

        return self._pods

    @cache
    def get_neighbours(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        up = pos[0] - 1, pos[1]
        dn = pos[0] + 1, pos[1]
        lt = pos[0], pos[1] - 1
        rt = pos[0], pos[1] + 1
        return [d for d in (up, lt, rt, dn) if d in self._pods]

    def state(self):
        return self.cost, tuple(self._pods.items())

    def move(self, dist, source, destination) -> None:
        self.cost += Burrow.ENERGY_LUT[self._pods[source]] * dist
        self._pods[source], self._pods[destination] = self._pods[destination], self._pods[source]

    def room_available(self, room_name) -> Optional[Tuple[int, int]]:
        positions = Burrow.ROOMS[room_name]

        high = self._pods[positions[0]]  # | |
        low = self._pods[positions[1]]   # |_|

        if low == '.' and high == '.':
            return positions[1]

        if low == room_name and high == '.':
            return positions[0]

        return None

    def path_is_clear(self, src, dst) -> int:
        q = {(src, 0), }
        visited = {src, }
        while q:
            n, c = q.pop()
            if n == dst:
                return c

            for pos in self.get_neighbours(n):
                if pos not in visited:
                    visited.add(pos)
                    if self._pods[pos] == '.':
                        q.add((pos, c+1))

        return 0

    def destinations(self):
        possibles = []

        # Let's go through all pods...
        for pos, pod_name in self._pods.items():
            if pod_name == '.':
                continue  # nothing to do; this is not a pod

            if self.in_final_spot(pod_name, pos):
                continue  # nothing to do; this pod is in a final room

            # The rest of the items are either in the WRONG ROOM or in a HALLWAY

            # Is a path to a good ROOM available?
            room = self.room_available(pod_name)
            if room:
                dist = self.path_is_clear(pos, room)
                if dist > 0:
                    # Room available and we can get there?  Let's GO!
                    return [(dist, pos, room)]

            # All that is left are options to leave a bad room and go into the hallway (if spot/path is available.)
            if pos not in Burrow.HALL['H']:
                for hallway in Burrow.HALL['H']:
                    dist = self.path_is_clear(pos, hallway)
                    if dist > 0:
                        possibles.append((dist, pos, hallway))

        return sorted(possibles, key=lambda x: x[0])

    def is_solved(self) -> bool:
        for room_name, pods in Burrow.ROOMS.items():
            for pod in pods:
                if str(self._pods[pod]) != room_name:
                    return False
        return True

    def winner(self, state) -> bool:
        for room_name, pods in Burrow.ROOMS.items():
            for pod in pods:
                if str(state[pod]) != room_name:
                    return False
        return True

    def in_final_spot(self, entity_name, pos) -> bool:
        positions = Burrow.ROOMS[entity_name]
        low = self._pods[positions[1]]

        if pos not in positions:
            return False

        if pos in positions:
            if pos == positions[1]:  # low position of the room (must be good).
                return True

            if pos == positions[0] and low and low == entity_name:
                return True

        return False

def do_work(burrow: Burrow, max_cost: int, seen: Set[int] = None) -> Optional[int]:
    if seen is None:
        seen = {burrow.state(), }

    if burrow.is_solved():
        return burrow.cost

    for dist, pos, neighbour in burrow.destinations():
        burrow.move(dist, pos, neighbour)
        state = burrow.state()
        if state not in seen:
            seen.add(state)
            if burrow.cost < max_cost:
                result = do_work(burrow, max_cost, seen)
                if result is not None:
                    return result

        burrow.move(dist * -1, neighbour, pos)
    return None


def part01(lines, max_cost: int) -> int:
    burrow = Burrow()
    costs = {max_cost, }
    while max_cost is not None:
        burrow.set_data(lines)
        max_cost = do_work(burrow, max_cost)
        if max_cost is not None:
            costs.add(max_cost)
    return min(costs)


def run():
    lines = lines_raw(r"./data/day_23.txt")
    max_cost = sys.maxsize  # 18051  # sys.maxsize
    assert part01(lines, max_cost) == 18_051
    # print(part02(lines, max_cost))  # 15_060?
    # import cProfile
    #
    # pr = cProfile.Profile()
    # pr.enable()
    # print(part01(lines, max_cost))
    # pr.disable()
    # pr.print_stats(sort="calls")



if __name__ == "__main__":
    run()

