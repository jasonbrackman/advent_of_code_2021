from __future__ import annotations

import re
from collections import deque
from typing import Iterator, List, Optional, Tuple

import helpers


class NodePair:
    EXPLODE_DEPTH = 4
    NUM_PATTERN = re.compile(r"-?\d+")

    def __init__(self, value=None, depth=None, parent=None):
        self.left: Optional[NodePair] = None
        self.right: Optional[NodePair] = None
        self.value: Optional[int] = value

        self.parent: Optional[NodePair] = parent
        self.depth: int = 0 if depth is None else depth

    def load(self, fish: List[List], node=None):
        if node is None:
            node = self

        left, right = fish

        if isinstance(left, int):
            node.left = NodePair(depth=node.depth + 1, parent=node)
            node.left.value = left
        else:
            node.left = self.load(left, NodePair(depth=node.depth + 1, parent=node))

        if isinstance(right, int):
            node.right = NodePair(depth=node.depth + 1, parent=node)
            node.right.value = right
        else:
            node.right = self.load(right, NodePair(depth=node.depth + 1, parent=node))

        return node

    @staticmethod
    def neighbours(node: NodePair) -> Tuple[Optional[NodePair], Optional[NodePair]]:
        p, n = None, None

        if node == node.root():
            return p, n

        if node.is_value():
            p, n = NodePair._neighbours(node)
        else:
            if node.left is not None:
                p, _ = NodePair._neighbours(node.left)
            if node.right is not None:
                _, n = NodePair._neighbours(node.right)

        return p, n

    def explode(self, node: NodePair) -> None:
        l_node, r_node = self.neighbours(node)

        if l_node and node.left:
            l_node.value += node.left.value
            node.left.value = 0

        if node.left:
            node.left.value = 0

        if r_node and node.right:
            r_node.value += node.right.value

        if node.right:
            node.right.value = 0

        if (node.left is node.right is None) is False:
            if node.left:
                node.value = node.left.value
                node.left = None
            if node.right:
                node.value = node.right.value
                node.right = None

    @staticmethod
    def _neighbours(node):
        prev_ = None
        next_ = None
        seen_ = False
        root_node = node.root()
        for n in NodePair.traverse(root_node):
            if n == node:
                seen_ = True
                continue
            else:
                if n.is_value():
                    if not seen_:
                        prev_ = n
                    else:
                        next_ = n
                        break
        return prev_, next_

    def is_value(self):
        return self.value is not None

    @staticmethod
    def can_calc(n: NodePair):
        if n.left is None or n.left.value is None:
            return False
        if n.right is None or n.right.value is None:
            return False
        return True

    def root(self):
        n = self
        while n.parent is not None:
            n = n.parent
        return n

    def add_left(self, other):
        self.left = other
        other.parent = self
        self.update_depth()

    def add_right(self, other):
        self.right = other
        other.parent = self
        self.update_depth()

    def update_depth(self):
        for x in self.traverse_bfs(self.root()):
            if x.parent is None:
                x.depth = 0
            else:
                x.depth = x.parent.depth + 1

    @staticmethod
    def add(n1, n2):
        new_node = NodePair(depth=0)
        n1.parent = new_node
        n2.parent = new_node
        new_node.left = n1
        new_node.right = n2

        # _ update the depth/parent
        for t in NodePair.traverse(new_node):
            if t != new_node:
                t.depth += 1

        return new_node

    @staticmethod
    def traverse_bfs(node: NodePair) -> Iterator[NodePair]:
        q = deque([node])
        visited = set()
        while q:
            n = q.popleft()
            visited.add(n)
            yield n

            if n.left and n.left not in visited:
                q.append(n.left)
            if n.right and n.right not in visited:
                q.append(n.right)

    @staticmethod
    def traverse(node: NodePair) -> Iterator[NodePair]:
        if node.left is not None:
            yield from NodePair.traverse(node.left)

        yield node

        if node.right is not None:
            yield from NodePair.traverse(node.right)

    def find_explosive_nodes(self) -> List[NodePair]:
        nodes = [
            n
            for n in self.traverse(self.root())
            if n.depth == self.EXPLODE_DEPTH and n.value is None
        ]
        return nodes

    def __str__(self):
        return (
            f"{self.value}"
            if self.is_value()
            else f'[{self.left or ""},{self.right or ""}]'
        )

    def pprint(self):
        print("*--")
        for x in NodePair.traverse(self):
            print("\t" * x.depth, f"{x.value if x.is_value() else '>'}")
        print("--*")

    def split_big_number(self) -> Tuple[NodePair, Optional[NodePair]]:
        """Find all numbers greater than 10 and return the parents to then do an ordered operation from
        left to right of exploding them into sets of two numbers."""
        for x in self.traverse(self.root()):
            if x.is_value():
                v = x.value
                if v > 9:
                    # let's split
                    plus_one = 1 if v % 2 != 0 else 0

                    n1 = NodePair(depth=x.depth + 1, parent=x)
                    n1.value = v // 2

                    n2 = NodePair(depth=x.depth + 1, parent=x)
                    n2.value = v // 2 + plus_one

                    x.left = n1
                    x.right = n2
                    x.value = None

                    return self, x
        return self, None

    def magnitude(self) -> Optional[int]:

        root_node = self.root()

        def get_next():
            for n in NodePair.traverse(root_node):
                if NodePair.can_calc(n):
                    return n
            return None

        n = get_next()

        while n is not None:
            n.value = self._magnify(n)
            n.left = n.right = None

            if n.parent is None:
                return n.value

            n = get_next()

        return None

    @staticmethod
    def _magnify(n) -> int:
        """Will raise if caller did not ensure a self.can_calc can happen."""

        t1 = 3 * n.left.value
        t2 = 2 * n.right.value
        t = t1 + t2
        # print(f'3 * {n.left.value} + 2 * {n.right.value} = ')
        # print(f'{t1} + {t2} = {t}')
        return t

    @staticmethod
    def explode_created(root_node: NodePair, created: NodePair) -> bool:
        nodes = root_node.find_explosive_nodes()
        for n in nodes:
            if created == n:
                root_node.explode(n)
                return True
        return False


def reduce(root_node):

    # __ explode nodes
    nodes = root_node.find_explosive_nodes()
    for n in nodes:
        root_node.explode(n)
        yield root_node

    created = True
    while created:
        # __ split nodes
        root_node, created = root_node.split_big_number()
        yield root_node

        # if this created a node that should be exploded do it now.
        result = root_node.explode_created(root_node, created)
        if result is True:
            yield root_node

    return root_node


def part01(lines: List[str]) -> int:
    school = deque([NodePair(depth=0).load(eval(line)) for line in lines])

    # primer
    final = NodePair.add(school.popleft(), school.popleft())

    while school:
        ii = reduce(final)
        t = None
        for i in ii:
            t = i
        final = NodePair.add(t, school.popleft())

    r: Optional[NodePair] = None
    ii = reduce(final)
    for i in ii:
        r = i

    return r.magnitude()


def part02(lines: List[str]) -> int:
    nums = []
    for fish1 in lines:
        for fish2 in lines:
            t1 = NodePair(depth=0).load(eval(fish1))
            t2 = NodePair(depth=0).load(eval(fish2))
            if str(t1) == str(t2):
                continue

            final = NodePair.add(t1, t2)
            r = [i for i in reduce(final)]
            if r:
                nums.append(r[-1].magnitude())

    return max(nums)


def run() -> None:
    lines = helpers.get_lines(r"./data/day_18.txt")

    assert part01(lines) == 3551
    assert part02(lines) == 4555


if __name__ == "__main__":
    run()
