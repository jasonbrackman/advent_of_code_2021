from typing import Dict, List, Tuple

import helpers

MARK = '*'

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

            dots.append((dot[1], dot[0]))  # y, x instead of x, y)

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
    total = sum(v == MARK for (i, j), v in table_part01.items() if i <= y and j <= x)
    assert total == 647

    # Part02
    table_part02 = create_dict(dots)
    x, y = fold_paper(folds, table_part02, x, y)

    expected = [  # HEJHJRCJ
        '*  * ****   ** *  *   ** ***   **    **',
        '*  * *       * *  *    * *  * *  *    *',
        '**** ***     * ****    * *  * *       *',
        '*  * *       * *  *    * ***  *       *',
        '*  * *    *  * *  * *  * * *  *  * *  *',
        '*  * ****  **  *  *  **  *  *  **   ** ',
    ]

    results = []
    for i in range(y - 1):
        r = ""
        for j in range(x - 2):
            r += table_part02.get((i, j), " ")
        results.append(r)

    for r, e in zip(results, expected):
        assert "".join(r) == e


def fold_paper(folds: List, table: Dict, x: int, y: int) -> Tuple[int, int]:

    for pos, fold in folds:
        if pos == 'y':
            y = fold
            y_add = y + y
            for i in range(y):
                for j in range(x):
                    ii = y_add - i
                    if (ii, j) in table:
                        table[(i, j)] = MARK

        elif pos == 'x':
            x = fold
            x_add = x + x
            for i in range(y):
                for j in range(x):
                    jj = x_add - j
                    if (i, jj) in table:
                        table[(i, j)] = MARK


    # for convenience, we add +1 to the x, y values for range()
    return x + 1, y + 1


def create_dict(dots):
    return {dot: MARK for dot in dots}


if __name__ == "__main__":
    run()
