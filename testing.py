from collections import defaultdict

stuff = """
S1: 0 -> S2: 9 Count: 40 2
S1: 1 -> S2: 4 Count: 40 4
S1: 2 -> S2: 12 Count: 39 6
S1: 3 -> S2: 6 Count: 40 8
S1: 4 -> S2: 1 Count: 40 10
S1: 5 -> S2: 15 Count: 40 12
S1: 6 -> S2: 1 Count: 68 13
S1: 7 -> S2: 1 Count: 82 14
S1: 8 -> S2: 1 Count: 96 15
S1: 9 -> S2: 0 Count: 40 17
S1: 10 -> S2: 31 Count: 41 19
S1: 11 -> S2: 0 Count: 53 20
S1: 12 -> S2: 2 Count: 39 22
S1: 13 -> S2: 1 Count: 111 23
S1: 14 -> S2: 23 Count: 38 25
S1: 15 -> S2: 1 Count: 139 26
S1: 16 -> S2: 1 Count: 153 27
S1: 17 -> S2: 2 Count: 53 28
S1: 18 -> S2: 1 Count: 167 29
S1: 19 -> S2: 1 Count: 180 30
S1: 20 -> S2: 2 Count: 67 31
S1: 21 -> S2: 0 Count: 61 32
S1: 22 -> S2: 1 Count: 191 33
S1: 23 -> S2: 1 Count: 202 34
S1: 24 -> S2: 1 Count: 206 35
S1: 25 -> S2: 1 Count: 220 36
S1: 26 -> S2: 1 Count: 231 37
S1: 27 -> S2: 1 Count: 241 38
S1: 28 -> S2: 1 Count: 249 39
S1: 29 -> S2: 30 Count: 40 41
S1: 30 -> S2: 29 Count: 40 43
S1: 31 -> S2: 0 Count: 90 44
S1: 0 -> S2: 2 Count: 145 44
S1: 1 -> S2: 3 Count: 249 45
S1: 2 -> S2: 0 Count: 145 45
S1: 3 -> S2: 5 Count: 249 46
S1: 4 -> S2: 0 Count: 173 46
S1: 5 -> S2: 6 Count: 249 46
S1: 6 -> S2: 7 Count: 249 47
S1: 7 -> S2: 2 Count: 364 47
S1: 8 -> S2: 2 Count: 364 47
S1: 9 -> S2: 2 Count: 364 47
S1: 10 -> S2: 0 Count: 173 47
S1: 11 -> S2: 1 Count: 262 47
S1: 12 -> S2: 0 Count: 173 47
S1: 13 -> S2: 2 Count: 364 47
S1: 14 -> S2: 1 Count: 262 47
S1: 15 -> S2: 2 Count: 364 47
S1: 16 -> S2: 0 Count: 187 47
S1: 17 -> S2: 0 Count: 187 47
S1: 18 -> S2: 2 Count: 364 47
S1: 19 -> S2: 2 Count: 364 47
S1: 20 -> S2: 0 Count: 187 47
S1: 21 -> S2: 1 Count: 270 47
S1: 22 -> S2: 2 Count: 364 47
S1: 23 -> S2: 2 Count: 364 47
S1: 24 -> S2: 2 Count: 364 47
S1: 25 -> S2: 2 Count: 364 47
S1: 26 -> S2: 2 Count: 364 47
S1: 27 -> S2: 2 Count: 364 47
S1: 28 -> S2: 2 Count: 364 47
S1: 29 -> S2: 0 Count: 215 47
S1: 30 -> S2: 0 Count: 215 47
S1: 31 -> S2: 2 Count: 364 47
S1: 0 -> S2: 4 Count: 215 47
S1: 1 -> S2: 8 Count: 270 48
S1: 2 -> S2: 10 Count: 364 49
S1: 3 -> S2: 11 Count: 262 50
S1: 4 -> S2: 12 Count: 215 50
S1: 5 -> S2: 13 Count: 249 51
S1: 6 -> S2: 14 Count: 249 52
S1: 7 -> S2: 15 Count: 249 52
S1: 8 -> S2: 9 Count: 292 52
S1: 9 -> S2: 16 Count: 292 53
S1: 10 -> S2: 17 Count: 364 54
S1: 11 -> S2: 18 Count: 262 55
S1: 12 -> S2: 20 Count: 215 56
S1: 13 -> S2: 19 Count: 249 57
S1: 14 -> S2: 21 Count: 263 58
S1: 15 -> S2: 22 Count: 249 59
S1: 16 -> S2: 23 Count: 292 59
S1: 17 -> S2: 24 Count: 364 60
S1: 18 -> S2: 26 Count: 262 61
S1: 19 -> S2: 18 Count: 262 61
S1: 20 -> S2: 27 Count: 228 62
S1: 21 -> S2: 28 Count: 263 63
S1: 23 -> S2: 25 Count: 292 64
S1: 24 -> S2: 29 Count: 392 64
"""

results = defaultdict(set)

for item in stuff.split('\n'):
    items = item.split()
    if items:
        s1 = items[1]
        s2 = items[4]
        results[s2].add(s1)
        ss = [results[r] for r in results[s2]]
        for s in ss:
            results[s2].update(s)
        print(s1, s2, len(results[s2]))

