from typing import Tuple

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

    def __str__(self):
        return f"Probe({self._x_pos=}, {self._y_pos=}"

    def load(self, area: str):
        self.clear()
        items = area.split()
        self._x_area = [int(i) for i in items[2][2:-1].split("..")]
        self._y_area = [int(i) for i in items[3][2:].split("..")]

    def update_velocity(self, x, y):
        self.clear()
        self._x_vel = x
        self._y_vel = y

    def clear(self):
        self._x_pos = 0
        self._y_pos = 0
        self.y_steps.clear()

    def step(self):
        # Add velocity to position
        self._x_pos += self._x_vel
        self._y_pos += self._y_vel

        # record the y position
        self.y_steps.add(self._y_pos)

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

    def check(self):
        return (
            self._x_area[0] <= self._x_pos <= self._x_area[1]
            and self._y_area[0] <= self._y_pos <= self._y_area[1]
        )


def run():
    lines = helpers.get_lines(r"./data/day_17.txt")
    probe = Probe()
    probe.load(lines[0])
    results = []

    # tweaked the ranges to make a guess as to the range that produces 'hits'
    for i in range(-100, 100):
        for j in range(0, 300):
            probe.update_velocity(j, i)

            while True:
                r = probe.step()
                if r == -1:
                    break
                if probe.check() is True:
                    max_y = max(probe.y_steps)
                    results.append(max_y)
                    break

    assert max(results) == 4005
    assert len(results) == 2953


if __name__ == "__main__":
    run()
