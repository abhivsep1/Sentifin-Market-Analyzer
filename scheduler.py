import sys
sys.path.insert(0, "D:/project_imp")

import time
from Ingestion.pipeline import run_ingestion
from model.sentiment import predict
from database.db import init_db, insert_results
from datetime import datetime

def run_cycle():
    print(f"\n[{datetime.utcnow().strftime('%H:%M:%S')}] Starting cycle...")
    
    print("Fetching data...")
    raw = run_ingestion()
    print(f"Fetched {len(raw)} items")
    
    print("Running inference...")
    texts = [item["text"] for item in raw]
    preds = predict(texts)
    
    for i, item in enumerate(raw):
        item["label"] = preds[i]["label"]
        item["score"] = preds[i]["score"]
    
    insert_results(raw)
    print(f"Stored {len(raw)} records")
    print("Cycle complete. Waiting 1 hour...")

if __name__ == "__main__":
    init_db()
    while True:
        run_cycle()
        time.sleep(3600)