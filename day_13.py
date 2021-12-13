import copy

import helpers


def parse(lines):
    dots = []
    folds = []
    x = -1
    y = -1
    for line in lines:
        if ',' in line:
            dot = [int(i) for i in line.split(',')]

            if dot[0] > x:
                x = dot[0]
            if dot[1] > y:
                y = dot[1]

            dots.append(dot)

        elif '=' in line:
            letter, num = line.split()[-1].split('=')
            folds.append([letter, int(num)])

    return x, y, dots, folds


def run():
    lines = helpers.get_lines(r'./data/day_13.txt')
    x, y, dots, folds = parse(lines)
    table = create_table(dots, x, y)

    assert part01([folds[0]], copy.deepcopy(table)) == 647

    result = part02(folds, copy.deepcopy(table))
    expected = [
        '#..#.####...##.#..#...##.###...##....##.',
        '#..#.#.......#.#..#....#.#..#.#..#....#.',
        '####.###.....#.####....#.#..#.#.......#.',
        '#..#.#.......#.#..#....#.###..#.......#.',
        '#..#.#....#..#.#..#.#..#.#.#..#..#.#..#.',
        '#..#.####..##..#..#..##..#..#..##...##..',
    ]
    for r, e in zip(result, expected):
        assert ''.join(r) == e


def part01(folds, table):
    result = fold_paper(folds, table)
    return sum(item.count('#') for item in result)


def part02(folds, table):
    return fold_paper(folds, table)


def fold_paper(folds, table):
    for pos, fold in folds:
        if pos == 'y':
            y = fold
            one, two = table[:y], list(reversed(table[y:]))
            for i in range(y):
                for j in range(len(one[0])):
                    if two[i][j] == '#':
                        one[i][j] = '#'
            table = one

        if pos == 'x':
            x = fold
            one, two = [t[:x] for t in table], [list(reversed(t[x + 1:])) for t in table]
            for i in range(len(one)):
                for j in range(x):
                    if two[i][j] == '#':
                        one[i][j] = '#'

            table = one

    return table


def create_table(dots, x, y):
    table = []
    for i in range(y + 1):
        row = []
        for j in range(x + 1):
            icon = '#' if [j, i] in dots else '.'
            row.append(icon)
        table.append(row)
    return table


if __name__ == "__main__":
    run()
