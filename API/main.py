import sys
sys.path.insert(0, "D:/project_imp")

from fastapi import FastAPI
from database.db import get_sentiment_by_ticker
from model.aggregator import aggregate

app = FastAPI(title="Market Sentiment API")

@app.get("/")
def root():
    return {"status": "running", "message": "Market Sentiment API is live"}

@app.get("/sentiment/{ticker}")
def get_sentiment(ticker: str, days: int = 7):
    rows = get_sentiment_by_ticker(ticker.upper(), days)
    results = [
        {
            "ticker": row[0],
            "label": row[1],
            "score": row[2],
            "fetched_at": row[3],
            "source": row[4],
            "text": row[5]
        }
        for row in rows
    ]
    return {"ticker": ticker.upper(), "count": len(results), "data": results}

@app.get("/signal/{ticker}")
def get_signal(ticker: str, days: int = 7):
    rows = get_sentiment_by_ticker(ticker.upper(), days)
    results = [{"label": row[1], "score": row[2]} for row in rows]
    signal = aggregate(results)
    return {"ticker": ticker.upper(), "signal": signal}

@app.get("/tickers")
def get_tickers():
    from config import TICKERS
    return {"tickers": TICKERS}