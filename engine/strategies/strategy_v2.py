# 相似度抑制
from .base import BaseStrategy
from engine.scorer import score_v2


class StrategyV2(BaseStrategy):
    name = "conservative2"

    def score(self, balls, context):
        return score_v2(
            balls,
            context["last_balls"],
            context["hot_set"],
            context["history"]
        )
