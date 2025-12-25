from .features import *


def explain(balls, last_balls, hot_set):
    explanation = []

    rep = count_repeat(balls, last_balls)
    explanation.append(f"重号数: {rep}")

    hot_hit = len(set(balls) & hot_set)
    explanation.append(f"热号命中: {hot_hit}")

    s = calc_sum(balls)
    explanation.append(f"和值: {s}")

    ac = calc_ac(balls)
    explanation.append(f"AC值: {ac}")

    oe = odd_even(balls)
    explanation.append(f"奇偶比: {oe[0]}:{oe[1]}")

    bs = big_small(balls)
    explanation.append(f"大小比: {bs[0]}:{bs[1]}")

    return explanation
