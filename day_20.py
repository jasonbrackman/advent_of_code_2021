from typing import List, Tuple

import helpers


def parse(path):
    lines = helpers.get_lines(path)
    algo = lines[0]
    r = [list(line.strip()) for line in lines[1:] if line]
    return algo, r


def get_window(pos: Tuple[int, int], input_: List[List[str]], pixel: str):

    items = []
    row, col = pos
    for r in (-1, 0, 1):
        for c in (-1, 0, 1):
            new_row = row + r
            new_col = col + c
            if 0 <= new_row < len(input_[0]) and 0 <= new_col < len(input_):
                items.append(input_[new_row][new_col])
            else:
                items.append(pixel)

    return int("".join(items).replace("#", "1").replace(".", "0"), 2)


def part01(input_: List[List[str]], algo, runs: int, debug: bool = False):
    # account for the infinity of the grid flip
    step0 = algo[0]
    step1 = step0 if step0 == "." else algo[-1]

    for index in range(1, runs + 1):
        pixel = step0 if index % 2 == 0 else step1
        input_ = add_padding(input_, pixel)

        # Going to be the output
        new_input = []

        assert len(input_) == len(input_[0])
        input_length = len(input_)

        for i in range(input_length):
            row = []
            for j in range(input_length):
                r = get_window((i, j), input_, pixel)
                row.append(algo[r])
            new_input.append(row)

        input_ = new_input
        if debug:
            for i_ in input_:
                print("".join(i_))
            print()
    return sum(i_.count("#") for i_ in input_)


def add_padding(input_, pixel):
    # add padding
    buff = [pixel] * len(input_[0])
    input_ = [buff] + input_ + [buff]
    for index in range(len(input_)):
        input_[index] = [pixel] + input_[index] + [pixel]

    return input_


def run():
    path = r"./data/day_20.txt"
    algo, input_image = parse(path)
    assert part01(input_image, algo, 2, debug=False) == 5419
    assert part01(input_image, algo, 50, debug=False) == 17325


if __name__ == "__main__":
    run()
