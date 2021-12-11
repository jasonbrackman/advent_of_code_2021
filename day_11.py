import helpers

def flash(grid, i, j):
    new = set()
    for ii in (i - 1, i, i + 1):
        if 0 <= ii < len(grid):
            for jj in (j - 1, j, j + 1):
                if 0 <= jj < len(grid[0]):
                    if grid[ii][jj] != 0:
                        grid[ii][jj] += 1
                        if grid[ii][jj] > 9:
                            grid[ii][jj] = 0
                            new.add((ii,jj))
    return new

# Rules
def step(grid, rounds):
    count = 0
    for step in range(rounds):
        flashed = set()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                # increase every cell by 1
                grid[i][j] += 1

                # if over 9 set to zero and mark as a flash
                if grid[i][j] > 9:
                    grid[i][j] = 0
                    flashed.add((i, j))

        # loop over all the flashed items for the step.
        while flashed:
            (i, j) = flashed.pop()
            flashed |= flash(grid, i, j)
            grid[i][j] = 0

            count += 1

        # Retun if all the cells flashed on this step
        if sum([sum(g) for g in grid]) == 0:
            return step+1

    # return the number of cells that have flashed over all steps
    return count


def run():
    lines = helpers.get_lines(r'./data/day_11.txt')

    grid = [[int(i) for i in line] for line in lines]
    assert step(grid, 100) == 1613

    grid = [[int(i) for i in line] for line in lines]
    assert step(grid, 1_000) == 510


if __name__ == "__main__":
    run()