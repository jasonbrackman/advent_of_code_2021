import copy

import helpers
from collections import defaultdict


class Node:
    def __init__(self):
        self.last = 'start'
        self.parts = ['start']
        self.dead_end = False

    def add_part(self, part):
        self.last = part
        if part.islower():
            if part in self.parts:
                # dead end
                self.dead_end = True
            else:
                self.parts.append(part)
        else:
            self.parts.append(part)

    def copy(self):
        new = Node()
        new.last = self.last
        new.parts = copy.copy(self.parts)
        new.dead_end = self.dead_end

        return new

    def __str__(self):
        return '->'.join(p for p in self.parts)

    def __repr__(self):
        return f"Node({self.last=}, {self.parts=})"


class NodePart01(Node):
    def __init__(self):
        super().__init__()


class NodePart02(Node):
    def __init__(self):
        super().__init__()

        self.small_caves = {'start', }
        self.other_caves = defaultdict(int)  # can visit up to two times
        self.used_time = False

    def add_part(self, part):
        self.last = part

        if part.islower():

            if part in self.small_caves:
                self.dead_end = True
            else:
                if self.used_time is False:
                    self.other_caves[part] += 1
                    if self.other_caves[part] >= 2:
                        self.used_time = True
                        for v in self.other_caves.keys():
                            self.small_caves.add(v)
                else:
                    self.small_caves.add(part)
                self.parts.append(part)
        else:
            self.parts.append(part)

    def copy(self):
        new = NodePart02()

        new.last = self.last
        new.dead_end = self.dead_end
        new.parts = list(self.parts)
        new.small_caves = set(self.small_caves)
        new.other_caves = copy.copy(self.other_caves)
        new.used_time = self.used_time

        return new

def children(rules, n: Node):
    new_nodes = []
    for rule in rules[n.last]:
        old_node = n.copy()
        old_node.add_part(rule)
        if old_node.dead_end is False:
            new_nodes.append(old_node)
    return new_nodes


def bfs(rules, node_type):
    count = 0
    n = node_type()
    q = [n]
    while q:
        node = q.pop()
        for item in children(rules, node):
            if item.last == 'end':
                count += 1
            elif item.dead_end is False:
                q.append(item)
    return count


def run():
    lines = helpers.get_lines(r'./data/day_12.txt')

    rules = defaultdict(list)

    for line in lines:
        k, v = line.split('-')
        rules[k].append(v)
        rules[v].append(k)

    assert bfs(rules, node_type=NodePart01) == 3298
    assert bfs(rules, node_type=NodePart02) == 93572


if __name__ == "__main__":
    run()
