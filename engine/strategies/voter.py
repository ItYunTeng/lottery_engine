class StrategyVoter:

    def __init__(self, strategies):
        self.strategies = strategies

    def vote(self, balls, context):
        scores = []
        for s in self.strategies:
            sc = s.score(balls, context)
            scores.append(sc)

        return {
            "avg": sum(scores) / len(scores),
            "max": max(scores),
            "min": min(scores),
            "scores": scores
        }
