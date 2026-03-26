import sys
sys.path.insert(0, "D:/project_imp")

import yfinance as yf
from datetime import datetime, timedelta
from config import TICKERS

def fetch_prices(tickers=TICKERS, days=14):
    prices = []
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    
    for ticker in tickers:
        data = yf.download(
            ticker,
            start=start.strftime("%Y-%m-%d"),
            end=end.strftime("%Y-%m-%d"),
            progress=False
        )
        for date, row in data.iterrows():
            prices.append({
                "ticker": ticker,
                "date": date.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2)
            })
    
    return prices