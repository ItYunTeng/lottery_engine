import urllib.request as ur
from bs4 import BeautifulSoup
import math
import csv
from engine.features import statistics

url = 'https://view.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=ssq&actionType=chzs&type=120&dpc=1'


def calc_ac_value(numbers):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    differences = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            differences.append(numbers[j] - numbers[i])

    unique_differences = set(differences)
    ac_value = len(unique_differences) - (len(numbers) - 1)
    return ac_value


def ac_diff(numbers):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    diffs = []
    # 获取索引
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            diffs.append((numbers[j] - numbers[i]) % 10)
    return diffs


def and_diff(numbers):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    return [(numbers[1] - numbers[0]) % 10, (numbers[3] - numbers[2]) % 10,
            (numbers[5] - numbers[4]) % 10]


def split_diff(numbers):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    return [(numbers[5] - numbers[0]) % 10, (numbers[4] - numbers[1]) % 10,
            (numbers[3] - numbers[2]) % 10]


def formula_diff(numbers, add):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    diff = []
    for v in numbers:
        diff.append((math.floor((add - v) / v)) % 10)

    return diff


def zero_model(numbers):
    if len(numbers) != 6:
        raise ValueError("need input six red bool")
    numbers = sorted(numbers)
    model = []
    for v in numbers:
        model.append(v % 3)
    return model


def model_val(add):
    diff = []
    s = [6, 5, 4]
    for i in s:
        diff.append((add % i) % 10)

    return diff


def save_data(rows):
    with open('data/pull_new.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def get_datas():
    req = ur.Request(url=url)
    page = ur.urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find('table', attrs={'class', 'zst_table'})
    if table is None:
        raise ValueError("文档不存在")

    rows = [[
        '期数', '星期', '红球', '篮球', '和值', 'AC', '分列差', '并列差', '公式差', '取模直', '非AC尾',
        '012路','样本分析-均值-方差-标准差'
    ]]
    tbody = table.find_all('tbody')
    trs = tbody[0].find_all('tr')

    for tr in trs:
        data = tr.find_all('td')
        cic = data[0].getText()
        week = data[2].getText()
        add = data[57].getText()
        model_vals = model_val(int(add))
        blue = int(
            tr.find_all('td', attrs={'class', 'chartball02'})[0].getText())

        tds = tr.find_all(name='td', class_=['chartball01', 'chartball20'])
        if len(tds) == 0:
            continue
        reds = []
        for td in tds:
            data = td.getText()
            reds.append(int(data))

        ac = calc_ac_value(reds)
        and_diffs = and_diff(reds)
        split_diffs = split_diff(reds)
        formula_diffs = formula_diff(reds, int(add))
        zero_models = zero_model(reds)
        stat = list(statistics(reds))
        add_ends = list(
            set(and_diffs + split_diffs + formula_diffs + model_vals))
        rows.append([
            cic, week, reds, blue, add, ac, split_diffs, and_diffs,
            formula_diffs, model_vals, add_ends, zero_models, stat
        ])
    print('拉取数据计算完成。。。。。。')
    save_data(rows)


if __name__ == "__main__":
    get_datas()
