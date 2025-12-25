class BaseStrategy:
    name = "base"

    def score(self, balls, context):
        raise NotImplementedError
