from collections import defaultdict
from typing import Dict, Tuple

import helpers


def parse(lines) -> Tuple[Dict[str, int], Dict[str, str], chr]:
    rules = iter(lines)  # create iter

    template = next(rules)
    next(rules)  # skip empty line
    rules = {rule.split()[0]: rule.split()[2] for rule in rules}

    # create counts for the template string
    counts = defaultdict(
        int, {k: template.count(k) for k, v in rules.items() if k in template}
    )

    return counts, rules, template[-1]


def run() -> None:
    lines = helpers.get_lines(r"./data/day_14.txt")
    counts, rules, extra = parse(lines)

    assert insertion_process(10, counts.copy(), extra, rules) == 3009
    assert insertion_process(40, counts.copy(), extra, rules) == 3459822539451


def insertion_process(
    steps: int, counts: Dict[str, int], extra: chr, rules: Dict[str, str]
) -> int:
    for step in range(steps):
        t = defaultdict(int)
        for (k1, k2), v in counts.items():
            new = rules[k1 + k2]
            t[k1 + new] += v
            t[new + k2] += v
            t[k1 + k2] -= v

        # Cannot add keys during an iteration loop, so
        # redoing the work and applying the changed
        # numbers to the original.
        for k, v in t.items():
            counts[k] += v

    totals = defaultdict(int)
    totals[extra] += 1
    for (k1, k2), v in counts.items():
        totals[k1] += v

    return max(totals.values()) - min(totals.values())


if __name__ == "__main__":
    run()
