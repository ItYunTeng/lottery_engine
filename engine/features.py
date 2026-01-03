import math
from collections import Counter
import numpy as np


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


def zero_model(balls):
    if len(balls) != 6:
        raise ValueError("need input six red bool")
    balls = sorted(balls)
    model = []
    for v in balls:
        model.append(v % 3)
    return model


# 012路统计：每期0,1,2的数量
def his_zero_model(history_data):
    model_counts = []
    for row in history_data:
        model = zero_model(row)
        c0 = model.count(0)
        c1 = model.count(1)
        c2 = model.count(2)
        model_counts.append((c0, c1, c2))
    return model_counts


def statistics(red_balls):
    mean = np.mean(red_balls)
    # ddof=1 表示样本方差（除以 n-1）
    variance = np.var(red_balls, ddof=1)
    std_dev = np.std(red_balls, ddof=1)
    return round(mean), round(variance), round(std_dev)


def find_most_common(lst):
    # 使用Counter来统计每个元素的出现次数
    counts = Counter(lst)
    # 找到出现次数最多的元素
    most_common = counts.most_common(1)
    # 如果列表为空，返回空元组
    return most_common[0] if most_common else ()
