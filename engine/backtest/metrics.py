def max_hit(real, pre_ds):
    """
    real: 实际开奖号（list）
    pre_ds: [{"balls": [...]}]
    """
    real = set(real)
    return max(len(real & set(p["balls"])) for p in pre_ds)


def hit_at_least(real, pre_ds, k):
    real = set(real)
    for p in pre_ds:
        if len(real & set(p["balls"])) >= k:
            return 1
    return 0
