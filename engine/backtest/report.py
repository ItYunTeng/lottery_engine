import numpy as np


def summary(results):
    max_hits = [r["max_hit"] for r in results]
    return {
        "rounds": len(results),
        "hit3_rate": float(np.mean([r["hit3"] for r in results])),
        "hit4_rate": float(np.mean([r["hit4"] for r in results])),
        "avg_max_hit": float(np.mean([r["max_hit"] for r in results])),
        "max_of_max_hit": max(max_hits)
    }
