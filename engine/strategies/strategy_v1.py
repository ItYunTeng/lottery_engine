# 保守
from .base import BaseStrategy
from engine.scorer import score_v1


class StrategyV1(BaseStrategy):
    name = "conservative1"

    def score(self, balls, context):
        return score_v1(
            balls,
            context["last_balls"],
            context["hot_set"]
        )
