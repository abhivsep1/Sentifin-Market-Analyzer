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

def init_price_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            close REAL,
            UNIQUE(ticker, date)
        )
    """)
    conn.commit()
    conn.close()

def insert_prices(prices: list):
    conn = sqlite3.connect(DB_PATH)
    conn.executemany("""
        INSERT OR IGNORE INTO price_data (ticker, date, close)
        VALUES (:ticker, :date, :close)
    """, prices)
    conn.commit()
    conn.close()

def get_prices_by_ticker(ticker: str, days: int = 7):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT date, close
        FROM price_data
        WHERE ticker = ?
        AND date >= date('now', ?)
        ORDER BY date ASC
    """, (ticker, f"-{days} days")).fetchall()
    conn.close()
    return rows

def get_daily_sentiment(ticker: str, days: int = 7):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT 
            DATE(fetched_at) as date,
            AVG(CASE 
                WHEN label = 'positive' THEN score
                WHEN label = 'negative' THEN -score
                ELSE 0
            END) as daily_score,
            COUNT(*) as count
        FROM sentiment_results
        WHERE ticker = ?
        AND fetched_at >= datetime('now', ?)
        GROUP BY DATE(fetched_at)
        ORDER BY date ASC
    """, (ticker, f"-{days} days")).fetchall()
    conn.close()
    return rows

def init_study_table():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_study (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT,
            date TEXT,
            time_of_day TEXT,
            sentiment_score REAL,
            signal TEXT,
            item_count INTEGER,
            UNIQUE(ticker, date, time_of_day)
        )
    """)
    conn.commit()
    conn.close()

def insert_study_record(records: list):
    conn = sqlite3.connect(DB_PATH)
    conn.executemany("""
        INSERT OR IGNORE INTO sentiment_study
        (ticker, date, time_of_day, sentiment_score, signal, item_count)
        VALUES (:ticker, :date, :time_of_day, :sentiment_score, :signal, :item_count)
    """, records)
    conn.commit()
    conn.close()

def get_study_data(ticker: str, days: int = 14):
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT date, time_of_day, sentiment_score, signal, item_count
        FROM sentiment_study
        WHERE ticker = ?
        AND date >= date('now', ?)
        ORDER BY date ASC, time_of_day ASC
    """, (ticker, f"-{days} days")).fetchall()
    conn.close()
    return rows