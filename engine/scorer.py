from .features import *
from .similarity import historical_similarity


def score_v1(balls, last_balls, hot_set):
    score = 0
    # 重号
    rep = count_repeat(balls, last_balls)
    score += 30 if rep == 1 else 20 if rep == 0 else -50
    # 热号（封顶，防追热）
    score += min(len(set(balls) & hot_set), 3) * 8
    # 和值
    s = calc_sum(balls)
    score += 15 if 80 <= s <= 110 else 8 if 70 <= s <= 120 else -10
    # AC
    ac = calc_ac(balls)
    score += 12 if 6 <= ac <= 9 else 6 if 5 <= ac <= 10 else -5
    # 奇偶 / 大小
    if odd_even(balls) in [(3, 3), (4, 2), (2, 4)]:
        score += 8

    if big_small(balls) == (3, 3):
        score += 7

    return score


def score_v2(balls, last_balls, hot_set, history):
    score = score_v1(balls, last_balls, hot_set)

    sim = historical_similarity(balls, history)

    # 相似度惩罚（防止形态复制）
    if sim >= 0.6:
        score -= 15
    elif sim >= 0.5:
        score -= 8
    else:
        score += 5

    return score
