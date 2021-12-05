import collections
from typing import List

import helpers


def plot_points(points, x1, y1, x2, y2, verticals=False):

    if x1 == x2:
        y_range = (y1, y2 + 1) if y1 < y2 else (y2, y1 + 1)
        for y in range(*y_range):
            points[(y, x1)] += 1

    elif y1 == y2:
        x_range = (x1, x2 + 1) if x1 < x2 else (x2, x1 + 1)
        for x in range(*x_range):
            points[(y1, x)] += 1

    else:
        if verticals:
            y_count = 1 if y1 < y2 else -1
            y_range = range(y1, y2 + y_count, y_count)

            x_count = 1 if x1 < x2 else -1
            x_range = range(x1, x2 + x_count, x_count)

            for x, y in zip(x_range, y_range):
                points[(y, x)] += 1


def process(lines: List[str], verticals=False) -> int:
    points = collections.defaultdict(int)
    for line in lines:
        p1, _, p2 = line.split()
        x1, y1 = [int(i) for i in p1.split(",")]
        x2, y2 = [int(i) for i in p2.split(",")]
        plot_points(points, x1, y1, x2, y2, verticals=verticals)

    return sum(v > 1 for k, v in points.items())


def run():
    path = r"./data/day_05.txt"
    lines = helpers.get_lines(path)
    assert process(lines, verticals=False) == 5576
    assert process(lines, verticals=True) == 18144


if __name__ == "__main__":
    run()
