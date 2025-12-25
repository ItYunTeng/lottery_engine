import random
from ss_ball_count import *
from engine.hoistorySuffixReds import *
from engine.rules import invalid_shape
from engine.features import count_repeat
from config.settings import *
from engine.fail_patterns import hit_fail_pattern


# ========== 你的原始函数 ==========
def calc_ac_value(numbers):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    differences = []
    for n in range(len(numbers)):
        for j in range(n + 1, len(numbers)):
            differences.append(numbers[j] - numbers[n])

    unique_differences = set(differences)
    ac_value = len(unique_differences) - (len(numbers) - 1)
    return ac_value


# ========== 步骤1：从flow.csv读取数据并取最后5行 ==========
def load_last_n_rows_from_csv(n=15):
    try:
        with open(HIS_CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            # 跳过表头
            data_rows = rows[1:]
            # 取最后n行
            last_n = data_rows[-n:] if len(data_rows) >= n else data_rows
            histories = []
            for row in last_n:
                red_str = row[2]  # 红球列（索引2）
                # 解析 "[1, 2, 3, 4, 5, 6]" 字符串为列表
                red_list = eval(red_str)
                histories.append(red_list)
            return histories
    except FileNotFoundError:
        print("找不到 flow.csv 文件，使用默认数据作为示例")


history_data = load_last_n_rows_from_csv(HOT_TOP_K)


def hot_bolls():
    # 热号统计
    freq = {}
    #  recent = df.tail(HOT_WINDOW)["balls"]
    for r in history_data[-HOT_WINDOW:]:
        for b in r:
            freq[b] = freq.get(b, 0) + 1

    return set(sorted(freq, key=freq.get, reverse=True)[:HOT_TOP_K])


# ========== 步骤2：分析历史数据 ==========
all_numbers = [num for row in history_data for num in row]
counter = Counter(all_numbers)

# 热号（出现>=2次，因为只有5行数据）
# hot_numbers = {num for num, count in counter.items() if count >= 2}
hot_numbers = hot_bolls()

# 冷号（出现<=1次）
cold_numbers = {num for num in range(1, 34) if num not in all_numbers}  # 完全没出过
rare_numbers = {num for num, count in counter.items() if count == 1}  # 出过1次
very_cold_numbers = cold_numbers | rare_numbers

# 统计历史特征
sums = [sum(row) for row in history_data]
avg_sum = sum(sums) / len(sums)
acs = [calc_ac_value(row) for row in history_data]
avg_ac = sum(acs) / len(acs)


# ========== 步骤3：生成候选组合 ==========
def generate_candidate():
    # 策略：至少1-2个热号，至多1个冷号，其余从剩余中选
    result = set()

    # 添加热号
    hot_sample_size = min(random.randint(1, 2), len(hot_numbers))
    if hot_numbers and hot_sample_size > 0:
        hot_sample = random.sample(list(hot_numbers), hot_sample_size)
        result.update(hot_sample)

    # 添加冷号（概率40%）
    if random.random() < 0.4 and very_cold_numbers:
        cold_pick = random.choice(list(very_cold_numbers))
        result.add(cold_pick)

    # 补充到6个
    remaining_pool = list(set(filtered_numbers) - result)
    while len(result) < 6:
        pick = random.choice(remaining_pool)
        result.add(pick)
        remaining_pool.remove(pick)

    return sorted(list(result))


def calculate_features(reds):
    totalScore = sum(reds)
    acValue = calc_ac_value(reds)
    zm = zero_model(reds)
    c0Value, c1Value, c2Value = zm.count(0), zm.count(1), zm.count(2)
    return totalScore, acValue, (c0Value, c1Value, c2Value)


def score_combination(reds):
    totalScore, acValue, model_dist = calculate_features(reds)

    # 计算与历史平均的偏差
    sum_score = abs(totalScore - avg_sum)
    ac_score = abs(acValue - avg_ac)

    # 012路计分：越接近(2,2,2)越好
    target_dist = (2, 2, 2)
    dist_score = sum(abs(a - b) for a, b in zip(model_dist, target_dist))

    # 和值权重最高，AC其次，分布最后
    total_score = sum_score * 1.0 + ac_score * 2.0 + dist_score * 1.5
    return total_score


suffixes = read_last_row_11th_column(HIS_CSV_PATH)
filtered_numbers = filter_numbers_by_suffix(suffixes, total_range=33)
# 生成大量候选并评分
candidates_with_scores = []
last_balls = history_data[-1]
fail_stats = {"hot": hot_bolls(), "cold": very_cold_numbers}
for _ in range(20000):  # 生成10000个候选
    balls = generate_candidate()
    if count_repeat(balls, last_balls) > MAX_REPEAT_WITH_LAST:
        continue

    if invalid_shape(balls, last_balls, history_data):
        continue

    if hit_fail_pattern(balls, last_balls, fail_stats):
        continue

    score = score_combination(balls)
    candidates_with_scores.append((balls, score))


def main():
    # ========== 步骤4：选出最佳10个 ==========
    sorted_candidates = sorted(candidates_with_scores, key=lambda x: x[1])
    top_10_combinations = [item[0] for item in sorted_candidates[:10]]

    # ========== 步骤5：输出manual_predictions ==========
    manual_predictions = top_10_combinations

    for i, combo in enumerate(manual_predictions):
        s, ac, m_dist = calculate_features(combo)
        print(f"{i + 1}: {combo} -> 和值:{s}, AC:{ac}, 012分布:{m_dist}")

    # 返回结果
    # 用于组合红球的循环
    with open(RED_BOLLS_CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(manual_predictions)


if __name__ == "__main__":
    main()
