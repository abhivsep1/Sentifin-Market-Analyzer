import sys
sys.path.insert(0, "D:/project_imp")

import feedparser
import time
from datetime import datetime
from config import SUBREDDITS, TICKERS

# minimum length for a headline to be considered meaningful
MIN_LENGTH = 60

# keywords that indicate a financially meaningful post
FINANCIAL_KEYWORDS = [
    "earnings", "revenue", "profit", "loss", "price", "stock",
    "market", "share", "invest", "bull", "bear", "target",
    "upgrade", "downgrade", "buy", "sell", "hold", "forecast",
    "guidance", "quarter", "annual", "growth", "decline", "surge",
    "drop", "crash", "rally", "ipo", "dividend", "acquisition",
    "merger", "bankruptcy", "debt", "fund", "analyst", "report"
]

def is_meaningful(text: str, ticker: str) -> bool:
    text_lower = text.lower()
    
    # must meet minimum length
    if len(text) < MIN_LENGTH:
        return False
    
    # must mention ticker or at least one financial keyword
    if ticker.lower() in text_lower:
        return True
    
    if any(kw in text_lower for kw in FINANCIAL_KEYWORDS):
        return True
    
    return False

def fetch_reddit(tickers=TICKERS):
    posts = []
    total_fetched = 0
    total_kept = 0

    for ticker in tickers:
        for sub in SUBREDDITS:
            url = (
                f"https://www.reddit.com/r/{sub}/search.rss"
                f"?q={ticker}&restrict_sr=1&sort=new"
            )
            feed = feedparser.parse(url)
            for entry in feed.entries:
                total_fetched += 1
                text = entry.title

                if not is_meaningful(text, ticker):
                    continue

                total_kept += 1
                posts.append({
                    "ticker": ticker,
                    "source": f"reddit/r/{sub}",
                    "text": text,
                    "fetched_at": datetime.utcnow().isoformat()
                })
            time.sleep(1)

    print(f"Reddit: kept {total_kept}/{total_fetched} posts after filtering")
    return posts