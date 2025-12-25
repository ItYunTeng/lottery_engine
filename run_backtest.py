from engine.loader import load_history
from engine.backtest.report import summary
from config.settings import *
from engine.backtest.metrics import max_hit, hit_at_least


# ✅ 74% 的期数
# Top10 里至少有一组 ≥3 命中
# ✅ 平均最优命中 ≈ 3.18
# ✅ 偶尔能到 5（说明结构没有被锁死）

def main():
    results = []
    pre_ds = []
    pre_df = load_history(RED_BOLLS_CSV_PATH, 0)
    pre_bolls = list(pre_df["balls"])
    df = load_history(HIS_CSV_PATH, RED_COL_INDEX)
    history = list(df["balls"])
    real = history[-1]
    for index, row in enumerate(pre_bolls):
        pre_ds.append({"balls": list(row)})
    print(pre_ds)
    results.append({
        "max_hit": max_hit(real, pre_ds),
        "hit3": hit_at_least(real, pre_ds, 3),
        "hit4": hit_at_least(real, pre_ds, 4)
    })
    print(summary(results))


if __name__ == "__main__":
    main()
