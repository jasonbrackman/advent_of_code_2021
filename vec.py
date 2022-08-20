from __future__ import annotations

from math import sqrt


class Vec3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self) -> float:
        """Synonymous with length.  Returns EXACT length."""
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def distance(self, other: Vec3) -> float:
        """The length between this Vec3 and another."""
        return Vec3(other.x - self.x, other.y - self.y, other.z - self.z).magnitude()

    def direction(self):
        """
        This is the normalized vector (unit 1 vector).
        - invalid for zero vectors.
        """
        m = self.magnitude()
        return Vec3(self.x / m, self.y / m, self.z / m)

    def __mul__(self, other):
        """also called inner product....
        - If 1, they point in the same direction.
        - If 0, they're orthogonal.
        - If -1, they point in opposite directions.
        """
        n1 = self.direction()
        n2 = other.direction()
        return n1.x * n2.x + n1.y * n2.y + n1.z * n2.z

    @classmethod
    def zero(cls) -> Vec3:
        """Return a Vec3 of 0, 0, 0"""
        return Vec3(0, 0, 0)

    def __str__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"

class Vec2:
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y

    def length(self):
        result = sqrt(self.x ** 2 + self.y ** 2)
        return round(result, 6)

    def distance(self, other):
        return Vec2(other.x - self.x, other.y - self.y).length()


class Vec:
    def __init__(self, x):
        self.x = x

    def length(self):
        return abs(self.x)

    def sign(self):
        return self.x / abs(self.x)

    def distance(self, other):
        return abs(self.x - other.x)


v1 = Vec3(1, 1, 1)
v2 = Vec3(-7, 4, 0)
print("V1:", v1)
print("V1 Magnitude:", v1.magnitude())
print("V1 Normalized:", v1.direction())
print("V1 Inner Product:", v1 * v2)

print(v1.distance(v2))

assert Vec2(2, -2).length() == 2.828427
assert Vec(-10).length() == 10
assert Vec(-5).sign() == -1
assert Vec(5).sign() == 1
assert Vec(-3).distance(Vec(1)) == 4
