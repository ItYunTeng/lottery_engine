# 生成1-33之间的整数列表
from itertools import combinations
import csv

red_ball_candidates = list(range(1, 34))
# 存储红球组合的列表
red_ball_combinations = []


def is_conti(num, reds):
    count = 0
    reds = sorted(reds)
    for i in range(1, len(reds)):
        if reds[i] == reds[i - 1] + 1:
            count += 1
            if count >= num:
                return True
        else:
            count = 0
    return False


# 用于组合红球的循环
for combination in combinations(red_ball_candidates, 6):
    if not is_conti(3, combination):
        red_ball_combinations.append(combination)
with open('data/red_bolls.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(red_ball_combinations)
