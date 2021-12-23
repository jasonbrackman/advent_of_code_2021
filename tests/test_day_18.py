import collections

import helpers
from day_18 import Node, reduce


def tests():
    test01()
    test02()
    test03()
    test03a()
    test04()
    test_magnitude()


def test01():
    lines = helpers.get_lines(r"../data/day_18_test.txt")
    # _ explosions
    explosions = True
    if explosions:
        expects = [
            "[[[[0,9],2],3],4]",
            "[7,[6,[5,[7,0]]]]",
            "[[6,[5,[7,0]]],3]",
            "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
        ]

        for fish, expect in zip(lines[:4], expects):
            node = Node(depth=0).load(eval(fish))
            ii = reduce(node, yield_steps=True)
            t = str(next(ii))
            assert t == expect, f"Explosion Test Error: Got {t}, expected {expect}"
        print("!!Explode Tests Complete!!")

        fish = lines[5]
        node = Node(depth=0).load(eval(fish))
        ii = reduce(node, yield_steps=True)
        t = str(next(ii))
        assert t == "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]"
        t = str(next(ii))
        assert t == "[[[[0,7],4],[15,[0,13]]],[1,1]]", f"E{t}"
        t = str(next(ii))
        assert t == "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
        t = str(next(ii))
        assert t == "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", f"E{t}"
        t = str(next(ii))
        assert t == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", f"E{t}"
        print("!!Split Tests Complete!!")


def test02():
    lines = helpers.get_lines(r"../data/day_18_test_sum.txt")
    school = collections.deque([])
    for line in lines:
        n = Node(depth=0).load(eval(line))
        school.append(n)

    final = Node.add(school.popleft(), school.popleft())

    while school:
        print("=" * 20)
        t = Node(depth=0)
        t.left = reduce(final)
        t.right = school.popleft()
        final = t
        print("-" * 25)
        print("ANSWER:", final.left)
        print("NEW:   ", final)
        print("-" * 25)

    ii = reduce(final, yield_steps=True)
    t = str(next(ii))
    assert (
        t == "[[[[4,0],[5,0]],[[[4,5],[2,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
    ), f"E{t}"
    assert (
        str(next(ii))
        == "[[[[4,0],[5,4]],[[0,[7,6]],[9,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
    )
    assert (
        str(next(ii))
        == "[[[[4,0],[5,4]],[[7,0],[15,5]]],[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]]"
    )
    assert (
        str(next(ii))
        == "[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[0,[11,3]],[[6,3],[8,8]]]]]"
    )
    assert (
        str(next(ii)) == "[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[11,0],[[9,3],[8,8]]]]]"
    )
    assert str(next(ii)) == "[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[11,9],[0,[11,8]]]]]"
    assert str(next(ii)) == "[[[[4,0],[5,4]],[[7,0],[15,5]]],[10,[[11,9],[11,0]]]]"
    assert str(next(ii)) == "[[[[4,0],[5,4]],[[7,0],[[7,8],5]]],[10,[[11,9],[11,0]]]]"
    t = str(next(ii))
    assert t == "[[[[4,0],[5,4]],[[7,7],[0,13]]],[10,[[11,9],[11,0]]]]", f"E{t}"
    print("!!Addition 1 Tests Complete!!")


def test03():
    lines = helpers.get_lines(r"../data/day_18_test_sum2.txt")
    school = collections.deque([])
    for line in lines:
        n = Node(depth=0).load(eval(line))
        school.append(n)

    final = Node.add(school.popleft(), school.popleft())

    ii = reduce(final, yield_steps=True)
    t = None
    for i in ii:
        t = i
    assert str(t) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"

    final = Node.add(t, school.popleft())
    ii = reduce(final, yield_steps=True)
    for i in ii:
        t = i

    assert str(t) == "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"

    final = Node.add(t, school.popleft())
    # print(final)
    ii = reduce(final, yield_steps=True)
    for i in ii:
        t = i
        # print(t)
    assert (
        str(t) == "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
    ), f"    E:{t}"


def test03a():
    lines = helpers.get_lines(r"../data/day_18_test_sum2a.txt")
    school = collections.deque([])
    for line in lines:
        n = Node(depth=0).load(eval(line))
        school.append(n)

    final = Node.add(school.popleft(), school.popleft())

    ii = reduce(final, yield_steps=True)
    t = None
    for i in ii:
        t = i

    assert str(t) == "[[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]]"


def test04():
    lines = helpers.get_lines(r"../data/day_18_test_sum2.txt")
    school = collections.deque([])
    for line in lines:
        n = Node(depth=0).load(eval(line))
        school.append(n)

    # primer
    final = Node.add(school.popleft(), school.popleft())
    while school:
        ii = reduce(final, yield_steps=True)
        t = None
        for i in ii:
            t = i
        final = Node.add(t, school.popleft())
    r = None
    ii = reduce(final, yield_steps=True)
    for i in ii:
        r = i
    assert str(r) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"
    print("!!Test 4 Complete!! ")


def test_magnitude():
    line = "[9,1]"
    n = Node(depth=0)
    n.load(eval(line))
    assert Node.magnitude(n) == 29, f"E:{n}"
    line = "[[9,1],[1,9]]"
    n = Node(depth=0)
    n.load(eval(line))
    assert Node.magnitude(n) == 129
    line = "[[1,2],[[3,4],5]]"
    n = Node(depth=0)
    n.load(eval(line))
    assert Node.magnitude(n) == 143
    line = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    n = Node(depth=0)
    n.load(eval(line))
    assert Node.magnitude(n) == 1384
    items = [
        "[[[[1,1],[2,2]],[3,3]],[4,4]]",  # becomes 445.
        "[[[[3,0],[5,3]],[4,4]],[5,5]]",  # becomes 791.
        "[[[[5,0],[7,4]],[5,5]],[6,6]]",  # becomes 1137.
        "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",  # becomes 3488.
    ]
    expected = [445, 791, 1137, 3488]
    for item, expect in zip(items, expected):
        n = Node(depth=0)
        n.load(eval(item))
        assert Node.magnitude(n) == expect
    print("!!Magnitude Tests Complete!!")

if __name__ == "__main__":
    tests()