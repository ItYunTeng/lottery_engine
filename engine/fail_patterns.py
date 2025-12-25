from .features import *
from config.settings import *


def hit_fail_pattern(balls, last_balls, fail_stats=None):
    """
    命中失败形态返回 True
    """

    # ① 重号过多
    if count_repeat(balls, last_balls) > MAX_REPEAT_WITH_LAST:
        return True

    # ② 极端和值
    s = calc_sum(balls)
    if s < 65 or s > 125:
        return True

    # ③ 极端 AC
    ac = calc_ac(balls)
    if ac <= 3 or ac >= 13:
        return True

    # ④ 连号过密
    cons_ec = 0
    for i in range(1, len(balls)):
        if balls[i] - balls[i - 1] == 1:
            cons_ec += 1
            if cons_ec >= 2:
                return True
        else:
            cons_ec = 0

    # ⑤ 全热 / 全冷
    if fail_stats:
        hot_hit = sum(1 for b in balls if b in fail_stats["hot"])
        cold_hit = sum(1 for b in balls if b in fail_stats["cold"])
        if hot_hit >= 5 or cold_hit >= 4:
            return True

    return False
