import sys
sys.path.insert(0, "D:/project_imp")

import feedparser
import time
from datetime import datetime
from config import SUBREDDITS, TICKERS

def fetch_reddit(tickers=TICKERS):
    posts = []
    for ticker in tickers:
        for sub in SUBREDDITS:
            url = (
                f"https://www.reddit.com/r/{sub}/search.rss"
                f"?q={ticker}&restrict_sr=1&sort=new"
            )
            feed = feedparser.parse(url)
            for entry in feed.entries:
                posts.append({
                    "ticker": ticker,
                    "source": f"reddit/r/{sub}",
                    "text": entry.title,  # short, suits your model
                    "fetched_at": datetime.utcnow().isoformat()
                })
            time.sleep(1)
    return posts