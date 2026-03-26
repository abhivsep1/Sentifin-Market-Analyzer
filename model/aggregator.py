import sys
sys.path.insert(0, "D:/project_imp")

# higher weight = more trusted source
SOURCE_WEIGHTS = {
    "newsapi": 1.5,
    "seekingalpha": 1.5,
    "reddit": 0.5
}

def get_source_weight(source: str) -> float:
    for key in SOURCE_WEIGHTS:
        if key in source.lower():
            return SOURCE_WEIGHTS[key]
    return 1.0  # default weight

def aggregate(results: list) -> dict:
    score_map = {"positive": 1, "neutral": 0, "negative": -1}
    
    if not results:
        return {"aggregate_score": 0, "signal": "HOLD", "count": 0}
    
    total_weight = 0
    weighted_sum = 0
    
    for r in results:
        source_weight = get_source_weight(r.get("source", ""))
        sentiment_score = score_map[r["label"]] * r["score"]
        weighted_sum += sentiment_score * source_weight
        total_weight += source_weight
    
    avg = weighted_sum / total_weight
    signal = "BUY" if avg > 0.3 else "SELL" if avg < -0.3 else "HOLD"
    
    return {
        "aggregate_score": round(avg, 4),
        "signal": signal,
        "count": len(results)
    }