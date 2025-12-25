import csv


def read_last_row_11th_column(csv_file_path):
    """
    从 CSV 文件中读取最后一行的第 11 列（索引为 10），
    并将其解析为整数列表，例如 "[0, 1, 3, 4]" -> [0, 1, 3, 4]
    """
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if not rows:
            raise ValueError("CSV 文件为空")
        last_row = rows[-1]
        if len(last_row) < 11:
            raise ValueError("最后一行没有第 11 列")
        data_str = last_row[10].strip()
        # 假设格式是 '[0, 1, 3, 4, 5, 6, 7, 9]' 这样的字符串
        try:
            numbers = eval(data_str)  # 注意：仅在信任数据源时使用 eval
            if not isinstance(numbers, list):
                raise ValueError("第 11 列内容不是列表格式")
            return [int(x) for x in numbers]
        except Exception as e:
            raise ValueError(f"无法解析第 11 列为列表: {e}")


def filter_numbers_by_suffix(valid_suffixes, total_range=33):
    """
    从 1 到 total_range（含）中筛选出以 valid_suffixes 中任意数字结尾的号码
    """
    result = []
    for num in range(1, total_range + 1):
        if num % 10 in valid_suffixes:
            result.append(num)
    return result


# 使用示例
if __name__ == "__main__":
    csv_path = "../data/pull_new.csv"  # 替换为你的 CSV 文件路径
    try:
        suffixes = read_last_row_11th_column(csv_path)
        filtered_numbers = filter_numbers_by_suffix(suffixes, total_range=33)
        print("读取到的后缀列表:", suffixes)
        print("筛选出的号码:", filtered_numbers)
    except Exception as e:
        print("错误:", e)
