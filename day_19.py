from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import helpers


def parse(lines: List[str]) -> List:
    scanner: Optional[Scanner] = None
    scanners = []
    for line in lines:
        if len(line) == 0:
            pass  # skip
        elif line.startswith("---"):
            if scanner is not None:
                scanner.rots()
                scanner.fingerprint()
                scanners.append(scanner)
            id_ = line.split()[2]
            scanner = Scanner(id_)
        else:
            if scanner is None:
                raise ValueError("Expected a scanner, but None found.")
            xyz = [int(i) for i in line.split(",")]
            scanner.add_point(xyz)

    if scanner is not None:
        scanner.rots()
        scanner.fingerprint()
        scanners.append(scanner)

    return scanners


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def manhattan_distance(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        # print(self, other, '>>')
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class Scanner:
    def __init__(self, name: str):
        self.name = name
        self.origin: Optional[Point] = None
        self.relative_key = 0
        self.points: List[Point] = []
        self.fingerprints: Dict[int, List[int]] = dict()
        self.rotations: Dict[int, List[Point]] = dict()

    def add_point(self, xyz: List[int]) -> None:
        x, y, z = 0, 0, 0
        if len(xyz) == 2:
            x, y = xyz
        if len(xyz) == 3:
            x, y, z = xyz

        self.points.append(Point(x, y, z))

    def rots(self) -> None:

        rotates = {
            0: lambda p: Point(p.x, p.y, p.z),
            1: lambda p: Point(p.x, p.y * -1, p.z * -1),
            2: lambda p: Point(p.x * -1, p.y, p.z * -1),
            3: lambda p: Point(p.x * -1, p.y * -1, p.z),
            4: lambda p: Point(p.x, p.z, p.y * -1),
            5: lambda p: Point(p.x, p.z * -1, p.y),
            6: lambda p: Point(p.x * -1, p.z, p.y),
            7: lambda p: Point(p.x * -1, p.z * -1, p.y),
            8: lambda p: Point(p.y, p.z, p.x),
            9: lambda p: Point(p.y, p.z * -1, p.x * -1),
            10: lambda p: Point(p.y * -1, p.z, p.x * -1),
            11: lambda p: Point(p.y * -1, p.z * -1, p.x * -1),
            12: lambda p: Point(p.y, p.x, p.z * -1),
            13: lambda p: Point(p.y, p.x * -1, p.z),
            14: lambda p: Point(p.y * -1, p.x, p.z),
            15: lambda p: Point(p.y * -1, p.x * -1, p.z * -1),
            16: lambda p: Point(p.z, p.x, p.y),
            17: lambda p: Point(p.z, p.x * -1, p.y * -1),
            18: lambda p: Point(p.z * -1, p.x, p.y * -1),
            19: lambda p: Point(p.z * -1, p.x * -1, p.y),
            20: lambda p: Point(p.z, p.y, p.x * -1),
            21: lambda p: Point(p.z, p.y * -1, p.x),
            22: lambda p: Point(p.z * -1, p.y, p.x),
            23: lambda p: Point(p.z * -1, p.y * -1, p.x * -1),
        }

        self.rotations = {
            k: [v(point) for point in self.points] for k, v in rotates.items()
        }

    def fingerprint(self):
        self.fingerprints.clear()
        for index, p1 in enumerate(self.points):
            self.fingerprints[index] = [p1.manhattan_distance(p2) for p2 in self.points]

    def __str__(self):
        return f"Scanner [{self.name}] - with {len(self.points)} beacons"


def compare_scanners(s1: Scanner, s2: Scanner) -> List[Tuple[Point, Point]]:

    for key01, fingerprint01 in s1.fingerprints.items():
        for key02, fingerprint02 in s2.fingerprints.items():

            point_pairs = []
            for index, u in enumerate(fingerprint02):
                if u in fingerprint01:
                    point_pairs.append(
                        (s1.points[fingerprint01.index(u)], s2.points[index])
                    )
                    if len(point_pairs) >= 12:
                        return point_pairs

    # Nothing to return
    return []


def count_visited(visited):
    a = len({a for (a, b) in visited})
    b = len({b for (a, b) in visited})
    return a + b


def part2(points):
    ...


def run():
    lines = helpers.get_lines(r"./data/day_19.txt")
    scanners = parse(lines)
    scanners2 = parse(lines)
    scanners[0].origin = Point(0, 0, 0)
    scanners2[0].origin = Point(0, 0, 0)
    p = part1b(scanners)

    # part1
    assert len(p.points) == 392

    # part2
    fix_up(p, scanners2)

    items = []
    for s1 in scanners2:
        for s2 in scanners2:
            if s1 != s2:
                if s1.origin is not None and s2.origin is not None:
                    # print("s1:", s1.origin)
                    # print("s2:", s2.origin)
                    items.append(s1.origin.manhattan_distance(s2.origin))

    # part2
    assert sorted(items)[-1] == 13332


def fix_up(s1, scanners):
    # s1 = scanners[0]
    for s2 in scanners:
        if s1 != s2:
            # update s2
            points = compare_scanners(s1, s2)
            _scanner_offsets(s2, points)


def part1(scanners):
    max_ = -1
    sca_ = None

    changes = True
    while changes:
        changes = False
        for s1 in scanners:
            for s2 in scanners:
                # skip if same scanner or already visited
                if s1 == s2:
                    continue

                points = compare_scanners(s1, s2)
                if not _scanner_offsets(s2, points):
                    continue

                # update s2
                a = s2.rotations[s2.relative_key]
                b = [p - s2.origin for p in s1.points]
                c = list(set(a) | set(b))

                c_len = len(c)
                if c_len == len(s2.points):
                    # nothing to do if the numbers are the same, skip the work
                    continue

                changes = True

                s2.points = c
                s2.rots()
                s2.fingerprint()

                if c_len > max_:
                    max_ = len(c)
                    sca_ = s2

                print("S1:", s1.name, "->", "S2:", s2.name, "Count:", len(s2.points))
                # 458 is too high
                # 443 is too high
                break
    return sca_


def is_a_pair(s1, s2) -> bool:
    points = compare_scanners(s1, s2)
    return _scanner_offsets(s2, points)


def part1b(scanners: List[Scanner]):
    s1 = scanners[0]
    visited = set()

    while scanners:
        s2 = scanners.pop()
        if not is_a_pair(s1, s2):
            visited.add(s2)
            if len(scanners) == 0:
                s1 = update_scanners_with_visited(s1, scanners, visited)

            continue

        # update s2
        a = s2.rotations[s2.relative_key]
        b = [p - s2.origin for p in s1.points]
        c = list(set(a) | set(b))

        s1.points = c
        s1.rots()
        s1.fingerprint()

        # print("S1:", s1.name, "Count:", len(s1.points), "Rotation:", s1.relative_key)
        # 458 is too high
        # 443 is too high

        if len(scanners) == 0:
            s1 = update_scanners_with_visited(s1, scanners, visited)

    return s1


def update_scanners_with_visited(s1, scanners, visited):
    if len(scanners) == 0:
        # put back the visited since we got a bit further
        for v in visited:
            scanners.insert(0, v)
        scanners.insert(0, s1)
        visited.clear()

    return scanners.pop()


def _scanner_offsets(s2, points):
    min_points = 11
    if len(points) >= min_points:
        # Brute force all rotations
        for x in range(24):
            results = []
            for (p1, p2) in points:
                if p2 in s2.points:
                    results.append(p1 - s2.rotations[x][s2.points.index(p2)])

            k, v = Counter(results).most_common(1)[0]
            if v >= min_points:
                s2.origin = k
                s2.relative_key = x
                return True
    return False


def _scanner_overlaps(
    scanners: List[Scanner],
) -> Dict[Scanner, Dict[Scanner, List[Tuple[Point, Point]]]]:
    results: Dict[Scanner, Dict[Scanner, List[Tuple[Point, Point]]]] = dict()
    for s1 in scanners:
        results[s1] = dict()
        for s2 in scanners:
            if s1 != s2:
                results[s1][s2] = compare_scanners(s1, s2)

    return results


if __name__ == "__main__":
    run()
