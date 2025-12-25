from engine.loader import load_history
from engine.selector import select_top
from engine.strategies.strategy_v1 import StrategyV1
from engine.strategies.strategy_v2 import StrategyV2
from engine.strategies.voter import StrategyVoter
from engine.explain import explain
from gen_red import *
import csv


def predict(top_n: int = 10):
    df = load_history(HIS_CSV_PATH, RED_COL_INDEX)
    history = list(df["balls"])
    # last_balls = df.iloc[-1]["balls"]
    # last_balls = history[-1]
    # 初始化策略
    strategies = [
        StrategyV1(),
        StrategyV2()
    ]

    results = []
    context = {
        "last_balls": last_balls,
        "hot_set": hot_numbers,
        "history": history,
    }

    voter = StrategyVoter(strategies)
    for i, c in enumerate(candidates_with_scores):
        sc = voter.vote(c[0], context)
        scores = sc["scores"]
        lst = list(c)
        lst[1] = scores
        if scores[1] >= SCORE_THRESHOLD:
            results.append({
                "balls": list(c),
                "score": scores[1],
                "explain": explain(c[0], last_balls, hot_numbers)
            })

    results = select_top(results, top_n)

    return {
        "last": last_balls,
        "result": results,
    }


def write_data_json(datas):
    bolls = []
    for result in datas['result']:
        bolls.append((result['balls'][0], result['explain']))

    with open(RED_BOLLS_CSV_PATH, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(bolls)


def main():
    write_data_json(predict(TOP_N))


if __name__ == "__main__":
    main()
