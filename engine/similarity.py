def jac_card(a, b):
    return len(set(a) & set(b)) / len(set(a) | set(b))


def historical_similarity(balls, history, window=30):
    """
    计算与最近 window 期的最大相似度
    """
    sims = [jac_card(balls, h) for h in history[-window:]]
    return max(sims)
