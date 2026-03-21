from .reddit_rss import fetch_reddit
from .newsapi import fetch_news

def run_ingestion():
    reddit_data = fetch_reddit()
    news_data = fetch_news()
    return reddit_data + news_data