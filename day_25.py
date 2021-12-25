# sea cucumbers
import helpers
from collections import defaultdict
from typing import DefaultDict, Tuple


def parse(path: str) -> Tuple[DefaultDict[Tuple[int, int], int], int, int]:
    board: DefaultDict[Tuple[int, int], int] = defaultdict(int)

    lines = helpers.get_lines(path)
    height = len(lines)
    width = len(lines[0])

    for i in range(height):
        for j in range(width):
            icon = lines[i][j]
            if icon == '.':
                board[i, j] = 0
            elif icon == '>':
                board[i, j] = 1
            else:
                board[i, j] = 2

    return board, width, height


def step(board: DefaultDict[Tuple[int, int], int], height, width) -> Tuple[int, DefaultDict[Tuple[int, int], int]]:
    moves = 0
    to_update = dict()
    # _ East first
    for k, v in board.items():
        if v == 1:
            y, x = k[0] % height, (k[1] + 1) % width
            if board[y, x] == 0:
                moves += 1
                to_update[y, x] = v
                to_update[k] = 0

    for k, v in to_update.items():
        board[k] = v

    # _ South second
    for k, v in board.items():
        if v == 2:
            y, x = (k[0] + 1) % height, k[1] % width
            if board[y, x] == 0:
                moves += 1
                to_update[y, x] = v
                to_update[k] = 0

    for k, v in to_update.items():
        board[k] = v

    return moves, board


def pprint(index, board, height: int, width: int):
    icons = {
        0: '.',
        1: '>',
        2: 'V',
    }

    for i in range(height):
        for j in range(width):
            if (i, j) in board:
                v = board[i, j]
                print(icons[v], end='')
            else:
                print('.', end='')
        print()

    print(f'{"-" * 10} [Finished {index}] {"-" * 10}')


def part01():
    board, width, height = parse(r'./data/day_25.txt')
    for index in range(1, 10_000):
        # pprint(index, board, height, width)
        moves, board = step(board, height, width)
        if moves == 0:
            return index
    return -1


def run():
    assert part01() == 351


if __name__ == "__main__":
    run()

