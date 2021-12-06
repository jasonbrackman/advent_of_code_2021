from collections import defaultdict

import helpers


def group_size_at_cycle(age_groups: defaultdict, cycle: int) -> int:

    for _ in range(cycle):
        new_dict = defaultdict(int)
        for k, v in age_groups.items():
            if k == 0:
                new_dict[8] += v
                new_dict[6] += v
            else:
                new_dict[k - 1] += v
        age_groups = new_dict
    return sum(age_groups.values())


def run() -> None:
    lines = helpers.get_lines(r"./data/day_06.txt")
    age_groups = defaultdict(int)
    for age in (int(i) for i in lines[0].split(",")):
        age_groups[age] += 1

    assert group_size_at_cycle(age_groups, 80) == 355386
    assert group_size_at_cycle(age_groups, 256) == 1613415325809


if __name__ == "__main__":
    run()
