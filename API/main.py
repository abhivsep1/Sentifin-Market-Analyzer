import sys
sys.path.insert(0, "D:/project_imp")

from fastapi import FastAPI
from database.db import get_sentiment_by_ticker
from model.aggregator import aggregate
from database.db import get_sentiment_by_ticker, get_prices_by_ticker
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

@app.get("/prices/{ticker}")
def get_prices(ticker: str, days: int = 7):
    rows = get_prices_by_ticker(ticker.upper(), days)
    prices = [
        {
            "date": row[0],
            "close": row[1]
        }
        for row in rows
    ]
    return {"ticker": ticker.upper(), "prices": prices}

@app.get("/daily_sentiment/{ticker}")
def get_daily_sentiment(ticker: str, days: int = 7):
    from database.db import get_daily_sentiment
    rows = get_daily_sentiment(ticker.upper(), days)
    data = [
        {
            "date": row[0],
            "daily_score": round(row[1], 4),
            "count": row[2]
        }
        for row in rows
    ]
    return {"ticker": ticker.upper(), "data": data}

@app.get("/study/{ticker}")
def get_study(ticker: str, days: int = 14):
    from database.db import get_study_data
    rows = get_study_data(ticker.upper(), days)
    data = [
        {
            "date": row[0],
            "time_of_day": row[1],
            "sentiment_score": row[2],
            "signal": row[3],
            "item_count": row[4]
        }
        for row in rows
    ]
    return {"ticker": ticker.upper(), "data": data}
