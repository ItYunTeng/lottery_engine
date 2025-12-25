def calc_sum(balls):
    return sum(balls)


def count_repeat(a, b):
    return len(set(a) & set(b))


def odd_even(balls):
    odd = sum(1 for x in balls if x % 2 == 1)
    return odd, 6 - odd


def big_small(balls):
    big = sum(1 for x in balls if x > 16)
    return big, 6 - big


def calc_ac(balls):
    diffs = set()
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            diffs.add(balls[j] - balls[i])
    return len(diffs) - (len(balls) - 1)
