import sys
sys.path.insert(0, "D:/project_imp")

import requests
from datetime import datetime, timedelta
from config import NEWSAPI_KEY, TICKERS

# only accept articles from these trusted financial sources
TRUSTED_SOURCES = [
    "reuters.com",
    "bloomberg.com", 
    "cnbc.com",
    "forbes.com",
    "wsj.com",
    "ft.com",
    "marketwatch.com",
    "businessinsider.com",
    "yahoo finance",
    "seeking alpha",
    "benzinga",
    "motley fool",
    "investopedia",
    "barrons",
    "thestreet"
]

def is_trusted_source(source_name: str) -> bool:
    source_lower = source_name.lower()
    return any(trusted in source_lower for trusted in TRUSTED_SOURCES)

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
            source_name = article["source"]["name"]
            
            if not is_trusted_source(source_name):
                continue
                
            text = article["title"]
            if not text or len(text) < 30:
                continue
                
            articles.append({
                "ticker": ticker,
                "source": source_name,
                "text": text,
                "fetched_at": datetime.utcnow().isoformat()
            })
    
    print(f"NewsAPI: fetched {len(articles)} articles from trusted sources")
    return articles