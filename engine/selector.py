def select_top(candidates, top_n):
    return sorted(candidates, key=lambda x: x["score"], reverse=True)[:top_n]
