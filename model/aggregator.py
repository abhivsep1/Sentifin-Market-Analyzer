import sys
sys.path.insert(0, "D:/project_imp")

def aggregate(results: list) -> dict:
    score_map = {"positive": 1, "neutral": 0, "negative": -1}
    if not results:
        return {"aggregate_score": 0, "signal": "HOLD", "count": 0}
    
    weighted = sum(
        score_map[r["label"]] * r["score"] for r in results
    )
    avg = weighted / len(results)
    
    signal = "BUY" if avg > 0.3 else "SELL" if avg < -0.3 else "HOLD"
    
    return {
        "aggregate_score": round(avg, 4),
        "signal": signal,
        "count": len(results)
    }