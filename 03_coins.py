import itertools

coins = [2, 7, 9, 5, 3]
perms = itertools.permutations(coins, 5)

for perm in perms:
    c = perm[0] + perm[1] * pow(perm[2], 2) + pow(perm[3], 3) - perm[4]
    if c == 399:
        print(perm)