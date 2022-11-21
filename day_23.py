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
from __future__ import annotations

import copy
from queue import PriorityQueue
from functools import cache
from typing import Dict, Tuple, Optional, List

from helpers import lines_raw, Node
from visuals import display

ENERGY_LUT = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

HALL = {
    "H": ((1, 1), (1, 2), (1, 4), (1, 6), (1, 8), (1, 10), (1, 11)),
}


def parse_data(data: List[str]) -> Dict[Tuple[int, int], str]:
    pods = dict()
    for row in range(len(data)):
        for col in range(len(data[row])):
            icon = data[row][col]
            if icon in (" ", "#"):
                pass
            else:
                pods[(row, col)] = icon

    return pods


def winner(
    state: Dict[Tuple[int, int], str], rooms: Dict[str, Tuple[Tuple[int, int], ...]]
) -> bool:
    for room_name, pods in rooms.items():
        for pod in pods:
            if state[pod] != room_name:
                return False
    return True


def in_final_spot(
    state: Dict[Tuple[int, int], str],
    rooms: Dict[str, Tuple[Tuple[int, int], ...]],
    pod_name: str,
    pos: Tuple[int, int],
) -> bool:
    positions = rooms[pod_name]
    if pos not in positions:
        return False

    # if the floors before the room are filled with the pod_name; then good to go.
    for p in positions:
        if pos == p:
            return True
        else:
            current_name = state[p]
            if current_name != pod_name:
                return False

    return False


def room_available(
    state: Dict[Tuple[int, int], str],
    rooms: Dict[str, Tuple[Tuple[int, int], ...]],
    room_name: str,
) -> Optional[Tuple[int, int]]:
    lowest_floor_available = None

    positions = rooms[room_name]

    # from lower floor to top check for: (1) room_name else False (2) then for '.' else False
    for p in positions:
        icon = state[p]
        if icon == ".":
            if lowest_floor_available is None:
                lowest_floor_available = p

        elif icon == room_name:
            # pass unless a floor is already empty -- then it is blocking.
            if lowest_floor_available is not None:
                return None

        else:
            # blocked
            return None

    return lowest_floor_available


@cache
def pos_neighbours(
    state: Dict[Tuple[int, int], str], pos: Tuple[int, int]
) -> List[Tuple[int, int]]:
    up = pos[0] - 1, pos[1]
    dn = pos[0] + 1, pos[1]
    lt = pos[0], pos[1] - 1
    rt = pos[0], pos[1] + 1

    return [d for d in (up, lt, rt, dn) if d in state]


def path_is_clear(
    state: Dict[Tuple[int, int], str], src: Tuple[int, int], dst: Tuple[int, int]
) -> int:
    q = {
        (src, 0),
    }
    visited = {
        src,
    }
    while q:
        n, c = q.pop()
        if n == dst:
            return c

        for pos in pos_neighbours(tuple(state.keys()), n):
            if pos not in visited:
                visited.add(pos)
                if state[pos] == ".":
                    q.add((pos, c + 1))

    return 0


def successors(
    state: Dict[Tuple[int, int], str], rooms: Dict[str, Tuple[Tuple[int, int], ...]]
) -> List[Tuple[int, Tuple[int, int], Tuple[int, int]]]:
    room_found = False
    results = []
    for src, pod_name in state.items():
        if pod_name == ".":
            continue  # nothing to do; this is not a pod

        if in_final_spot(state, rooms, pod_name, src):
            continue  # nothing to do; this pod is in a final room

        # The rest of the items are either in the WRONG ROOM or in a HALLWAY

        # Is a path to a good ROOM available?
        dst = room_available(state, rooms, pod_name)
        if dst:
            dist = path_is_clear(state, src, dst)
            if dist > 0:
                room_found = True
                # Room available and we can get there?  Let's GO!
                results.append((dist, src, dst))

        # All that is left are options to leave a bad room and go into the hallway (if spot/path is available.)
        if room_found is False:
            if src not in HALL["H"]:
                for dst in HALL["H"]:
                    dist = path_is_clear(state, src, dst)
                    if dist > 0:
                        results.append((dist, src, dst))

    return results


def pprint(lines: List[str], state: Dict[Tuple[int, int], str]) -> None:
    raw = [list(line) for line in lines]
    for k, v in state.items():
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


def raw(lines: List[str], state: Dict[Tuple[int, int], str]) -> None:
    raw = [list(line) for line in lines]
    for k, v in state.items():
        i, j = k
        if v is None:
            raw[i][j] = "."
        else:
            raw[i][j] = v

    return raw


def bfs(
    state: Dict[Tuple[int, int], str], rooms: Dict[str, Tuple[Tuple[int, int], ...]]
) -> Optional[Node]:
    q: PriorityQueue[Node] = PriorityQueue()
    q.put(Node(state, None, cost=0))
    seen = {
        (0, tuple(state.values())),
    }

    while not q.empty():
        node = q.get()

        state = node.state
        cost = node.cost
        if winner(state, rooms):
            return node

        for dist, src, dst in successors(state, rooms):

            new_state = copy.deepcopy(state)

            new_cost = cost + ENERGY_LUT[state[src]] * dist
            new_state[src], new_state[dst] = new_state[dst], new_state[src]

            new_state_hash: Tuple[int, Tuple[str, ...]] = (
                new_cost,
                tuple(new_state.values()),
            )
            if new_state_hash not in seen:
                seen.add(new_state_hash)
                q.put(Node(new_state, node, cost=new_cost))

    return None


def run() -> None:

    lines = lines_raw(r"./data/day_23.txt")
    state = parse_data(lines)

    rooms: Dict[str, Tuple[Tuple[int, int], ...]] = {
        "A": ((3, 3), (2, 3)),
        "B": ((3, 5), (2, 5)),
        "C": ((3, 7), (2, 7)),
        "D": ((3, 9), (2, 9)),
    }
    result = bfs(state, rooms)
    assert result.cost == 18_051

    lines = lines_raw(r"./data/day_23_part2.txt")
    state = parse_data(lines)
    rooms: Dict[str, Tuple[Tuple[int, int], ...]] = {
        "A": ((5, 3), (4, 3), (3, 3), (2, 3)),
        "B": ((5, 5), (4, 5), (3, 5), (2, 5)),
        "C": ((5, 7), (4, 7), (3, 7), (2, 7)),
        "D": ((5, 9), (4, 9), (3, 9), (2, 9)),
    }
    result = bfs(state, rooms)
    assert result.cost == 50_245

    # items = []
    #
    # while result is not None:
    #     r = raw(lines, result.state)
    #     items.append(r)
    #     result = result.parent
    #
    # count = 0
    # for r in reversed(items):
    #     display.generic_out(
    #         r,
    #         {
    #             "#": "blackish",
    #             ".": "white",
    #             "A": "red",
    #             "B": "green",
    #             "C": "blue",
    #             "D": "purple",
    #         },
    #         "day_23",
    #         count,
    #     )
    #     count += 1
    # display.generate_gif(r"./images", "day_23")


if __name__ == "__main__":
    run()
