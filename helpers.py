import json
import multiprocessing
import time
from dataclasses import dataclass
from itertools import tee, pairwise
from typing import Any, List, NamedTuple, Iterator


def get_lines(path: str) -> List[str]:
    with open(path, "r") as text:
        return [line.strip() for line in text.readlines()]


def get_ints(path: str) -> List[int]:
    with open(path, "r") as text:
        return [int(i) for i in text.readlines()]


def yield_ints(path: str) -> Iterator[int]:
    with open(path, "r") as text:
        for i in text.readlines():
            yield int(i)


def window(iterable: Iterator[Any], size: int) -> Iterator[Any]:
    if size == 2:
        # Use the built-in pairwise
        return pairwise(iterable)

    items = tee(iterable, size)
    for count, item in enumerate(items):
        for c in range(count):
            next(item, None)
    return zip(*items)


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


@dataclass
class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Pos(self.x * other, self.y * other)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y + other.y)


class Node:
    def __init__(self, state, parent) -> None:
        """
        :param state: The Node identity to be compared to another Node.
        :param parent:
        """
        self.state = state
        self.parent = parent


def rotate_matrix_right(grid: List[List[Any]]) -> List[List[Any]]:
    rotated = [[] for _ in range(len(grid[0]))]
    for cell in grid:
        for index, c in enumerate(cell):
            rotated[index].append(c)
    return rotated


# def bfs(
#     initial: T, goal_test: Callable[[T], bool], successors: Callable[[T], List[T]]
# ) -> Optional[Node[T]]:
#     # frontier is where we've yet to go
#     frontier: Queue[Node[T]] = Queue()
#     frontier.push(Node(initial, None))  # explored is where we've been
#
#     explored: Set[T] = {initial}
#
#     # keep going while there is more to explore
#     while not frontier.empty:
#         current_node: Node[T] = frontier.pop()
#         current_state: T = current_node.state  # if we found the goal, we're done
#         if goal_test(current_state):
#             return current_node
#
#         # check where we can go next and haven't explored
#         for child in successors(current_state):
#             if child in explored:  # skip children we already explored
#                 continue
#             explored.add(child)
#             frontier.push(Node(child, current_node))
#
#     return None


def time_it(command):
    t1 = time.perf_counter()
    command()
    print(
        f"[{str(command.__module__)}.{command.__name__}]: Completed in {(time.perf_counter() - t1)*1_000:0.1f} ms"
    )


def time_it_all(args: List):
    with multiprocessing.Pool(4) as p:
        p.map(time_it, args)
