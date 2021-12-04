import helpers


def get_gamma_rate(lines):
    final = [0] * len(lines[0])
    for line in lines:
        items = list(line)
        for index, item in enumerate(items):
            final[index] += item == "1"

    g = ["1" if f > len(lines) // 2 else "0" for f in final]
    e = ["0" if f > len(lines) // 2 else "1" for f in final]
    return int("".join(g), 2), int("".join(e), 2)


def part01(lines) -> int:
    gamma_rate, epsilon_rate = get_gamma_rate(lines)
    return gamma_rate * epsilon_rate


def get_generator_rating(lines, index):
    nums = [line[index] == "1" for line in lines]
    if sum(nums) < len(lines) // 2:
        return [line for line in lines if line[index] == "0"]
    else:
        return [line for line in lines if line[index] == "1"]


def get_scrubbing_rating(lines, index):
    nums = [line[index] == "0" for line in lines]
    if sum(nums) > len(lines) // 2:
        return [line for line in lines if line[index] == "1"]
    else:
        return [line for line in lines if line[index] == "0"]


def part02(lines) -> int:
    x = _reduce_func(get_generator_rating, lines[:])
    y = _reduce_func(get_scrubbing_rating, lines[:])
    return x * y


def _reduce_func(func, lines):
    for index in range(len(lines[0])):
        lines = func(lines, index)
        if len(lines) == 1:
            return int(lines[0], 2)

    raise RuntimeError


def run():
    lines = helpers.get_lines(r"./data/day_03.txt")
    assert part01(lines) == 3633500
    assert part02(lines) == 4550283


if __name__ == "__main__":
    run()
