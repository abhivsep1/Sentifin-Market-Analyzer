import sys
sys.path.insert(0, "D:/project_imp")

import time
import schedule
from datetime import datetime
from Ingestion.pipeline import run_ingestion
from model.sentiment import predict
from model.aggregator import aggregate
from model.stocks import fetch_prices
from database.db import (
    init_db, init_price_table, init_study_table,
    insert_results, insert_prices, insert_study_record
)
from config import TICKERS

SCORE_MAP = {"positive": 1, "neutral": 0, "negative": -1}
SOURCE_WEIGHTS = {"newsapi": 1.5, "seekingalpha": 1.5, "reddit": 0.5}

def get_source_weight(source: str) -> float:
    for key in SOURCE_WEIGHTS:
        if key in source.lower():
            return SOURCE_WEIGHTS[key]
    return 1.0

def get_time_of_day() -> str:
    hour = datetime.utcnow().hour
    if hour < 8:
        return "morning"
    elif hour < 13:
        return "afternoon"
    else:
        return "evening"

def run_study_cycle():
    print(f"\n[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}] Running study cycle...")
    time_of_day = get_time_of_day()
    today = datetime.utcnow().strftime("%Y-%m-%d")

    # fetch and run inference
    raw = run_ingestion()
    texts = [item["text"] for item in raw]
    preds = predict(texts)

    for i, item in enumerate(raw):
        item["label"] = preds[i]["label"]
        item["score"] = preds[i]["score"]

    # store raw results
    insert_results(raw)

    # compute per ticker study record
    study_records = []
    for ticker in TICKERS:
        ticker_items = [
            item for item in raw if item["ticker"] == ticker
        ]

        if not ticker_items:
            continue

        # weighted aggregation
        total_weight = 0
        weighted_sum = 0
        for item in ticker_items:
            w = get_source_weight(item["source"])
            weighted_sum += SCORE_MAP[item["label"]] * item["score"] * w
            total_weight += w

        score = weighted_sum / total_weight if total_weight > 0 else 0
        signal = "BUY" if score > 0.3 else "SELL" if score < -0.3 else "HOLD"

        study_records.append({
            "ticker": ticker,
            "date": today,
            "time_of_day": time_of_day,
            "sentiment_score": round(score, 4),
            "signal": signal,
            "item_count": len(ticker_items)
        })

    insert_study_record(study_records)
    print(f"Study records stored for {len(study_records)} tickers")
    for r in study_records:
        print(f"  {r['ticker']} | {r['time_of_day']} | score: {r['sentiment_score']} | {r['signal']} | items: {r['item_count']}")

    # fetch and store prices once per evening run
    if time_of_day == "evening":
        print("\nFetching closing prices...")
        prices = fetch_prices()
        insert_prices(prices)
        print(f"Stored {len(prices)} price records")

    print("Cycle complete.")

if __name__ == "__main__":
    # initialize all tables
    init_db()
    init_price_table()
    init_study_table()

    print("Study runner started.")
    print("Scheduled runs: 9:00 AM, 1:00 PM, 6:00 PM UTC")
    print("Run one cycle immediately to verify...")

    # run once immediately to verify everything works
    run_study_cycle()

    # then schedule
    schedule.every().day.at("09:00").do(run_study_cycle)
    schedule.every().day.at("13:00").do(run_study_cycle)
    schedule.every().day.at("18:00").do(run_study_cycle)

    while True:
        schedule.run_pending()
        time.sleep(60)