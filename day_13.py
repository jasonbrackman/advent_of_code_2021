from typing import Dict, List, Tuple

import helpers


def parse(lines):
    dots = []
    folds = []
    x = -1
    y = -1
    for line in lines:
        if "," in line:
            dot = [int(i) for i in line.split(",")]

            if dot[0] > x:
                x = dot[0]
            if dot[1] > y:
                y = dot[1]

            dots.append(dot)

        elif "=" in line:
            letter, num = line.split()[-1].split("=")
            folds.append([letter, int(num)])

    return x, y, dots, folds


def run():
    lines = helpers.get_lines(r"./data/day_13.txt")
    x, y, dots, folds = parse(lines)

    # Part01
    table_part01 = create_dict(dots)
    x, y = fold_paper([folds[0]], table_part01, x, y)
    assert (
        sum(v == "#" for (i, j), v in table_part01.items() if i <= y and j <= x) == 647
    )

    # Part02
    table_part02 = create_dict(dots)
    x, y = fold_paper(folds, table_part02, x, y)

    expected = [  # HEJHJRCJ
        "#..#.####...##.#..#...##.###...##....##.",
        "#..#.#.......#.#..#....#.#..#.#..#....#.",
        "####.###.....#.####....#.#..#.#.......#.",
        "#..#.#.......#.#..#....#.###..#.......#.",
        "#..#.#....#..#.#..#.#..#.#.#..#..#.#..#.",
        "#..#.####..##..#..#..##..#..#..##...##..",
    ]

    results = []
    for i in range(y - 1):
        r = ""
        for j in range(x - 1):
            r += table_part02.get((i, j), ".")
        results.append(r)
    for r, e in zip(results, expected):
        assert "".join(r) == e


def fold_paper(folds: List, table: Dict, x: int, y: int) -> Tuple[int, int]:

    for pos, fold in folds:
        y = fold if pos == "y" else y
        x = fold if pos == "x" else x

        for i in range(y):
            for j in range(x):
                ii = y + (y - i) if pos == "y" else i
                jj = x + (x - j) if pos == "x" else j
                if table.get((ii, jj), ".") == "#":
                    table[(i, j)] = "#"

    # for convenience, we add +1 to the x, y values for range()
    return x + 1, y + 1


def create_dict(dots):
    table = dict()
    for (x, y) in dots:
        table[(y, x)] = "#"
    return table


if __name__ == "__main__":
    run()
