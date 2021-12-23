import collections
import re
from typing import Iterator, List, Optional

import helpers



class Node:
    EXPLODE_DEPTH = 4
    NUM_PATTERN = re.compile(r"-?\d+")

    def __init__(self, depth, parent=None):
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.value: Optional[int] = None

        self.parent: Optional["Node"] = parent
        self.depth: int = depth

    def __lt__(self, other):
        return self.depth < other.depth

    def load(self, fish, node=None):
        if node is None:
            node = self

        left, right = fish

        if isinstance(left, int):
            node.left = left
        else:
            node.left = self.load(left, Node(node.depth + 1, parent=node))

        if isinstance(right, int):
            node.right = right
        else:
            node.right = self.load(right, Node(node.depth + 1, parent=node))

        return node

    def can_calc(self, n) -> bool:
        if isinstance(self, Node):
            a = n.left
            b = n.right
            return isinstance(a, int) is isinstance(b, int) is True
        return False

    def _magnify(self, n) -> int:
        """Will raise if caller did not enusure a self.can_calc can happen."""
        return 3 * n.left + 2 * n.right

    def magnitude(self) -> int:

        node = self.root()
        left_switch = True
        while isinstance(node, Node):
            if node.can_calc(node):
                if node.parent is None:
                    return self._magnify(node)

                v = 3 * node.left + 2 * node.right

                if left_switch:
                    left_switch = False
                    node.parent.left = v
                else:
                    left_switch = True
                    node.parent.right = v
                node = self.root()

            if isinstance(node.left, int) and isinstance(node.right, Node):
                node = node.right
                left_switch = False
                continue

            if isinstance(node.left, Node) and isinstance(node.right, int):
                node = node.left
                left_switch = True
                continue

            if left_switch:
                node = node.left
            else:
                node = node.right

        return self._magnify(self)

    def root(self):
        n = self
        while n.parent is not None:
            n = n.parent
        return n

    @staticmethod
    def add(n1, n2):
        new_node = Node(depth=0)
        for t in n1.traverse(n1):
            if hasattr(t, "depth"):
                t.depth += 1
        new_node.left = n1
        new_node.left.parent = new_node
        for t in n2.traverse(n2):
            if hasattr(t, "depth"):
                t.depth += 1
        new_node.right = n2
        new_node.right.parent = new_node
        return new_node

    def find_explosive_nodes(self) -> List["Node"]:
        nodes = []
        for n in self.traverse(self.root()):
            if hasattr(n, "depth"):
                if n.depth == self.EXPLODE_DEPTH:
                    nodes.append(n)
        return nodes

    def split_big_numbers(self, node=None):
        """Find all numbers greater than 10 and return the parents to then do an ordered operation from
        left to right of exploding them into sets of two numbers."""

        created = []

        s = str(self)

        items = re.findall(self.NUM_PATTERN, str(self) if node is None else str(node))
        for item in items:

            v = int(item)
            if v > 9:
                plus_one = 1 if v % 2 != 0 else 0
                n = str([v // 2, v // 2 + plus_one])
                s = s.replace(str(v), n, 1)
                created.insert(0, n)
                return Node(depth=0).load(eval(s)), created
        return Node(depth=0).load(eval(s)), created

    def explode(self, node):
        big_nums = []
        l_node, l_side = self._get_adjacent_node("left", node)
        r_node, r_side = self._get_adjacent_node("right", node)

        if l_node:
            v = getattr(l_node, l_side)
            setattr(l_node, l_side, v + node.left)
            if v + node.left > 9:
                big_nums.append(l_node)
            if l_side == "left" and not r_node:
                l_node.right = 0  # the sum total of the parent node
                # node.parent = None  # remove the original linkage
        node.left = 0

        if r_node:
            # print("RNODE:", r_node)
            v = getattr(r_node, r_side)
            setattr(r_node, r_side, v + node.right)
            if v + node.right > 9:
                big_nums.append(r_node)
            if r_side == "right" and not l_node:
                # print("why?", r_side)
                r_node.left = 0  # the sum total of the parent node
                # node.parent = None  # remove the original linkage
        node.right = 0

        if node.left == node.right == 0:
            # print("node parent left:", node.parent.left, node.parent.left == node)
            # print("node parent right:", node.parent.right, node.parent.right == node)

            if node.parent.left == node and isinstance(node.parent.left, Node):
                node.parent.left = 0

            if node.parent.right == node and isinstance(node.parent.right, Node):
                node.parent.right = 0

        return big_nums

    def traverse(self, node: "Node") -> Iterator["Node"]:
        if isinstance(node, Node):
            yield from self.traverse(node.left)
            yield node
            yield from self.traverse(node.right)
        else:
            yield node

    @staticmethod
    def _get_adjacent_node(attr, node):
        other_attr = "left" if attr == "right" else "right"
        p = node
        visited = set()
        while p:
            visited.add(p)
            # print(">>>", p, p.left, '<-', p.parent, '->', p.right)
            # if p.parent is None -- but the adjacent is a Node and not an int, we must climb
            # the opposite tree looking for the top most stem that contains an int.
            if p.parent is None:
                # we know that the answer is not an int

                # is it a Node?
                r = getattr(p, attr)
                if isinstance(r, Node):
                    # if this is the root of the node we are investigating -- then it's not helpful.
                    # but if its adjacent -- we are interested.
                    if r in visited:
                        # print("skipping as it looks like we're just climbing where we came from.")
                        return None, None

                    p = r
                    while True:
                        r = getattr(p, other_attr)
                        if isinstance(r, Node):
                            p = r
                            continue
                        # print(p, other_attr)
                        return p, other_attr
                return None

            r = getattr(p.parent, attr)

            if isinstance(r, Node):
                if r not in visited:
                    test = Node.search_up(r, other_attr)
                    return test, other_attr

            if isinstance(r, int):
                # print("R:", r, getattr(p.parent, other_attr))
                return p.parent, attr
            p = p.parent

        return None, None

    @staticmethod
    def search_up(node, attr):
        old_node = node
        new_node = node
        while hasattr(old_node, attr):
            new_node = old_node
            old_node = getattr(new_node, attr)

        return new_node

    def __str__(self):
        return f"[{self.left},{self.right}]"

    def __repr__(self):
        return f"Node"


def explode_created(root_node, created):
    nodes = root_node.find_explosive_nodes()

    for c in created:
        for n in nodes:

            if c.replace(" ", "") == str(n):
                root_node.explode(n)
                return root_node
    return None


def reduce(root_node, yield_steps=False):
    # __ explode nodes
    nodes = root_node.find_explosive_nodes()
    for n in nodes:
        big_nums = root_node.explode(n)
        if yield_steps:
            yield root_node

    # __ split nodes
    root_node, created = root_node.split_big_numbers()

    items = []
    items.extend(created)
    while created:
        if yield_steps:
            yield root_node

        # if this created a node that should be exploded do it now.
        result = explode_created(root_node, created)
        if result is not None:
            root_node = result
            if yield_steps:
                yield root_node

        root_node, created = root_node.split_big_numbers()
        items.extend(created)

    return root_node


def part01():
    lines = helpers.get_lines(r"./data/day_18.txt")
    school = collections.deque([])
    for line in lines:
        n = Node(depth=0).load(eval(line))
        school.append(n)

    # primer
    final = Node.add(school.popleft(), school.popleft())
    while school:
        ii = reduce(final, yield_steps=True)
        t = None
        for i in ii:
            t = i
        final = Node.add(t, school.popleft())
    r = None
    ii = reduce(final, yield_steps=True)
    for i in ii:
        r = i

    return r.magnitude()


def part02():
    school = helpers.get_lines(r"./data/day_18.txt")

    nums = []
    for fish1 in school:
        for fish2 in school:
            t1 = Node(depth=0).load(eval(fish1))
            t2 = Node(depth=0).load(eval(fish2))
            if str(t1) == str(t2):
                continue

            final = Node.add(t1, t2)
            r = None
            ii = reduce(final, yield_steps=True)
            for i in ii:
                r = i

            if r is not None:
                nums.append(r.magnitude())

    return max(nums)


def run():
    assert part01() == 3551
    assert part02() == 4555


if __name__ == "__main__":
    run()
