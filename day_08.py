from typing import List, Set, Dict, Tuple

import helpers


def decode(digits: Set[str], p2=False) -> Dict[str, int]:
    r = dict()

    visited = set()
    for digit in digits:
        if len(digit) == 2:
            r[digit] = 1
        elif len(digit) == 3:
            r[digit] = 7
        elif len(digit) == 7:
            r[digit] = 8
        elif len(digit) == 4:
            r[digit] = 4

    for k in r.keys():
        visited.add(k)

    if p2:
        inv_r = {v: k for k, v in r.items()}
        for digit in digits:
            if digit not in visited:
                if len(digit) == 5:
                    if all(i in digit for i in inv_r[1]):
                        r[digit] = 3
                        inv_r[3] = digit
                        visited.add(digit)
                    elif sum([(i in digit) for i in inv_r[4]]) == 3:
                        r[digit] = 5
                        visited.add(digit)
                    else:
                        r[digit] = 2
                        visited.add(digit)

        for digit in digits:
            if digit not in visited:
                if len(digit) == 6:
                    if any(i not in digit for i in inv_r[1]):
                        r[digit] = 6
                        visited.add(digit)

                    elif all(i in digit for i in inv_r[3]):
                        r[digit] = 9
                        visited.add(digit)

                    else:
                        r[digit] = 0
                        visited.add(digit)

    return r


def part01(data: Tuple[Set[str], List[str]]) -> int:
    count = 0
    for digits, outputs in data:
        r = decode(digits, p2=False)
        for o in outputs:
            if r.get(o, None) is not None:
                count += 1
    return count


def part02(data: Tuple[Set[str], List[str]]) -> int:
    total = 0
    for digits, outputs in data:
        r = decode(digits, p2=True)
        num = ""
        for o in outputs:
            num += str(r.get(o, None))

        total += int(num)
    return total


def run():
    lines = helpers.get_lines(r"./data/day_08.txt")
    data = []
    for line in lines:
        digits, outputs = line.split("|")
        d_ints = {"".join(sorted(d)) for d in digits.split()}
        o_ints = ["".join(sorted(o)) for o in outputs.split()]  # order matters

        data.append((d_ints, o_ints))

    assert part01(data) == 456
    assert part02(data) == 1091609


if __name__ == "__main__":
    run()
