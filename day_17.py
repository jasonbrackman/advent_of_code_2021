from typing import Optional

import helpers


class Probe:
    def __init__(self) -> None:
        # _ position
        self._x_pos = 0
        self._y_pos = 0

        # _ velocity
        self._x_vel = 0
        self._y_vel = 0

        # _ area to check for target
        self._x_area = []
        self._y_area = []

        # _ record steps
        self.y_steps = set()
        self.history = []

    def min_y(self):
        return min(self._y_area[0], 0)

    def max_y(self):
        return max(0 if not self.y_steps else max(self.y_steps), 0)

    def max_x(self):
        return self._x_area[1]

    def pprint(self, max_y):
        min_y = self.min_y()
        max_y = max(0, max_y)

        for y in range(max_y, min_y - 2, -1):
            in_y_range = self._y_area[0] <= y <= self._y_area[1]
            print(f'{y:03}', end='')
            for x in range(self._x_area[1] + 1):
                if y == x == 0:
                    print('S', end='')
                elif (x, y) in self.history:
                    print('*', end='')
                elif self._x_area[0] <= x <= self._x_area[1] and in_y_range:
                    print('T', end='')
                else:
                    print(' ', end='')
            print()

        var = len(str(self._x_area[1])) % 10
        for x in range(var):
            print(f'   ', end='')
            for index in range(self._x_area[1]+1):
                print(str(index).zfill(var)[x], end='')
            print()

    def __str__(self) -> str:
        return f"Probe({self._x_pos=}, {self._y_pos=}"

    def load(self, area: str) -> None:
        self.clear()
        items = area.split()
        self._x_area = [int(i) for i in items[2][2:-1].split("..")]
        self._y_area = [int(i) for i in items[3][2:].split("..")]

    def update_velocity(self, x: int, y: int) -> None:
        self.clear()
        self._x_vel = x
        self._y_vel = y

    def clear(self) -> None:
        self._x_pos = 0
        self._y_pos = 0
        self.y_steps.clear()
        self.history.clear()

    def step(self) -> Optional[int]:
        # Add velocity to position
        self._x_pos += self._x_vel
        self._y_pos += self._y_vel

        # record the y position
        self.y_steps.add(self._y_pos)
        self.history.append((self._x_pos, self._y_pos))

        # _ Update velocity

        # X wants to get to zero
        if self._x_vel > 0:
            self._x_vel -= 1
        elif self._x_vel < 0:
            self._x_vel += 1

        # Y gets dragged down by gravity
        self._y_vel -= 1

        # if the missile has gone too far to the right or too far down -- let's just exit early.
        if self._x_pos > self._x_area[1] or self._y_pos < self._y_area[0]:
            return -1

    def check(self) -> bool:
        return (
            self._x_area[0] <= self._x_pos <= self._x_area[1]
            and self._y_area[0] <= self._y_pos <= self._y_area[1]
        )


def run():
    lines = helpers.get_lines(r"./data/day_17.txt")
    probe = Probe()
    probe.load(lines[0])
    results = []

    # Chose a number that seemed to ensure all 'hits' possible are captured.
    for y in range(probe.min_y(), 100):
        for x in range(0, probe.max_x() + 1):

            probe.update_velocity(x, y)

            while True:
                if probe.step() == -1:
                    break
                if probe.check() is True:
                    max_y = max(probe.y_steps)
                    results.append(max_y)
                    # probe.pprint(max_y)
                    break

    # print(max(results), len(results))
    assert max(results) == 4005
    assert len(results) == 2953


if __name__ == "__main__":
    run()
