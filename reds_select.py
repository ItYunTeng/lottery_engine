import csv
import ast
from itertools import combinations


def read_csv_first_column(csv_path):
    """
    读取CSV文件的第一列，将其解析为数字列表的集合
    """
    csv_combinations = set()

    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # 确保行不为空
                try:
                    # 1. 去除引号并解析字符串为列表
                    # 例如将 "[1, 6, 9, 17, 19, 23]" 转换为 [1, 6, 9, 17, 19, 23]
                    list_str = row[0].strip().strip('"\'')
                    number_list = ast.literal_eval(list_str)

                    # 2. 排序并转换为元组，以便存入集合进行高效比对
                    sorted_tuple = tuple(sorted(number_list))
                    csv_combinations.add(sorted_tuple)

                except Exception as e:
                    print(f"解析行出错: {row[0]}, 错误: {e}")
                    continue
    print(f"从 CSV 文件中成功读取 {len(csv_combinations)} 个组合。")
    return csv_combinations


def generate_my_combinations():
    # 1. 定义数据
    data = [
        [2, 12, 22, 32],
        [10, 20, 30],
        [5, 15, 25],
        [9, 19, 29],
        [3, 13, 23, 33],
        [4, 14, 24],
        [6, 16, 26],
        [7, 17, 27],
        [8, 18, 28]
    ]

    # 2. 合并成一个大列表
    all_numbers = []
    for row in data:
        all_numbers.extend(row)

    print(f"总共有 {len(all_numbers)} 个数字，准备生成 C({len(all_numbers)}, 6) 种组合...")

    # 3. 生成所有 6 个数的组合
    # 注意：combinations 生成的是元组
    all_combinations = set(combinations(sorted(all_numbers), 6))

    print(f"生成完毕！总共 {len(all_combinations)} 种组合。")

    return all_combinations


if __name__ == "__main__":
    # 1. 生成你的组合 (集合A)
    my_combs_set = generate_my_combinations()

    # 2. 读取CSV文件中的组合 (集合B)
    # 请将这里的路径替换为你实际的CSV文件路径
    csv_file_path = "data/red_bolls.csv"
    csv_combs_set = read_csv_first_column(csv_file_path)

    # 3. 计算交集 (共同存在的组合)
    # 这是最重要的一步，找出既在你的逻辑中，又在历史数据里的组合
    intersection = my_combs_set & csv_combs_set
    print(f"双方共同的组合 (交集) 数量: {len(intersection)}")

    # 6. 保存结果到新文件
    with open("data/section_results.txt", "w", encoding="utf-8") as f:
        f.write(f"共找到 {len(intersection)} 个匹配的组合。\n\n")
        for comb in sorted(intersection):  # 排序后写入，方便查看
            f.write(f"{list(comb)}\n")
    print(f"\n交集结果已保存到 'section_results.txt'")
