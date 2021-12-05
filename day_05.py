import collections
from dataclasses import dataclass
from typing import Dict, List, Tuple

import helpers


@dataclass(frozen=True)
class Point:
    x: int
    y: int


def plot_points(points, p1, p2, verticals=False):

    if p1.x == p2.x:
        y_range = (p1.y, p2.y + 1) if p1.y < p2.y else (p2.y, p1.y + 1)
        for y in range(*y_range):
            points[(y, p1.x)] += 1

    elif p1.y == p2.y:
        x_range = (p1.x, p2.x + 1) if p1.x < p2.x else (p2.x, p1.x + 1)
        for x in range(*x_range):
            points[(p1.y, x)] += 1

    else:
        if verticals:
            y_count = 1 if p1.y < p2.y else -1
            y_range = range(p1.y, p2.y + y_count, y_count)

            x_count = 1 if p1.x < p2.x else -1
            x_range = range(p1.x, p2.x + x_count, x_count)

            for x, y in zip(x_range, y_range):
                points[(y, x)] += 1


def process_data(lines: List[str]) -> List[Tuple[Point, Point]]:
    data = []
    for line in lines:
        p1, _, p2 = line.split()
        x1, y1 = [int(i) for i in p1.split(",")]
        x2, y2 = [int(i) for i in p2.split(",")]
        data.append((Point(x=x1, y=y1), Point(x=x2, y=y2)))

    return data


def process_lines(data: List[Tuple[Point, Point]], verticals=False) -> Dict[str, int]:
    points = collections.defaultdict(int)
    for (p1, p2) in data:
        plot_points(points, p1, p2, verticals=verticals)
    return points


def process_result(data: List[Tuple[Point, Point]], verticals=False) -> int:
    points = process_lines(data, verticals=verticals)
    return sum(v > 1 for k, v in points.items())


def run():
    path = r"./data/day_05.txt"
    lines = helpers.get_lines(path)
    data = process_data(lines)
    assert process_result(data, verticals=False) == 5576
    assert process_result(data, verticals=True) == 18144


if __name__ == "__main__":
    run()
