import helpers


def check_line(line):

    chunks = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }

    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    stack = []
    for c in list(line):
        if c in '[({<':
            stack.append(c)
        else:
            if chunks[stack[-1]] == c:
                stack.pop()
            else:
                return points[c]  # corrupted

    return stack


def part01(lines):
    total = []
    for line in lines:
        total.append(check_line(line))
    return sum(t for t in total if isinstance(t, int))


def part02(lines):
    points2 = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4,
    }

    items = []
    for line in lines:
        s = check_line(line)
        if not isinstance(s, int):
            items.append(list(reversed(s)))

    scores = []
    for item in items:
        score = 0
        for i in item:
            score *= 5
            score += points2[i]
        scores.append(score)

    return sorted(scores)[len(scores) // 2]


def run():
    lines = helpers.get_lines(r'./data/day_10.txt')
    assert part01(lines) == 271245
    assert part02(lines) == 1685293086


if __name__ == "__main__":
    run()
