# ssq_crawler_500star_direct.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import warnings
warnings.filterwarnings('ignore')

# 直接请求数据接口（返回 HTML <tr> 片段）
DATA_URL = "https://datachart.500star.com/ssq/history/newinc/history.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://datachart.500star.com/ssq/history/history.shtml"
}


def main():
    print("正在从 500 彩票网接口直接获取双色球历史数据...")

    try:
        # 请求数据接口（返回一堆 <tr>）
        params = {
            "limit": "10000",  # 足够大
            "sort": "asc"  # 从最早到最新
        }
        resp = requests.get(DATA_URL, headers=HEADERS, params=params, timeout=15)
        resp.encoding = 'gb2312'  # 关键！网站使用 GB2312 编码

        # 解析返回的 HTML 片段（它是一堆 <tr>）
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.find_all('tr')

        records = []
        for row in rows:
            tds = row.find_all('td')
            if len(tds) < 9:
                continue  # 跳过无效行
            reds = []
            try:
                # 根据你提供的源码结构，字段顺序为：
                # [期号, 红1, 红2, 红3, 红4, 红5, 红6, 蓝, ..., 日期]
                issue = tds[0].get_text(strip=True)  # 如 "2025149"
                reds.append(int(tds[1].get_text(strip=True)))
                reds.append(int(tds[2].get_text(strip=True)))
                reds.append(int(tds[3].get_text(strip=True)))
                reds.append(int(tds[4].get_text(strip=True)))
                reds.append(int(tds[5].get_text(strip=True)))
                reds.append(int(tds[6].get_text(strip=True)))
                blue = int(tds[7].get_text(strip=True))
                date_str = tds[-1].get_text(strip=True)  # 最后一列是日期

                # 验证日期格式
                if not re.match(r'\d{4}-\d{2}-\d{2}', date_str):
                    continue

                record = {
                    "日期": date_str,
                    "期号": issue,
                    "红球": reds,
                    "篮球": blue
                }
                records.append(record)

            except (ValueError, IndexError, AttributeError):
                continue

        if not records:
            print("❌ 未提取到任何有效数据，请检查接口返回内容。")
            # 可选：打印前500字符用于调试
            print("接口返回前500字符：")
            print(resp.text[:500])
            return

        # 去重 + 排序
        df = pd.DataFrame(records)
        df['日期'] = pd.to_datetime(df['日期'])
        df = df.drop_duplicates(subset=['期号']).sort_values('日期').reset_index(drop=True)

        # 保存
        output_file = "ssq_full_history.csv"
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ 成功获取 {len(df)} 期完整历史数据！已保存至 {output_file}")
        print("\n最早3期：")
        print(df[['日期', '红球', '篮球']].head(5).to_string(index=False))
        print("\n最新3期：")
        print(df[['日期', '红球', '篮球']].tail(5).to_string(index=False))

    except Exception as e:
        print(f"❌ 爬取失败: {e}")


if __name__ == "__main__":
    main()
