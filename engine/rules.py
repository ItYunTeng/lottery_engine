from .features import *


def invalid_shape(balls, last_balls):
    if count_repeat(balls, last_balls) >= 3:
        return True

    s = calc_sum(balls)
    if s < 60 or s > 130:
        return True

    ac = calc_ac(balls)
    if ac < 4 or ac > 12:
        return True

    if odd_even(balls) in [(6, 0), (0, 6)]:
        return True

    if big_small(balls) in [(5, 1), (1, 5)]:
        return True

    return False
