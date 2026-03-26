import sys
sys.path.insert(0, "D:/project_imp")

from Ingestion.reddit_rss import fetch_reddit
from Ingestion.seekingalpha import fetch_seekingalpha

def run_ingestion():
    reddit_data = fetch_reddit()
    sa_data = fetch_seekingalpha()
    
    all_data = reddit_data + sa_data
    print(f"Total ingested: {len(all_data)} items")
    return all_data