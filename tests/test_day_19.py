import math
from itertools import combinations

import helpers
from day_19 import parse, Scanner


t1 = """
--- scanner 0 ---
0,2
4,1
3,3

--- scanner 1 ---
-1,-1
-5,0
-2,1
"""

t2 = """
--- scanner 0 ---
-1,-1,1
-2,-2,2
-3,-3,3
-2,-3,1
5,6,-4
8,0,7

--- scanner 0 ---
1,-1,1
2,-2,2
3,-3,3
2,-1,3
-5,4,-6
-8,-7,0

--- scanner 0 ---
-1,-1,-1
-2,-2,-2
-3,-3,-3
-1,-3,-2
4,6,5
-7,0,8

--- scanner 0 ---
1,1,-1
2,2,-2
3,3,-3
1,3,-2
-4,-6,5
7,0,8

--- scanner 0 ---
1,1,1
2,2,2
3,3,3
3,1,2
-6,-4,-5
0,7,-8
"""


def distance(p1, p2):
    a = (p2[0] - p1[0]) ** 2
    b = (p2[1] - p1[1]) ** 2
    c = (p2[2] - p1[2]) ** 2
    return math.sqrt(a + b + c)


def area(a, b, c):
    s = (a + b + c) / 2
    na = s - a
    nb = s - b
    nc = s - c

    r = math.sqrt(s * na * nb * nc)
    if r == 0:
        # not a triangle
        r = float("Nan")
    return r


def get_areas_from_scanner(s: Scanner):
    areas = []
    areas_alts = []
    points = [(x, y, z) for x, y, z in zip(s.x, s.y, s.z)]
    for p1, p2, p3 in combinations(points, 3):
        aa = round(area(distance(p1, p2), distance(p2, p3), distance(p3, p1),), 5)
        areas.append(aa)

        p1 = p1[1:]
        p2 = p2[1:]
        p3 = p3[1:]
        aa = round(area(distance(p1, p2), distance(p2, p3), distance(p3, p1), ), 5)
        areas_alts.append(aa)

    return areas, areas_alts


def test_match_triangle_area():
    scanners = parse([s for s in t1.split("\n")])
    s1: Scanner = scanners[0]
    s2: Scanner = scanners[1]
    a1, a1_alt = get_areas_from_scanner(s1)
    a2, a2_alt = get_areas_from_scanner(s2)
    for a, b in zip(a1, a2):
        assert math.isclose(a, b) is True


def get_all_areas():
    # scanners = parse([s for s in t2.split("\n")])
    scanners = parse(helpers.get_lines(r'../data/day_19_test.txt'))
    temp = None
    for s in scanners:
        print(s)
        areas, areas_alts = get_areas_from_scanner(s)

        if temp is None:
            temp = areas_alts
        else:
            for option in areas, areas_alts:
                z = [o for o in option if o in temp]
                if len(z) >= 12:
                    print(f'\tMatched: {len(z)}')


test_match_triangle_area()
get_all_areas()
