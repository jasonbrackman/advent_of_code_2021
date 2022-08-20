import helpers

lines = helpers.get_lines(r'./data/day_09.txt')
items = [[int(i) for i in line] for line in lines]


def neighbours(i, j):
    all_ = []

    for ii in (i-1, i+1):
        if 0 <= ii <= len(items)-1:
            all_.append(items[ii][j])

    for jj in (j-1, j+1):
        if 0 <= jj <= len(items[0])-1:
            all_.append(items[i][jj])

    assert len(all_) > 1

    return all_


def basins(i, j):
    # return early if we are at an edge already
    if items[i][j] == 9:
        return []

    # add the initial starting part as part of the valid basin pieces
    valid = {(i, j)}

    # Queue it up for a neighbour search
    q = [(i, j)]

    # We only want to visit any place once.
    visited = set()

    while q:
        i, j = q.pop()

        visited.add((i, j))

        # collect up down neighbours
        for ii in (i - 1, i + 1):
            if 0 <= ii <= len(items) - 1:
                if (ii, j) not in visited:
                    if items[ii][j] != 9:
                        valid.add((ii, j))
                        q.append((ii, j))

        # collect left right neighbours
        for jj in (j - 1, j + 1):
            if 0 <= jj <= len(items[0]) - 1:
                if (i, jj) not in visited:
                    if items[i][jj] != 9:
                        valid.add((i, jj))
                        q.append((i, jj))

    # return valid neighbours
    return valid


def part01():
    results = []
    for i in range(len(items)):
        for j in range(len(items[0])):
            n = neighbours(i, j)
            if items[i][j] < min(n):
                results.append(items[i][j])

    return sum(i + 1 for i in results)


def part02():
    visited = set()
    basins_ = []
    for i in range(len(items)):
        for j in range(len(items[0])):
            if (i, j) not in visited:
                visited.add((i, j))
                n = basins(i, j)

                basins_.append(n)
                visited |= set(n)

    collection = 1
    for i, b in enumerate(reversed(sorted(basins_, key=len))):
        if i == 3:
            return collection
        else:
            collection *= len(b)

    raise RuntimeError("Something went wrong.")


def run():
    assert part01() == 504
    assert part02() == 1558722


if __name__ == "__main__":
    run()
