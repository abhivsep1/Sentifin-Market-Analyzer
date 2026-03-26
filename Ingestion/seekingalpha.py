import sys
sys.path.insert(0, "D:/project_imp")

import feedparser
from datetime import datetime
from config import TICKERS

def fetch_seekingalpha(tickers=TICKERS):
    posts = []
    
    for ticker in tickers:
        url = f"https://seekingalpha.com/api/sa/combined/{ticker}.xml"
        
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                text = entry.title
                if not text or len(text) < 30:
                    continue
                    
                posts.append({
                    "ticker": ticker,
                    "source": "seekingalpha",
                    "text": text,
                    "fetched_at": datetime.utcnow().isoformat()
                })
                
        except Exception as e:
            print(f"SeekingAlpha error for {ticker}: {e}")
            continue
    
    print(f"SeekingAlpha: fetched {len(posts)} posts")
    return posts