import sys
sys.path.insert(0, "D:/project_imp")

import requests
from datetime import datetime, timedelta
from config import NEWSAPI_KEY, TICKERS

def fetch_news(tickers=TICKERS):
    articles = []
    for ticker in tickers:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": ticker,
            "language": "en",
            "sortBy": "publishedAt",
            "from": (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "apiKey": NEWSAPI_KEY,
            "pageSize": 20
        }
        response = requests.get(url, params=params)
        data = response.json()
        for article in data.get("articles", []):
            articles.append({
                "ticker": ticker,
                "source": article["source"]["name"],
                "text": article["title"],
                "fetched_at": datetime.utcnow().isoformat()
            })
    return articles