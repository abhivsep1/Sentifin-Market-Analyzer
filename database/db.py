import sys
sys.path.insert(0, "D:/project_imp")

import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            source TEXT,
            text TEXT,
            label TEXT,
            score REAL,
            fetched_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_results(results: list):
    conn = sqlite3.connect(DB_PATH)
    conn.executemany("""
        INSERT INTO sentiment_results 
        (ticker, source, text, label, score, fetched_at)
        VALUES (:ticker, :source, :text, :label, :score, :fetched_at)
    """, results)
    conn.commit()
    conn.close()

def get_sentiment_by_ticker(ticker: str, days: int = 7):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT ticker, label, score, fetched_at, source, text
        FROM sentiment_results
        WHERE ticker = ?
        AND fetched_at >= datetime('now', ?)
        ORDER BY fetched_at DESC
    """, (ticker, f"-{days} days")).fetchall()
    conn.close()
    return rows